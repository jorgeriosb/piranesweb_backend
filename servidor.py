from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
import os
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import text

connection = None
#jaja


ENV = os.environ.get('ENV')

#engine = create_engine('postgresql://user:password@host/database')
#metadata.create_all(engine)



app = Flask(__name__)

if ENV == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://arcadia:pinares2024@postgres-db.clm8ssljcpfm.us-east-1.rds.amazonaws.com:5432/arcadia"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
else:    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#engine2 = create_engine('postgresql://iclarpro:2015@localhost/arcadia', connect_args={'options': '-csearch_path={}'.format('public,arcadia,public')})
if ENV == "production":
    engine = create_engine("postgresql://arcadia:pinares2024@postgres-db.clm8ssljcpfm.us-east-1.rds.amazonaws.com:5432/arcadia")
    connection = engine.connect()
else:
    engine = create_engine('postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia')
    connection = engine.connect()

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




@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    result = db.session.execute(text("SELECT distinct(c.codigo), c.nombre, c.rfc, cc.saldo, i.iden1, i.iden2, c.codigo  FROM cuenta cc join cliente c on c.codigo=cc.fk_cliente join inmueble i on cc.fk_inmueble=i.codigo where saldo>0"))
    clientes = result.fetchall()

    # Convert list of tuples to a list of dictionaries
    clientes_list = [{"id":cliente[0], "cuenta": cliente[0], "nombre": cliente[1], "rfc": cliente[2], "saldo":cliente[3], "manzana":cliente[4], "lote":cliente[5], "cliente":cliente[6]} for cliente in clientes]
    response  =jsonify(clientes_list)
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    return response

@app.route('/api/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    user = Cliente.query.get(id)
    if not user:
        return jsonify({"error": "Cliente not found"}), 404

    response  =jsonify(user.as_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    return response

@app.route('/api/clientes', methods=['POST'])
def add_cliente():
    new_cliente = request.get_json()

    if not new_cliente or not new_cliente.get('name') or not new_cliente.get('email'):
        return jsonify({"error": "Missing data"}), 400

    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute(
    #     "INSERT INTO clientes (name, email) VALUES (%s, %s) RETURNING id;",
    #     (new_cliente['name'], new_cliente['email'])
    # )
    # new_id = cursor.fetchone()[0]
    # conn.commit()
    # cursor.close()
    # conn.close()

    #return jsonify({"id": new_id, "name": new_cliente['name'], "email": new_cliente['email']}), 201
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True)
