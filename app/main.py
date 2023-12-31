import json

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()
app.title = "Documentación de la API"
app.version = "1.0.0"


class Ninja(BaseModel):
    id: Optional[int] = None
    name: str
    pharase: str
    technique: str
    type: str
    village: str


@app.get('/',  tags=["Home"], response_class=HTMLResponse)
def get_index():
    return HTMLResponse("<h1> Hola mundo </h1>")


@app.get('/ninjas', tags=["Ninjas"])
def get_ninjas():

    try:
        with open('./db/data.json', 'r', encoding="utf8") as file:
            data = json.loads(file.read())
            return data['ninjas']

    except Exception as e:
        print(e)


@app.get('/ninjas/{id}', tags=["Ninjas"])
def get_ninja_by_id(id: int):

    try:
        with open('./db/data.json', 'r', encoding="utf8") as file:
            data = json.loads(file.read())
        
            for ninja in data['ninjas']:
                if ninja['id'] == id:
                    return ninja
            return {}

    except Exception as e:
        print(e)


@app.get('/ninjas/', tags=["Ninjas"])
def get_ninja_by_category(category: str):
    
    try:
        with open('./db/data.json', 'r', encoding="utf8") as file:
            data = json.loads(file.read())
    
            return list(filter(lambda ninja: ninja['type'] == category, data['ninjas']))

    except Exception as e:
        print(e)


@app.post('/ninjas', tags=["Ninjas"])
def create_ninja(ninja: Ninja):
    
    try:
        with open('./db/data.json', 'r', encoding="utf8") as file:
            data = json.loads(file.read())

            nuevo_ninja = {
                "id": len(data['ninjas']) + 1,
                "name": ninja.name,
                "pharase": ninja.pharase,
                "technique": ninja.technique,
                "type": ninja.type,
                "village": ninja.village
            }

            data['ninjas'].append(nuevo_ninja)
            
            result = {"ninjas": data['ninjas']}

            with open('./db/data.json', 'w', encoding="utf8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
                return nuevo_ninja

    except Exception as e:
        print(e)


@app.put('/ninjas/{id}', tags=["Ninjas"])
def update_ninja(id: int, nuevo_ninja: Ninja):

    try:
        with open('./db/data.json', 'r', encoding="utf8") as file:
            data = json.loads(file.read())
            
            for ninja in data['ninjas']:
                if ninja['id'] == id:
                    ninja['name'] = nuevo_ninja.name
                    ninja['pharase'] = nuevo_ninja.pharase
                    ninja['technique'] = nuevo_ninja.technique
                    ninja['type'] = nuevo_ninja.type
                    ninja['village'] = nuevo_ninja.village
                    
                    result = {"ninjas": data['ninjas']}

                    with open('./db/data.json', 'w', encoding="utf8") as file:
                        json.dump(result, file, ensure_ascii=False, indent=4)
                        return ninja

    except Exception as e:
        print(e)


@app.delete('/ninjas/{id}', tags=["Ninjas"])
def delete_ninja(id: int):

    try:
        with open('./db/data.json', 'r', encoding="utf8") as file:
            data = json.loads(file.read())
            
            filtered_ninjas = list(filter(lambda ninja: ninja['id'] != id, data['ninjas']))

            result = {"ninjas": filtered_ninjas}
            
            with open('./db/data.json', 'w', encoding="utf8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
                return id

    except Exception as e:
        print(e)