# faostat-pull
An automated diff tool for checking new iterations of the FAOstat data, and pulling new updates.


## Running
`python serial_run.py`

## Logs
There are two types of logs - changes.log in the main directory and diff.log in each sub directory.

#### Changes.log
This contains a list of updated files and the date they were downloaded. 
```
############ 2019-05-21 ############

Adding: Agri-Environmental Indicators: Land Use - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Agri/Environmental_Indicators/Land_Use.csv
Adding: Inputs: Land Use - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Inputs/Land_Use.csv
Adding: Agri-Environmental Indicators: Emissions by sector - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Agri/Environmental_Indicators/Emissions_by_sector.csv
Adding: Forestry: Forestry Production and Trade - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Forestry/Forestry_Production_and_Trade.csv
Adding: Prices: Producer Prices - Annual - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Prices/Producer_Prices/Annual.csv
Adding: Prices: Exchange rates - Annual - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Prices/Exchange_rates/Annual.csv
Adding: Investment: Government Expenditure - \\storage.its.york.ac.uk\sei\SEI-Y RESEARCH GROUPS\SCP Group\SHARED RESOURCES\FAOSTAT_DATA\Investment/Government_Expenditure.csv
etc.
```

#### diff.log
Contained in each subdirectory and contains a diff between the old and the updated file.
