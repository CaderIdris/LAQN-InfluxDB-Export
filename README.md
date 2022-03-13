<h1 align="center">
London Air Quality Network InfluxDB Export Tool
</h1>

---

Unofficial Python3 script that utilises the [LAQN API](http://api.erg.ic.ac.uk/AirQuality/help) to download metadata for all monitoring stations in the [London Air Quality Network](http://www.londonair.org.uk), then download measurement data from the website in csv format and reformat it for upload to an InfluxDB 2.x database.

CSVs are downloaded from the website instead of using the API as it includes a tag for whether the data is ratified.

<p align="center">
	<a href="#key-features">Key Features</a> ● 
	<a href="#requirements">Requirements</a> ●
	<a href="#operational-procedure">Operational procedure</a> ●
	<a href="#settings">Settings</a> ●
	<a href="#api">API</a> ●
	<a href="#license">License</a>
</p>

---

## Key Features

- Downloads metadata for all measurement stations in the London Air Quality Network
- Downloads specified measurements across a specified time range, one station at a time, seven days at a time
- Formats measurements in to a `list` of `dicts` and uploads them to an InfluxDB 2.x database

---

## Requirements

- This program was developed on a 64 bit x86 **Ubuntu 20.04** machine with **Python 3.9** 
	- Earlier version of Python 3, other operating systems and architectures may work but are untested
- **python3-pip** and **python3-venv** are required for creating the virtual environment for the program to run with

---

## Operational Procedure

```
# Clone the repository
$ git clone https://github.com/CaderIdris/LAQN-InfluxDB-Export.git

# Enter the repository
$ cd LAQN-InfluxDB-Export

# Setup the virtual environment
$ ./venv_setup.sh

# Configure settings.json with required measurement frequency, pollutants and InfluxDB configuration

# Run software
$ ./run.sh

# Input date range to download data
	Start Date: (YYYY-MM-DD)
	End Data: (YYY-MM-DD
```

---

## Settings

### config.json

|Key|Type|Description|Options|
|---|---|---|---|
|*Pollutants*|`list` of `str`|Measurands to download data for, leave empty for all|See below|
|*Frequency*|`str`|Measurement frequency|"15min": 15 minute average<br />"hourly": Hourly average<br />"roll8": Rolling 8 hour average<br />"roll24": Rolling 24 hour average<br />"daily": 24 hour average|
|||||
| **LAQN** |Subcategory|Contains all config variables used to communicate with LAQN API and wesite|-|
|*API Address*|`str`|HTTP address for LAQN API|HTTP address|
|*Metadata Address*|`str`|URI to be added to *API Address* to query metadata of all stations in network|Valid Uri|
|*csv Address*|`str`|HTTP address to query data from LAQN|HTTP Address|
|**Tags**|Subcategory of **LAQN**|Translations to make LAQN API codes human readable in InfluxDB Database|-|
|*@LocalAuthorityCode*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@LocalAuthorityName*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@SiteCode*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@SiteName*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@SiteType*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@DataOwner*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@DataManager*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|**Fields**|Subcategory of **LAQN**|Translations to make LAQN API codes human readable in InfluxDB Database|-|
|*@Latitude*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@Longitude*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|||||
|**Other Metadata**|Subcategory of **LAQN**|Translations to make LAQN API codes human readable in InfluxDB database|-|
|*@DateOpened*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*@DateClosed*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|*Species*|`str`|Name to use in InfluxDB|`str` with no escape characters|
|||||
|**Pollutant Codes**|Subcategory of **LAQN**|Codes used in LAQN website data query for measurands|-|
|*Carbon Monoxide*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Nitric Oxide*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Nitrogen Dioxide*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Oxides of Nitrogen*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Ozone*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Ozone*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*PM10*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*PM2.5*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Sulphur Dioxide*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Temperature*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Wind Direction*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|*Wind Speed*|`str`|Measurand code to use in query|`str` recognised by LAQN data download website|
|||||
|**Influx**|Subcategory|Information used to communicate with InfluxDB Database|-|
|*Bucket*|`str`|Bucket to export data to|Any valid bucket|
|*IP*|`str`|IP address of InfluxDB 2.x database|Valid IP address|
|*Port*|`str`|Port of InfluxDB 2.x database|Valid port for database (usually 8086)|
|*Token*|`str`|Auth token for InfluxDB 2.x database|Auth token provided by database admin|
|*Organisation*|`str`|Organisation your token is associated with|Organisation associated with auth token|
|||||
|*Debug Stats*|`bool`|Print debug stats?|true/false|


---

## API

---

## License

GNU General Public License v3
