import sys
import psycopg2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QCalendarWidget, QPushButton, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

db_config = {
    "dbname": "loja_test",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

class GeradorGrafico(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('calendario.ui', self)
        
        self.conn = psycopg2.connect(**db_config)
        
        self.pushButton.clicked.connect(self.generate_chart) #Ação do botão gerar gráfico
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout = QVBoxLayout(self.graphicsView)
        self.layout.addWidget(self.canvas)
        self.pushButton_2.clicked.connect(self.generate_report) #Ação do botão de gerar o relatório
        self.calendarWidget_2.selectionChanged.connect(self.update_line_edit)
        self.calendarWidget_3.selectionChanged.connect(self.update_line_edit_2)
        
    #Método para gerar o gráfico
    def generate_chart(self):
        start_date = self.calendarWidget_2.selectedDate().toString("dd/MM/yyyy") #Variável que vai guardar a data
        end_date = self.calendarWidget_3.selectedDate().toString("dd/MM/yyyy")

        # Buscar dados do banco de dados dentro do between
        conn = psycopg2.connect(**db_config)  
        cursor = conn.cursor()
        query = f"SELECT data_venda, valor FROM vendas WHERE data_venda BETWEEN '{start_date}' AND '{end_date}'"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        # Coloca os dados no gráfico
        dates = [result[0] for result in results]
        values = [result[1] for result in results]
        self.figure.clear()

        ax = self.figure.add_subplot(111) 
        ax.plot(values, dates, marker='o') #plot é uma função da biblioteca Matplotlib para colocar os dados no gráfico
        ax.set_xlabel('Valor') #Função set_xlabel para criar o eixo X. Eu peguei o campo DATA da minha tabela.
        ax.set_ylabel('Data') #Função set_xlabel para criar o eixo Y. Eu peguei o campo VALOR da minha tabela.
        ax.set_title('Gráfico de Vendas por Data') #Função set_title para criar o título do gráfico
        self.canvas.draw()
    
    def update_line_edit(self):
        selected_date = self.calendarWidget_2.selectedDate()
        self.lineEdit.setText(selected_date.toString("dd/MM/yyyy"))
        
    def update_line_edit_2(self):
        selected_date = self.calendarWidget_3.selectedDate()
        self.lineEdit_2.setText(selected_date.toString("dd/MM/yyyy"))
        
    #Método para gerar o relatório   
    def generate_report(self):
        start_date = self.calendarWidget_2.selectedDate().toPyDate()
        end_date = self.calendarWidget_3.selectedDate().toPyDate()

        # Fetch data from the database within the selected date range
        conn = psycopg2.connect(**db_config)  # Replace with your actual database name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendas WHERE data_venda BETWEEN %s AND %s", (start_date, end_date))
        sales_data = cursor.fetchall()
        conn.close()
        
        pdf_filename = "relatorio_vendas.pdf" # Mude para o nome que você desejar
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter) # Pode mudar para A4 se quiser
        elements = []
        
        # Aqui ele vai criar as colunas do relatório. Cabeçalho do relatório

        data = [["Vendedor", "Descrição_venda", "Valor", "Data Venda"]]  
        for sale in sales_data:
            data.append([sale[0], sale[1], str(sale[2]), sale[3]]) 

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)

        self.statusbar.showMessage(f"Relatório gerado: {pdf_filename}", 5000)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = GeradorGrafico()
  window.show()
  sys.exit(app.exec_())
  