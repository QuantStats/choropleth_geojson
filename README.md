The module was inspired by the work presented on http://vincepota.com/plotly_choropleth_map.html and also on https://github.com/vincepota/plotly_choropleth_tutorial.

The module enables the plotting of a choropleth map from a compatible geojson file. To check for the compatibility of a geojson file, the file can be uploaded to http://geojson.io/#map=2/20.0/0.0. If the area of the map that corresponds to the geographical region on the geojson file is shaded, then the geojson file is compatibile to be used with this module. The module also requires an API key from Mapbox. An API key can be obtained for free from https://docs.mapbox.com/help/how-mapbox-works/access-tokens/.

A choropleth map is a heatmap-like geographical plot. It displays a region of interest with subregions colored. The color intensity is determined
by the magnitude of the data of interest in each subregion. For example, say the data of interest is the human population of each country with the
region of interest being the North American continent, and the subregions are the countries present in that continent. A choropleth map will shade
the countries with varying shades of red that represent the magnitude of the population level in each country. This can range from light red to the
least populous country to dark red to the most populous country.

Suppose that the population data is saved to one of the columns in a pandas dataframe, with index representing each country, and there is a compatible geojson file. Then, a minimal working example to plot the choropleth map is as follows,

'
import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'my_mapbox_apikey123alpha890'

df = pd.read_csv('population_data.csv', index_col = 0)

with open(r'north_america.json') as f:
    geojson = json.load(f)
	
northamerica = cg.choropleth(apikey, df, geojson, 'Country')
fig = northamerica.choroplot()

offline.plot(fig, auto_open=True)
'

