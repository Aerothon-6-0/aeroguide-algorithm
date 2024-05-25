from fastapi import FastAPI
from pydantic import BaseModel
from algo import get_path

app = FastAPI()

class Item(BaseModel):
    source : dict
    destination : dict
    coordinates: list

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


