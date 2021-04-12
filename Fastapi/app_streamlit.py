### RUN USING streamlit run app_streamlit.py it will start on localhost:8501 ###
## for 0 prediction weekday, tem- 20 ,25,27,490,0.003
from pycaret.classification import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import six
import joblib
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
sys.modules['sklearn.externals.six'] = six
#import six


model = load_model('catboost classifier 17dec2020')

def predict(model, input_df):
    predictions_df = predict_model(estimator=model, data=input_df)
    predictions = predictions_df['Label'][0]
    return predictions

def run():

    from PIL import Image
    image = Image.open('dsp3.jpeg')
    image = image.resize((300,100))
    #new_img.save("car_resized.jpg", "JPEG", optimize=True)
    image_meeting_room = Image.open('meeting room.JPG')
    image_meeting_room = image_meeting_room.resize((300,100))

    #st.image(image,use_column_width=True)
    st.sidebar.image(image)
    add_selectbox = st.sidebar.selectbox(
    "How would you like to predict?",
    ("Online", "Batch","About"))

    st.sidebar.info('This app is created to predict Office Room occupancy prediction')
    #st.sidebar.success('https://www.pycaret.org')
    
    #st.sidebar.image(image)
    st.sidebar.image(image_meeting_room)

    st.title("Office Room occupancy prediction")

    if add_selectbox == 'Online':
        input_user =  st.date_input('User input Date')
        #datetime_object = datetime.strptime(input_user, "%d-%m-%Y")
        user_year = input_user.year
        user_month = input_user.month
        user_day = input_user.day
        user_weekend = input_user.weekday()
        #user_weekend
        user_weekend1 = 1 if user_weekend > 5 else 0
        user_temperature = st.number_input('Temperature', min_value=1, value=23)
        user_humidity = st.number_input('Humidity', min_value=1, value=27)
        user_light = st.number_input('Light in Lux', min_value=1, value=460)
        user_co2 = st.number_input('CO2 in ppm', min_value=1, value=1040)
        user_HumidityRatio = st.slider('Humidity ratio', min_value = 0.000, max_value = 1.000,step=0.001, value=0.004,format="%.3f")
        

        output=""
        output1=""

        #input_dict = {'OCCUPANCY' : OCCUPANCY, 'EXPENSE' : EXPENSE, 'ADR' : ADR, 'REVENUE' : REVENUE}
        user_df_data = [[user_year,user_month,user_weekend1,user_day,user_temperature,user_humidity,user_light,user_co2,user_HumidityRatio]]
        user_df_colnames = ["Year","Month","weekend","day","Temperature","Humidity","Light","CO2","HumidityRatio"]
        
        input_df = pd.DataFrame(user_df_data,columns = user_df_colnames)

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            #output=str(output)
            #output1 = output.apply(lambda x: "Occupied" if x ==1 else "Available")
            #output1 = output.apply(lambda x: x.map({1 : 'Occupied', 0 : 'Available'}))
        
        #output_dict = ""
        output_dict = {1 : 'Occupied', 0 : 'Available'}
        
        final_label = ""
        final_label = np.where(output == 1, 'Occupied',np.where(output == 0,"Available","???????"))

        #st.success('The Room will be ' + str(final_label))
        
        #st.success('The Room occupancy will be {}'.format(output_dict[output]))
        st.success(f'The Room  will be {final_label}')

    if add_selectbox == 'Batch':

        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model,data=data)
            st.write(predictions)
            
    if add_selectbox == 'About':
                
                    st.subheader("Built with Streamlit and Pycaret")
                    st.subheader("Hunaidkhan Pathan")
                    st.subheader("https://www.linkedin.com/in/hunaidkhan/")
    
    
    st.button("Re-run")
    check
if __name__ == '__main__':
    run()