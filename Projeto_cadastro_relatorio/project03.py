from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QRadioButton, QCheckBox, QPushButton, QComboBox, QWidget, QTableView, QBoxLayout
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.uic import loadUi
import psycopg2
import sys
class MainWindow(QMainWindow):
    #Método construtor
    def __init__(self):
        super().__init__()
        loadUi('menu.ui', self)

        self.pushButton.clicked.connect(self.inserir_no_banco)
        self.pushButton_2.clicked.connect(self.gerar_relatorio)
        self.connection = psycopg2.connect(dbname="aula_30_08_2023", user="postgres", password="1234", host="localhost",
                                           port="5432")

        self.carregar_cidades()

   
    #Método que vai gerar o relatório
    def gerar_relatorio(self):
        #variavel que guardará o nome do arquivo
        arquivo = "relatorio.pdf"
        #conexão com o banco e executara a query
        cur = self.connection.cursor()
        cur.execute("SELECT nome, tipo, adimplente, cidade FROM clientes")
        #variavel guardara o resultado da query
        resultado_relatorio = cur.fetchall()
        #Variavel guaradará o formato da pagina
        page_size = SimpleDocTemplate(arquivo, pagesize=letter)
        #Essa variavel recebe a classe onde estiliza a página
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        #Organizar os dados dentro do arquivo PDF
        data = [['Nome', 'Tipo', 'Adimplente', 'Cidade']]
        for record in resultado_relatorio:
            nome, tipo, adimplente, cidade = record
            data.append([nome, tipo, adimplente, cidade])
        table = Table(data)
        table.setStyle(style)
        
        # Adicionar a tabela ao documento PDF
        page_size.build([table])
        print(f"Relatório gerado como {arquivo}")
        # Fechar conexão com o banco
        cur.close()

        
    #Método que vai carregar as cidades quando solicitado    
    def carregar_cidades(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT cidade FROM city")
        cidades = cursor.fetchall()
        cursor.close

        for cidade in cidades:
            self.comboBox.addItem(cidade[0])


    #Método para inserir no banco
    def inserir_no_banco(self):
        nome = self.lineEdit.text()
        tipo = "PF" if self.radioButton.isChecked() else "PJ"
        adimplente = "SIM" if self.checkBox.isChecked() else "NÃO"
        cidade = self.comboBox.currentText()


        cursor = self.connection.cursor()


        #Vai entrar neste bloco para executar o código
        try:
            cursor.execute("INSERT INTO public.clientes (nome, tipo, adimplente, cidade)  VALUES (%s, %s, %s, %s)", (nome, tipo, adimplente, cidade))
            self.connection.commit()

            QMessageBox.information(self, "Cadastro realizado", "Cadastro realizado com sucesso!")
            self.limpar_campos
       
        #Se o TRY não funcionar, desse para esse bloco
        except psycopg2.Error as e:
            print(e)
            QMessageBox.warning(self, "Erro", "O cadastro não pode ser realizado.")
       
        #Encerra a conexão
        finally:
            cursor.close()


    #Método para limpar os campos
    def limpar_campos(self):
        self.lineEdit.clear()
        self.radioButton.setChecked(False)
        self.checkBox.setChecked(False)
        self.radioButton2.setChecked(False)

#Função declarativa principal. O programa começa aqui
if __name__ == '__main__':
  app = QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())
