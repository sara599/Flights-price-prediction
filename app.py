import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

Inputs = joblib.load("Inputs.pkl")
Model = joblib.load("Model.pkl")


def get_new_duration(dep_day,dep_H, dep_M,arrv_day, arrv_H, arrv_M):
    
    if (dep_day == arrv_day ):
        d = (arrv_H * 60 + arrv_M) - (dep_H * 60 + dep_M)
    elif(dep_day != arrv_day):
        d = (1440 - (dep_H * 60 + dep_M)) + (arrv_H * 60 + arrv_M )
        
    return d

def prediction(Airline,  Source, Destination, Total_Stops, day, month, year, Dep_hour, Dep_min, Arrival_hour, 
               Arrival_min, Duration_in_min):
    
    test_df = pd.DataFrame(columns=Inputs)
    test_df.at[0,"Airline"] = Airline
    test_df.at[0,"Source"] = Source
    test_df.at[0,"Destination"] = Destination
    test_df.at[0,"Total_Stops"] = Total_Stops
    test_df.at[0,"day"] = day
    test_df.at[0,"month"] = month
    test_df.at[0,"year"] = year
    test_df.at[0,"Dep_hour"] = Dep_hour
    test_df.at[0,"Dep_min"] = Dep_min
    test_df.at[0,"Arrival_hour"] = Arrival_hour
    test_df.at[0,"Arrival_min"] = Arrival_min
    test_df.at[0,"Duration_in_min"] = Duration_in_min
 
 
    
    st.dataframe(test_df)
    result = Model.predict(test_df)[0]
    return result



def main():
    
    st.title("Flight Budget")
    Airline = st.selectbox("Airline" , ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
       'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia', 'other',
       'Multiple carriers Premium economy'] )
    Source = st.selectbox("Source" , ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai'] )
    Destination = st.selectbox("Destination" , ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad'] )
    Total_Stops = st.text_input("Stops") 
       
    dep_date = st.date_input( "Date of journey")
    dep_day = dep_date.day
    dep_month = dep_date.month
    dep_year = dep_date.year
    
    arr_date = st.date_input( "Date of Arrival")
    arr_day = arr_date.day

    
    # Get the time input from the user
    dep_time = st.time_input("Select Departure Time")
    # Convert the time input to a datetime object
    datetime_obj = datetime.combine(datetime.today(), dep_time)
    Dep_hour = datetime_obj.hour
    Dep_min = datetime_obj.minute
    
    arrival_time = st.time_input("Select Arraivel Time")
    datetime_obj2 = datetime.combine(datetime.today(), arrival_time)
    Arrival_hour = datetime_obj2.hour
    Arrival_min = datetime_obj2.minute
    
    Duration_in_min= get_new_duration(dep_day,Dep_hour, Dep_min,arr_day, Arrival_hour, Arrival_min)
    # if(dep_date and dep_time and arr_date and arrival_time):
    #     if (dep_day == arr_day ):
    #         Duration_in_min = (Arrival_hour * 60 + Arrival_min) - (Dep_hour * 60 + Dep_min)
            
    #     elif(dep_day != arr_day):
    #         Duration_in_min = (1440 - (Dep_hour * 60 + Dep_min)) + (Arrival_hour * 60 + Arrival_min )
            
    # Duration_in_min = get_new_duration(dep_day , Dep_hour, Dep_min, arr_day ,Arrival_hour,Arrival_min)
    
    
    
    if st.button("predict"):
        result = prediction(Airline,  Source, Destination, Total_Stops, dep_day, dep_month, dep_year, Dep_hour,
                            Dep_min, Arrival_hour,Arrival_min, Duration_in_min)
        st.text(f"The price will be :  {round(result)}")
        


    

        







    
    
    
    
    
if __name__ == '__main__':
    main()    