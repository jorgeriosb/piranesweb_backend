from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from servidor import Cuenta, Documento, Movimiento, db, app


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

        # validar saldo
        total_docs = db.session.query(
            func.coalesce(func.sum(Documento.saldo), 0)
        ).filter(
            Documento.fk_cuenta == cuenta_id
        ).scalar()

        if round(total_docs, 2) + saldo_documento_matar != round(saldo_actual, 2):
            raise Exception("El saldo no coincide con los documentos")

        # borrar documentos pendientes
        Documento.query.filter(
            Documento.codigo >= primer_documento,
            Documento.fk_cuenta == cuenta_id,
            Documento.saldo > 0,
            Documento.saldo == Documento.cargo
        ).delete()

        nuevo_total = saldo_actual + interes
        monto_documento = round(nuevo_total / numero_documentos, 2)
        fecha_elaboracion = date.today()

        # obtener máximos códigos
        max_doc_codigo = db.session.query(func.max(Documento.codigo)).scalar() or 0
        max_mov_codigo = db.session.query(func.max(Movimiento.codigo)).scalar() or 0

        for i in range(numero_documentos):
            fecha_vencimiento = fecha_primer_vencimiento + relativedelta(months=i)

            # --------- DOCUMENTO ---------
            max_doc_codigo += 1
            doc = Documento(
                codigo=max_doc_codigo,
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

            # --------- MOVIMIENTO ---------
            max_mov_codigo += 1
            relacion = f"R{i+1}/{numero_documentos}"

            mov = Movimiento(
                codigo=max_mov_codigo,
                cantidad=monto_documento,
                fecha=fecha_elaboracion,
                relaciondepago=relacion,
                cargoabono="C",
                fechavencimientodoc=fecha_vencimiento,
                fk_documento=max_doc_codigo,
                fk_tipo=2,
                numrecibo=None
            )
            db.session.add(mov)

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
        reestructurar_cuenta(
            cuenta_id=2572,
            saldo_actual=524716.83,
            interes=538181.55,
            fecha_primer_vencimiento='2026-03-15',
            numero_documentos=18,
            primer_documento=35482,
            saldo_documento_matar=0
        )