from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from servidor import Cuenta, Documento, db, app
from datetime import datetime
from dateutil.relativedelta import relativedelta

def prueba():
    c = Cuenta.query.get(2000)
    print("viendo cuenta ", Cuenta)

def reestructurar_cuenta(
    cuenta_id=2570,
    saldo_actual=208273.76,
    interes=138583.69,
    fecha_primer_vencimiento='2024-03-24',
    numero_documentos=36,
    primer_documento=34202,
    saldo_documento_matar=0

):
    try:
        fecha_primer_vencimiento = datetime.strptime(
            fecha_primer_vencimiento, "%Y-%m-%d"
        ).date()

        cuenta = Cuenta.query.filter_by(codigo=cuenta_id).first()
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        # validar que el saldo coincide con documentos
        total_docs = db.session.query(
            func.coalesce(func.sum(Documento.saldo), 0)
        ).filter(
            Documento.fk_cuenta == cuenta_id
        ).scalar()
        # esta cantidad tiene que ser el saldo del documento que se mato si es que existe
        if round(total_docs, 2)+saldo_documento_matar != round(saldo_actual, 2):
            raise Exception("El saldo no coincide con los documentos")    


        # borrar documentos pendientes
        Documento.query.filter(
            Documento.codigo>=primer_documento,
            Documento.fk_cuenta == cuenta_id,
            Documento.saldo > 0,
            Documento.saldo == Documento.cargo
        ).delete()

        nuevo_total = saldo_actual + interes

        monto_documento = round(nuevo_total / numero_documentos, 2)

        fecha_elaboracion = date.today()

        documentos = []

        max_codigo = db.session.query(func.max(Documento.codigo)).scalar() or 0
        for i in range(numero_documentos):
            fecha_vencimiento = fecha_primer_vencimiento + relativedelta(months=i)
            max_codigo += 1

            doc = Documento(
                codigo=max_codigo,
                fechadeelaboracion=fecha_elaboracion,
                fechadevencimiento=fecha_vencimiento,
                fechadevencimientovar=fecha_vencimiento,
                saldo=monto_documento,
                cargo=monto_documento,
                abono=0,
                fk_cuenta=cuenta_id,
                fk_tipo=16
            )

            db.session.add(doc)

        # actualizar saldo cuenta
        cuenta.saldo = nuevo_total

        db.session.commit()

        return {
            "cuenta": cuenta_id,
            "saldo_anterior": saldo_actual,
            "interes": interes,
            "saldo_nuevo": nuevo_total,
            "documentos": numero_documentos
        }

    except Exception as e:
        db.session.rollback()
        raise e


if __name__ == "__main__":
    with app.app_context():
        # quezada
        #reestructurar_cuenta(cuenta_id=2570,
        # saldo_actual=208273.76,
        # interes=138583.69,
        # fecha_primer_vencimiento='2024-03-24',
        # numero_documentos=36,
        # primer_documento=34202, 
        # saldo_documento_matar=1207.20)

        #REBECA ENRIQUEZ 
        # reestructurar_cuenta(cuenta_id=2970,
        # saldo_actual=495029.64,
        # interes=144090.45,
        # fecha_primer_vencimiento='2026-01-18',
        # numero_documentos=36,
        # primer_documento=42337, 
        # saldo_documento_matar=0)

        # Francisco Javier Barragan Silva
        reestructurar_cuenta(cuenta_id=2572,
        saldo_actual=524716.83,
        interes=538181.55,
        fecha_primer_vencimiento='2026-03-15',
        numero_documentos=18,
        primer_documento=35482, 
        saldo_documento_matar=0)