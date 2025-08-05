NYC Taxi Trip Analysis
This project provides a comprehensive data pipeline and analysis of NYC taxi trip data, from raw ingestion to interactive visualization. The goal is to provide insights into trip patterns and fare amounts across different geographic zones in New York City.

1. Project Architecture
The project follows a modern data stack architecture, automating the flow of data through several key components:

Airflow: Orchestrates the entire data pipeline, from extracting raw data to triggering dbt transformations.

SQLite: Serves as the lightweight, file-based data warehouse where raw data is stored and dbt models are built.

dbt (data build tool): Transforms raw trip data and geographic zone information into clean, analysis-ready tables.

Power BI: Connects to the final dbt models to create interactive dashboards and a choropleth map.

2. Data Sources
NYC Taxi Trip Data: Raw trip data (yellow taxi).

NYC Taxi Zones: A geographic Shapefile (zones.shp) containing the polygon boundaries for each taxi zone.

3. Key Features
Automated ELT Pipeline: An Airflow DAG automates data extraction, loading, and transformation.

Robust Data Model: A dbt project creates a clean, star-schema data model for easy analysis.

Interactive Power BI Dashboard: A dashboard visualizing trip metrics, including:

Trip count and fare amount by zone.

Time-series analysis of taxi activity.

A choropleth map of NYC, colored by aggregated fare amounts per zone.

4. Prerequisites
Before running this project, you need to have the following software installed:

Windows Subsystem for Linux (WSL) with Ubuntu

Docker and Docker Compose

Python 3.9+

Power BI Desktop

QGIS (for working with geographic data)

5. Setup and Installation
Clone the repository:

Open your WSL/Ubuntu terminal.

Bash

git clone [your-repository-url]
cd [your-project-directory]
Start the Docker containers:

From within the WSL terminal, run:

Bash

docker-compose up -d
This will launch Airflow, the SQLite database, and any other services.

Run dbt:

Navigate to your dbt project directory within the WSL terminal:

Bash

cd dbt_project/
dbt debug
dbt run
6. Power BI Visualization
The final step is to connect Power BI to your transformed data and create the map visual. This section is a detailed guide to a common set of issues with the Power BI Shape Map visual and the specific fix required.

Preparing the Geographic Data
The Shape Map visual is very particular about its input file. To fix the common issues of "glitchy lines" and non-matching data, you must:

Reproject the data: The visual requires your map to be in the EPSG:4326 (WGS84) projection. Your original geojson file is in EPSG:2263 (New York Long Island).

Rename the key field: The visual requires the key column in your TopoJSON file to be named "name" to correctly match with your data's key (e.g., OBJECTID).

Use mapshaper.org to perform these transformations:

Go to https://mapshaper.org.

Upload your zones.geojson file.

In the console (press Ctrl + ;), run the following commands sequentially:

Bash

# Set the source projection
-proj from=EPSG:2263

# Reproject to WGS84
proj wgs84

# Rename the key field from OBJECTID to name
rename-fields name=OBJECTID

# Export as TopoJSON
-o format=topojson
Connecting Power BI
Connect to SQLite: Due to issues with Power BI's connectors and WSL paths (e.g., \\wsl$\...), it is recommended to manually copy your SQLite database file from the WSL file system to a local Windows drive (e.g., C:\Users\YourUser\data\).

In Power BI, connect to your SQLite database file from the new local drive location.

Create the visual:

Add a "Shape Map" visual to your report.

In the "Format your visual" pane, go to "Map settings" -> "Add map" and upload the TopoJSON file you created.

Drag your name field (which contains your OBJECTID data) to the "Location" field.

Drag your aggregated fare_amount measure to the "Color saturation" field.

7. Troubleshooting
Python Scripting Errors: If you encounter DLL load failed or ImportError, the issue is likely a corrupted Python environment or an incorrect path. The best solution is a clean Anaconda re-installation and ensuring Power BI is pointed to the correct installation path.

Visual rendering issues: If your map is not rendering correctly, it is often due to an issue with the underlying TopoJSON file. The above steps for mapshaper are a direct fix for the two most common causes of this issue.

8. License
This project is licensed under the MIT License.
