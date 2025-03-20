from pydoc import Doc
from xml.dom.minidom import Document
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


ENV = os.environ.get('ENV')
USER = os.environ.get('USERD')
PASS = os.environ.get('PASS')
HOST = os.environ.get('HOSTD')





app = Flask(__name__)

if ENV == "production":
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{USER}:{PASS}@{HOST}:5432/arcadia"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
else:    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jorge.rios:Mexiquito1991$@localhost/arcadia"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret"
if ENV == "production":
    engine = create_engine(f"postgresql://{USER}:{PASS}@{HOST}:5432/arcadia")
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
    

class Documento(db.Model):
    __tablename__ = 'documento'
    
    # Define columns based on the SQL schema
    codigo = db.Column(db.Integer, primary_key=True, nullable=False)
    fechadeelaboracion = db.Column(db.Date, nullable=False)
    fechadevencimiento = db.Column(db.Date, nullable=False)
    fechadevencimientovar = db.Column(db.Date, nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    cargo = db.Column(db.Float, nullable=False)
    abono = db.Column(db.Float, nullable=False)
    
    # Foreign keys
    fk_cuenta = db.Column(db.Integer, nullable=False)
    fk_tipo = db.Column(db.Integer, nullable=False)
    
    # Relationship (if necessary to link with other tables)
    # For example, linking to "Cuenta" and "Tipo" tables:
    # cuenta = db.relationship('Cuenta', backref='documentos')
    # tipo = db.relationship('Tipo', backref='documentos')
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Movimiento(db.Model):
    __tablename__ = 'movimiento'
    
    codigo = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    relaciondepago = db.Column(db.String, nullable=True)
    cargoabono = db.Column(db.String(1), nullable=False)
    fechavencimientodoc = db.Column(db.Date, nullable=True)
    fk_documento = db.Column(db.Integer, nullable=False)
    fk_tipo = db.Column(db.Integer, nullable=False)
    numrecibo = db.Column(db.Integer, nullable=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# aqui arriba estan los modelos




@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("usuario", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, expires_delta=False)
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
            join inmueble i on cc.fk_inmueble=i.codigo  where i.fk_etapa in (8,9,10,33,34,35) order by 1"""))
    clientes = result.fetchall()

    # Convert list of tuples to a list of dictionaries
    clientes_list = [{"id":cliente[0], "cliente": cliente[1], 
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

def validaCliente(cliente):
    cliente["fechadenacimiento"] = None if cliente.get("fechadenacimiento") == "" else cliente.get("fechadenacimiento")
    cliente["conyugefechadenacimiento"] = None if cliente.get("conyugefechadenacimiento") == "" else cliente.get("conyugefechadenacimiento")
    cliente["edad"] = None if cliente.get("edad") == "" else cliente.get("edad")

    return cliente
    
@app.route('/api/clientes', methods=['POST'])
def add_cliente():
    new_cliente = request.get_json()
    new_cliente = validaCliente(new_cliente)
    #print("viendo cliente", new_cliente)

    if not new_cliente.get('nombre'):
        return jsonify({"status": "error", "message":"Missing data"}), 400
    
    if new_cliente.get("clienteNuevo"):
        new_cliente.pop("clienteNuevo")
        result = db.session.execute(text("""select max(codigo) from cliente"""))
        codigo = result.fetchone()[0]
        new_cliente["codigo"]=int(codigo+1)
        cliente = Cliente(**new_cliente)
        db.session.add(cliente)
        db.session.commit()    
    else:
        new_cliente.pop("clienteNuevo")
        cliente_find = Cliente.query.get(new_cliente.get('codigo'))
        if cliente_find:
            return jsonify({"status": "error", "message":"Ya existe ese codigo"}), 400
        cliente = Cliente(**new_cliente)
        db.session.add(cliente)
        db.session.commit()
    return jsonify({"status":"good", "data":cliente.as_dict()})


@app.route('/api/cuenta/<int:id>', methods=['GET'])
@jwt_required()
def cuenta_id(id):
    cuenta = Cuenta.query.get(id)
    if not cuenta:
        return jsonify({"error": "Cuenta not found"}), 404
    response  =jsonify(cuenta.as_dict())
    return response

@app.route('/api/cuenta/<int:id>/documentos', methods=['GET'])
@jwt_required()
def cuenta_id_documentos(id):
    documentos = Documento.query.filter_by(fk_cuenta=id).order_by(Documento.codigo).all() #db.session.execute(db.select(Documento).filter_by(fk_cuenta=id)).scalars()
    if not documentos:
        return jsonify({"error": "Cuenta not found"}), 404
    response  =[x.as_dict() for x in documentos]
    response = jsonify(list(map(lambda x: {"id":x["codigo"], **x}, response)))
    return response

@app.route('/api/inmueble/<int:id>', methods=['GET'])
@jwt_required()
def inmueble_id(id):
    inmueble = Inmueble.query.get(id)
    if not inmueble:
        return jsonify({"error": "inmueble not found"}), 404
    response  =jsonify(inmueble.as_dict())
    return response


@app.route('/api/documento/<int:id>/movimientos', methods=['GET'])
@jwt_required()
def get_documento_movimientos(id):
    movimientos = db.session.execute(db.select(Movimiento).filter_by(fk_documento=id)).scalars()
    if not movimientos:
        return jsonify({"error": "Movimientos not found"}), 404
    response  =[x.as_dict() for x in movimientos]
    response = jsonify(list(map(lambda x:{"id":x["codigo"], 
                "cantidad":x["cantidad"], "fecha":x["fecha"], 
                "cargoabono":x["cargoabono"],
                "fechavencimientodoc":x["fechavencimientodoc"], 
                "numrecibo":x["numrecibo"]}, response)))
    return response


@app.route('/api/documento/<int:id>/pagoanterior', methods=['POST'])
@jwt_required()
def documento_pago_anterior(id):
    req= request.get_json()
    documento = Documento.query.get(id)
    if not documento:
        return jsonify({"status":"error", "message":"no se encontro documento"})
    if documento.saldo <= 0:
        return jsonify({"status":"error","message":"ya esta pagado"})
    if documento.saldo < float(req["cantidad"]):
        return jsonify({"status":"error","message":"no se puede pagar una cantidad mayor que la que tiene"})
    result = db.session.execute(text("""SELECT max(codigo) +1 from movimiento"""))
    movimiento_id = result.fetchone()
    query = f"""insert into movimiento 
        (codigo, cantidad, fecha, 
        cargoabono, fk_documento, fk_tipo, numrecibo)
        values ({movimiento_id[0]}, {req["cantidad"]}, '{req["fecha"]}', 'A', {id}, 4, {req["numrecibo"]})"""
    result = db.session.execute(text(query))
    db.session.commit()
    documento.saldo-=float(req["cantidad"])
    documento.abono+=float(req["cantidad"])
    db.session.commit()
    result = db.session.execute(text(f"""update cuenta set saldo=(saldo-{float(req["cantidad"])}) where codigo={documento.fk_cuenta}"""))
    db.session.commit()
    return jsonify({"status":"good", "message":"movimiento de abono realizado"})





if __name__ == '__main__':
    app.run(debug=True)
