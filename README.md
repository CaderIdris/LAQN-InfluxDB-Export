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

**NB: Some items in the LAQN category are the codes/addresses used to communicate with the LAQN API and website. Options not beginning with @ should only be changed if the LAQN change them**

#### Options for *Pollutants*:
- `"Carbon Monoxide"`
- `"Nitric Oxide"`
- `"Nitrogen Dioxide"`
- `"Oxides of Nitrogen"`
- `"Ozone"`
- `"PM10"`
- `"PM2.5"`
- `"SO2"`
- `"Temperature"`
- `"Wind Direction"`
- `"Wind Speed"`

---

## API

### [main.py](./main.py)
The main script used to run the program, utilises modules found in [modules](./modules) using config specified in [Settings](./Settings)

#### Command line arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
| -s / --start-date | `str` | Date to begin data download (YYYY-MM-DD) | Y | None |
| -e / --end-date | `str` | Date to end data download (YYYY-MM-DD) | Y None |
|-c / --config | `str` | Alternate path to config file, use `/` in pleace of `\` | N | Settings.config.json |

#### Functions

##### parse_date_string

Parses input string and returns `datetime` object. The string can have the following formats (see [strftime](http://strftime.org) for more info):
|Simplified|strftime|
|---|---|
|YYYY|%Y|
|YYYY-MM|%Y-%m|
|YYYY/MM|%Y/%m|
|YYYY\MM|%Y\%m|
|YYYY.MM|%Y.%m|
|YYYY-MM-DD|%Y-%m-%d|
|YYYY/MM/DD|%Y/%m/%d|
|YYYY\MM\DD|%Y\%m\%d|
|YYYY.MM.DD|%Y.%m.%d|

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*date_string*|`str`|The string to be parsed in to a `datetime` object|Y|None|

###### Returns

`datetime object parsed from *date_string*

###### Raises

|Error Type|Cause|
|---|---|
|`ValueError`|*date_string* does not match any of the valid formats|

##### fancy_print

Makes a nicer output to the console

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*str_to_print*|`str`|String that gets printed to console|Y|None|
|*length*|`int`|Character length of output|N|70|
|*form*|`str`|Output type (listed below)|N|NORM|
|*char*|`str`|Character used as border, should only be 1 character|N|\U0001F533 (White box emoji)|
|*end*|`str`|Appended to end of string, generally should be `\n` unless output is to be overwritten, then use `\r`|N|\r|
|*flush*|`bool`|Flush the output stream?|N|False|

**Valid options for _form_**
| Option | Description |
|---|---|
|TITLE|Centres the string, one char at start and end|
|NORM|Left aligned string, one char at start and end|
|LINE|Prints line of *char* of specified *length*|

##### get_json

Open json file and return as dict

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*path_to_json*|`str`|The path to the json file, can be relative e.g Settings/config.json|Y|None|

###### Returns

`dict` containing contents of json file

###### Raises

|Error Type|Cause|
|---|---|
|`FileNotFoundError`|File is not present|
|`ValueError`|Formatting error in json file, such as ' used instead of " or comma after last item|

### [laqn.py](./modules/laqn.py)

Contains all classes and functions pertaining to communication with ACOEM UK API

#### Classes

##### LAQNAPI

Handles requesting metadata from LAQN API and downloading measurements from LondonAir website

###### Keyword Arguments

None

###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*metadata*|`dict`|Contains metadata for all stations in LAQN network, site code used as key|
|*measurement_csvs*|`defaultdict`| Contains csvs storing measurement data separated by year, then site |
|*measurement_jsons*|`defaultdict`| Contains jsons storing measurement data and metadata separated by year then site. Jsons are formatted for upload to InfluxDB 2.x database |

###### Methods

**get_metadata**

Downloads metadata from LAQN API

- Keyword arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*laqn_config*|`dict`|Contains information for communicating with LAQN API and website, specifically stored in the *"LAQN"* subsection of config.json|Y|None|


**get_measurements**

Downloads measurements from LAQN website in csv format

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*station_name*|`str`|The station code to download data for|Y|None|
|*start_date*|`datetime`|Date to start downloading measurements from|Y|None|
|*end_date|`datetime`|Date to end measurement download|Y|None|
|*config*|`dict`|Config.json|Y|None|

**csv_to_json_list**

Reformats measurement csvs to list of jsons for upload to InfluxDB 2.x

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*station_name*|`str`|Station code|Y|None|
|*date*|`datetime`|Start date|Y|None|

**csv_as_text**

Returns `dataframe` as `str`

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*station_name*|`str`|Station code|Y|None|
|*year*|`str`|Year data was recorded|Y|None|

- Returns

String representation of measurement csv (or empty string if no data present)

**csv_save**

Save csv file to path

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*path*|`str`| Path to save csv to | Y | None|
|*station_name*|`str`|Station code|Y|None|
|*year*|`str`|Year data was recorded|Y|None|

**clear_measurement_csvs**

Clears all measurement csvs from memory

**clear_measurement_jsons**

Clears all measurement jsons from memory

### [influxwrite.py](./modules/influxwrite.py)

Contains functions and classes pertaining to writing data to InfluxDB 2.x database

#### Classes

##### InfluxWriter

Handles connection and export to InfluxDB 2.x database

###### Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*influx_config*|`dict`|Contains all info relevant to connecting to InfluxDB database|

###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*config*|`dict`|Config info for InfluxDB 2.x database|
|*client*|`InfluxDBClient`|Client object for InfluxDB 2.x database|
|*write_client*|`InfluxDBClient.write_api`|Write client object for InfluxDB 2.x database|

###### Methods

**write_container_list

Writes list of measurement containers to InfluxDB 2.x database, synchronous write used as asynchronous write caused memory issues on a 16 GB machine.

- Keyword Arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*list_of_containers*|`list`|Exports list of data containers to InfluxDB 2.x database|

Containers must have the following keys:
|Key|Description|
|---|---|
|*time*|Measurement time in datetime format|
|*measurement*|Name of measurement in the bucket|
|*fields*|Measurements made at *time*|
|*tags*|Metadata for measurements made at *time*|

- Returns
None

### [timetools.py](./modules/timetools.py)

Temporary class used for time based calculations, will be replaced eventually

#### Classes

##### TimeCalculator

Used for time based calculations

###### Keyword arguments

| Argument | Type | Usage | Required? | Default |
|---|---|---|---|---|
|*date_start*|`datetime`|Start date|Y|None|
|*date_end*|`datetime`|End date|Y|None|

###### Attributes

| Attribute | Type | Description |
|---|---|---|
|*start*|`datetime`|Start date|
|*end*|`datetime`|End date|

###### Methods

**day_difference**

Calculates days between *start* and *end*

- Keyword Arguments
None

- Returns
`int` representing number of days between *start* and *end*

**week_difference**

Calculates weeks between *start* and *end*

- Keyword Arguments

None

- Returns

`int` representing number of days between *start* and *end*

**year_difference**

Calculates years between *start* and *end*

- Keyword Arguments

None

- Returns

`int` representing number of days between *start* and *end*

---

## License

GNU General Public License v3
