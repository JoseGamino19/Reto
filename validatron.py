import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

def obtener_password_aleatorio_de_archivo(filename="passwords.txt"):
    try:
        with open(filename, "r") as f:
            contenido = f.read()
    except FileNotFoundError:
        return None

    if not contenido:
        return None

    intentos = 0
    max_intentos = 100

    while intentos < max_intentos:
        start = random.randint(0, 10000)
        end = start + random.randint(5, 8)
        password_aleatorio = contenido[start:end]
        if 5 <= len(password_aleatorio) <= 8:
            return password_aleatorio
        intentos += 1
    return None

password_correcto = obtener_password_aleatorio_de_archivo()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/login"):
            query = parse_qs(urlparse(self.path).query)
            password_ingresado = query.get("password", [None])[0]

            if not password_ingresado:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Se requiere el parámetro 'password'"}).encode())
                return

            acerto = password_ingresado == password_correcto
            response = {
                "acerto": acerto,
                "password_correcto": password_correcto
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Servidor corriendo en http://localhost:8080")
    httpd.serve_forever()
