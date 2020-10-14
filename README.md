# Data loaders for UA SRC

This repo contains the code for processing data for the UA Superfund Research Center data project. This includes data for Garden Roots as well as data collected for the collaborative projects between UA and UC San Diego and between UA and the Colorado School of Mines.

Cyverse path for data: `/iplant/home/rwalls/ua-src-data`

*note:* The data on CyVerse are only available to project personel.

# Data Processing SOP

1. Gather raw data

 a. Store data as they are originally in shared CyVerse folder under use case name, under ‘raw-data’.

 b. Add file to readme in each raw folder.

 c. Include a data dictionary defining variables

2. Preprocess data

make data “tidy” by converting to CSV, with single header row.
standardize column headers, map to ontology templates. Output is a CSV file. Store on CyVerse under ‘pre-processed’
Single data loader to put into relational MySQL DB (Central Scrutinizer) 
This acts as a validation step and allows us to do quick viz before processing.
See Central Scrutinizer in GH: https://github.com/UA-SRC-data/data_loaders
Once the Ontology Data Pipeline is running, data can go directly into it, without needing to go into a DB first.

3. From scrutinizer, push data to Mongo DB
Used to feed preliminary API
This can go away once the pipeline is running, to be replaced by step 6

4. Run data through Ontology Data Pipeline
Triplifier
store output in graph format - ttl files
Output enhanced datasets using SPARQL queries to CSV - Store on CyVerse
Output data into repository format (JSON for each dataset) 
store in DB (mongo or relational or elastic)

5. Serve data from DB via API
Portals pulls data using API

