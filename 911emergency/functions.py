from pandas import *
import datetime as dt
import json
import os

# read 911 csv
cwd = os.getcwd() + '/' + 'montgomeryPA_911.csv'
data = read_csv(cwd)

#converting the timestamp to pandas datetime format
pandas.to_datetime(data['timeStamp'])

#Emergency overview for an year input by the user
def emergency_overview(year):
    overview_data = data[data['timeStamp'].str.contains(year)]
    overview_data_ems = overview_data[overview_data['title'].str.contains('EMS:')]
    overview_data_fire = overview_data[overview_data['title'].str.contains('Fire:')]
    overview_data_traffic = overview_data[overview_data['title'].str.contains('Traffic:')]
    count_ems = len(overview_data_ems.index)
    count_fire = len(overview_data_fire.index)
    count_traffic = len(overview_data_traffic.index)
    dictionary = {"EMS": count_ems, "Fire": count_fire, "Traffic": count_traffic}
    dictionary = [{"label": i , "value": j} for i,j in dictionary.items()]
    result = json.dumps(dictionary)
    return dictionary

print (emergency_overview('2016'))

#Trend for an Emergency sub-category in a specific year
def emergency_trend(year, emergency_type, sub_emergency_type):
    trend_data = data[data['timeStamp'].str.contains(year)]
    trend_data = trend_data[trend_data['title'].str.contains(emergency_type + " " + sub_emergency_type)]
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    dict_trend = {}
    for i in range(1, 13):
        count = len((trend_data[trend_data['timeStamp'].str.contains(year+'/'+str(i)+'/')]).index)
        dict_trend[month[i-1]] = count
        trend_data_dict = [{"label": i , "value": j} for i,j in dict_trend.items()]
    return trend_data_dict

print (emergency_trend('2016', 'EMS:', 'ASSAULT VICTIM'))

#Trend comparison for two sub-categories of an emergency type for a specific year
def emergency_trend_comparison(year, emergency_type, sub_emergency_type1, sub_emergency_type2):
    dict_trend1 = emergency_trend(year, emergency_type, sub_emergency_type1)
    dict_trend2 = emergency_trend(year, emergency_type, sub_emergency_type2)
    dict_trend = {sub_emergency_type1: dict_trend1 , sub_emergency_type2: dict_trend2}
    dict_trend = [{"label": i , "value": j} for i,j in dict_trend.items()]
    return dict_trend

print (emergency_trend_comparison('2016', 'EMS:', 'ASSAULT VICTIM', 'CARDIAC EMERGENCY'))