import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDoubleValidator


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interactive Map')
        self.setGeometry(100, 100, 800, 600)

        # Crearea layout-ului principal
        main_layout = QHBoxLayout()

        # Partea stângă cu QHBoxLayout pentru QLabel și QLineEdit, și un QPushButton
        left_layout = QVBoxLayout()

        # Crearea unui QHBoxLayout pentru label și text_field
        field_layout1 = QHBoxLayout()
        field_layout2 = QHBoxLayout()

        layout_bedrooms = QHBoxLayout()
        layout_bathrooms = QHBoxLayout()
        layout_sqm_living = QHBoxLayout()
        layout_floors = QHBoxLayout()
        layout_condition = QHBoxLayout()
        layout_grade = QHBoxLayout()
        layout_yr_built = QHBoxLayout()
        layout_yr_renovated = QHBoxLayout()
        layout_sqm_above = QHBoxLayout()
        layout_sqm_basement = QHBoxLayout()
        layout_sqm_lot = QHBoxLayout()

        # Setarea validatorului pentru a accepta doar numere (inclusiv cu zecimale și semn)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

        # Crearea și adăugarea etichetei și câmpului de text în field_layout1
        self.label1 = QLabel("un numar:")
        self.text_field1 = QLineEdit()
        self.text_field1.setValidator(validator)

        field_layout1.addWidget(self.label1)
        field_layout1.addWidget(self.text_field1)

        # ----------------
        """ 
        label_bedrooms
        field_bedrooms
        
        label_bathrooms
        field_bathrooms
        
        label_sqm_living
        field_sqm_living
        
        label_floors
        field_floors
        
        label_condition
        field_condition
        
        label_grade
        field_grade
        
        label_yr_built
        field_yr_built
        
        label_yr_renovated
        field_yr_renovated
        
        label_sqm_above
        field_sqm_above
        
        label_sqm_basement
        field_sqm_basement
        
        label_sqm_lot
        field_sqm_lot
        
        
         """

        self.label2 = QLabel("un alt numar:")
        self.text_field2 = QLineEdit()
        self.text_field2.setValidator(validator)

        field_layout2.addWidget(self.label2)
        field_layout2.addWidget(self.text_field2)

        # Adăugarea field_layout1 și butonului în left_layout
        left_layout.addLayout(field_layout1)
        left_layout.addLayout(field_layout2)
        self.submit_button = QPushButton("Submit")
        left_layout.addWidget(self.submit_button)

        # Crearea unui container pentru partea stângă
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # Partea dreaptă cu harta interactivă
        web_view = QWebEngineView()
        web_view.load(QUrl("http://localhost:5000/"))

        # Adăugarea widget-urilor la layout-ul principal
        # Valoarea mai mică face partea stângă mai îngustă
        main_layout.addWidget(left_widget, 2)
        # Valoarea mai mare face partea dreaptă mai largă
        main_layout.addWidget(web_view, 2)

        # Setarea layout-ului principal ca widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Conectează butonul "Submit" la slotul pentru a printa valoarea
        self.submit_button.clicked.connect(self.print_value)

    # Slot pentru a prelua și afișa valoarea din text_field1
    def print_value(self):
        value1 = self.text_field1.text()
        value2 = self.text_field2.text()
        print(f"Valoarea introdusă este: {value1} {value2}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
