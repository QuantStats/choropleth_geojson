import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'pk.eyJ1IjoidmlvbGV0eWVsbG93IiwiYSI6ImNqdGZrZ2NtMjAyOWw0M250Nm9vdTh4MnEifQ.6Wk26C8g0ZvHtN-o43hDkw'

df = pd.read_csv('sg_density_data.csv', index_col = 0)

with open(r'sg.json') as f:
    geojson = json.load(f)
	
sg = cg.choropleth(apikey, df, geojson, 'name')
fig = sg.choroplot()

offline.plot(fig, auto_open=True)
