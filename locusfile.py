from locust import HttpUser, task, between

class BibliotecaUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Se ejecuta cuando el usuario virtual inicia la prueba"""
        resp = self.client.post("/libros", json={
            "titulo": "Libro Locust",
            "autor": "Autor Virtual",
            "categoria": "General"
        })

        if resp.status_code == 200:
            self.mi_libro_id = resp.json()["id"]
        else:
            self.mi_libro_id = None

    @task(2)
    def listar_libros(self):
        """Listar todos los libros"""
        self.client.get("/libros")

    @task(2)
    def obtener_libro(self):
        """Obtener el libro propio"""
        if self.mi_libro_id:
            resp = self.client.get(f"/libros/{self.mi_libro_id}", catch_response=True)
            if resp.status_code in [200, 404]:
                resp.success()
            else:
                resp.failure(f"Error inesperado: {resp.status_code}")

    @task(2)
    def actualizar_libro(self):
        """Actualizar el libro propio"""
        if self.mi_libro_id:
            resp = self.client.put(f"/libros/{self.mi_libro_id}", json={
                "titulo": "Libro actualizado Locust",
                "autor": "Autor Virtual",
                "categoria": "Juvenil"
            }, catch_response=True)

            if resp.status_code in [200, 404]:
                resp.success()
            else:
                resp.failure(f"Error inesperado: {resp.status_code}")

    @task(1)
    def eliminar_libro(self):
        """Eliminar el libro propio"""
        if self.mi_libro_id:
            resp = self.client.delete(f"/libros/{self.mi_libro_id}", catch_response=True)
            if resp.status_code in [200, 404]:
                resp.success()
            else:
                resp.failure(f"Error inesperado: {resp.status_code}")


    # -----------------
    #   ENDPOINTS EVALUACIONES
    # -----------------
    @task(1)
    def evaluacion_infantil(self):
        self.client.get("/evaluaciones/libros?edad=10&suscripcion=regular")

    @task(1)
    def evaluacion_juvenil(self):
        self.client.get("/evaluaciones/libros?edad=15&suscripcion=regular")

    @task(1)
    def evaluacion_general(self):
        self.client.get("/evaluaciones/libros?edad=30&suscripcion=regular")

    @task(1)
    def evaluacion_premium(self):
        self.client.get("/evaluaciones/libros?edad=25&suscripcion=premium")
