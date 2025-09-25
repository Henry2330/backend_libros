from fastapi.testclient import TestClient
from main_libros import app

client = TestClient(app)


# Tests de evaluación de clientes


def test_endpoint_infantil():
    respuesta = client.get("/evaluaciones/libros?edad=10&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "Infantil"

def test_endpoint_premium():
    respuesta = client.get("/evaluaciones/libros?edad=20&suscripcion=premium")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert "Libros Digitales Exclusivos" in body["data"]["acceso"]

def test_endpoint_juvenil():
    respuesta = client.get("/evaluaciones/libros?edad=15&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "Juvenil"

def test_endpoint_general():
    respuesta = client.get("/evaluaciones/libros?edad=30&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "General"

def test_endpoint_edad_negativa():
    respuesta = client.get("/evaluaciones/libros?edad=-5&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "RECHAZADO"
    assert body["data"]["califica"] is False


# Tests de CRUD de libros


def test_obtener_libros():
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)

def test_crear_libro():
    nuevo_libro = {
        "titulo": "Don Quijote",
        "autor": "Miguel de Cervantes",
        "categoria": "General"
    }
    respuesta = client.post("/libros", json=nuevo_libro)
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["titulo"] == "Don Quijote"
    assert body["autor"] == "Miguel de Cervantes"

def test_obtener_libro_por_id():
    # asumimos que existe el libro con id=1
    respuesta = client.get("/libros/1")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert "titulo" in body
    assert "autor" in body

def test_actualizar_libro():
    # primero creamos un libro
    nuevo_libro = {
        "titulo": "El Principito",
        "autor": "Antoine de Saint-Exupéry",
        "categoria": "Infantil"
    }
    creado = client.post("/libros", json=nuevo_libro).json()
    libro_id = creado["id"]

    # ahora lo actualizamos
    datos_actualizados = {
        "titulo": "El Principito (Edición Revisada)",
        "autor": "Antoine de Saint-Exupéry",
        "categoria": "Infantil"
    }
    respuesta = client.put(f"/libros/{libro_id}", json=datos_actualizados)
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["titulo"] == "El Principito (Edición Revisada)"

def test_eliminar_libro():
    # primero creamos un libro para eliminarlo
    nuevo_libro = {
        "titulo": "Libro Temporal",
        "autor": "Autor X",
        "categoria": "General"
    }
    creado = client.post("/libros", json=nuevo_libro).json()
    libro_id = creado["id"]

    # ahora lo eliminamos
    respuesta = client.delete(f"/libros/{libro_id}")
    assert respuesta.status_code == 200
    assert respuesta.json()["mensaje"] == "Libro eliminado"

    # verificamos que ya no exista
    respuesta2 = client.get(f"/libros/{libro_id}")
    assert respuesta2.status_code == 404

