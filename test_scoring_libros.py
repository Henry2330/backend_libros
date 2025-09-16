from scoring_libros import evaluar_libros_cliente

def test_rechazo_por_edad_invalida():
    resultado = evaluar_libros_cliente(-5, "regular")
    assert resultado["califica"] is False

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

def test_premium_extra():
    resultado = evaluar_libros_cliente(25, "premium")
    assert "Libros Digitales Exclusivos" in resultado["acceso"]
