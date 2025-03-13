from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
#import sqlalchemy
from sqlalchemy import create_engine
import os
#from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import text
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

connection = None
#jaja


ENV = os.environ.get('ENV')

#engine = create_engine('postgresql://user:password@host/database')
#metadata.create_all(engine)



app = Flask(__name__)

if ENV == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://arcadia:pinares2024@postgres-db.clm8ssljcpfm.us-east-1.rds.amazonaws.com:5432/arcadia"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
else:    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
#engine2 = create_engine('postgresql://iclarpro:2015@localhost/arcadia', connect_args={'options': '-csearch_path={}'.format('public,arcadia,public')})
if ENV == "production":
    engine = create_engine("postgresql://arcadia:pinares2024@postgres-db.clm8ssljcpfm.us-east-1.rds.amazonaws.com:5432/arcadia")
    connection = engine.connect()
else:
    engine = create_engine('postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia')
    connection = engine.connect()

db = SQLAlchemy(app)

CORS(app)
jwt = JWTManager(app)


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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Inmueble(db.Model):
    __tablename__ = 'inmueble'  # Specifies the table name

    # Define columns as per your PostgreSQL schema
    codigo = db.Column(db.Integer, primary_key=True)  # Primary key
    iden1 = db.Column(db.String, nullable=True)
    iden2 = db.Column(db.String, nullable=True)
    tipo = db.Column(db.String, nullable=True)
    superficie = db.Column(db.Numeric, nullable=True)
    titulo1 = db.Column(db.String, nullable=True)
    lindero1 = db.Column(db.String, nullable=True)
    titulo2 = db.Column(db.String, nullable=True)
    lindero2 = db.Column(db.String, nullable=True)
    titulo3 = db.Column(db.String, nullable=True)
    lindero3 = db.Column(db.String, nullable=True)
    titulo4 = db.Column(db.String, nullable=True)
    lindero4 = db.Column(db.String, nullable=True)
    indiviso = db.Column(db.Numeric, nullable=True)
    condominio = db.Column(db.String, nullable=True)
    cuentacatastral = db.Column(db.String, nullable=True)
    precio = db.Column(db.Numeric, nullable=True)
    inmueble = db.Column(db.String, nullable=False)  # This column is NOT NULL
    superficiecasa = db.Column(db.Numeric, nullable=True)
    domiciliooficial = db.Column(db.String, nullable=True)
    fechadeventa = db.Column(db.Date, nullable=True)
    fk_etapa = db.Column(db.Integer, nullable=False)  # Foreign key to etapa
    escriturado = db.Column(db.String, nullable=True)
    fk_escrituras = db.Column(db.Integer, nullable=True)
    fk_notario = db.Column(db.Integer, nullable=True)
    fechaescriturado = db.Column(db.String, nullable=True)
    preciopormetro = db.Column(db.Numeric, nullable=True)
    referenciapago = db.Column(db.String, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("usuario", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/api/clientes', methods=['GET'])
@jwt_required()
def get_clientes():
    result = db.session.execute(text("""SELECT distinct(cc.codigo) as cuenta, c.codigo as cliente, 
            c.nombre, c.rfc, cc.saldo, i.iden1, i.iden2 
            FROM cuenta cc join cliente c on c.codigo=cc.fk_cliente 
            join inmueble i on cc.fk_inmueble=i.codigo where saldo>0"""))
    clientes = result.fetchall()

    # Convert list of tuples to a list of dictionaries
    clientes_list = [{"id":cliente[1], "cuenta": cliente[0], 
            "nombre": cliente[2], "rfc": cliente[3], "saldo":cliente[4], 
            "manzana":cliente[5], "lote":cliente[6]} for cliente in clientes]
    response  =jsonify(clientes_list)
    # response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
    # response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    # response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    return response

@app.route('/api/clientes/<int:id>', methods=['GET'])
@jwt_required()
def get_cliente(id):
    user = Cliente.query.get(id)
    if not user:
        return jsonify({"error": "Cliente not found"}), 404

    response  =jsonify(user.as_dict())
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


@app.route('/api/cuenta/<int:id>', methods=['GET'])
@jwt_required()
def cuenta_id(id):
    cuenta = Cuenta.query.get(id)
    if not cuenta:
        return jsonify({"error": "Cuenta not found"}), 404
    response  =jsonify(cuenta.as_dict())
    return response

@app.route('/api/inmueble/<int:id>', methods=['GET'])
@jwt_required()
def inmueble_id(id):
    inmueble = Inmueble.query.get(id)
    if not inmueble:
        return jsonify({"error": "inmueble not found"}), 404
    response  =jsonify(inmueble.as_dict())
    return response


if __name__ == '__main__':
    app.run(debug=True)
