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
        self.setGeometry(100, 100, 950, 600)

        # Crearea layout-ului principal
        main_layout = QHBoxLayout()

        # Partea stângă cu QHBoxLayout pentru QLabel și QLineEdit, și un QPushButton
        left_layout = QVBoxLayout()

        # Crearea unui QHBoxLayout pentru label și text_field
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
        self.label_bedrooms = QLabel("Bedrooms:")
        self.field_bedrooms = QLineEdit()
        self.field_bedrooms.setValidator(validator)

        self.label_bathrooms = QLabel("Bathrooms:")
        self.field_bathrooms = QLineEdit()
        self.field_bathrooms.setValidator(validator)

        self.label_sqm_living = QLabel("Living Area (sqm):")
        self.field_sqm_living = QLineEdit()
        self.field_sqm_living.setValidator(validator)

        self.label_floors = QLabel("Floors:")
        self.field_floors = QLineEdit()
        self.field_floors.setValidator(validator)

        self.label_condition = QLabel("Condition:")
        self.field_condition = QLineEdit()
        self.field_condition.setValidator(validator)

        self.label_grade = QLabel("Grade:")
        self.field_grade = QLineEdit()
        self.field_grade.setValidator(validator)

        self.label_yr_built = QLabel("Year Built:")
        self.field_yr_built = QLineEdit()
        self.field_yr_built.setValidator(validator)

        self.label_yr_renovated = QLabel("Year Renovated:")
        self.field_yr_renovated = QLineEdit()
        self.field_yr_renovated.setValidator(validator)

        self.label_sqm_above = QLabel("Above Area (sqm):")
        self.field_sqm_above = QLineEdit()
        self.field_sqm_above.setValidator(validator)

        self.label_sqm_basement = QLabel("Basement Area (sqm):")
        self.field_sqm_basement = QLineEdit()
        self.field_sqm_basement.setValidator(validator)

        self.label_sqm_lot = QLabel("Lot Area (sqm):")
        self.field_sqm_lot = QLineEdit()
        self.field_sqm_lot.setValidator(validator)

        layout_bedrooms.addWidget(self.label_bedrooms)
        layout_bedrooms.addWidget(self.field_bedrooms)

        layout_bathrooms.addWidget(self.label_bathrooms)
        layout_bathrooms.addWidget(self.field_bathrooms)

        layout_sqm_living.addWidget(self.label_sqm_living)
        layout_sqm_living.addWidget(self.field_sqm_living)

        layout_floors.addWidget(self.label_floors)
        layout_floors.addWidget(self.field_floors)

        layout_condition.addWidget(self.label_condition)
        layout_condition.addWidget(self.field_condition)

        layout_grade.addWidget(self.label_grade)
        layout_grade.addWidget(self.field_grade)

        layout_yr_built.addWidget(self.label_yr_built)
        layout_yr_built.addWidget(self.field_yr_built)

        layout_yr_renovated.addWidget(self.label_yr_renovated)
        layout_yr_renovated.addWidget(self.field_yr_renovated)

        layout_sqm_above.addWidget(self.label_sqm_above)
        layout_sqm_above.addWidget(self.field_sqm_above)

        layout_sqm_basement.addWidget(self.label_sqm_basement)
        layout_sqm_basement.addWidget(self.field_sqm_basement)

        layout_sqm_lot.addWidget(self.label_sqm_lot)
        layout_sqm_lot.addWidget(self.field_sqm_lot)

        # Adăugarea field_layout1 și butonului în left_layout
        left_layout.addLayout(layout_bedrooms)
        left_layout.addLayout(layout_bathrooms)
        left_layout.addLayout(layout_sqm_living)
        left_layout.addLayout(layout_floors)
        left_layout.addLayout(layout_condition)
        left_layout.addLayout(layout_grade)
        left_layout.addLayout(layout_yr_built)
        left_layout.addLayout(layout_yr_renovated)
        left_layout.addLayout(layout_sqm_above)
        left_layout.addLayout(layout_sqm_basement)
        left_layout.addLayout(layout_sqm_lot)

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
        bedrooms = self.field_bedrooms.text()
        bathrooms = self.field_bathrooms.text()
        sqm_living = self.field_sqm_living.text()
        floors = self.field_floors.text()
        condition = self.field_condition.text()
        grade = self.field_grade.text()
        yr_built = self.field_yr_built.text()
        yr_renovated = self.field_yr_renovated.text()
        sqm_above = self.field_sqm_above.text()
        sqm_basement = self.field_sqm_basement.text()
        sqm_lot = self.field_sqm_lot.text()

        # read x and y from the file coordinates.txt
        with open("coordinates.txt", "r") as file:
            coords = file.read().splitlines()
            # if coords is empty, set default values to 0
            if not coords:
                coords_x = 0
                coords_y = 0
            else:
                coords = coords[0].split(",")
                coords_x = coords[0]
                coords_y = coords[1]

        if coords_x == 0:
            return

        print(f"Bedrooms: {bedrooms}")
        print(f"Bathrooms: {bathrooms}")
        print(f"Living Area (sqm): {sqm_living}")
        print(f"Floors: {floors}")
        print(f"Condition: {condition}")
        print(f"Grade: {grade}")
        print(f"Year Built: {yr_built}")
        print(f"Year Renovated: {yr_renovated}")
        print(f"Above Area (sqm): {sqm_above}")
        print(f"Basement Area (sqm): {sqm_basement}")
        print(f"Lot Area (sqm): {sqm_lot}")
        print(f"X: {coords_x}")
        print(f"Y: {coords_y}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
