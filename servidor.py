from pydoc import Doc, doc
from xml.dom.minidom import Document
from flask import Flask, jsonify, request, send_file, make_response
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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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


@app.route('/api/documentos/pagar', methods=['POST'])
@jwt_required()
def pagar_documentos_varios():
    req = request.get_json()
    print("viendo valores ", req)
    cantidad = float(req["cantidad"])
    lista_catidades = [float(x.get("cantidad", 0))+ float(x.get("intereses"))  for x in req["formData"]]
    total_suma = sum(lista_catidades)
    intereses = sum([float(x.get("intereses", 0)) for x in req["formData"]])
    pago = sum([float(x.get("cantidad", 0)) for x in req["formData"]])
    if cantidad != total_suma:
        return jsonify({"status":"error", "message":"la suma de las cantidades no corresponde con el valor del pago total"})
    recibo = crear_recibo(pago, intereses, cantidad, req["referencia"], req["fecha"])
    if recibo:
        for documento in req["formData"]:
            pagar_documento(documento, req["fecha"], recibo)

    hacer_recibopdf(req)
    return jsonify({"status":"good"})


@app.route('/api/gixamortizacion/<int:id>', methods=['GET'])
@jwt_required()
def get_gixamortizacion(id):
    gixamortizacion = GixAmortizacion.query.filter_by(cuenta=id).scalar()
    if not gixamortizacion:
        return jsonify({"error": "gixamortizacion not found"}), 404
    response  =jsonify(gixamortizacion.as_dict())
    return response


def hacer_recibopdf(req):
    pass



def crear_recibo(pago, intereses, total, referencia, fecha):
    result = db.session.execute(text("""select max(codigo) from recibo"""))
    codigo = result.fetchone()[0]
    codigo+=1
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
def download_recibo(id):
    html_content = """
    <!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Recibo 21799</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 40px;
    }
    h2, h3 {
      margin: 0;
      padding: 0;
    }
    .row {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      margin-bottom: 5px;
    }
    .field {
      width: 50%;
      box-sizing: border-box;
      padding: 4px 10px;
    }
    .field p {
      margin: 4px 0;
    }
    .label {
      font-weight: bold;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    table, th, td {
      border: 1px solid #aaa;
    }
    th, td {
      padding: 8px;
      text-align: left;
    }
    .section {
      margin-top: 30px;
    }
    ol {
      padding-left: 20px;
    }
  </style>
</head>
<body>

  <h2>Arcadia Promotora, S. de R.L. de C.V.</h2>
  <p><strong>R.F.C.:</strong> APR-910816-FJ3</p>

  <div class="section">
    <h3>RECIBO: 21799</h3>

    <!-- Two-column layout, line by line -->
    <table style="width: 100%; margin-top: 20px; border-collapse: collapse;">
  <tr>
    <td style="width: 50%; padding: 5px;"><strong>Cuenta:</strong> 2961</td>
    <td style="width: 50%; padding: 5px;"><strong>Fecha de Aplicación:</strong> Febrero 05, 2025</td>
  </tr>
  <tr>
    <td style="padding: 5px;"><strong>Inmueble:</strong> 2771</td>
    <td style="padding: 5px;"><strong>Id. del Inmueble:</strong> C 113 - Quinta Sección</td>
  </tr>
  <tr>
    <td style="padding: 5px;"><strong>Cliente:</strong> 2716</td>
    <td style="padding: 5px;"><strong>Fecha de Pago:</strong> Febrero 04, 2025</td>
  </tr>
  <tr>
    <td style="padding: 5px;"><strong>Nombre del Cliente:</strong> GULNARA MOLINA ROMAN</td>
    <td style="padding: 5px;"><strong>Saldo Posterior al Pago:</strong> $178,807.04</td>
  </tr>
  <tr>
    <td style="padding: 5px;"><strong>Saldo Actual:</strong> $201,157.92</td>
    <td></td>
  </tr>
</table>
  </div>

  <div class="section">
    <h4>Movimientos</h4>
    <table>
      <thead>
        <tr>
          <th>Movimiento</th>
          <th>Importe</th>
          <th>Mensualidad</th>
          <th>Mes a Pagar</th>
          <th>Documento</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>85756</td>
          <td>$22,350.88</td>
          <td>16/24</td>
          <td>03/02/2025</td>
          <td>42084</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="section">
    <p><strong>Pago a Capital:</strong> $22,350.88</p>
    <p><strong>Intereses Moratorios:</strong> $0.00</p>
    <p><strong>Total a Pagar:</strong> $22,350.88</p>
    <p><strong>Referencia:</strong> </p>
    <p><strong>Id. del Recibo:</strong> 25586</p>
    <p style="margin-top: 40px;">__________________________<br>Firma del Cajero</p>
  </div>

  <div class="section">
    <p><strong>Observaciones:</strong></p>
    <ol>
      <li>El pago deberá hacerse con depósito bancario según la referencia que le corresponda a su terreno.</li>
      <li>El horario de oficina es de 9:00 a 14:00 y de 16:00 a 18:30 horas de Lunes a Viernes.</li>
      <li>Si el día de vencimiento es inhábil bancario, el pago deberá hacerse el día hábil inmediato anterior.</li>
      <li>Los intereses moratorios se calculan a la fecha de corte de este estado de cuenta.</li>
      <li>El presente estado de cuenta solo será válido como recibo si presenta la firma del cajero.</li>
      <li>Favor de pagar con cheque cruzado a nombre de Arcadia Promotora, S. de R.L. de C.V. y este recibo causará efecto salvo buen cobro del cheque.</li>
    </ol>
  </div>

</body>
</html>
    """

    # Generate PDF in memory
    pdf_bytes = pdfkit.from_string(html_content, False)  # False = return as bytes
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='recibo_21799.pdf'
    )





    #necesito agarrar el movimiento con cargoabono='C' y fk_docucumento=documento 
    # para obtener relaciondepago y poner ese valor al movimiento
    #crear movimiento y descontar a documento


    # codigo = db.Column(db.Integer, primary_key=True)
    # cantidad = db.Column(db.Float, nullable=False)
    # fecha = db.Column(db.Date, nullable=False)
    # relaciondepago = db.Column(db.String, nullable=True)
    # cargoabono = db.Column(db.String(1), nullable=False)
    # fechavencimientodoc = db.Column(db.Date, nullable=True)
    # fk_documento = db.Column(db.Integer, nullable=False)
    # fk_tipo = db.Column(db.Integer, nullable=False)
    # numrecibo = db.Column(db.Integer, nullable=True)
    pass






if __name__ == '__main__':
    app.run(debug=True)
