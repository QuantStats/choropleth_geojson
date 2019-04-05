import choropleth_geojson as cg
import pandas as pd
import json
import plotly.offline as offline

apikey = 'my_mapbox_apikey123alpha890'

df = pd.read_csv('resident-households-by-planning-area-and-monthly-household-income-from-work.csv', index_col = 0)

#An example with a pandas dataframe that is not compatible and has to be modified for compatibility,
#the dataframe also contains missing values

#the data cutoff point at monthly income of at least SGD8000
df = df.iloc[290:]

#Modify the dataframe to be compatible with the format required by the choropleth_geojson module
my_dict = dict()

for pa in df['level_3'].unique():
    my_dict[pa] = round(df[df['level_3']==pa]['value'].sum(),1)

del my_dict['Others']

df = pd.DataFrame(data=[*my_dict.values()], index=my_dict.keys(),columns=['value'])

#Ready to plot with a compatible dataframe
with open(r'sg.json') as f:
    geojson = json.load(f)

lat = 1.3521
lon = 103.8198
cmap = 'plasma'
zoom = 9.8
opacity = 0.7
ptitle ='Residents (in thousands) with monthly income of at least SGD8000 by planning area'
ctitle = "Number of residents ('000)"

sg = cg.choropleth(apikey, df, geojson, 'name')
fig = sg.choroplot(cmap, ptitle, ctitle, lat, lon, zoom, opacity,\
                   missing_label='Not reported', missing_color='g', round_=None, scale=1000, ticks='inside',\
                   layer_fill_dict=dict(below='building'))

savefile = 'sg_income.html'
offline.plot(fig, filename = savefile, auto_open=True)
