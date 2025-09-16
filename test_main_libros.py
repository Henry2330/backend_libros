from fastapi.testclient import TestClient
from main_libros import app

client = TestClient(app)

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

def test_endpoint_sin_suscripcion():
    respuesta = client.get("/evaluaciones/libros?edad=25&suscripcion=")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "General"
    assert "Libros Digitales Exclusivos" not in body["data"]["acceso"]

def test_endpoint_edad_negativa():
    respuesta = client.get("/evaluaciones/libros?edad=-5&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "RECHAZADO"
    assert body["data"]["califica"] is False

def test_endpoint_edad_cero():
    respuesta = client.get("/evaluaciones/libros?edad=0&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "Infantil"

def test_endpoint_edad_12():
    respuesta = client.get("/evaluaciones/libros?edad=12&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "Juvenil"

def test_endpoint_edad_18():
    respuesta = client.get("/evaluaciones/libros?edad=18&suscripcion=regular")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "General"

def test_endpoint_edad_justo_premium():
    respuesta = client.get("/evaluaciones/libros?edad=18&suscripcion=premium")
    assert respuesta.status_code == 200
    body = respuesta.json()
    assert body["status"] == "APROBADO"
    assert body["data"]["categoria"] == "General"
    assert "Libros Digitales Exclusivos" in body["data"]["acceso"]