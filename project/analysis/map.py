import pandas as pd
import geopandas as gpd
import folium

def create_interactive_map():
    df = pd.read_csv("./scraper/data/base_row_properties.csv")
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:4326")

    m = folium.Map(location=[50.851409, 4.350694], zoom_start=8)

    for _, row in gdf.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Type: {row['subtype_of_property']}<br>Price: €{row['price']}<br>Address: {row['street']}, {row["postal_code"]} {row["locality_name"]}",
        ).add_to(m)

    m.save("properties_map.html")