# README

## General info
This script takes a list of alias codes and generates the trail file to export the .stp and .stl files from the related 3D model and the .pdf from the related drawing, if any. It wants two things as inputs:
1. A .txt file containing the list of alias codes to browse By default it assumes it is the .txt file given as an output of ProductionDocCollector - see that script, but it is possible to choose another file instead, if needed.
2. The folder where the alias codes will be browsed.

Then, it proceeds to generate the trail file needed for Creo to export those files automatically. The output can be found in a local folder inside the user's Documents named as this script.

## Get ProductionDocCollector.exe

To generate the executable file, CMD in this folder, then input:

`python -m PyInstaller --onefile --windowed --name ProductionDocCollector main.py`

__________________________

Developed and tested with:
- Python 3.13.14
- openpyxl 3.1.5
- PyInstaller 6.21.0