"""This is the docstring for the choropleth_geojson.py module. The module enables the plotting of a choropleth map from a compatible geojson file.
A choropleth map is a heatmap-like geographical plot. It displays a region of interest with subregions colored. The color intensity is determined
by the magnitude of the data of interest in each subregion. For example, say the data of interest is the human population of each country with the
region of interest being the North American continent, and the subregions are the countries present in that continent. A choropleth map will shade
the countries with varying shades of red that represent the magnitude of the population level in each country. This can range from light red to the
least populous country to dark red to the most populous country.
"""

import json
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize, to_rgba
from matplotlib import cm
import plotly.offline as offline

class choropleth():
    """The main class to perform the choropleth map plotting. The main method to perform the plot is choroplot(), other methods are auxiliary methods.

    """

    def __init__(self, apikey, df, geojson, glabel):
        """
        Parameters
        ----------
        apikey : str
            The API key (also called token access) used to access Mapbox scattermapbox that is needed to perform the plot.
            See https://docs.mapbox.com/help/how-mapbox-works/access-tokens/ to obtain an API key for free.
            
        df : pandas_dataframe object
            The pandas dataframe that supplies the data for each subregion.
            
        geojson : dict
            The geojson file that supplies the coordinates (latitude and longitude) in a dictionary of each subregion.
            The geojson file has to be in a compatible format for the choropleth map to work. A user can check for
            compatibility on http://geojson.io/#map=2/20.0/0.0 by uploading and opening their geojson file there. If the
            subregions are shaded, then the geojson files are compatible.
            

        glabel : str
            The label of the subregion in the geojson dictionary, e.g. 'State', 'County', 'Name', 'ID', etc.

        """
        """

        Returns
        -------
        output: an instance of the choropleth class
            An instance of the choropleth class with attributes apikey, df, geojson, glabel (see parameters for description),
            and n (the number of subregions).

        """
        
        self.apikey_ = apikey
        self.df_ = df
        self.geojson_ = geojson
        self.glabel_ = glabel

        self.n_ = len(self.geojson_['features'])

    #main plot function
    def choroplot(self, cmap='coolwarm', ptitle='', ctitle='', lat=0, lon=0, zoom=0, opacity=1, col_str='', \
                  missing_label='No data', missing_color='0.5', round_=None, scale=1, ticks='outside', **kwargs):

        """
        Parameters
        ----------
        cmap : str
            (Default: 'coolwarm')
            The colormap to color the subregions.

            Possible values are one of the following,
            
            [Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, 
            GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, 
            Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, 
            Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, 
            Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, 
            YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, 
            cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, 
            gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, 
            gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, 
            hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, 
            pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, 
            tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, 
            twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r],

            note that the postfix _r means reversed.
            
        ptitle : str
            (Default: '' (no title))
            The plot title.
            
        ctitle : str
            (Default: '' (no title))
            The colorbar title.

        lat : num
            (Default: 0)
            The latitude where the choropleth centers when displayed. This is only for display conveniences. Otherwise, the user can
            always zoom and navigate to the plotted region if the display is not centered correctly.

        lon : num
            (Default: 0)
            The longitude where the choropleth centers when displayed. This is only for display conveniences. Otherwise, the user can
            always zoom and navigate to the plotted region if the display is not centered correctly.

        zoom : num
            (Default: 0)
            The zoom amount to apply when the choropleth is displayed. This is only for display conveniences. Otherwise, the user can
            always zoom and navigate to the plotted region if the display is not centered correctly.

        opacity: num in the scale of [0, 1]
            (Default: 1)
            The opacity of the plotted color on the subregions.

        col_str: str
            (Default: '')
            The column string of the pandas_dataframe where the data for each subregion is stored.

        missing_label: str
            (Default: 'No data')
            The string to displayed when NaN, NA or an empty data entry is encountered.

        missing_color: color
            (Default: '0.5', a gray color with a RGB value of [255*0.5, 255*0.5, 255*0.5])

            From https://matplotlib.org/_modules/matplotlib/colors.html, a valid color is either
            
            * an RGB or RGBA tuple of float values in "[0, 1]" (e.g., "(0.1, 0.2, 0.5)"
              or  "(0.1, 0.2, 0.5, 0.3)");
            * a hex RGB or RGBA string (e.g., "'#0F0F0F'" or "'#0F0F0F0F'");
            * a string representation of a float value in "[0, 1]" inclusive for gray
              level (e.g., "'0.5'");
            * one of ``{'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}``;
            * a X11/CSS4 color name;
            * a name from the `xkcd color survey <https://xkcd.com/color/rgb/>`__;
              prefixed with ``'xkcd:'`` (e.g., ``'xkcd:sky blue'``);
            * one of ``{'tab:blue', 'tab:orange', 'tab:green',
              'tab:red', 'tab:purple', 'tab:brown', 'tab:pink',
              'tab:gray', 'tab:olive', 'tab:cyan'}`` which are the Tableau Colors from the
              'T10' categorical palette (which is the default color cycle);
            * a "CN" color spec, i.e. `'C'` followed by a single digit, which is an index
              into the default property cycle (``matplotlib.rcParams['axes.prop_cycle']``);
              the indexing occurs at artist creation time and defaults to black if the
              cycle does not include color.
            

        round_: int
            (Default: None (no rounding))
            The number of decimal places to round the data to for display.

        scale: num
            (Default: 1 (no scaling))
            The multiplicative scale to apply to the data for display. For example, the data
            is stored in terms of percentage but the user wants to display the data in decimal,
            the scale to apply in this case is 0.01.

        ticks: str
            (Default: 'outside', the ticks are outside of the colorbar)
            
            The placement of the ticks on the colorbar. Possible values are one of the following,
            ['', 'inside', 'outside'], where '' indicates no ticks displayed.

        kwargs
            Some examples of valid kwargs include width=1000 and height=1000 for altering the display.
        
        """
        """
        Returns
        -------
        output: dict
            A matplotlib figure dictionary for display and saving.

        """
        
        self.lat_ = lat
        self.lon_ = lon
        self.cmap_ = cmap
        self.zoom_ = zoom
        self.ptitle_ = ptitle
        self.ctitle_ = ctitle
        self.opacity_ = opacity
        self.col_str_ = col_str
        self.missing_label_ = missing_label
        self.missing_color_ = missing_color
        self.round_ = round_
        self.scale_ = scale
        self.ticks_ = ticks
        
        self.reindex_df()
        
        if self.col_str_:
            series = self.df_[col_str]
        else:
            series = self.df_[self.df_.columns[0]]
            
        sources = choropleth.make_sources(self.geojson_)
        lat_cen, lon_cen = choropleth.get_centers(self.geojson_)

        scatter_colors, colorscale = choropleth.get_color_info(series, self.cmap_, self.missing_color_)
        hover_text = choropleth.get_hover_text(series, self.round_, self.scale_, self.missing_label_)

        data = dict(type='scattermapbox',
            lat=lat_cen,
            lon=lon_cen,
            mode='markers',
            text=hover_text,
            hoverinfo='text',
            marker=dict(size=1,
                        color = scatter_colors,
                        showscale = True,
                        cmin = series.min(),
                        cmax = series.max(),
                        colorscale = colorscale,
                        colorbar = dict(title = self.ctitle_, ticks = self.ticks_)
                       )           
             )

        
        layers=(#the line to draw borders
                [dict(sourcetype = 'geojson',
                      source = sources[k],
                      type = 'line',    
                      line = dict(width = 1),
                      color = 'black',
                      ) for k in range(self.n_)
                  ] +
                #the fill to color the borders
                [dict(sourcetype = 'geojson',
                      source = sources[k],
                      type = 'fill',
                      color = scatter_colors[k],
                      opacity = self.opacity_
                     ) for k in range(self.n_)
                 ]

                
                )

        layout = dict(#the layout specifications
                      title=self.ptitle_,
                      autosize = False,
                      width = 1000,
                      height = 800,
                      hovermode = 'closest',
                      mapbox=dict(accesstoken=self.apikey_,
                                  layers=layers,
                                  center=dict(
                                            lat=self.lat_,
                                            lon=self.lon_),
                                  zoom=zoom,
                                  style='light'
                                  )
                      )

        layout.update(kwargs)
        fig = dict(data=[data], layout=layout)
        return fig
        
    ###auxiliary functions###  
        
    #reformat and reindex the df
    def reindex_df(self):
        """Reindex the supplied pandas_dataframe with the geographical subregions in the geojson file.
        The geojson file takes precendence, i.e. index names not in the pandas_dataframe will be
        omitted when mapping the choropleth.

        """
        n = self.n_
        area_name = [self.geojson_['features'][k]['properties'][self.glabel_] for k in range(n)]
        area_name_lowcase = [word.lower() for word in area_name]

        self.df_.index = self.df_.index.map(str.lower)
           
        self.df_ = self.df_[[k in area_name_lowcase for k in self.df_.index]].reindex(area_name_lowcase)
        self.df_.index = area_name

    #get_centers for data
    def get_centers(geojson):
        """Get coordinates for the markers to be used for the hover texts.

        """
        lat_cen, lon_cen =[], []
        n = len(geojson['features'])

        for k in range(n):
            geometry = geojson['features'][k]['geometry']

            if geometry['type'] == 'Polygon':
                coords=np.array(geometry['coordinates'][0])
            #take the first polygon in the case of a multipolygon    
            elif geometry['type'] == 'MultiPolygon':
                coords=np.array(geometry['coordinates'][0][0])

            # the mean as the center of the polygon
            lon_cen.append(np.mean(coords[:, 0]))
            lat_cen.append(np.mean(coords[:, 1]))
            
        return lat_cen, lon_cen

    #sources for layers and downsampling if the data is too huge
    def make_sources(geojson, downsample = 0):
        """Extract the sources (latitudes and longitudes) for mapping the choropleth. There is
        also an option to downsample in case there are too many subregions to map.

        """
        sources = []
        geojson_temp = geojson['features']

        for item in geojson_temp:

            if downsample > 0:
                coords = np.array(item['geometry']['coordinates'][0][0])
                coords = coords[::downsample]
                item['geometry']['coordinates'] = [[coords]]

            sources.append(dict(type = 'FeatureCollection',
                                features = [item])
                          )
        return sources

    #scatter_colors and colorscale for data
    def get_color_info(series, cmap, missing_color):
        """Return the scatter_colors, the list of color intensities to map to each subregion,
        and the color_scale, the data scale that corresponds to the color intensities."""
        cmin = series.min()
        cmax = series.max()
        sm = cm.ScalarMappable(norm=Normalize(vmin=cmin, vmax=cmax), cmap=cm.get_cmap(cmap))
        missing_color = 'rgba'+str(to_rgba(missing_color))
        xrange = np.linspace(0, 1, len(series))
        values = np.linspace(cmin, cmax, len(series))
        scatter_colors = ['rgba' + str(sm.to_rgba(data, bytes = True, alpha = 1)) if not np.isnan(data) else missing_color for data in series]
        color_scale = [[i, 'rgba' + str(sm.to_rgba(j, bytes = True))] for i,j in zip(xrange, values)]

        return scatter_colors, color_scale
        

    #hover_text for data
    def get_hover_text(series, round_=None, scale=1, missing_label='No data'):
        """Return the hover_text, the list that contains the informative text to display on each subregion upon hover."""
        text_value = (series*scale).apply(lambda t, rnd=round_: round(t, rnd) if rnd !=None else t).astype(str)
        with_data = '<b>{}</b> <br> {}'
        without_data = '<b>{}</b> <br> '+ missing_label

        return [with_data.format(j,i) if i != 'nan' else without_data.format(j) for j,i in zip(series.index, text_value)]
