import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'pk.eyJ1IjoidmlvbGV0eWVsbG93IiwiYSI6ImNqdGZrZ2NtMjAyOWw0M250Nm9vdTh4MnEifQ.6Wk26C8g0ZvHtN-o43hDkw'

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
