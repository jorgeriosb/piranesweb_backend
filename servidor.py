from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    codigo = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String, nullable=False)
    rfc = db.Column(db.String)
    nacionalidad = db.Column(db.String)
    lugardenacimiento = db.Column(db.String)
    fechadenacimiento = db.Column(db.Date)
    estadocivil = db.Column(db.String)
    situacion = db.Column(db.CHAR)
    regimen = db.Column(db.CHAR)
    ocupacion = db.Column(db.CHAR)
    domicilio = db.Column(db.String)
    colonia = db.Column(db.String)
    cp = db.Column(db.String)
    ciudad = db.Column(db.String)
    estado = db.Column(db.String)
    telefonocasa = db.Column(db.String)
    telefonotrabajo = db.Column(db.String)
    conyugenombre = db.Column(db.String)
    conyugenacionalidad = db.Column(db.String)
    conyugelugardenacimiento = db.Column(db.String)
    conyugefechadenacimiento = db.Column(db.Date)
    conyugerfc = db.Column(db.String)
    conyugeocupacion = db.Column(db.CHAR)
    contpaq = db.Column(db.String)
    curp = db.Column(db.String)
    conyugecurp = db.Column(db.String)
    email = db.Column(db.String)
    numeroidentificacion = db.Column(db.String)
    identificacion = db.Column(db.String)
    edad = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Cuenta(db.Model):
    __tablename__ = "cuenta"

    codigo = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    saldo = db.Column(db.Float)
    fk_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    fk_inmueble = db.Column(db.Integer, db.ForeignKey("inmueble.id"), nullable=True)
    fk_tipo_cuenta = db.Column(db.Integer, db.ForeignKey("tipo_cuenta.id"), nullable=True)
    congelada = db.Column(db.Integer, nullable=True)  # Consider changing to Boolean if appropriate

# Set up database connection details
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://iclarpro:2015@localhost/arcadia')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia')
#engine2 = create_engine('postgresql://iclarpro:2015@localhost/arcadia', connect_args={'options': '-csearch_path={}'.format('public,arcadia,public')})


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/sabe2', methods=['GET'])
def prueba():
    return jsonify({})

@app.route('/jaja', methods=['GET'])
def lala():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cliente;")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert list of tuples to a list of dictionaries
    clientes_list = [{"id": cliente[0], "name": cliente[1], "email": cliente[2]} for cliente in clientes]

    return jsonify(clientes_list)

@app.route('/sabe', methods=['GET'])
def lalala():
    clientes = []
    clienteq = Cliente.query.all()
    cuentaq = Cuenta.query.all()
    for x in clienteq:
        clientes.append(dict(codigo=x.codigo, nombre=x.nombre, rfc=x.rfc))
    return jsonify(clientes)


@app.route('/clientes', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT distinct(c.codigo), c.nombre, c.rfc, cc.saldo, i.iden1, i.iden2, c.codigo  FROM cuenta cc join cliente c on c.codigo=cc.fk_cliente join inmueble i on cc.fk_inmueble=i.codigo where saldo>0")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert list of tuples to a list of dictionaries
    clientes_list = [{"id":cliente[0], "cuenta": cliente[0], "nombre": cliente[1], "rfc": cliente[2], "saldo":cliente[3], "manzana":cliente[4], "lote":cliente[5], "cliente":cliente[6]} for cliente in clientes]
    response  =jsonify(clientes_list)
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    return response

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM cliente WHERE codigo ={id}")
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    user = Cliente.query.get(id)
    print("eje")
    print(user)

    if cliente is None:
        return jsonify({"error": "Cliente not found"}), 404

    response  =jsonify(user.as_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    return response

@app.route('/clientes', methods=['POST'])
def add_cliente():
    new_cliente = request.get_json()

    if not new_cliente or not new_cliente.get('name') or not new_cliente.get('email'):
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (name, email) VALUES (%s, %s) RETURNING id;",
        (new_cliente['name'], new_cliente['email'])
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"id": new_id, "name": new_cliente['name'], "email": new_cliente['email']}), 201


if __name__ == '__main__':
    app.run(debug=True)
