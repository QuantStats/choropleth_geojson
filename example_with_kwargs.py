import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'my_mapbox_apikey123alpha890'

df = pd.read_csv('elspot_yearly.csv', index_col = 0)

with open(r'nordpool.json') as f:
    geojson = json.load(f)

cmap = 'Spectral_r'
ptitle ='Electricity spot prices in March 2019'
ctitle = 'DKK per megawatt'
col_str = 'DKK'
lat = 61.97
lon = 19.36
zoom = 3.2

nordpool = cg.choropleth(apikey, df, geojson, 'name')
fig = nordpool.choroplot(cmap=cmap, ptitle=ptitle, ctitle=ctitle, col_str=col_str, lat=lat, lon=lon, zoom=zoom, width=700, height=800)

savefile = 'nordpool.html'
offline.plot(fig, filename = savefile, auto_open=True)
