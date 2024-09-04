import sqlite3
from datetime import datetime, timedelta

class DataManager:
    def __init__(self, db_name='finanzas.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS ingresos (
                                  id INTEGER PRIMARY KEY,
                                  nombre TEXT,
                                  monto INTEGER,
                                  medio_pago TEXT,
                                  motivo TEXT,
                                  estado TEXT,
                                  fecha_hora TEXT
                                )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS egresos (
                                  id INTEGER PRIMARY KEY,
                                  nombre TEXT,
                                  monto INTEGER,
                                  medio_pago TEXT,
                                  motivo TEXT,
                                  fecha_hora TEXT
                                )''')

    def add_ingreso(self, nombre, monto, medio_pago, motivo, estado):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            self.conn.execute('''INSERT INTO ingresos (nombre, monto, medio_pago, motivo, estado, fecha_hora)
                                 VALUES (?, ?, ?, ?, ?, ?)''', 
                                 (nombre, monto, medio_pago, motivo, estado, fecha_hora))

    def add_egreso(self, nombre, monto, medio_pago, motivo):
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.conn:
            self.conn.execute('''INSERT INTO egresos (nombre, monto, medio_pago, motivo, fecha_hora)
                                 VALUES (?, ?, ?, ?, ?)''', 
                                 (nombre, monto, medio_pago, motivo, fecha_hora))

    def get_total_dinero(self):
        with self.conn:
            ingreso_total = self.conn.execute('SELECT SUM(monto) FROM ingresos').fetchone()[0] or 0
            egreso_total = self.conn.execute('SELECT SUM(monto) FROM egresos').fetchone()[0] or 0
        return ingreso_total - egreso_total

    def get_ingresos_por_cliente(self):
        with self.conn:
            return self.conn.execute('SELECT nombre, SUM(monto) FROM ingresos GROUP BY nombre').fetchall()

    def get_ingresos_egresos_por_mes(self, mes):
        with self.conn:
            ingresos = self.conn.execute('SELECT SUM(monto) FROM ingresos WHERE strftime("%m", fecha_hora) = ?', (mes,)).fetchone()[0] or 0
            egresos = self.conn.execute('SELECT SUM(monto) FROM egresos WHERE strftime("%m", fecha_hora) = ?', (mes,)).fetchone()[0] or 0
        return ingresos, egresos

    def get_registros_filtrados(self, filtro):
        with self.conn:
            if filtro == 'dia':
                fecha_inicio = datetime.now().strftime("%Y-%m-%d")
                query = '''SELECT 'ingreso' as tipo, nombre, monto, fecha_hora FROM ingresos WHERE date(fecha_hora) = ?
                           UNION
                           SELECT 'egreso' as tipo, nombre, monto, fecha_hora FROM egresos WHERE date(fecha_hora) = ?'''
                params = (fecha_inicio, fecha_inicio)

            elif filtro == 'semana':
                fecha_inicio = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
                query = '''SELECT 'ingreso' as tipo, nombre, monto, fecha_hora FROM ingresos WHERE date(fecha_hora) BETWEEN ? AND date('now')
                           UNION
                           SELECT 'egreso' as tipo, nombre, monto, fecha_hora FROM egresos WHERE date(fecha_hora) BETWEEN ? AND date('now')'''
                params = (fecha_inicio, fecha_inicio)

            elif filtro == 'año':
                fecha_inicio = datetime.now().strftime("%Y")
                query = '''SELECT 'ingreso' as tipo, nombre, monto, fecha_hora FROM ingresos WHERE strftime("%Y", fecha_hora) = ?
                           UNION
                           SELECT 'egreso' as tipo, nombre, monto, fecha_hora FROM egresos WHERE strftime("%Y", fecha_hora) = ?'''
                params = (fecha_inicio, fecha_inicio)

            else:  # Mes por defecto
                fecha_inicio = datetime.now().strftime("%Y-%m")
                query = '''SELECT 'ingreso' as tipo, nombre, monto, fecha_hora FROM ingresos WHERE strftime("%Y-%m", fecha_hora) = ?
                           UNION
                           SELECT 'egreso' as tipo, nombre, monto, fecha_hora FROM egresos WHERE strftime("%Y-%m", fecha_hora) = ?'''
                params = (fecha_inicio, fecha_inicio)

            registros = self.conn.execute(query, params).fetchall()

        return [{'tipo': tipo, 'nombre': nombre, 'monto': monto, 'fecha_hora': fecha_hora} for tipo, nombre, monto, fecha_hora in registros]

