# creates a configuration file for the relevant cities with their coordinates
import json

haifa_dict = {}
haifa_dict['latitude'] = 32.7940
haifa_dict['longitude'] = 34.9896

tel_aviv_dict = {}
tel_aviv_dict['latitude'] = 32.0853
tel_aviv_dict['longitude'] = 34.7818

beer_sheva_dict = {}
beer_sheva_dict['latitude'] = 31.2530
beer_sheva_dict['longitude'] = 34.7915

eilat_dict = {}
eilat_dict['latitude'] = 29.5577
eilat_dict['longitude'] = 34.9519

config = {"Haifa": haifa_dict, "Tel_Aviv": tel_aviv_dict, "Beer_Sheva": beer_sheva_dict, "Eilat": eilat_dict}

with open('city_configuration_data.json', 'w') as f:
    json.dump(config, f)
