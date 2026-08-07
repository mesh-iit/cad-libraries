# README

## General info
This script takes a BOM file in .xlsx format as an input (MWS format as per 2026 is perfect), stores all the alias codes with their rev. it can find in it, then collects all the related .pdf, .stp and .stl files it can find inside Production Doc (Sharepoint) and copies them to a local folder inside the user's Documents. It also generates a .txt report where it writes the codes with rev. it could not find. This script is very useful when preparing manufacturing documentation to send to MWS or an external supplier.

In order to use the app, the Production Doc folder must be findable by Windows Explorer (Esplora Risorse). For this purpose it is advisable to sync all the Silo Mechanics-related files locally.


## Get ProductionDocCollector.exe

To generate the executable file, CMD in this folder, then input:

`python -m PyInstaller --onefile --windowed --name ProductionDocCollector main.py`

__________________________

Developed and tested with:
- Python 3.13.14
- openpyxl 3.1.5
- PyInstaller 6.21.0