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



def update_documentos_and_cuenta(cuenta_codigo):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Step 1: Get all documentos linked to the given cuenta
        cursor.execute("""
            SELECT codigo, cargo FROM documento 
            WHERE fk_cuenta = %s
        """, (cuenta_codigo,))
        documentos = cursor.fetchall()

        if not documentos:
            print(f"No documentos found for cuenta {cuenta_codigo}")
            return

        # Step 2: Reset each documento (abono = 0, saldo = cargo)
        for doc in documentos:
            doc_codigo, doc_cargo = doc
            cursor.execute("""
                UPDATE documento 
                SET abono = 0, saldo = %s
                WHERE codigo = %s
            """, (doc_cargo, doc_codigo))

        # Step 3: Update each documento with movimiento sums
        for doc in documentos:
            doc_codigo, doc_cargo = doc

            # Get total abono from movimientos where cargoabono = 'A'
            cursor.execute("""
                SELECT COALESCE(SUM(cantidad), 0) FROM movimiento 
                WHERE fk_documento = %s AND cargoabono = 'A'
            """, (doc_codigo,))
            total_abono = cursor.fetchone()[0]

            # Update documento with new abono and new saldo
            new_saldo = doc_cargo - total_abono
            cursor.execute("""
                UPDATE documento 
                SET abono = %s, saldo = %s
                WHERE codigo = %s
            """, (total_abono, new_saldo, doc_codigo))

        # Step 4: Recalculate cuenta saldo
        cursor.execute("""
            SELECT COALESCE(SUM(cargo), 0) FROM documento WHERE fk_cuenta = %s
        """, (cuenta_codigo,))
        total_cargo = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(movimiento.cantidad), 0) 
            FROM movimiento
            JOIN documento ON movimiento.fk_documento = documento.codigo
            WHERE documento.fk_cuenta = %s AND movimiento.cargoabono = 'A'
        """, (cuenta_codigo,))
        total_abonos = cursor.fetchone()[0]

        # Calculate new cuenta saldo
        new_saldo = total_cargo - total_abonos

        # Update cuenta saldo
        cursor.execute("""
            UPDATE cuenta 
            SET saldo = %s 
            WHERE codigo = %s
        """, (new_saldo, cuenta_codigo))

        # Commit changes
        conn.commit()
        print(f"Updated documentos and cuenta saldo for cuenta {cuenta_codigo} successfully.")

    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Example usage
if __name__ == "__main__":
    cuenta_codigo = 2690  # Replace with the actual cuenta code
    update_documentos_and_cuenta(cuenta_codigo)
