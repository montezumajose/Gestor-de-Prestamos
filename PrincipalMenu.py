from MenuPrincipal import *
from ConnectionDB import ConnectionDatabase
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from openpyxl import Workbook
import os
import subprocess

#Clase para cargar UI Menu principal
class MenuPrincipal (QtWidgets.QMainWindow, Ui_Form):
    #Constructor de UI Menu Principal
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Principal
        self.pushButton_probar.clicked.connect(self.ValidateConnectionDB)
        self.pushButton_salir.clicked.connect(self.Exit)

        #Agregar deudor
        self.pushButtonAddTab2.clicked.connect(self.AddInformationDeudor)

        #Buscar deudor
        self.pushButtonSearchTab3.clicked.connect(self.searchDeudor)
        self.pushButtonDeleteTab3.clicked.connect(self.deleteDuedor)

        #Ver todos los prestamos
        self.pushButtonSearchTab5.clicked.connect(self.viewPrestamos)

        #Abonar 
        self.pushButtonSearchTab4.clicked.connect(self.searchDeudorAbono)
        self.pushButtonTab4.clicked.connect(self.abonar)

        #Exportar Excel
        self.pushButtonSearchTab5_2.clicked.connect(self.exportarExcel)

        #Hacer backup
        self.pushButtonSaveTab6.clicked.connect(self.toDoBackup)

        #Calculadora
        self.pushButtonCalculateTab7.clicked.connect(self.calculatePrestamo)

    #Validar conexion de DB
    def ValidateConnectionDB(self):
        try:    
            db = ConnectionDatabase()
            db.connection()
            db.closeDataBase()
            QMessageBox.information(self,"Conexión", "Conectado correctamenta a la base de datos.")
        except Exception as e:
            QMessageBox.critical(self,"Error de conexión",f"No se puede conectar a la base de datos. \nMotivo: {e}")

    #Cerrar ventana    
    def Exit(self):
        self.close()
    
    #Aniadir informacion del deudor
    def AddInformationDeudor(self):
        name = self.lineEditNameTab2.text()
        lastName = self.lineEditLastNameTab2.text()
        cedula = self.lineEditIdTab2.text()
        date = self.dateEditTab2.date()
        dateString = date.toString(self.dateEditTab2.displayFormat())
        loan = self.doubleSpinBoxTab2.value()
        percentage = self.doubleSpinBoxTab2_2.value()
        formPayment = self.comboBoxTab2.currentText()
    
        reply = QMessageBox.question(self, "Confirmación","Si los datos están correctos \n¿Quieres agregar al deudor?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if(reply == QMessageBox.Yes):
            try:
                db = ConnectionDatabase()
                db.connection()
                db.informationDeudor(nombre=name,apellido=lastName,cedula=cedula,fecha=dateString,prestamo=loan,cuota=percentage,formaPagar=formPayment)
                db.closeDataBase()

                QMessageBox.information(self,"Información","Los datos del deudor fueron agregados correctamente.")
            except Exception as e:
                QMessageBox.warning(self,"Error",f"El problema fue ocasionado por:\n {e}")

    #buscar deudor            
    def searchDeudor(self):
        db = ConnectionDatabase()
        db.connection()
        data = db.searchDeudor(cedula= self.lineEditIdTab3.text())
        db.closeDataBase()

        self.tableWidgetTab3.setRowCount(len(data))
        self.tableWidgetTab3.setColumnCount(15)

        for row,(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o) in enumerate(data):
            self.tableWidgetTab3.setItem(row, 0, QTableWidgetItem(str(a)))
            self.tableWidgetTab3.setItem(row, 1, QTableWidgetItem(b))
            self.tableWidgetTab3.setItem(row, 2, QTableWidgetItem(c))
            self.tableWidgetTab3.setItem(row, 3, QTableWidgetItem(d))
            self.tableWidgetTab3.setItem(row, 4, QTableWidgetItem(e))
            self.tableWidgetTab3.setItem(row, 5, QTableWidgetItem(f"{f:.2f}"))
            self.tableWidgetTab3.setItem(row, 6, QTableWidgetItem(f"{g:.2f}"))
            self.tableWidgetTab3.setItem(row, 7, QTableWidgetItem(h))
            self.tableWidgetTab3.setItem(row, 8, QTableWidgetItem(str(i)))
            self.tableWidgetTab3.setItem(row, 9, QTableWidgetItem(f"{j:.2f}"))
            self.tableWidgetTab3.setItem(row, 10, QTableWidgetItem(f"{k:.2f}"))
            self.tableWidgetTab3.setItem(row, 11, QTableWidgetItem(l))
            self.tableWidgetTab3.setItem(row, 12, QTableWidgetItem(f"{m:.2f}"))
            self.tableWidgetTab3.setItem(row, 13, QTableWidgetItem(f"{n:.2f}"))
            self.tableWidgetTab3.setItem(row, 14, QTableWidgetItem(f"{o:.2f}"))

    #eliminar deudor
    def deleteDuedor(self):
        try:
            reply = QMessageBox.question(self, "Confirmación","Si la cedula y ID son correctos \n¿Quieres eliminar al deudor?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if(reply == QMessageBox.Yes):    
                
                db = ConnectionDatabase()
                db.connection()
                request = db.deleteID(iD=self.lineEditIdTab3_2.text(), cedula=self.lineEditIdTab3.text())
                db.closeDataBase()
                if request == True:
                    QMessageBox.information(self,"Información", "Se eliminó correctamente.")
                else:
                    QMessageBox.warning(self,"Problema", "Verifique los campos cédula y ID.")
        except Exception as e:
            QMessageBox.critical(self,"Error",f"Se ha producido un error\n Error: {e}")

    #buscar deudor nombre y apellido
    def searchDeudorAbono(self):
        try:
            db = ConnectionDatabase()
            db.connection()
            result = db.abonarSearchDeudor (iD=self.lineEditIdTab4_2.text(), cedula=self.lineEditIdTab4.text())
            db.closeDataBase()
            nameAll = result[0]+" "+result[1]
            self.lineEditNameLastNameTab4.setText(nameAll)
        except Exception:
            QMessageBox.critical(self,"Error", f"Algo salió mal, verifique los datos.")

    #abono del deudor
    def abonar(self):
        try:
            reply = QMessageBox.question(self, "Confirmación","Asegurese que los datos sean correctos\n¿Quieres continuar con el proceso de abono?",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:    
                iD = self.lineEditIdTab4_2.text()
                abonoCapital = self.doubleSpinBoxTab4.value()
                abonoInteres = self.doubleSpinBoxTab4_2.value()
                date = self.dateEditTab4.date()
                dateAbono = date.toString(self.dateEditTab2.displayFormat())
                
                db = ConnectionDatabase()
                db.connection()
                baseReply = db.abonarDeudor(iD=iD, capital= abonoCapital, interes=abonoInteres, fecha=dateAbono)
                db.closeDataBase()

                if baseReply == True:
                    QMessageBox.information(self,"Información","Los datos fueron actualizados correctamente.")
                else:
                    QMessageBox.critical(self,"Problema","Algo salió mal, revisa los datos e intente nuevamente.")
        except Exception:
            QMessageBox.warning(self,"Problema","Lo siento, hubo un problema. Por favor verifique que los datos estén correctos.")

    #ver todos los prestamos
    def viewPrestamos(self):
        db = ConnectionDatabase()
        db.connection()
        data = db.searchAll()
        db.closeDataBase()

        self.tableWidgetTab3_2.setRowCount(len(data))
        self.tableWidgetTab3_2.setColumnCount(15)

        for row,(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o) in enumerate(data):
            self.tableWidgetTab3_2.setItem(row, 0, QTableWidgetItem(str(a)))
            self.tableWidgetTab3_2.setItem(row, 1, QTableWidgetItem(b))
            self.tableWidgetTab3_2.setItem(row, 2, QTableWidgetItem(c))
            self.tableWidgetTab3_2.setItem(row, 3, QTableWidgetItem(d))
            self.tableWidgetTab3_2.setItem(row, 4, QTableWidgetItem(e))
            self.tableWidgetTab3_2.setItem(row, 5, QTableWidgetItem(f"{f:.2f}"))
            self.tableWidgetTab3_2.setItem(row, 6, QTableWidgetItem(f"{g:.2f}"))
            self.tableWidgetTab3_2.setItem(row, 7, QTableWidgetItem(h))
            self.tableWidgetTab3_2.setItem(row, 8, QTableWidgetItem(str(i)))
            self.tableWidgetTab3_2.setItem(row, 9, QTableWidgetItem(f"{j:.2f}"))
            self.tableWidgetTab3_2.setItem(row, 10, QTableWidgetItem(f"{k:.2f}"))
            self.tableWidgetTab3_2.setItem(row, 11, QTableWidgetItem(l))
            self.tableWidgetTab3_2.setItem(row, 12, QTableWidgetItem(f"{m:.2f}"))
            self.tableWidgetTab3_2.setItem(row, 13, QTableWidgetItem(f"{n:.2f}"))
            self.tableWidgetTab3_2.setItem(row, 14, QTableWidgetItem(f"{o:.2f}"))

    #exportar informacion en Excel   
    def exportarExcel(self):
        try:
            usercomand = "powershell $env:username"
            result = subprocess.run(usercomand, capture_output=True, text=True, shell=True)
        
            if result.returncode == 0:
                #Guarda el nombre de usuario actual
                username = result.stdout.strip()

            rutaArchivo = os.path.join(f"C:\\Users\\{username}\\Downloads", "Informacion de deudores.xlsx")
            wb = Workbook()
            ws = wb.active

            db = ConnectionDatabase()
            db.connection()
            datos = db.searchAll()
            db.closeDataBase()

            datosLista = [list(fila) for fila in datos]
            
            for row in datosLista:
                ws.append(row)
            wb.save(rutaArchivo)

            QMessageBox.information(self,"Información","Se guardó el excel correctamente.\nSe guardó en descargas.")
        except Exception:
            QMessageBox.critical(self,"Error","Algo salió mal y no se guardó el archivo excel.")

    #hacer backup DB
    def toDoBackup(self):
        try:
            db = ConnectionDatabase
            db.backupDatabase()

            QMessageBox.information(self,"Información","Se respaldó la base de datos sastifactoramiente.\nBuscalo en el escritorio en la carpeta Backup.")
        except Exception:
            QMessageBox.critical(self,"Error", "No se pudo respladar la base de datos.")

    #calculadora de prestamo
    def calculatePrestamo(self):
        cantidadPrestamo = self.doubleSpinBoxTab7.value()
        cuota = self.doubleSpinBoxTab7_2.value()

        result = ((cuota / 100) * cantidadPrestamo) + cantidadPrestamo 
        val = round(result,2)
        formatString = f"{val:.2f}"
        self.labelTotalTab7.setText(formatString)





