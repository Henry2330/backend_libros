def evaluar_libros_cliente(edad, suscripcion):
  
    if edad < 0:
        return {"califica": False, "categoria": None, "acceso": []}

    # Premium tiene acceso adicional
    if suscripcion.lower() == "premium":
        acceso_extra = ["Libros Digitales Exclusivos"]
    else:
        acceso_extra = []

    if edad < 12:
        return {"califica": True, "categoria": "Infantil", "acceso": ["Libros Infantiles"] + acceso_extra}

    if 12 <= edad < 18:
        return {"califica": True, "categoria": "Juvenil", "acceso": ["Libros Juveniles"] + acceso_extra}

    return {"califica": True, "categoria": "General", "acceso": ["Libros Generales"] + acceso_extra}


print(evaluar_libros_cliente(10, "regular"))
print(evaluar_libros_cliente(15, "premium"))
print(evaluar_libros_cliente(30, "premium"))
