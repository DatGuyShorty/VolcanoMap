# Volcano Map Generator

This project visualizes volcanoes on an interactive map using Python and Folium.

## Overview

The main script, [`generate_map.py`](generate_map.py), reads volcano data from a CSV file (`Volcanoes.txt`) and generates an interactive HTML map (`volcano_map.html`). Each volcano is represented by a marker colored by elevation, with a popup showing its name, links, and an image (if available) from Wikipedia.

## Features

- **Markers by Elevation:**  
  - Green: Elevation < 1000m  
  - Orange: 1000m ≤ Elevation < 3000m  
  - Red: Elevation ≥ 3000m

- **Popups:**  
  Each marker popup includes:
  - Volcano name (with Google and Wikipedia links)
  - Image from Wikipedia (if available)
  - Elevation, type, and status

- **Layer Control:**  
  Toggle visibility of volcanoes by elevation group.

- **MiniMap:**  
  A small overview map in the corner.

## Usage

1. **Install dependencies:**
   ```sh
   pip install pandas folium requests beautifulsoup4
   ```

2. **Prepare the data:**  
   Ensure `Volcanoes.txt` is present and formatted with columns: `LAT`, `LON`, `NAME`, `ELEV`, `TYPE`, `STATUS`.

3. **Run the script:**
   ```sh
   python generate_map.py
   ```

4. **View the map:**  
   Open `map1.html` in your browser.

## File Descriptions

- [`generate_map.py`](generate_map.py): Main script to generate the volcano map.
- `Volcanoes.txt`: Input data file with volcano information.
- `map1.html`: Output interactive map (generated).
- `readme.md`: Project documentation.

## Notes

- The script fetches volcano images from Wikipedia. If no image is found, a message is shown in the popup.
- Internet connection is required for fetching images and map tiles.
