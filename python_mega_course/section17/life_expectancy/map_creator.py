#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : map_creator.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 11/4/2020
# =============================================================================
"""
Based on course content so far (video 135 - Adding Points), I thought about
putting in practice some of these section techniques, creating a map indicating
countries with low and high life expectancy.
"""
# =============================================================================

import pandas as pd
from geopy.geocoders import ArcGIS
import folium

# Reading data with pandas
#  this file contains the following index:
#   Entity,Code,Year,Life expectancy
#  data is comma separated.
#  This Entity (country, continent) repeats for each year available (1543 to 2019)
#  I will be using multi-indexing
data_file = r'data/life-expectancy.csv'
data_df = pd.read_csv(data_file, sep=',', index_col=['Entity', 'Year'])
# dropping rows with NaNs (mostly continents without code)
data_df.dropna(axis=0, inplace=True)
# remove "world" from countries list - although the data is interesting, not really useful for plotting on map
data_df.drop('World', level='Entity', inplace=True)
# sort data - Ascending on countries, descending on years
data_df.sort_index(ascending=[True, False])
# get only last year available for each country
data_df = data_df[~data_df.index.get_level_values(0).duplicated(keep='last')]

# get countries geolocation
geo_coder = ArcGIS()
geo_codes_countries_dict = {country: geo_coder.geocode(country) for country in data_df.index.levels[0]}
data_df['geo_loc'] = data_df.index.map(lambda idx: geo_codes_countries_dict[idx[0]])

# Create two FeatureGroup - high (>80) and low( <70)
fg_high = folium.FeatureGroup(name="High expectancy")
fg_low  = folium.FeatureGroup(name="Low expectancy")

for (data_row_idx, data_row_serie) in data_df.iterrows():
    country = data_row_idx[0]
    year    = data_row_idx[1]
    life_expectancy = round(data_row_serie['Life expectancy'], 1)
    geo_loc = data_row_serie['geo_loc']

    if life_expectancy >= 80:
        fg_high.add_child(
            folium.Marker(location=(geo_loc.latitude, geo_loc.longitude),
                          popup=f"{country} - Expectancy: {life_expectancy} ({year})",
                          icon=folium.Icon(
                              color='green')
                          )
        )
    elif life_expectancy <= 70:
        fg_low.add_child(
            folium.Marker(location=(geo_loc.latitude, geo_loc.longitude),
                          popup=f"{country} - Expectancy: {life_expectancy} ({year})",
                          icon=folium.Icon(
                              color='red')
                          )
        )

map = folium.Map()
map.add_child(fg_high)
map.add_child(fg_low)
map.save("life_expectancy_map.html")
