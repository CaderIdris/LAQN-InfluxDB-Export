"""
"""

__copyright__ = "2021, Joe Hayward"
__credits__ = ["Joe Hayward"]
__license__ = "GNU General Public License v3.0"
__version__ = "0.1"
__maintainer__ = "Joe Hayward"
__email__ = "j.d.hayward@surrey.ac.uk"
__status__ = "Alpha"

import requests as req
import datetime as dt
import pandas as pd
import numpy as np
from collections import defaultdict


class LAQNAPI:
    """
    """
    def __init__(self):
        """
        """
        self.metadata = dict()
        self.measurement_csvs = defaultdict(dict)

    def get_metadata(self, laqn_config):
        """ Download metadata from LAQN site

        Downloads metadata about the LAQN network using the LAQN API and
        translates some of the keys based on info in the config file

        Keyword arguments:
            laqn_config (dict): Config file found in Settings/config.json,
            specifically the LAQN section

        Variables:

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
        """
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
        print(len(list(set(csv_measurements["Species"]))))




