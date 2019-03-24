import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'my_mapbox_apikey123alpha890'

df = pd.read_csv('sg_density_data.csv', index_col = 0)

with open(r'sg.json') as f:
    geojson = json.load(f)

lat = 1.3521
lon = 103.8198
cmap = 'viridis'
zoom = 9.8
opacity = 0.7
ptitle ='Singapore population density by planning area'
ctitle = 'Population per square kilometer'

sg = cg.choropleth(apikey, df, geojson, 'name')
fig = sg.choroplot(cmap, ptitle, ctitle, lat, lon, zoom, opacity)

savefile = 'sg_density.html'
offline.plot(fig, filename = savefile, auto_open=True)
