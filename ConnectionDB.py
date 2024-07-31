import mysql.connector
import subprocess
from datetime import datetime
import os

#Clase para la conexión a la base de datos y querys
class ConnectionDatabase:

    #conexion DB
    def connection (self):
        self.connection = mysql.connector.connect(
            host="__HOST__",
            port="__PORT__",
            user="__USER__",
            password="__PASSWORD__",
            database="__NAMEDATABASE__"
        )

    #validar usuarios
    def login (self, username, password):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()

        query = "SELECT cedula, contrasenia FROM administradores WHERE cedula = %s"
        cursor.execute(query, (username,))

        result = cursor.fetchone()

        if (result[0] == username and result[1] == password):
            return True
        else:
            return False
    
    #cerrar conexion DB
    def closeDataBase(self):
        if (self.connection and self.connection.is_connected()):
            self.connection.close()

    #insertar infomacion del deudor    
    def informationDeudor(self,nombre, apellido, cedula, fecha, prestamo, cuota, formaPagar):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()

        values = (nombre, apellido, cedula, fecha, prestamo, cuota, formaPagar)
        query = """INSERT INTO deudores (nombre, apellido, cedula, fecha_inicio, prestamo, cuota, forma_pagar)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        cursor.execute(query,values)

        interes = (cuota / 100) * prestamo
        total = prestamo + interes
        
        value = (cedula, fecha, prestamo, interes, total)
        querySecond = """INSERT INTO abonos (deudor_id, abono_capital, abono_interes, fecha_abono, total_capital_debe, total_interes_debe, total_debe) 
        VALUES ((SELECT id FROM deudores WHERE cedula = %s AND fecha_inicio = %s), 0, 0, '00/00/00', %s, %s, %s)"""
        cursor.execute(querySecond,value)

        self.connection.commit()
        cursor.close()
    
    #insertar informacion del abono de un deudor
    def abonarDeudor(self, iD, capital, interes, fecha):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()

        #validar información de la base de datos para hacer el calculo
        query = "SELECT abono_capital, abono_interes, total_capital_debe, total_interes_debe FROM abonos WHERE deudor_id = %s"
        cursor.execute(query, (iD,))
        result = cursor.fetchone()

        if result:
            #calculo
            abonoCapital = capital + result[0]
            abonoInteres = interes + result[1]

            totalCapital = result[2] - capital  
            totalInteres = result[3] - interes  

            totalCapital = abs(totalCapital)
            totalInteres = abs(totalInteres)

            totalDebe = totalCapital + totalInteres

            #actualizar informacion en la base de datos
            queryTwo = """UPDATE abonos SET abono_capital = %s, abono_interes = %s, fecha_abono = %s, total_capital_debe = %s, total_interes_debe = %s, total_debe = %s 
            WHERE deudor_id = %s"""

            cursor.execute(queryTwo, (abonoCapital, abonoInteres, fecha, totalCapital, totalInteres, totalDebe, iD))
            self.connection.commit()
            cursor.close()
            
            return True
        
        cursor.close()
        return False

    #eliminar un deudor
    def deleteID(self,iD,cedula):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()
        
        query = "SELECT id FROM deudores WHERE id = %s AND cedula = %s"
        cursor.execute(query, (iD,cedula,))
        deudor = cursor.fetchone()

        if deudor:
            # Eliminar los abonos asociados
            cursor.execute("DELETE FROM abonos WHERE deudor_id = %s", (iD,))
            
            # Eliminar el deudor
            cursor.execute("DELETE FROM deudores WHERE id = %s", (iD,))
            
            # Confirmar la transacción
            self.connection.commit()
        else:  
            cursor.close()
            return False
        cursor.close()
        return True
    
    #consultar informacion de un deudor
    def searchDeudor(self, cedula):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()
        
        query = "SELECT d.*, a.* FROM deudores d JOIN abonos a ON d.id = a.deudor_id WHERE d.cedula = %s"
        cursor.execute(query, (cedula,))

        result = cursor.fetchall()
        cursor.close()
        return result

    #consultar informacion de todos los deudores
    def searchAll(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()
        
        query = "SELECT d.*, a.* FROM deudores d LEFT JOIN abonos a ON d.id = a.deudor_id;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    #consulta de deudor
    def abonarSearchDeudor(self,iD,cedula):
        cursor = self.connection.cursor(dictionary=True)
        cursor = self.connection.cursor()

        query = "SELECT nombre, apellido FROM deudores WHERE id=%s and cedula=%s"
        cursor.execute(query,(iD,cedula,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    #hacer un backup DB en una ruta especifico
    def backupDatabase():
        usercomand = "powershell $env:username"
        result = subprocess.run(usercomand, capture_output=True, text=True, shell=True)
        
        if result.returncode == 0:
            # Imprimir la salida del comando
            username = result.stdout.strip()
        
        host = "localhost"
        user = "backup"
        database = "gestordeprestamos"

        # Obtener la fecha actual en formato DD-MM-YYYY
        fechaActual = datetime.now().strftime("%d/%m/%y")
        fecha = fechaActual.replace("/","")

        # Construir el nombre del archivo de respaldo
        nombre_archivo = "gestordeprestamos"+fecha+".sql"

        # Ruta completa del archivo de respaldo
        ruta_archivo = os.path.join(f"C:\\Users\\{username}\\Desktop\\Backup",nombre_archivo)
        
        #Construir el comando mysqldump
        command = f"mysqldump -h {host} -u {user} {database} > {ruta_archivo}"
        
        # Ejecutar el comando en la línea de comandos
        subprocess.run(command, shell=True)