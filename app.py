from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector

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

@app.route("/buscar", methods=["GET"])
def buscar():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos_pagos")
    registros = cursor.fetchall()
    con.close()
    return jsonify({"data": registros})

@app.route("/registrar", methods=["POST"])
def registrar():
    args = request.json
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()
    
    sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
    val = (args["telefono"], args["archivo"])
    cursor.execute(sql, val)
    con.commit()
    
    curso_pago = {
        "Id_Curso_Pago": cursor.lastrowid,
        "Telefono": args["telefono"],
        "Archivo": args["archivo"]
    }
    
    pusher_client = pusher.Pusher(
        app_id="1868455",
        key="613876ac427a3cc5a9f9",
        secret="6768ebc9cfd867046a84",
        cluster="us3",
        ssl=True
    )
    pusher_client.trigger("canalCursosPagos", "registroCursoPago", curso_pago)
    return jsonify(curso_pago)

@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    args = request.json
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "UPDATE tst0_cursos_pagos SET Telefono = %s, Archivo = %s WHERE Id_Curso_Pago = %s"
    val = (args["telefono"], args["archivo"], id)
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return jsonify({"mensaje": "Registro actualizado", "Id_Curso_Pago": id})

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "DELETE FROM tst0_cursos_pagos WHERE Id_Curso_Pago = %s"
    cursor.execute(sql, (id,))
    con.commit()
    con.close()

    return jsonify({"mensaje": "Registro eliminado", "Id_Curso_Pago": id})

if __name__ == "__main__":
    app.run(debug=True)
