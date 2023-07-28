from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import os

#pobranie ilosci herbat z env
teas = { "BlackTea": int(os.getenv('BlackTea', 0)),
         "GreenTea": int(os.getenv('GreenTea', 0)),
         "FruitTea": int(os.getenv('FruitTea', 0)),
         "Coffee": int(os.getenv('Coffee', 0))
}

app = FastAPI()

class AllowedTeas(str, Enum):
    teaB = "BlackTea"
    teaG = "GreenTea"
    teaF =  "FruitTea"
    coffee = "Coffee"

#teatype musi mieć nazwę klucza z teas
@app.get("/makeTea/{teatype}")
def tea_maker(teatype: AllowedTeas):
    if(teatype == "Coffee"):
        raise HTTPException(status_code=418,
                            detail="jestem automatem do herbaty, nie maszyną do kawy")
    if(teas[teatype] > 0):
        teas[teatype] -= 1
        return {"message": "Smacznego!"}
    else:
        raise HTTPException(status_code=503,
                            detail="nie ma takiej herbaty w ofercie")

@app.put("/addTea/{teatype}/{amount}")
def add_tea(teatype: AllowedTeas, amount: int):
    if (teatype == "Coffee"):
        raise HTTPException(status_code=418,
                            detail="jestem automatem do herbaty, nie maszyną do kawy")
    if(amount <= 0): #gdy ktoś poda ujemną ilość
        raise HTTPException(status_code=400,
                            detail="Error ocured! ilość dodawanej herbaty musi być dodatnia")
    else:
        teas[teatype] += amount
        return {"message": "Dodano herbatę.",
                "amount": teas[teatype]}

@app.get("/showAmount")
def tea_amount():
    tea2 = teas.copy()
    tea2.pop("Coffee")
    return {"teas": tea2}