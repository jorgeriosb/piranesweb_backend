import json
from pydoc import Doc, doc
from xml.dom.minidom import Document
from flask import Flask, jsonify, request, send_file, make_response, render_template
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
import pdfkit
import io
from datetime import date, datetime, timedelta
import math

from num2words import num2words
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from sqlalchemy import extract
from collections import defaultdict
import calendar
from functools import reduce
from dateutil.relativedelta import relativedelta





def calcular_fecha_fin(fecha_inicio, mensualidades):
    """
    Suma la cantidad de mensualidades a la fecha_inicio y regresa la fecha final.

    :param fecha_inicio: fecha de inicio (datetime.date o datetime.datetime)
    :param mensualidades: número de meses a sumar (int)
    :return: fecha final (datetime.date)
    """
    return fecha_inicio + relativedelta(months=mensualidades - 1)



def numero_a_letras_mxn(cantidad):
    """
    Convierte una cantidad numérica a texto estilo moneda MXN.
    Ejemplo: 790440.84 -> "Setecientos noventa mil cuatrocientos cuarenta pesos 84/100 M.N."
    """
    cantidad = round(float(cantidad), 2)
    parte_entera = int(cantidad)
    parte_decimal = int(round((cantidad - parte_entera) * 100))

    letras = num2words(parte_entera, lang='es').capitalize()
    return f"{letras} pesos {parte_decimal:02d}/100 M.N."


def fecha_a_letras(fecha, leyenda=False):
    [a,m,d] = fecha.split("-")
    mes = ""
    if m =="01":
        mes ="Enero"
    if m =="02":
        mes ="Febrero"
    if m =="03":
        mes ="Marzo"
    if m =="04":
        mes ="Abril"
    if m =="05":
        mes ="Mayo"
    if m =="06":
        mes ="Junio"
    if m =="07":
        mes ="Julio"
    if m =="08":
        mes ="Agosto"
    if m =="09":
        mes ="Septiembre"
    if m =="10":
        mes ="Octubre"
    if m =="11":
        mes ="Noviembre"
    if m =="12":
        mes ="Diciembre"
    if leyenda:
        return f"{d} días del mes de {mes} del {a}"
    return f"{d} de {mes} del {a}"




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


class Vendedor(db.Model):
    __tablename__ = 'vendedor'

    codigo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    domicilio = db.Column(db.String)
    cp = db.Column(db.String)
    ciudad = db.Column(db.String)
    estado = db.Column(db.String)
    telefono = db.Column(db.String)
    rfc = db.Column(db.String)
    email = db.Column(db.String)
    activo = db.Column(db.Boolean)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class GixAmortizacion(db.Model):
    __tablename__ = 'gixamortizacion'

    pkamortizacion = db.Column(db.Numeric, primary_key=True, nullable=False)
    fechacaptura = db.Column(db.Date)
    fechaelaboracion = db.Column(db.Date)
    formapago = db.Column(db.CHAR)
    fkcliente = db.Column(db.Integer)
    fkvendedor = db.Column(db.Integer)
    fketapa = db.Column(db.Integer)
    fkinmueble = db.Column(db.Integer)
    tasainteresanual = db.Column(db.Numeric)
    plazomeses = db.Column(db.Integer)
    fechaprimerpago = db.Column(db.Date)
    preciocontado = db.Column(db.Numeric)
    descuentop = db.Column(db.Numeric)
    descuentoc = db.Column(db.Numeric)
    enganchep = db.Column(db.Numeric)
    enganchec = db.Column(db.Numeric)
    fechaenganche = db.Column(db.Date)
    saldoafinanciar = db.Column(db.Numeric)
    pagomensualfijo = db.Column(db.Numeric)
    contrato = db.Column(db.Integer)
    cuenta = db.Column(db.Integer)

    def as_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            result[column.name] = value
        result["id"]=getattr(self, "pkamortizacion")
        return result


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

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, date):
                result[column.name] = value.strftime('%Y-%m-%d')
            else:
                result[column.name] = value
        return result


class Cuenta(db.Model):
    __tablename__ = "cuenta"

    codigo = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    saldo = db.Column(db.Float)
    fk_cliente =  db.Column(db.Integer) #db.Column(db.Integer, db.ForeignKey("cliente.codigo"), nullable=True)
    fk_inmueble =  db.Column(db.Integer) #db.Column(db.Integer, db.ForeignKey("inmueble.codigo"), nullable=True)
    fk_tipo_cuenta = db.Column(db.Integer)  # db.Column(db.Integer, db.ForeignKey("tipo_cuenta.id"), nullable=True)
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

    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    def as_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            result[column.name] = value
        result["id"]=getattr(self, "codigo")
        return result
    

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
        result = {}
        for c in self.__table__.columns:
            if c.name in ["saldo", "cargo", "abono"]:
                val = getattr(self, c.name)
                val  = round(val,2)
                result[c.name] = val
            else:
                result[c.name] = getattr(self, c.name)
        return result
    
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

class Recibo(db.Model):
    __tablename__ = 'recibo'

    codigo = db.Column(db.Integer, primary_key=True, nullable=False)
    fechaemision = db.Column(db.Date, nullable=False)
    abonocapital = db.Column(db.Float, nullable=False)
    interesmoratorio = db.Column(db.Float, nullable=False)
    totalrecibo = db.Column(db.Float, nullable=False)
    referencia = db.Column(db.String)  # Adjust max length if needed
    status = db.Column(db.String(1), nullable=False)  # For "char"
    fk_desarrollo = db.Column(db.Integer)
    consdesarrollo = db.Column(db.Integer)
    fechaaplicacion = db.Column(db.Date)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String)
    cuentabancaria = db.Column(db.String)
    clabe = db.Column(db.String)
    domicilio = db.Column(db.String)
    telefono = db.Column(db.String)
    rfc = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Departamento(db.Model):
    __tablename__ = 'departamento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Solicitud(db.Model):
    __tablename__ = 'solicitud'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_proveedor = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    fk_departamento = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    fechapago = db.Column(db.Date)
    fechaelaboracion = db.Column(db.Date)
    estatus = db.Column(db.String, nullable=False)

    

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# aqui arriba estan los modelos




@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("usuario", None)
    password = request.json.get("password", None)
    if username not in ["luz", "malr", "eli", "test"] or password not in ["test2", "mexsoros1969", "jgq8928o", "Pinares1443"]:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username, expires_delta=False)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/api/clientescuenta', methods=['GET'])
@jwt_required()
def get_clientescuenta():
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

@app.route('/api/clientesall', methods=['GET'])
@jwt_required()
def get_clientes():
    clientes = [x.as_dict() for x in Cliente.query.order_by(Cliente.nombre).all()]
    response = jsonify(clientes)
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
        #new_cliente.pop("clienteNuevo")
        cliente_find = Cliente.query.get(new_cliente.get('codigo'))
        if cliente_find:
            return jsonify({"status": "error", "message":"Ya existe ese codigo"}), 400
        cliente = Cliente(**new_cliente)
        db.session.add(cliente)
        db.session.commit()
    return jsonify({"status":"good", "data":cliente.as_dict()})

@app.route('/api/clientes/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_cliente(id):
    new_cliente = request.get_json()
    new_cliente = validaCliente(new_cliente)
    print("viendo cliente ", new_cliente)
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'message': 'User not found'}), 404
    Cliente.query.filter_by(codigo=id).update(new_cliente)
    db.session.commit()
    cliente = Cliente.query.get(id)
    return jsonify({"status":"good", "data":cliente.as_dict()})
    


def get_tipo_documento(id):
    print("codigo ", id)
    result = db.session.execute(text("""select descripcion1 from tipo where codigo={}""".format(id)))
    descripcion1 = result.fetchone()
    if descripcion1:
        print("viendo esto ", descripcion1[0])
        return descripcion1[0]
    else:
        return ""

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
    response = jsonify(list(map(lambda x: {"id":x["codigo"], "tipo":get_tipo_documento(x["fk_tipo"]), **x}, response)))
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


@app.route('/api/updateinmuebleprecio', methods=['POST'])
@jwt_required()
def update_inmueble_precio():
    req= request.get_json()
    id = req["inmueble"]
    precioxm2 = req["precio"]
    print("id ", id, " precioxm2 ", precioxm2)
    inmueble = Inmueble.query.get(id)
    if not inmueble:
        return jsonify({"status":"error", "message":"no se encontro inmueble"})
    result = db.session.execute(text(f"""update inmueble set preciopormetro={precioxm2}, precio=({precioxm2}*superficie)  where codigo={id}"""))
    db.session.commit()
    return jsonify({"status":"good", "message":"precio actualizado"})





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


@app.route('/api/documentos/pagar', methods=['POST'])
@jwt_required()
def pagar_documentos_varios():
    req = request.get_json()
    print("viendo valores ", req)
    cantidad = float(req["cantidad"])
    lista_catidades = [round(float(x.get("cantidad", 0)),2)+ round(float(x.get("intereses")),2) for x in req["formData"]]
    total_suma = round(sum(lista_catidades),2)
    intereses = sum([round(float(x.get("intereses", 0)),2) for x in req["formData"]])
    pago = sum([round(float(x.get("cantidad", 0)),2) for x in req["formData"]])
    if cantidad != total_suma:
        return jsonify({"status":"error", "message":"la suma de las cantidades no corresponde con el valor del pago total"})
    recibo = crear_recibo(pago, intereses, cantidad, req["referencia"], req["fecha"])
    if recibo:
        for documento in req["formData"]:
            pagar_documento(documento, req["fecha"], recibo)
    #hacer_recibopdf(req) no se si haga falta
    print("regreso este recibo ", recibo)
    return jsonify({"status":"good", "recibo":recibo})


@app.route('/api/gixamortizacion/<int:id>', methods=['GET'])
@jwt_required()
def get_gixamortizacion(id):
    gixamortizacion = GixAmortizacion.query.filter_by(cuenta=id).scalar()
    if not gixamortizacion:
        return jsonify({"error": "gixamortizacion not found"}), 404
    response  =jsonify(gixamortizacion.as_dict())
    return response


# def hacer_recibopdf(req):
#     pass



def crear_recibo(pago, intereses, total, referencia, fecha):
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    result = db.session.execute(text("""select max(codigo) from recibo"""))
    codigo = result.fetchone()[0]
    nummovimiento = db.session.execute(text("""select max(numrecibo) from movimiento"""))
    num = nummovimiento.fetchone()[0]
    codigo+=1
    if num > codigo:
        codigo = num+1
    llenado = {"codigo":codigo, "fechaemision":fecha, "abonocapital":pago, 
        "interesmoratorio":intereses, "totalrecibo":total, "referencia":referencia,
        "status":"A", "fk_desarrollo":5, "fechaaplicacion":fecha_hoy}
    recibo = Recibo(**llenado)
    db.session.add(recibo)
    db.session.commit()
    return codigo

def pagar_documento(documento, fecha_pago, recibo):
    result = db.session.execute(text("""select max(codigo) from movimiento"""))
    codigo = result.fetchone()[0]
    codigo+=1
    result = db.session.execute(text(f"""select relaciondepago from movimiento where fk_documento={documento["id"]} and cargoabono='C'"""))
    relacionpago = result.fetchone()[0]
    llenado = {"codigo":codigo, "cantidad":documento["cantidad"], "fecha":fecha_pago, "relaciondepago":relacionpago,
        "cargoabono":"A", "fechavencimientodoc":documento["fechadevencimiento"], "fk_documento":documento["id"], "fk_tipo":4, "numrecibo":recibo}
    movimiento = Movimiento(**llenado)
    db.session.add(movimiento)
    db.session.commit()
    doc = Documento.query.get(documento["id"])
    if doc:
        doc.saldo-=float(documento["cantidad"])
        doc.abono+=float(documento["cantidad"])
        db.session.commit()
    cuenta = Cuenta.query.get(doc.fk_cuenta)
    if cuenta:
        cuenta.saldo-=float(documento["cantidad"])
        db.session.commit()
    return True


@app.route('/api/recibo/<int:id>')
@jwt_required()
def download_recibo(id):
    print("viendo el recibo ", id)
    recibo = Recibo.query.get(id)
    if not recibo:
        return jsonify({"error": "recibo not found"}), 404
    movimientos = db.session.execute(db.select(Movimiento).filter_by(numrecibo=id)).scalars()
    if not movimientos:
        return jsonify({"error": "movimientos not found"}), 404
    firstmov = movimientos.first()
    documento = Documento.query.get(firstmov.fk_documento)
    if not documento:
        return jsonify({"error": "documento not found"}), 404
    cuenta = Cuenta.query.get(documento.fk_cuenta)
    if not cuenta:
        return jsonify({"error": "cuenta not found"}), 404
    gixamortizacion = GixAmortizacion.query.filter_by(cuenta=cuenta.codigo).scalar()
    if not gixamortizacion:
        return jsonify({"error": "gixamortizacion not found"}), 404
    cliente = Cliente.query.get(gixamortizacion.fkcliente)
    if not cliente:
        return jsonify({"error": "cliente not found"}), 404
    inmueble = Inmueble.query.get(cuenta.fk_inmueble)
    if not inmueble:
        return jsonify({"error": "inmueble not found"}), 404

    
    movimientos = db.session.execute(db.select(Movimiento).filter_by(numrecibo=id)).scalars()
    good_movimientos = [x.as_dict() for x in movimientos]

    context = {
        'cuenta': cuenta,
        'cliente': cliente,
        "movimientos":good_movimientos,
        "recibo": recibo,
        "inmueble": inmueble
    }
    

    # Generate PDF in memory
    #pdf_bytes = pdfkit.from_string(html_content, False)  # False = return as bytes
    rendered = render_template('recibo.html', **context)

    # PDFKit options
    options = {
        'enable-local-file-access': '',  # VERY important to allow local file access (e.g., image)
    }

    # Generate PDF
    pdf = pdfkit.from_string(rendered, False, options=options)
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='recibo_21799.pdf'
    )


@app.route('/api/inmueblesdisponibles', methods=['GET'])
@jwt_required()
def get_inmuebles_disponibles():
    inmueble_cuenta = [x.fk_inmueble for x in Cuenta.query.with_entities(Cuenta.fk_inmueble).all()]
    inmuebles_disponibles = [x.as_dict() for x in Inmueble.query.filter(~Inmueble.codigo.in_(inmueble_cuenta), Inmueble.fk_etapa.in_([8,9,10,33,34,35])).order_by(Inmueble.iden2, Inmueble.iden1).all()]
    print("cuantos hay ", len(inmuebles_disponibles))
    response = jsonify(inmuebles_disponibles)
    return response


@app.route('/api/vendedores', methods=['GET'])
@jwt_required()
def get_vendedores():
    vendedores = [x.as_dict() for x in Vendedor.query.all()]
    response = jsonify(vendedores)
    return response


@app.route('/api/otro', methods=['GET'])
@jwt_required()
def otro():
    inmuebles_cuenta = Cuenta.query.with_entities(Cuenta.fk_inmueble).all()
    Inmueble.query.filter(~Inmueble.codigo.in_(inmuebles_cuenta)).all()
    response = jsonify({})
    return response



@app.route('/api/tablaamortizacion', methods=['POST'])
@jwt_required()
def genera_amortizacion():
    req= request.get_json()    

    superficie = float(req["inmueble_superficie"])
    precio_m2 = float(req["inmueble_preciopormetro"])
    enganche = float(req["enganche"])
    interes_anual = float(req.get("interes_anual", 0))  # en porcentaje 10.0
    mensualidades = int(req.get("mensualidades",0))
    descuento = float(req.get("descuento"))
    formadepago = req.get("formadepago")

    # Calcular tabla de amortización
    # Cálculos iniciales
    total_intereses = 0
    mensualidad = 0
    precio_inmueble = superficie * precio_m2
    saldo_a_financiar = superficie * precio_m2 - enganche
    if descuento >0:
        saldo_a_financiar-=descuento

    interes_mensual = interes_anual / 100 / 12
    total_a_pagar = 0
    if mensualidades:
        if interes_mensual > 0:
            mensualidad = saldo_a_financiar * (interes_mensual * (1 + interes_mensual) ** mensualidades) / ((1 + interes_mensual) ** mensualidades - 1)
        else:
            mensualidad = saldo_a_financiar / mensualidades

        mensualidad = round(mensualidad, 2)

    # Generar tabla de amortización
    if formadepago == "R":
        tabla = []
        saldo = saldo_a_financiar
        fecha_inicio = datetime.strptime(req["fechaprimerpago"], "%Y-%m-%d")    #datetime.today() # falta esto de fechas

        for i in range(1, mensualidades + 1):
            interes = round(saldo * interes_mensual, 2)
            abono = round(mensualidad - interes, 2)
            saldo = round(saldo - abono, 2)
            if saldo < 0: saldo = 0.00

            tabla.append({
                "n_pago": i,
                "fecha":  (fecha_inicio + relativedelta(months=i-1)).strftime("%d-%m-%Y"),    # (fecha_inicio + timedelta(month=1 * i)).strftime("%d-%m-%Y"),
                "abono": abono,
                "interes": interes,
                "mensualidad": mensualidad,
                "saldo": saldo
            })

        # Totales
        total_intereses = round(sum(p["interes"] for p in tabla), 2)
        total_a_pagar = round(mensualidad * mensualidades, 2)
    else:
        fecha_inicio = datetime.strptime(req["fechaprimerpago"], "%Y-%m-%d")
        tabla = []
        tabla.append({
                "n_pago": 1,
                "fecha": (fecha_inicio + relativedelta(months=0)).strftime("%d-%m-%Y"),
                "abono": saldo_a_financiar,
                "interes": 0,
                "mensualidad": saldo_a_financiar,
                "saldo": 0
            })


    context = {
        "inmueble_iden1":req["inmueble_iden1"],
        "inmueble_iden2":req["inmueble_iden2"],
        "superficie":superficie,
        "precio_m2":precio_m2,
        "enganche":enganche,
        "saldo_a_financiar":saldo_a_financiar,
        "mensualidades":mensualidades,
        "interes_anual":interes_anual,
        "total_intereses":total_intereses if total_intereses else 0,
        "total_a_pagar":total_a_pagar,
        "mensualidad":mensualidad if mensualidad else 0,
        "tabla":tabla,
        "descuento":descuento,
        "precio_inmueble":precio_inmueble
    }
    

    # Generate PDF in memory
    #pdf_bytes = pdfkit.from_string(html_content, False)  # False = return as bytes
    rendered = render_template('amortizacion.html', **context)

    # PDFKit options
    options = {
        'enable-local-file-access': '',  # VERY important to allow local file access (e.g., image)
    }

    # Generate PDF
    pdf = pdfkit.from_string(rendered, False, options=options)
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='amortizacion.pdf'
    )


@app.route('/api/pagare', methods=['POST'])
@jwt_required()
def genera_pagare():
    req= request.get_json()
    mensualidad = 0
    fecha = datetime.strptime(req["fecha_inicio"], '%Y-%m-%d').date()
    
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    if req.get("plazo_meses"):
        mensualidad = req["total_pagare"] / req.get("plazo_meses")
        fecha_final = calcular_fecha_fin(fecha, req.get("plazo_meses"))
    else:
        mensualidad = req["total_pagare"]
        fecha_final = calcular_fecha_fin(fecha, 1)
    
    fecha_fin = fecha_final.strftime('%Y-%m-%d')

    mensualidad = round(mensualidad, 2)
    context = {
        "acreedor": req["acreedor"],
        "domicilio_acreedor": req["domicilio_acreedor"],
        "total_pagare": req["total_pagare"],
        "total_letras": f"{numero_a_letras_mxn(req["total_pagare"])}",
        "plazo_meses": req.get("plazo_meses") if req.get("plazo_meses") else 1,
        "mensualidad": mensualidad,
        "fecha_inicio": req["fecha_inicio"],
        "fecha_inicio_letras": fecha_a_letras(req["fecha_inicio"]),
        "fecha_fin": fecha_fin,
        "fecha_fin_letras": fecha_a_letras(fecha_fin),
        "interes_moratorio": 40,
        "fecha_actual": fecha_hoy,
        "fecha_actual_letras": fecha_a_letras(fecha_hoy, True),
        "nombre_suscriptor": req["nombre_suscriptor"],
        "domicilio_suscriptor": req["domicilio_suscriptor"],
        "telefono_suscriptor": req["telefono_suscriptor"],
        "diadepago": fecha_fin.split("-")[2]
    }
    # Generate PDF in memory
    #pdf_bytes = pdfkit.from_string(html_content, False)  # False = return as bytes
    rendered = render_template('pagare.html', **context)

    # PDFKit options
    options = {
        'enable-local-file-access': '',  # VERY important to allow local file access (e.g., image)
    }

    # Generate PDF
    pdf = pdfkit.from_string(rendered, False, options=options)
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='pagare.pdf'
    )

@app.route('/api/solicitud', methods=['POST'])
@jwt_required()
def genera_solicitud():
    req= request.get_json()
    print("viendo request ", req)
    solicitud = Solicitud(**req)
    db.session.add(solicitud)
    db.session.commit()
    proveedor = Proveedor.query.get(req["fk_proveedor"])
    departamento = Departamento.query.get(req["fk_departamento"])
    context = {
        "descripcion": req["descripcion"], 'cantidad': req["cantidad"], 'fechapago': req["fechapago"],
         'fechaelaboracion':req["fechaelaboracion"], 'proveedor': proveedor, 'departamento': departamento
    }
    # Generate PDF in memory
    #pdf_bytes = pdfkit.from_string(html_content, False)  # False = return as bytes
    rendered = render_template('solicitud.html', **context)

    # PDFKit options
    options = {
        'enable-local-file-access': '',  # VERY important to allow local file access (e.g., image)
    }

    # Generate PDF
    pdf = pdfkit.from_string(rendered, False, options=options)
    response = make_response(send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='solicitud.pdf'
    ))
    response.headers['X-Custom-Value'] = solicitud.id
    response.headers['Access-Control-Expose-Headers'] = 'X-Custom-Value'
    return response

def get_detail(solicitud):
    pro = Proveedor.query.get(solicitud["fk_proveedor"])
    solicitud["proveedor"]=pro.nombre
    dep = Departamento.query.get(solicitud["fk_departamento"])
    solicitud["departamento"] = dep.nombre
    return solicitud

@app.route('/api/solicitudes', methods=['GET'])
@jwt_required()
def get_solicitudes():
    solicitudes = [x.as_dict() for x in Solicitud.query.all()]
    good = list(map(lambda x: get_detail(x), solicitudes))
    response = jsonify(good)
    return response

@app.route('/api/solicitud/<int:id>', methods=['GET'])
@jwt_required()
def solicitud_id(id):
    solicitud = Solicitud.query.get(id)
    if not solicitud:
        return jsonify({"error": "solicitud not found"}), 404
    response  =jsonify(solicitud.as_dict())
    return response

@app.route('/api/solicitud/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_solicitud(id):
    req = request.get_json()
    solicitud = Solicitud.query.get(id)
    if not solicitud:
        return jsonify({'message': 'solicitud not found'}), 404
    Solicitud.query.filter_by(id=id).update(req)
    db.session.commit()
    sol = Solicitud.query.get(id)
    return jsonify({"status":"good", "data":sol.as_dict()})



@app.route('/api/contrato', methods=['POST'])
@jwt_required()
def genera_contrato():
    mensualidad =0
    req= request.get_json()
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    estadocivil = ""
    if req.get("estado_civil"):
        print("entro ", req["estado_civil"])
        if req["estado_civil"] =="0":
            print("aqui")
            estadocivil="Soltero"
        if req["estado_civil"] =="1":
            print("aca")
            estadocivil="Casado"
    else:
        estadocivil = "Desconocido"
    saldo_pendiente = float(req["precio_total"]) - (float(req.get("descuento", 0))+ float(req["anticipo"]))
    if req.get("plazo_meses", 0) >0:
        fecha = datetime.strptime(req["fecha_primer_pago"], '%Y-%m-%d').date()
        fecha_final = calcular_fecha_fin(fecha, req["plazo_meses"])
        fecha_fin = fecha_final.strftime('%Y-%m-%d')
        mensualidad = saldo_pendiente / req.get("plazo_meses")
        mensualidad = round(mensualidad, 2)
        
    else:
        fecha = datetime.strptime(req["fecha_primer_pago"], '%Y-%m-%d').date()
        fecha_final = calcular_fecha_fin(fecha, 1)
        fecha_fin = fecha_final.strftime('%Y-%m-%d')
    
    context = {
        "comprador_nombre": req["comprador_nombre"],
        "comprador_nacionalidad": req["comprador_nacionalidad"],
        "superficie_m2":float(req["superficie_m2"]),
        "precio_total": float(req["precio_total"]),
        "precio_total_letras": f"{numero_a_letras_mxn(req["precio_total"])}",
        "anticipo": float(req["anticipo"]),
        "anticipo_letras": f"{numero_a_letras_mxn(req["anticipo"])}",
        "saldo_escritura": saldo_pendiente, #este no se de donde lo tengo que agarrar
        "saldo_escritura_letras": f"{numero_a_letras_mxn(str(saldo_pendiente))}",
        "fecha_contrato": fecha_hoy,
        "fecha_letras": fecha_a_letras(fecha_hoy),
        "nombre_vendedora": "ARCADIA PROMOTORA S. DE R.L. DE C.V.",
        "lindero1": req["lindero1"],
        "lindero2": req["lindero2"],
        "lindero3": req["lindero3"],
        "lindero4": req["lindero4"],
        "titulo1": req["titulo1"],
        "titulo2": req["titulo2"],
        "titulo3": req["titulo3"],
        "titulo4": req["titulo4"],
        "iden1": req["iden1"],
        "iden2": req["iden2"],
        "numeroidentificacion": req["numeroidentificacion"],
        "identificacion": req["identificacion"],
        "comprador_edad": req["comprador_edad"],
        "estado_civil" : estadocivil,
        "comprador_domicilio": req["comprador_domicilio"],
        "comprador_ciudad": req["comprador_ciudad"],
        "comprador_estado":req["comprador_estado"],
        "comprador_cp":req["comprador_cp"],
        "comprador_colonia": req["comprador_colonia"],
        "fk_etapa":req["fk_etapa"],
        "forma_de_pago": req["forma_de_pago"],
        "plazo_meses": req.get("plazo_meses", 0),
        "fecha_primer_pago": fecha_a_letras(req["fecha_primer_pago"]),
        "fecha_fin": fecha_a_letras(fecha_fin),
        "comprador_email":req.get("comprador_email", ""),
        "mensualidad":mensualidad,
        "mensualidad_letras": f"{numero_a_letras_mxn(mensualidad)}",
    }
    # Generate PDF in memory
    #pdf_bytes = pdfkit.from_string(html_content, False)  # False = return as bytes
    if req["fk_etapa"] == 34:
        rendered = render_template('contratoetapa5.html', **context)
    if req["fk_etapa"] == 35:
        rendered = render_template('contratoetapa6.html', **context)
    header_html = render_template("logo.html")
    with open("temp_header.html", "w", encoding="utf-8") as f:
        f.write(header_html)

    # PDFKit options
    options = {
        'margin-top': '35mm',
        'encoding': 'UTF-8',
        'header-html': 'temp_header.html',
        'header-spacing': '5',  # space between header and content
        'enable-local-file-access': '',  # VERY important to allow local file access (e.g., image)
    }

    # Generate PDF
    pdf = pdfkit.from_string(rendered, False, options=options)
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='pagare.pdf'
    )



@app.route('/api/amortizacion', methods=['POST'])
@jwt_required()
def guardar_amortizacion():
    req= request.get_json()
    mensualidad =0

    superficie = float(req["superficie_m2"])
    precio_m2 = float(req["inmueble_preciopormetro"])
    enganche = float(req["enganche"])
    interes_anual = float(req.get("interes_anual", 0))  # en porcentaje 10.0
    mensualidades = int(req.get("plazo_meses",0))
    descuento = float(req.get("descuento", 0))

    # Calcular tabla de amortización
    # Cálculos iniciales
    saldo_a_financiar = superficie * precio_m2 - enganche
    if descuento >0:
        saldo_a_financiar-=descuento

    interes_mensual = interes_anual / 100 / 12
    total_a_pagar = 0
    if req["forma_de_pago"] != "C":
        if interes_mensual > 0:
            mensualidad = saldo_a_financiar * (interes_mensual * (1 + interes_mensual) ** mensualidades) / ((1 + interes_mensual) ** mensualidades - 1)
        else:
            mensualidad = saldo_a_financiar / mensualidades

        mensualidad = round(mensualidad, 2)
    
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    result = db.session.execute(text("""select max(pkamortizacion) from gixamortizacion"""))
    codigo = result.fetchone()[0]
    pk = codigo+1
    llenado = {"pkamortizacion":pk, "fechaelaboracion":fecha_hoy, "fechacaptura":fecha_hoy, "fechaelaboracion":fecha_hoy, "formapago":req["forma_de_pago"], "fkcliente":req["fk_cliente"],
        "fkvendedor":req["fkvendedor"], "fketapa":req["fk_etapa"], "fkinmueble":req["fkinmueble"], "tasainteresanual":req.get("interes_anual", 0),
        "plazomeses":req.get("plazo_meses",0), "fechaprimerpago":req["fecha_primer_pago"], "preciocontado":float(req["precio_total"]), "descuentop":0,
        "descuentoc":descuento, "enganchep":0, "enganchec":float(req["enganche"]), "fechaenganche":req["fechaenganche"],
        "saldoafinanciar":saldo_a_financiar, "pagomensualfijo":mensualidad, "contrato":0, "cuenta":None
        }
    movimiento = GixAmortizacion(**llenado)
    db.session.add(movimiento)
    db.session.commit()
    response = jsonify({"status":"good", "data":{"amortizacion":pk}})
    return response
    

def crear_documento(doc, relaciondepago=None):
    result = db.session.execute(text("""select max(codigo) from documento"""))
    codigo = result.fetchone()[0]
    pk_documento = codigo+1
    doc["codigo"] = pk_documento
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    documento = Documento(**doc)
    db.session.add(documento)
    db.session.commit()
    db.session.execute(text(f"""delete from movimiento where fk_documento={documento.codigo}"""))
    result = db.session.execute(text("""select max(codigo) from movimiento"""))
    codigo = result.fetchone()[0]
    pk_movimiento = codigo+1
    movimiento = Movimiento(**{"codigo":pk_movimiento, "cantidad":doc["cargo"], 
        "fecha":fecha_hoy, "relaciondepago":relaciondepago,
        "cargoabono":'C', "fechavencimientodoc":doc["fechadevencimiento"],
        "fk_documento":documento.codigo, "fk_tipo":doc["fk_tipo"], "numrecibo":None })
    db.session.add(movimiento)
    db.session.commit()
    return (documento, movimiento)
    


def generar_documentos(req, cuenta):
    interes_anual = float(req.get("interes_anual", 0))  # en porcentaje 10.0
    mensualidades = int(req.get("plazo_meses",0))
    mensualidad =0
    interes_mensual = interes_anual / 100 / 12
    enganche = float(req["enganche"])
    superficie = float(req["superficie_m2"])
    precio_m2 = float(req["inmueble_preciopormetro"])
    descuento = float(req.get("descuento", 0))
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    fecha_vencimiento = req["fecha_primer_pago"]
    precio_total = superficie * precio_m2

    documentos_recibo= []


    #aqui  hago el enganche
    llenado_enganche = {"fechadeelaboracion":fecha_hoy,
        "fechadevencimiento":req["fecha_enganche"], "fechadevencimientovar":req["fecha_enganche"],
        "saldo":enganche, "cargo":enganche, "abono":0, "fk_cuenta":cuenta, "fk_tipo":1
    }
    (enganche_documento, enganche_movimiento) = crear_documento(llenado_enganche, "mensualidad (enganche)")
    documentos_recibo.append(enganche_documento)
    saldo_a_financiar = superficie * precio_m2 - enganche


    #sigue el documento de descuento
    if descuento >0:
        saldo_a_financiar-=descuento
        llenado_descuento = {"fechadeelaboracion":fecha_hoy,
        "fechadevencimiento":fecha_vencimiento, "fechadevencimientovar":fecha_vencimiento,
        "saldo":descuento, "cargo":descuento, "abono":0, "fk_cuenta":cuenta, "fk_tipo":14
        }
        (descuento_documento, descuento_movimiento) = crear_documento(llenado_descuento, "descuento")
        documentos_recibo.append(descuento_documento)
        #crear_movimiento_abono({"cantidad":descuento, "fecha":fecha_hoy, })

    #el resto del pago    
    if req["forma_de_pago"] != "C": # C=Contado R=credito
        if interes_mensual > 0:
            mensualidad = saldo_a_financiar * (interes_mensual * (1 + interes_mensual) ** mensualidades) / ((1 + interes_mensual) ** mensualidades - 1)
        else:
            mensualidad = saldo_a_financiar / mensualidades
        mensualidad = round(mensualidad, 2)
        print("viendo esto ", req["fecha_primer_pago"])
        fecha_inicio = datetime.strptime(req["fecha_primer_pago"], "%a, %d %b %Y %H:%M:%S GMT")
        for i in range(1, mensualidades + 1):
            fecha_vencimiento = (fecha_inicio + relativedelta(months=i - 1))
            llenado_contado = {"fechadeelaboracion":fecha_hoy,
            "fechadevencimiento":fecha_vencimiento, "fechadevencimientovar":fecha_vencimiento,
            "saldo":mensualidad, "cargo":mensualidad, "abono":0, "fk_cuenta":cuenta, "fk_tipo":2
            }
            (resto_documento, resto_movimiento) = crear_documento(llenado_contado, f"{i}/{mensualidades}")
   
    else:
        llenado_contado = {"fechadeelaboracion":fecha_hoy,
            "fechadevencimiento":fecha_vencimiento, "fechadevencimientovar":fecha_vencimiento,
            "saldo":saldo_a_financiar, "cargo":saldo_a_financiar, "abono":0, "fk_cuenta":cuenta, "fk_tipo":2
            }
        (resto_documento, resto_movimiento) = crear_documento(llenado_contado, "1/1")







@app.route('/api/cuenta', methods=['POST'])
@jwt_required()
def guardar_cuenta():
    req= request.get_json()
    result = db.session.execute(text("""select max(codigo) from cuenta"""))
    codigo = result.fetchone()[0]
    pk_cuenta = codigo+1
    superficie = float(req["superficie_m2"])
    precio_m2 = float(req["inmueble_preciopormetro"])
    enganche = float(req["enganche"])
    interes_anual = float(req.get("interes_anual", 0))  # en porcentaje 10.0
    mensualidades = int(req.get("plazo_meses",0))
    descuento = float(req.get("descuento", 0))
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    mensualidad =0

    # Calcular tabla de amortización
    # Cálculos iniciales
    precio_total = superficie * precio_m2
    # saldo_a_financiar = superficie * precio_m2 - enganche
    # if descuento >0:
    #     saldo_a_financiar-=descuento

    # interes_mensual = interes_anual / 100 / 12
    # total_a_pagar = 0
    # if req["forma_de_pago"] != "C":
    #     if interes_mensual > 0:
    #         mensualidad = saldo_a_financiar * (interes_mensual * (1 + interes_mensual) ** mensualidades) / ((1 + interes_mensual) ** mensualidades - 1)
    #     else:
    #         mensualidad = saldo_a_financiar / mensualidades

    #     mensualidad = round(mensualidad, 2)

    llenado_cuenta = {"codigo":pk_cuenta, "fecha":fecha_hoy, "saldo":precio_total, "fk_cliente":req["fk_cliente"], "fk_inmueble":req["fkinmueble"], "fk_tipo_cuenta":1, "congelada":0}
    movimiento = Cuenta(**llenado_cuenta)
    db.session.add(movimiento)
    db.session.commit()
    amortizacion = db.session.execute(db.select(GixAmortizacion).filter_by(pkamortizacion=req["amortizacion"])).scalar_one()
    amortizacion.cuenta=pk_cuenta
    db.session.commit()
    generar_documentos(req, pk_cuenta)
    db.session.execute(text("""update inmueble set fechadeventa='{}' where codigo={}""".format(fecha_hoy, req["fkinmueble"])))   
    db.session.commit()    

    response = jsonify({"status":"good", "data":{"cuenta":pk_cuenta}})
    return response

def get_detalle_amortizacion(amortizacion):
    inmueble = Inmueble.query.get(amortizacion["fkinmueble"])
    cliente = Cliente.query.get(amortizacion["fkcliente"])
    amortizacion["inmueble"] = inmueble.as_dict()
    amortizacion["cliente"] = cliente.as_dict()
    return amortizacion

@app.route('/api/amortizacionsincuenta', methods=['GET'])
@jwt_required()
def amortizacion_disponible():
    amortizaciones = [x.as_dict() for x in GixAmortizacion.query.filter(GixAmortizacion.cuenta.is_(None)).order_by(GixAmortizacion.pkamortizacion).all()]
    good_values = list(map(lambda x: get_detalle_amortizacion(x), amortizaciones))
    response = jsonify(amortizaciones)
    return response

@app.route('/api/amortizacion/<int:id>', methods=['GET'])
@jwt_required()
def amortizacion_id(id):
    amortizacion = GixAmortizacion.query.get(id)
    if not amortizacion:
        return jsonify({"error": "inmueble not found"}), 404
    response  =jsonify(amortizacion.as_dict())
    return response



@app.route('/api/resumen', methods=['GET'])
@jwt_required()
def resumen():
    results = (
    db.session.query(
        func.date_trunc('month', GixAmortizacion.fechaelaboracion).label('month'),
        func.count(func.distinct(GixAmortizacion.fkinmueble)).label('sold_count')
    )
    .filter(GixAmortizacion.fkinmueble.isnot(None))
    .group_by(func.date_trunc('month', GixAmortizacion.fechaelaboracion))
    .order_by(func.date_trunc('month', GixAmortizacion.fechaelaboracion))
    .all()
    )
    values = [{"id":i ,"month": r.month.strftime("%Y-%m"), "count": r.sold_count} for i, r in enumerate(results)]
    response = jsonify({"status":"good", "data":values})
    return response

def get_sold_inmuebles_by_month(year: int, month: int):
    results = (
        db.session.query(Inmueble)
        .join(GixAmortizacion, GixAmortizacion.fkinmueble == Inmueble.codigo)
        .filter(
            extract('year', GixAmortizacion.fechaelaboracion) == year,
            extract('month', GixAmortizacion.fechaelaboracion) == month,
            GixAmortizacion.cuenta.isnot(None)
             
        )
        .all()
    )

    return [inmueble.as_dict() for inmueble in results]


@app.route('/api/resumen2', methods=['GET'])
@jwt_required()
def resumen2():
    results = (
    db.session.query(
        func.date_trunc('month', GixAmortizacion.fechaelaboracion).label('month'),
        func.count(func.distinct(GixAmortizacion.fkinmueble)).label('sold_count')
    )
    .filter(GixAmortizacion.fkinmueble.isnot(None))
    .group_by(func.date_trunc('month', GixAmortizacion.fechaelaboracion))
    .order_by(func.date_trunc('month', GixAmortizacion.fechaelaboracion))
    .all()
    )
    yearly_data = defaultdict(lambda: {month: 0 for month in range(1, 13)})
    for row in results:
        year = row.month.year
        month = row.month.month
        yearly_data[year][month] = row.sold_count
    values = []
    month_names_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    for i, (year, months) in enumerate(sorted(yearly_data.items())):
        row = {'id': i, 'year': year}
        total = 0
        for idx, name in enumerate(month_names_es, start=1):
            count = months[idx]
            row[name] = count
            total += count
        row['Total'] = total
        values.append(row)
    
    response = jsonify({"status":"good", "data":values})
    return response


@app.route('/api/resumen/<path:fecha>')
@jwt_required()
def get_resumen_fecha(fecha):
    print("viendo fecha ", fecha)
    [y,m] = fecha.split("-")
    records = get_sold_inmuebles_by_month(int(y), int(m))
    response = jsonify({"status":"good", "data":records})
    return response


@app.route('/api/saldos')
@jwt_required()
def get_saldos():
    total_etapa34 =0
    total_etapa35 = 0
    total_vendido_34 =0
    total_vendido_35 =0
    total_descuento_34=0
    total_descuento_35=0
    inmueble_cuenta = [x.fk_inmueble for x in Cuenta.query.with_entities(Cuenta.fk_inmueble).all()]
    inmuebles_disponibles_34 = [x.as_dict() for x in Inmueble.query.filter(~Inmueble.codigo.in_(inmueble_cuenta), Inmueble.fk_etapa.in_([34])).order_by(Inmueble.iden2, Inmueble.iden1).all()]
    inmuebles_disponibles_35 = [x.as_dict() for x in Inmueble.query.filter(~Inmueble.codigo.in_(inmueble_cuenta), Inmueble.fk_etapa.in_([35])).order_by(Inmueble.iden2, Inmueble.iden1).all()]
    if inmuebles_disponibles_34:
        for x in inmuebles_disponibles_34:
            valor = x.get("precio", 0)
            total_etapa34+=valor if valor != None else 0
    if inmuebles_disponibles_35:
        for x in inmuebles_disponibles_35:
            valor = x.get("precio", 0)
            total_etapa35+=valor if valor != None else 0


    inmuebles_vendidos_34 = [x.as_dict() for x in Inmueble.query.filter(Inmueble.codigo.in_(inmueble_cuenta), Inmueble.fk_etapa.in_([34])).order_by(Inmueble.codigo, Inmueble.iden1).all()]
    for x in inmuebles_vendidos_34:
            valor = x.get("precio", 0)
            cuenta = db.session.execute(db.select(Cuenta).filter_by(fk_inmueble=x["codigo"])).scalar_one()
            amortizacion = db.session.execute(db.select(GixAmortizacion).filter_by(cuenta=cuenta.codigo)).scalar_one()
            total_vendido_34+=valor if valor != None else 0
            total_descuento_34+= valor-amortizacion.descuentoc
            
    
    inmuebles_vendidos_35 = [x.as_dict() for x in Inmueble.query.filter(Inmueble.codigo.in_(inmueble_cuenta), Inmueble.fk_etapa.in_([35])).order_by(Inmueble.codigo, Inmueble.iden1).all()]
    for x in inmuebles_vendidos_35:
            valor = x.get("precio", 0)
            cuenta = db.session.execute(db.select(Cuenta).filter_by(fk_inmueble=x["codigo"])).scalar_one()
            print("iendo cuenta ", cuenta)
            amortizacion = db.session.execute(db.select(GixAmortizacion).filter_by(cuenta=cuenta.codigo)).scalar_one()
            total_vendido_35+=valor if valor != None else 0
            total_descuento_35+= valor-amortizacion.descuentoc

    response = jsonify({"Disponible Etapa 5": '${:20,.2f}'.format(total_etapa34), "Disponible Etapa 6": '${:20,.2f}'.format(total_etapa35),
                        "Vendido Etapa 5 (Contratado)": '${:20,.2f}'.format(total_vendido_34), "Vendido Etapa 6 (Contratado)": '${:20,.2f}'.format(total_vendido_35),
                        "Vendido Etapa 5 (Vendido)": '${:20,.2f}'.format(total_descuento_34), "Vendido Etapa 6 (Vendido)": '${:20,.2f}'.format(total_descuento_35)},
                        )
    return response


@app.route('/api/proveedor', methods=['GET'])
@jwt_required()
def get_proveedores():
    proveedores = [x.as_dict() for x in Proveedor.query.all()]
    response = jsonify(proveedores)
    return response

@app.route('/api/departamento', methods=['GET'])
@jwt_required()
def get_departamentos():
    departamentos = [x.as_dict() for x in Departamento.query.all()]
    response = jsonify(departamentos)
    return response




if __name__ == '__main__':
    app.run(debug=True)
