from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from scoring_libros import evaluar_libros_cliente

app = FastAPI()


libros_db = []
contador_id = 1

class Libro(BaseModel):
    titulo: str
    autor: str
    categoria: str

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

# CRUD de libros

# Simulación de una base de datos en memoria
libros_db = [
    {"id": 1, "titulo": "Cien Años de Soledad", "autor": "Gabriel García Márquez", "categoria": "General"},
    {"id": 2, "titulo": "El Principito", "autor": "Antoine de Saint-Exupéry", "categoria": "Infantil"},
]

contador_id = max([l["id"] for l in libros_db]) + 1

# ENDPOINTS CRUD 

@app.get("/libros", response_model=List[dict])
def listar_libros():
    return libros_db


@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in libros_db:
        if libro["id"] == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.post("/libros")
def crear_libro(libro: Libro):
    global contador_id
    nuevo_libro = libro.model_dump()
    nuevo_libro["id"] = contador_id   
    libros_db.append(nuevo_libro)
    contador_id += 1
    return nuevo_libro


@app.put("/libros/{libro_id}")
def actualizar_libro(libro_id: int, libro: Libro):
    for l in libros_db:
        if l["id"] == libro_id:
            l.update(libro.model_dump())
            return l
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    for l in libros_db:
        if l["id"] == libro_id:
            libros_db.remove(l)
            return {"mensaje": "Libro eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")
