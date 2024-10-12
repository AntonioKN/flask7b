from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tst0_cursos_pagos")
    
    registros = cursor.fetchall()
    con.close()

    return jsonify(registros)

@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
    val = (data["telefono"], data["archivo"])
    cursor.execute(sql, val)
    
    con.commit()
    id_curso_pago = cursor.lastrowid
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1868455",
        key="613876ac427a3cc5a9f9",
        secret="6768ebc9cfd867046a84",
        cluster="us3",
        ssl=True
    )

    curso_pago = {
        "Id_Curso_Pago": id_curso_pago,
        "Telefono": data["telefono"],
        "Archivo": data["archivo"]
    }

    pusher_client.trigger("canalCursosPagos", "registroCursoPago", curso_pago)
    return jsonify(curso_pago), 201

@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "UPDATE tst0_cursos_pagos SET Telefono = %s, Archivo = %s WHERE Id_Curso_Pago = %s"
    val = (data["telefono"], data["archivo"], id)
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    return jsonify({"message": "Registro actualizado exitosamente"}), 200

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "DELETE FROM tst0_cursos_pagos WHERE Id_Curso_Pago = %s"
    val = (id,)
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    return jsonify({"message": "Registro eliminado exitosamente"}), 200

if __name__ == "__main__":
    app.run(debug=True)
