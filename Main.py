from PyQt5.QtWidgets import QMessageBox #Importar MessageBox
from ValidateUser import * #Importar UI login
from PrincipalMenu import MenuPrincipal #Importar UI principal
from ConnectionDB import ConnectionDatabase #Importar todas Querys

#Clase para cargar UI login
class ValidateUser (QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButtonLogin.clicked.connect(self.validation)

    #verificar validacion de user, para acceder a la UI de menu
    def validation(self):
        try:
            db = ConnectionDatabase()
            db.connection()
            result = db.login(username=self.lineEditUserName.text(), password=self.lineEditPassword.text())
            db.closeDataBase()
            if (result == True):
                self.menuPrincipal = MenuPrincipal()
                self.menuPrincipal.show()
                self.close()
            else:
                QMessageBox.critical(self, 'Error', 'Usuario o contraseña incorrecta') 
        except Exception:
            QMessageBox.critical(self, 'Error', f'Usuario o contraseña incorrecta')  
            
#Cargar programa
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    window = ValidateUser()
    window.show()
    app.exec_()