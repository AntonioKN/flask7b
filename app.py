from flask import Flask, render_template, request
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
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tst0_cursos_pagos")
    
    registros = cursor.fetchall()
    con.close()

    return {"data": registros}

@app.route("/registrar", methods=["GET"])
def registrar():
    args = request.args

    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor()

    sql = "INSERT INTO tst0_cursos_pagos (Telefono, Archivo) VALUES (%s, %s)"
    val = (args["telefono"], args["archivo"])
    cursor.execute(sql, val)
    
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1868455",
        key="613876ac427a3cc5a9f9",
        secret="6768ebc9cfd867046a84",
        cluster="us3",
        ssl=True
    )

    curso_pago = {
        "Id_Curso_Pago": cursor.lastrowid,
        "Telefono": args["telefono"],
        "Archivo": args["archivo"]
    }

    pusher_client.trigger("canalCursosPagos", "registroCursoPago", curso_pago)
    return curso_pago

if __name__ == "__main__":
    app.run(debug=True)
