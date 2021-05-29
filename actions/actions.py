# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd


def get_hospital_details(zipcode):
    df = pd.read_csv("hospital_directory.csv", low_memory=False)
    dfnew = df[df['Pincode'] == zipcode][['Hospital_Name', "Mobile_Number", "Location"]]
    s, i = "",  5
    for row in dfnew.iterrows():
        i -= 1
        if i <= 0:
            break
        else:
            s += f'Name: {row[1][0]} \nMobileNumber: {984353245} \nLocation: {row[1][2]}\n'
    return s

def get_hospital_details_city(cityname):
    df = pd.read_csv("hospital_directory.csv", low_memory=False)
    cityname = " ".join([s.capitalize() for s in cityname.split(" ")])
    f = open("district.txt", 'r')
    citynames = f.read().split(", ")
    if cityname in citynames:
        for name in citynames:
            if cityname in name:
                dfnew = df[df['District'] == name][['Hospital_Name', "Mobile_Number", "Location"]]
                s, i = "", 5
                for row in dfnew.iterrows():
                    i -= 1
                    if i <= 0:
                        break
                    else:
                        s += f'Name: {row[1][0]} \nMobileNumber: {984353245} \nLocation: {row[1][2]}\n'
                return s
            else:
                return "Try again"
    else:
        return "Try entering city name"





class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_get_hospital_by_zipcode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f'{get_hospital_details(tracker.get_slot("zipcode"))}')
        return []



class ActionHospitalsCity(Action):
    def name(self) -> Text:
        return "action_get_hospital_by_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain:Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f'{get_hospital_details_city(tracker.get_slot("location"))}')
        return []
