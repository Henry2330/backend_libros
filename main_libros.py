from fastapi import FastAPI, HTTPException
from scoring_libros import evaluar_libros_cliente

app = FastAPI()

@app.get("/evaluaciones/libros")
def evaluar_libros(edad: int, suscripcion: str):


    resultado = evaluar_libros_cliente(edad, suscripcion)

    if resultado["califica"]:
        return {
            "status": "APROBADO",
            "mensaje": f"Usted puede acceder a la categoría {resultado['categoria']}",
            "data": resultado
        }
    else:
        return {
            "status": "RECHAZADO",
            "mensaje": "No puede acceder a libros con los datos proporcionados",
            "data": resultado
        }
