#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template, request
import jsonify
import pandas as pd
import pickle
import datetime
import numpy as np
import calendar


# In[2]:


# Load the model
model = pickle.load(open('flight-fare-prediction-model.pkl','rb'))

# Load the saved data to show on the page
airlines = list(pickle.load(open('saved_data/airlines.pkl','rb')))
source_cities = pickle.load(open('saved_data/source_cities.pkl','rb'))
destination_cities = pickle.load(open('saved_data/destination_cities.pkl','rb'))

# Remove outlier 'Jet Airways Business' from airlines 
airlines.remove('Jet Airways Business')
airlines = np.asarray(airlines)

data = {}
data['airlines'] = airlines
data['source_cities'] = source_cities
data['destination_cities'] = destination_cities


# In[3]:


airlines


# In[4]:


# Utility methods
weekday_map = {'Monday':0,'Tuesday':1,'Wednesday':2,'Thursday':3,'Friday':4,'Saturday':5,'Sunday':6}    
    
def find_week_day(date):
    try:
        if ~pd.isnull(date):
            # day = datetime.datetime.fromisoformat(date.str).weekday()
            day = date.weekday()
            return weekday_map.get(calendar.day_name[day])
    except Exception as ex:
        print(f'Exception in date parsing for value {date}')
        print(ex)
        return date  


# In[5]:


# Define the main app
app = Flask(__name__,template_folder='views')


# In[6]:


# Define the end points
@app.route('/',methods=['GET'])
def home():
    return render_template('home.html',data=data)

'''
INPUT FROM USER

'Year','Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission_Type', 'Owner'
'''

'''
INPUT FOR MODEL

[
Total_Stops 
Airline_Jet Airways
Journey_Day 
Duration
Journey_Month 
Arrival_Hour 
Dept_Hour 
weekday
Destination_New Delhi
Airline_Multiple carriers 
Airline_IndiGo
Airline_Air India 
Destination_Delhi 
Destination_Cochin
Source_Delhi 
Source_Mumbai 
Destination_Hyderabad
Airline_Vistara
Source_Kolkata 
Airline_SpiceJet
]

'''
@app.route('/predict',methods=['POST'])
def predict():
    
    # Initialize the variables to 0
    Airline_JetAirways = 0
    Airline_MultipleCarriers = 0
    Airline_IndiGo = 0
    Airline_AirIndia  = 0
    Airline_Vistara = 0
    Airline_SpiceJet = 0
    
    Journey_Day = 0
    Journey_Month = 0
    Duration = 0
    
    Arrival_Hour = 0 
    Dept_Hour  = 0

    Weekday = 0
    
    Destination_NewDelhi = 0
    Destination_Delhi  = 0
    Destination_Cochin = 0
    Destination_Hyderabad = 0
    
    Source_Delhi  = 0
    Source_Mumbai  = 0
    Source_Kolkata  = 0    
    
    
    form = request.form
    
    Total_Stops = int(form['Total_Stops'])
    
    # Set airline
    airline = form['Airline']
    if airline == 'Jet Airways':
        Airline_JetAirways = 1
    elif airline == 'Multiple Carriers':
        Airline_MultipleCarriers =1
    elif airline == 'IndiGo':
        Airline_IndiGo = 1
    elif airline == 'Air India':
        Airline_AirIndia == 1
    elif airline == 'Vistara':
        Airline_Vistara = 1
    elif airline == 'SpiceJet':
        Airline_SpiceJet = 1
        
    
    # Set Journey date & hour
    Departure_datetime = datetime.datetime.fromisoformat(form['Departure_datetime'])
    Arrival_datetime = datetime.datetime.fromisoformat(form['Arrival_datetime'])
    Journey_Day = Departure_datetime.day
    Journey_Month = Departure_datetime.month
    
    # Set Arrival_Hour
    Arrival_Hour = Arrival_datetime.hour
    # Set Dept_Hour
    Dept_Hour = Departure_datetime.hour
    
    # Set Weekday
    Weekday = find_week_day(Departure_datetime)
    
    # Set Destination city
    Destination_city = form['Destination_city']
    
    if Destination_city == 'New Delhi':
        Destination_NewDelhi = 1
    elif Destination_city == 'Delhi':
        Destination_Delhi = 1
    elif Destination_city == 'Cochin':
        Destination_Cochin = 1
    elif Destination_city == 'Hyderabad':
        Destination_Hyderabad = 1
        
    # Set Source city
    Source_city = form['Source_city']
    
    if Source_city == 'Delhi':
        Source_Delhi = 1
    elif Source_city == 'Kolkata':
        Source_Kolkata = 1
    elif Source_Mumbai == 'Mumbai':
        Source_Mumbai = 1
    
    
    # Set Duration (in hours)
    Duration = (Arrival_datetime - Departure_datetime).total_seconds()/3600

    print(Duration)
    # Predict
    air_fare = model.predict([[Total_Stops,Airline_JetAirways,Journey_Day,Duration,Journey_Month,Arrival_Hour ,Dept_Hour , Weekday,Destination_NewDelhi, Airline_MultipleCarriers,Airline_IndiGo, Airline_AirIndia,Destination_Delhi , Destination_Cochin,Source_Delhi , Source_Mumbai ,Destination_Hyderabad, Airline_Vistara,Source_Kolkata ,Airline_SpiceJet]])
    print(f'Air fare is predicted as : {air_fare[0]}')
    return render_template('home.html',prediction_text="Predicted Air Fare is Rs. {}".format(air_fare[0]),data=data)
    


# In[ ]:


# Start the App in DEBUG mode.
if __name__=="__main__":
    app.run(debug=True, use_reloader=False)


# In[ ]:




