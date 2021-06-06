""" laqn.py

This module contains all code necessary to communicate with the LAQN API and
the website to download metadata, measurements and then format them in a list
of jsons suitable for export to an InfluxDB 2.x database.

Classes:
    LAQN API: Downlaods LAQN data using a combo of the API and website
"""

__copyright__ = "2021, Idris Hayward"
__credits__ = ["Idris Hayward"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0 RC"
__maintainer__ = "Idris Hayward"
__email__ = "j.d.hayward@surrey.ac.uk"
__status__ = "Release Candidate"

import requests as req
import datetime as dt
import pandas as pd
import numpy as np
from collections import defaultdict


class LAQNAPI:
    """ Downloads LAQN data using a combo of the API and website

    This class is used to download metadata and measurements from the LAQN.
    The metadata is downloaded via an API query to the official API. The site
    code contained within the metadata is then used to locate the site on the
    londonair website where a data query is formatted and a csv downloaded.

    The LAQN API can be used to download measurements in a variety of formats
    but the documentation is poor and it appears to be difficult to get
    measurements at a different frequency than the default 1h or get the
    ratification status of them. The csvs on the website can do both of these,
    so they are downloaded instead.

    Attributes:
        metadata (dict): Dictionary containing metadata for all sites, each
        site is represented by a key (site code) and the value is another
        dict containing all info downloaded from the LAQN API

        measurement_csvs (defaultdict): Defaultdict containing all csvs
        with LAQN measurements split by year, then site

        measurement_jsons (defaultdict): Defaultdict containing all jsons
        with LAQN measurements split by year, then site formatted for export
        to an InfluxDB 2.x database

    Methods:
        get_metadata: Downloads metadata from the LAQN API and stores it
        in a dict

        get_measurements: Downloads csvs of LAQN measurements from the
        LAQN website

        csv_to_json_list: Convert csvs to list of jsons for export to InfluxDB
        2.x database

        csv_as_text: Convert csv to string format

        csv_save: Save csv to path

        clear_measurement_csvs: Clear measurement_csvs instance to free memory

        clear_measurement_jsons: Clear measurement_jsons instance to free
        memory
    """
    def __init__(self):
        """ Initialises the class
        """
        self.metadata = dict()
        self.measurement_csvs = defaultdict(dict)
        self.measurement_jsons = defaultdict(dict)

    def get_metadata(self, laqn_config):
        """ Download metadata from LAQN site

        Downloads metadata about the LAQN network using the LAQN API and
        translates some of the keys based on info in the config file

        Keyword arguments:
            laqn_config (dict): Config file found in Settings/config.json,
            specifically the LAQN section

        Variables:
            metadata_request (Request): Result of request to LAQN API
            
            metadata_raw (dict): Result of request to LAQN API in json format

            station_name (str): The name of the station from the API

            station_dict (dict): Container for metadata for a station

        """
        # Request metadata
        metadata_request = req.get(f"{laqn_config['API Address']}/"
                                   f"{laqn_config['Metadata Address']}")
        metadata_raw = metadata_request.json()['Sites']['Site']
        # Make it look nicer
        for station in metadata_raw:
            station_name = station['@SiteName']
            station_dict = {
                    'tags': {},
                    'fields': {}
                    }
            for key, code in laqn_config["Tags"].items():
                station_dict['tags'][code] = station[key]
            for key, code in laqn_config["Fields"].items():
                station_dict['fields'][code] = station[key]
            self.metadata[station_name] = station_dict

    def get_measurements(self, station_name, start_date, end_date, config):
        """ Downloads measurements from the LAQN website in csv format

        The LAQN API does offer an option to download measurements. However,
        documentation for it is either incomplete or it is not intended to be
        used for the purposes it is here. Using the API, it is only possible
        to get measurements at 1h averages. There are options present to
        request different measurement periods but there's nothing in the
        documentation listing the valid options and trial and error could not
        find how to get 15 minute data. There also appears to be no option to
        get the ratification status of the data. For these reasons, the csvs that can be downloaded on the LAQN website were used instead.

        The csvs on the LAQN website are generated based on a query, so this
        is exploited for the program. The query requires the following info:
        - Site code (Obtained via the metadata query) {&site=}
        - Species to download measurements for (The codes for these are in the
          config.json file) {&species[1 to 6]=}
        - Start time (When to download measurements from, %d-%b-%Y format)
          {&start=}
        - End time (When to finish measurement download, %d-%b-%Y format)
          {&end=}
        - res (unknown, changing values had to discernible effect, fixed to 6)
          {&res=}
        - Period (Measurement periods e.g 1h) {&period=}

        As the query only takes 6 pollutants, if more than 6 pollutants are
        needed the query is split in to sets of 5 pollutants (requesting 6
        sometimes causes an error). The csvs from these queries are appended
        together and saved.

        The csvs have the following columns:
        - Site: Site name
        - Species: Species measured
        - ReadingDateTime: When the measurement started (average beginning)
        - Value: Measurement value
        - Units: Units of the measurement
        - Provisional or Ratified: Status of the measurement

        Keyword Arguments:
            station_name (str): The name of the station, corresponds to the
            metadata key

            start_date (datetime): Date to start downloading measurtements
            from

            end_date (datetime): Date to end measurement download

            config (dict): config file (Settings/config.json)

        Variables:
            allowed_pollutants (list): The pollutants to be downloaded, in
            string format. Valid entries can be found in the README. If the
            list in config.json is empty, all pollutants are added to it.

            download_stages (int): The amount of separate csv downloads to
            perform (calculated assuming 5 pollutants at a time)

            pollutants_per_stage (list): List of lists, the sublists contain
            5 elements with either pollutants to download or None to
            fill up the remainder if needed.

            site_code (str): The download code for the site, found in metadata

            csv_measurements (DataFrame): The measurements downloaded from the
            LAQN, appended together

            data_url (str): Generated url+query for the csv

            raw_csv (DataFrame): csv from LAQN website
        """
        # Determine pollutants to download, if list is empty download all
        allowed_pollutants = config['Pollutants']
        if len(allowed_pollutants) == 0:
            allowed_pollutants = list(
                    config['LAQN']['Pollutant Codes'].keys()
                    )
        # LAQN can do max 6 pollutants at a time but 5 are done at a time 
        # here to be safe
        download_stages = int(np.ceil(len(allowed_pollutants) / 5))
        pollutants_per_stage = list()
        for download_stage in range(0, download_stages):
            pollutants = allowed_pollutants[
                    download_stage*5:(download_stage*5)+5
                    ]
            while len(pollutants) < 5:
                pollutants.append(None)
            pollutants_per_stage.append(pollutants)
            # Python doesn't throw an index error when using list slices
        # Generate urls to download csv, download them, append multiple and
        # save them all to measurement_csvs
        site_code = self.metadata[station_name]['tags']['Site Code']
        csv_measurements = pd.DataFrame()
        for pollutants in pollutants_per_stage:
            data_url = f"{config['LAQN']['csv Address']}site={site_code}"
            for pollutant in range(0, 5):
                if pollutants[pollutant] is not None:
                    pollutant_code = config['LAQN']['Pollutant Codes'][
                           pollutants[pollutant]
                            ]
                else:
                    pollutant_code = ""
                data_url = f"{data_url}&species{pollutant+1}={pollutant_code}"
            data_url = (
                    f"{data_url}&start={start_date.strftime('%d-%b-%Y')}"
                    f"&end={end_date.strftime('%d-%b-%Y')}&res=6"
                    f"&period={config['Frequency']}"
                    )
            raw_csv = pd.read_csv(data_url)
            csv_measurements = csv_measurements.append(
                    raw_csv, ignore_index=True
                    )
        self.measurement_csvs[start_date.strftime('%Y-%m-%d')][
                station_name
                ] = csv_measurements

    def csv_to_json_list(self, station_name, date):
        """ Formats csvs for export to InfluxDB 2.x

        The csvs downloaded from the LAQN website need to be formatted for
        export to an InfluxDB 2.x instance.

        Keyword Arguments:
            station_name (str): Name of the station, used to locate it in
            measurement_csvs

            date (datetime): Start date, used to locate csv in
            measurement_csvs (formatted to correct format in method)

        Variables:
            csv_file (DataFrame): Full csv from LAQN website

            json_list (list): List of jsons to export to InfluxDB 2.x database

            data_container (dict): Contains all measurements and tags in
            correct format for Influx
        """
        csv_file = self.measurement_csvs[
                date.strftime('%Y-%m-%d')
                ][station_name]
        if csv_file is None:
            return None
        json_list = list()
        for index, row in csv_file.iterrows():
            if row["Value"] != row["Value"]:
                continue
                # Check for NaN, skip if present
            data_container = {
                    "time": dt.datetime.strptime(
                        row["ReadingDateTime"],
                        "%d/%m/%Y %H:%M"
                        ),
                    "measurement": "London Air Quality Network",
                    "fields": {
                        row['Species']: row["Value"]
                        },
                    "tags": {
                        f"{row['Species']} status": row[
                            "Provisional or Ratified"
                            ],
                        f"{row['Species']} Units": row['Units']
                        }
                    }
            data_container["tags"] = {
                    **data_container["tags"],
                    **self.metadata[station_name]["tags"]
                    }
            data_container["fields"] = {
                    **data_container["fields"],
                    **self.metadata[station_name]["fields"]
                    }
            json_list.append(data_container)
        self.measurement_jsons[date.strftime('%Y-%m-%d')][
                station_name
                ] = json_list

    def csv_as_text(self, station_name, year):
        """ Return dataframe as text

        Keyword Arguments:
            station_name (str): Used to locate DataFrame

            year (str): Used to locate DataFrame

        Returns:
            String representation of csv, or blank string if no csv
            present
        """
        if self.measurement_csvs[year][station_name] is not None:
            return self.measurement_csvs[year][station_name].to_csv()
        else:
            return ""

    def csv_save(self, path, station_name, year):
        """ Save csv file to path

        Keyword Arguments:
            path (str): Path to save csv to

            station_name (str): Used to locate DataFrame

            year (str): Used to locate DataFrame
        """
        if self.measurement_csvs[year][station_name] is not None:
            self.measurement_csvs[year][station_name].to_csv(
                    path_or_buf=path
                    )

    def clear_measurement_csvs(self):
        self.measurement_csvs = defaultdict(dict)

    def clear_measurement_jsons(self):
        self.measurement_jsons = defaultdict(dict)
