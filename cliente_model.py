from servidor import db

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

    def __repr__(self):
        return f'<Cliente {self.nombre}>'