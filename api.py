from fastapi import FastAPI
from pydantic import BaseModel
from algo import get_path
from generate_matrix import generateMatrix

app = FastAPI()

class Item(BaseModel):
    source : dict
    destination : dict
    coordinates: list

class LatLong(BaseModel):
    source : dict
    destination : dict

@app.get("/")
async def root() :
    return {"message" : "hello from the other side"}

@app.post("/")
async def getData(item : Item):
    data = get_path(item.coordinates, item.source, item.destination)


    return {
        "distance" : data[0],
        "path1_risk_percentage" : data[2],
        "path1_risk_message" : data[3],
        "path1" :data[1],
        "path2_risk_percentage" : data[5],
        "path2_risk_message" : data[6],
        "path2" :data[4],
    }

@app.post("/getMatrix/")
async def getMatrix(item : LatLong) :
    return {'matrix' : generateMatrix([item.source['lat'],item.source['long']],[item.destination['lat'],item.destination['long']])}


