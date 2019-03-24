import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'my_mapbox_apikey123alpha890'

df = pd.read_csv('sg_density_data.csv', index_col = 0)

with open(r'sg.json') as f:
    geojson = json.load(f)
	
sg = cg.choropleth(apikey, df, geojson, 'name')
fig = sg.choroplot()

offline.plot(fig, auto_open=True)
