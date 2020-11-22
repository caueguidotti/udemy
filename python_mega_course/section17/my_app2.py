#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# File        : my_app2.py
# Project     : udemy
# Created By  : Caue Guidotti
# Created Date: 11/14/2020
# =============================================================================
"""
This is my approach to the second "real life" application
- This creates a map containing layers which will display countries
information such as absolute population, area, population density, and life
expectancy
"""
# =============================================================================

import json
import folium
import numpy as np
import pandas as pd
from colour import Color
from functools import partial


def read_world_data_json(file_path):
    """
    Reads the json data used as GeoJson
    :param file_path: path to the GeoJson file
    :return: processed json file
    """
    with open(file_path, encoding='utf-8-sig') as json_fid:
        json_str_data = json_fid.read()
    json_data = json.loads(json_str_data)
    return json_data


def read_expectancy_data_csv(file_path):
    """
    Reads the life expectancy data file into a pandas dataframe
    :param file_path: life expectancy file path
    :return: pandas dataframe
    """
    data_df = pd.read_csv(file_path, sep=',', index_col=['Entity', 'Year'])
    # dropping rows with NaNs (mostly continents without code)
    data_df.dropna(axis=0, inplace=True)
    # remove "world" from countries list - although the data is interesting, not really useful for plotting on map
    data_df.drop('World', level='Entity', inplace=True)
    # sort data - Ascending on countries, descending on years
    data_df.sort_index(ascending=[True, False])
    # get only last year available for each country
    data_df = data_df[~data_df.index.get_level_values(0).duplicated(keep='last')]
    # drop index year (as they are all the last one available anyways
    data_df.index = data_df.index.droplevel(level='Year')

    return data_df


def get_world_data_as_df(json_data):
    """
    Transform the GeoJson feature properties in a pandas DataFrame.
    Applies some adjustments over this data as well
    :param json_data: GeoJson data dictionary
    :return: pandas dataframe containing countries information
    """
    feat_props_list = [feat['properties'] for feat in json_data['features']]
    feat_props_df = pd.DataFrame(feat_props_list).set_index('NAME')
    feat_props_df.loc[:, 'AREA'] = feat_props_df['AREA'] * 10  # convert to km2
    return feat_props_df


def get_country_location(country_name, countries_df):
    if country_name in countries_df.index:
        lat_value = countries_df.loc[country_name, 'LAT']
        long_value = countries_df.loc[country_name, 'LON']
    else:
        lat_value = 0
        long_value = 0

    return lat_value, long_value


def get_country_area(country_name, countries_df, min_area=10**-6):
    if country_name in countries_df.index:
        area_value = countries_df.loc[country_name, 'AREA']
    else:
        area_value = 0

    area_value = max(area_value, min_area)  # avoid null areas

    return area_value


def get_country_population(country_name, countries_df):
    if country_name in countries_df.index:
        pop_value = countries_df.loc[country_name, 'POP2005']
    else:
        pop_value = 0

    return pop_value


def get_country_density(country_name, countries_df):
    country_pop = get_country_population(country_name, countries_df)
    country_area = get_country_area(country_name, countries_df)

    country_density = country_pop/country_area
    return round(country_density, 2)


def get_country_life_expectancy(country_name, countries_df):
    if country_name in countries_df.index:
        expectancy_value = countries_df.loc[country_name, 'Life expectancy']
    else:
        expectancy_value = 0

    return round(expectancy_value, 1)


def get_color_gradient(num_div, color_start='white', color_end='red'):
    return [color.get_hex() for color in Color(color_start).range_to(color_end, steps=num_div)]


def get_color(color_gradient, value, dist):
    gradient_index = max(np.sum(value >= dist) - 1, 0)
    return color_gradient[gradient_index]


def get_style_dict(fill_color, fill_opacity=1):
    style_dict = {
        'fillColor': fill_color,
        'fillOpacity': fill_opacity,
    }

    return style_dict


def style_fn_population(feature, countries_df):
    country_name = feature['properties']['NAME']
    pop_value = get_country_population(country_name, countries_df)

    pop_dist = np.array([1*10**6, 10*10**6, 25*10**6, 50*10**6, 100*10**6, 150*10**6, 300*10**6, 500*10**6])
    fill_color = get_color(get_color_gradient(len(pop_dist)), pop_value, pop_dist)

    style_dict = get_style_dict(fill_color)
    return style_dict


def style_fn_density(feature, countries_df):
    country_name = feature['properties']['NAME']
    den_value = get_country_density(country_name, countries_df)

    den_dist = np.array([5, 10, 25, 50, 100, 150, 300, 500])
    fill_color = get_color(get_color_gradient(len(den_dist)), den_value, den_dist)

    style_dict = get_style_dict(fill_color)
    return style_dict


def create_geo_json(geo_json_data, **kwargs):
    return folium.GeoJson(data=geo_json_data, **kwargs)


def get_country_marker(country, countries_df, marker_color='blue', marker_opacity=1):
    html = """<h4>Country information:</h4>
Name: <a href="https://www.google.com/search?q=Country%%20%%22%s%%22" target="_blank">%s</a><br>
Population: %s<br>
Area: %s km2<br>
Population Density: %s ppl/km2<br>
Life Expectancy: %s years<br>
"""
    area = get_country_area(country, countries_df)
    population = get_country_population(country, countries_df)
    density = get_country_density(country, countries_df)
    life_expectancy = get_country_life_expectancy(country, countries_df)
    lat, lon = get_country_location(country, countries_df)

    iframe = folium.IFrame(html=html % (country, country, population, area, density, life_expectancy),
                           width=300, height=150)

    marker = folium.Marker(location=(lat, lon),
                           popup=folium.Popup(iframe),
                           icon=folium.Icon(color=marker_color))

    return marker


def add_countries_markers(countries_df, markers_feature_group):
    countries_df.index.map(lambda country:
                           markers_feature_group.add_child(get_country_marker(country, countries_df)))


world_data_geo_json = read_world_data_json(file_path="volcanoes/data/world.json")
world_data_df = get_world_data_as_df(world_data_geo_json)
life_expectancy_df = read_expectancy_data_csv(file_path="life_expectancy/data/life-expectancy.csv")
# combine both data - keep only countries that exists on both dfs (inner join)
world_data_df = pd.concat([world_data_df, life_expectancy_df['Life expectancy']], axis=1, join='inner', sort=False)

# create geo json for map
pop_geo_json = create_geo_json(world_data_geo_json,
                               style_function=partial(style_fn_population, countries_df=world_data_df))

den_geo_json = create_geo_json(world_data_geo_json,
                               style_function=partial(style_fn_density, countries_df=world_data_df))

# create feature groups
fg_pop = folium.FeatureGroup(name="Absolute Population")
fg_den = folium.FeatureGroup(name="Population Density")
fg_marks = folium.FeatureGroup(name="Countries Marker")

# add to feature groups
fg_pop.add_child(pop_geo_json)
fg_den.add_child(den_geo_json)
add_countries_markers(world_data_df, fg_marks)

# create map and add feature groups
map = folium.Map(tiles='Stamen Terrain', location=(0, 0), zoom_start=2)
map.add_child(fg_pop)
map.add_child(fg_den)
map.add_child(fg_marks)

# add layer control and save map
map.add_child(folium.LayerControl())
map.save("world_map.html")
