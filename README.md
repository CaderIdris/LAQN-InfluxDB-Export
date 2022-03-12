<h1 align="center">
ACOEM UK API InfluxDB Export Tool
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

---

## API

---

##License

GNU General Public License v3
