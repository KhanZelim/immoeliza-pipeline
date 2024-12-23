import pandas as pd
import geopandas as gpd
import folium
import sys
import os

def create_interactive_map():
    df = pd.read_csv("../scraper/data/base_row_properties.csv")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

    m = folium.Map(location=[50.851409, 4.350694], zoom_start=8)

    for _, row in gdf.iterrows():
        if pd.notna(row['lat']) and pd.notna(row['lon']):
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=f"Type: {row['subtype_of_property']}<br>Price: €{row['price']}<br>Address: {row['street']}, {row["postal_code"]} {row["locality_name"]}<br><a href={row["link"]}>Link</a>"
            ).add_to(m)

    images_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', 'analysis', 'images')
 
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    image_path = os.path.join(images_folder, 'properties_map.html')

    m.save(image_path)

    print(f"Map saved to {image_path}")