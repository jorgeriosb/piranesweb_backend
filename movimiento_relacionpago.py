import psycopg2
import os

# Database connection parameters
ENV = os.environ.get('ENV')
USER = os.environ.get('USERD')
PASS = os.environ.get('PASS')
HOST = os.environ.get('HOSTD')
DB_PARAMS = {
    "dbname": "arcadia",
    "user": "jorge.rios",
    "password": "Mexiquito1991$",
    "host": "localhost",
    "port": "5432"
}

# production
if ENV == "production":
    DB_PARAMS = {
        "dbname": "arcadia",
        "user": USER,
        "password": PASS,
        "host": HOST,
        "port": "5432"
    }



def update_documentos_relacion_pago():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Step 1: Get all documentos linked to the given cuenta
        cursor.execute("""
            select codigo from cuenta where fecha>='2025-01-01' order by codigo;
        """)
        cuentas = cursor.fetchall()

        if not cuentas:
            print(f"No cuentas found for cuenta {cuentas}")
            return

        for cuenta in cuentas:
            codigo = cuenta[0]
            cursor.execute(f"""
            select m.codigo from movimiento m  join documento d on m.fk_documento=d.codigo where d.fk_cuenta={codigo} and d.fk_tipo=1 and m.cargoabono='C'
            """)
            enganche = cursor.fetchone()
            if enganche:
                codigo_enganche = enganche[0]
                cursor.execute(f"""update movimiento set relaciondepago='Pagaré (enganche)' where codigo={codigo_enganche}""")

            cursor.execute(f"""
            select m.codigo from movimiento m  join documento d on m.fk_documento=d.codigo where d.fk_cuenta={codigo} and d.fk_tipo=14 and m.cargoabono='C'
            """)
            descuento = cursor.fetchone()
            if descuento:
                codigo_descuento = enganche[0]
                cursor.execute(f"""update movimiento set relaciondepago='Reducción de Precio' where codigo={codigo_descuento}""")
            
            cursor.execute(f"""
            select m.codigo from movimiento m  join documento d on m.fk_documento=d.codigo where d.fk_cuenta={codigo} and d.fk_tipo=2 and m.cargoabono='C' order by codigo
            """)
            movimientos = cursor.fetchall()
            cantidad_movs = len(movimientos)
            for i, mov in enumerate(movimientos, 1):
                codigo = mov[0]
                cursor.execute(f"""update movimiento set relaciondepago='Pagaré (mensualidad) {i}/{cantidad_movs}' where codigo={codigo}""")
        
        # Commit changes
        conn.commit()
        print(f"Updated  documentos relacxion de pagos successfully.")

    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    update_documentos_relacion_pago()
