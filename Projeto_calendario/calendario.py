import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCalendarWidget, QPushButton
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate

class MainWindow(QMainWindow):
    #Método construtor
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('calendario.ui', self)
        
        self.calendarWidget_2.selectionChanged.connect(self.update_line_edit)
        self.calendarWidget_3.selectionChanged.connect(self.update_line_edit_2)
        
    def update_line_edit(self):
        selected_date = self.calendarWidget_2.selectedDate()
        self.lineEdit.setText(selected_date.toString("dd/MM/yyyy"))
        
    def update_line_edit_2(self):
        selected_date = self.calendarWidget_3.selectedDate()
        self.lineEdit_2.setText(selected_date.toString("dd/MM/yyyy"))

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())
  
  