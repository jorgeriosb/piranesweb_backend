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
from datetime import date, datetime

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
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
    result = db.session.execute(text("""select max(codigo) from recibo"""))
    codigo = result.fetchone()[0]
    nummovimiento = db.session.execute(text("""select max(numrecibo) from movimiento"""))
    num = nummovimiento.fetchone()[0]
    codigo+=1
    if num > codigo:
        codigo = num+1
    llenado = {"codigo":codigo, "fechaemision":fecha, "abonocapital":pago, 
        "interesmoratorio":intereses, "totalrecibo":total, "referencia":referencia,
        "status":"A", "fk_desarrollo":5, "fechaaplicacion":fecha}
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






if __name__ == '__main__':
    app.run(debug=True)
