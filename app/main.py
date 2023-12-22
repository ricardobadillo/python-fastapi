from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get('/', response_class=HTMLResponse)
def get_index():
    return """
        <h1> Hola mundo </h1>
    """


@app.get('/contact')
def get_list():
    return {"name": "Ricardo", "edad": 29}