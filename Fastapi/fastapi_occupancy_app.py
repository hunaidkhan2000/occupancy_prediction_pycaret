## Code Created by Hunaidkhan Pathan ###
### run using  uvicorn fastapi_occupancy_app:app --reload --port 1111
##postman - http://127.0.0.1:1111/?enter_date=20-02-2020&user_temperature=23&user_humidity=30&user_light=460&user_co2=1060&user_HumidityRatio=0.04
##curl - curl -X POST "http://127.0.0.1:1111/?enter_date=20-03-2021&user_temperature=23&user_humidity=50&user_light=460&user_co2=1060&user_HumidityRatio=0.04" -H  "accept: application/json" -d ""

import uvicorn
from fastapi import FastAPI,Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse

import os 
import pandas as pd
import numpy as np 
from pycaret.classification import *
from datetime import datetime
import pickle


model = load_model('catboost classifier 17dec2020')


app = FastAPI(title="Office Occupancy prediction fast API",
    description="predicts the office room availibility  ",
    version="1.0",default_response_class=ORJSONResponse)


    
# Routes
@app.post('/check')
async def index():
    return {"text":"Hello data science prophet Masters"}

# ML Aspect
@app.post('/')
async def predict(
          enter_date:str =Query(..., description="Enter Date in dd-mm-yyyy formate i.e. 01-02-2020 ",),
          user_temperature: int =Query(..., description="Enter Temperature in Celcius (ex- 23)",),
          user_humidity: int =Query(..., description="Enter humidity in % (ex- 30)",),
          user_light: int =Query(..., description="Enter light in LUX (ex- 460)",),
          user_co2: int =Query(..., description="Enter CO2 in PPM (ex- 1067) ",),
          user_HumidityRatio: float =Query(..., description="Enter humidity ratio between 0 to 1 (ex- 0.04)",)):
    
    datetime_object = datetime.strptime(enter_date, "%d-%m-%Y")
    user_year = datetime_object.year
    user_month = datetime_object.month
    user_weekend = datetime_object.weekday()
    user_weekend
    user_day = datetime_object.day
    user_weekend1 = 1 if user_weekend > 5 else 0
    user_weekend1
    user_df_data = [[user_year,user_month,user_weekend1,user_day,user_temperature,user_humidity,user_light,user_co2,user_HumidityRatio]]
    user_df_colnames = ["Year","Month","weekend","day","Temperature","Humidity","Light","CO2","HumidityRatio"]
    user_df = pd.DataFrame(user_df_data,columns = user_df_colnames)
    predictions = predict_model(estimator=model,data=user_df)
    print(predictions)
    predictions1 = predictions.to_dict('records')[0]
    return(predictions1)
    
 
    



## Code Created by Hunaidkhan Pathan ###