from scoring_libros import evaluar_libros_cliente


def test_rechazo_por_edad_invalida():
    resultado = evaluar_libros_cliente(-5, "regular")
    assert resultado["califica"] is False


# --- Categorías principales ---

def test_infantil():
    resultado = evaluar_libros_cliente(10, "regular")
    assert resultado["categoria"] == "Infantil"
    assert "Libros Infantiles" in resultado["acceso"]

def test_juvenil():
    resultado = evaluar_libros_cliente(15, "regular")
    assert resultado["categoria"] == "Juvenil"
    assert "Libros Juveniles" in resultado["acceso"]

def test_general():
    resultado = evaluar_libros_cliente(25, "regular")
    assert resultado["categoria"] == "General"
    assert "Libros Generales" in resultado["acceso"]


# --- Beneficio premium ---

def test_premium_extra():
    resultado = evaluar_libros_cliente(25, "premium")
    assert "Libros Digitales Exclusivos" in resultado["acceso"]

def test_premium_infantil():
    resultado = evaluar_libros_cliente(8, "premium")
    assert "Libros Infantiles" in resultado["acceso"]
    assert "Libros Digitales Exclusivos" in resultado["acceso"]

def test_premium_juvenil():
    resultado = evaluar_libros_cliente(16, "premium")
    assert "Libros Juveniles" in resultado["acceso"]
    assert "Libros Digitales Exclusivos" in resultado["acceso"]


# --- Límite de edades ---

def test_infantil_limite_inferior():
    resultado = evaluar_libros_cliente(0, "regular")
    assert resultado["categoria"] == "Infantil"

def test_juvenil_limite_inferior():
    resultado = evaluar_libros_cliente(13, "regular")
    assert resultado["categoria"] == "Juvenil"

def test_juvenil_limite_superior():
    resultado = evaluar_libros_cliente(17, "regular")
    assert resultado["categoria"] == "Juvenil"

def test_general_limite():
    resultado = evaluar_libros_cliente(18, "regular")
    assert resultado["categoria"] == "General"


# --- Otros escenarios ---

def test_suscripcion_vacia():
    resultado = evaluar_libros_cliente(25, "")
    assert "Libros Digitales Exclusivos" not in resultado["acceso"]

def test_general_edad_alta():
    resultado = evaluar_libros_cliente(120, "regular")
    assert resultado["categoria"] == "General"
    assert resultado["califica"] is True
