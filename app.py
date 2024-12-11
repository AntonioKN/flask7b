from flask import Flask, render_template, request, jsonify
import pusher
from modelo import ConexionDB, CursoPagoModelo

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de Pusher
pusher_client = pusher.Pusher(
    app_id="1868455",
    key="613876ac427a3cc5a9f9",
    secret="6768ebc9cfd867046a84",
    cluster="us3",
    ssl=True
)

# Ruta para la vista principal
@app.route("/")
def index():
    return render_template("app.html")

# Controlador: Buscar registros
@app.route("/buscar")
def buscar():
    try:
        registros = CursoPagoModelo.obtener_todos()
        return jsonify(registros)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador: Registrar un nuevo registro
@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json

    try:
        id_curso_pago = CursoPagoModelo.insertar(data["telefono"], data["archivo"])
        curso_pago = {
            "Id_Curso_Pago": id_curso_pago,
            "Telefono": data["telefono"],
            "Archivo": data["archivo"]
        }
        
        # Notificar a través de Pusher
        pusher_client.trigger("canalCursosPagos", "registroCursoPago", curso_pago)
        return jsonify(curso_pago), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador: Actualizar un registro existente
@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json

    try:
        CursoPagoModelo.actualizar(id, data["telefono"], data["archivo"])
        return jsonify({"message": "Registro actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Controlador: Eliminar un registro
@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    try:
        CursoPagoModelo.eliminar(id)
        return jsonify({"message": "Registro eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
