import geopandas as gpd

data = gpd.read_file("dsproject17/presentation/world_m.shp")
data.plot()