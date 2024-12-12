from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

app = Flask(__name__)

class ControladorCursosPagos:
    def notificarActualizacionCursoPago(self, curso_pago):
        pusher_client = pusher.Pusher(
            app_id="1868455",
            key="613876ac427a3cc5a9f9",
            secret="6768ebc9cfd867046a84",
            cluster="us3",
            ssl=True
        )
    
        pusher_client.trigger("canalCursosPagos", "registroCursoPago", curso_pago)

    def buscar(self):
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )

        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tst0_cursos_pagos")
        
        registros = cursor.fetchall()
        con.close()

        return jsonify(registros)

    def registrar(self, telefono, archivo):
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )

        cursor = con.cursor()

        sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
        val = (telefono, archivo)
        cursor.execute(sql, val)
        
        con.commit()
        id_curso_pago = cursor.lastrowid
        con.close()

        curso_pago = {
            "Id_Curso_Pago": id_curso_pago,
            "Telefono": telefono,
            "Archivo": archivo
        }

        self.notificarActualizacionCursoPago(curso_pago)

        return jsonify(curso_pago), 201

    def actualizar(self, id, telefono, archivo):
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )

        cursor = con.cursor()

        sql = "UPDATE tst0_cursos_pagos SET Telefono = %s, Archivo = %s WHERE Id_Curso_Pago = %s"
        val = (telefono, archivo, id)
        cursor.execute(sql, val)
        
        con.commit()
        con.close()

        return jsonify({"message": "Registro actualizado exitosamente"}), 200

    def eliminar(self, id):
        con = mysql.connector.connect(
            host="185.232.14.52",
            database="u760464709_tst_sep",
            user="u760464709_tst_sep_usr",
            password="dJ0CIAFF="
        )

        cursor = con.cursor()

        sql = "DELETE FROM tst0_cursos_pagos WHERE Id_Curso_Pago = %s"
        val = (id,)
        cursor.execute(sql, val)
        
        con.commit()
        con.close()

        return jsonify({"message": "Registro eliminado exitosamente"}), 200

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/buscar")
def buscar():
    controlador = ControladorCursosPagos()
    return controlador.buscar()

@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json
    controlador = ControladorCursosPagos()
    return controlador.registrar(data["telefono"], data["archivo"])

@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json
    controlador = ControladorCursosPagos()
    return controlador.actualizar(id, data["telefono"], data["archivo"])

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    controlador = ControladorCursosPagos()
    return controlador.eliminar(id)

if __name__ == "__main__":
    app.run(debug=True)
