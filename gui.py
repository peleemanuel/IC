import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QMessageBox, QProgressBar)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from datetime import datetime
import networkx as nx
import osmnx as ox
import pandas as pd
from xgboost import XGBRegressor

class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    priceUpdated = pyqtSignal(float)

    def __init__(self, lat, lon, bedrooms, bathrooms, sqm_living, floors, condition, grade, yr_built, yr_renovated, sqm_above, sqm_basement, sqm_lot):
        super().__init__()
        self.lat = lat
        self.lon = lon
        self.bedrooms = int(bedrooms)
        self.bathrooms = float(bathrooms)
        self.sqm_living = float(sqm_living)
        self.floors = float(floors)
        self.condition = int(condition)
        self.grade = int(grade)
        self.yr_built = int(yr_built)
        self.yr_renovated = int(yr_renovated)
        self.sqm_above = float(sqm_above)
        self.sqm_basement = float(sqm_basement)
        self.sqm_lot = float(sqm_lot)

    def fetch_pois(self):
        dist = 1250
        network_type = 'walk'
        plot = True
        lat = float(self.lat)
        lon = float(self.lon)
        point = (lat, lon)
        self.progress.emit(5)
        try:
            G = ox.graph_from_point(point, dist=dist, network_type=network_type, simplify=True)
            self.progress.emit(24)
            amenities = [
                'hospital', 'clinic', 'doctors', 'pharmacy', 'dentist',
                'school', 'college', 'kindergarten', 'university', 'library', 'music_school',
                'supermarket', 'marketplace', 'mall', 'bank', 'bureau_de_change',
                'restaurant', 'cafe', 'bar', 'pub', 'biergarten',
                'theatre', 'cinema', 'museum', 'arts_centre', 'gallery',
                'bus_station', 'ferry_terminal', 'taxi', 'car_rental', 'bicycle_rental', 'car_sharing',
                'park', 'stadium', 'swimming_pool', 'sports_centre'
            ]
            self.progress.emit(26)
            pois = ox.geometries_from_point(point, tags={'amenity': amenities}, dist=dist)
            self.progress.emit(37)
            nearest_node = ox.distance.nearest_nodes(G, lon, lat)
            self.progress.emit(44)
        except Exception as e:
            print(f"Error fetching POIs for location ({lat}, {lon}): {e}")
            return None, None, None

        if plot and G is not None:
            fig, ax = ox.plot_graph(G, show=False, close=False)
            pois['geometry'].plot(ax=ax, color='red', markersize=30)
            x, y = G.nodes[nearest_node]['x'], G.nodes[nearest_node]['y']
            ax.scatter(x, y, color='blue', s=100, zorder=5)
            self.progress.emit(50)
            return G, pois, nearest_node

        self.progress.emit(50)
        return G, pois, nearest_node

    def run(self):
        self.progress.emit(1)
        graph, points_of_interest, nearest_node = self.fetch_pois()
        self.progress.emit(60)
        if graph:
            avg_node_degree = sum(dict(graph.degree()).values()) / len(graph.nodes)
            degree_centrality = nx.degree_centrality(graph)
            betweenness_centrality = nx.betweenness_centrality(graph)
            closeness_centrality = nx.closeness_centrality(graph)
            density = nx.density(graph)
            self.progress.emit(90)
            model = XGBRegressor()
            model.load_model('notebooks/model.json')
            self.progress.emit(93)
            features = {
                "bedrooms": [self.bedrooms],
                "bathrooms": [self.bathrooms],
                "sqm_living": [self.sqm_living],
                "floors": [self.floors],
                "condition": [self.condition],
                "grade": [self.grade],
                "yr_built": [self.yr_built],
                "yr_renovated": [self.yr_renovated],
                "avg_degree": [avg_node_degree],
                "degree_centrality": [degree_centrality[nearest_node]],
                "betweenness_centrality": [betweenness_centrality[nearest_node]],
                "closeness_centrality": [closeness_centrality[nearest_node]],
                "density": [density],
                "sqm_above": [self.sqm_above],
                "sqm_basement": [self.sqm_basement],
                "sqm_lot": [self.sqm_lot],
            }
            df = pd.DataFrame(features)
            predicted_price = model.predict(df)[0]
            seattlePriceIndex = 262
            timisoaraPriceIndex = 152.28
            predicted_price = predicted_price * timisoaraPriceIndex / seattlePriceIndex
            print("Predicted price:", predicted_price)
            self.progress.emit(100) 
            self.priceUpdated.emit(predicted_price)

        else:
            QMessageBox.critical(None, "Error", "Error fetching POIs and graph data.")
            print("Error fetching POIs and graph data.")
        self.finished.emit()

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interactive Map')
        self.setGeometry(100, 100, 950, 650)

        main_layout = QVBoxLayout()
        form_and_map_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)

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
        layout_result = QHBoxLayout()
        layout_desired_price = QHBoxLayout()  # Layout for desired price input

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)

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
        self.field_condition.setValidator(QIntValidator(1, 5))

        self.label_grade = QLabel("Grade:")
        self.field_grade = QLineEdit()
        self.field_grade.setValidator(QIntValidator(1, 12))

        self.label_yr_built = QLabel("Year Built:")
        self.field_yr_built = QLineEdit()
        self.field_yr_built.setValidator(QIntValidator(1500, datetime.now().year))

        self.label_yr_renovated = QLabel("Year Renovated:")
        self.field_yr_renovated = QLineEdit()
        self.field_yr_renovated.setValidator(QIntValidator(0, datetime.now().year))

        self.label_sqm_above = QLabel("Above Area (sqm):")
        self.field_sqm_above = QLineEdit()
        self.field_sqm_above.setValidator(validator)

        self.label_sqm_basement = QLabel("Basement Area (sqm):")
        self.field_sqm_basement = QLineEdit()
        self.field_sqm_basement.setValidator(validator)

        self.label_sqm_lot = QLabel("Lot Area (sqm):")
        self.field_sqm_lot = QLineEdit()
        self.field_sqm_lot.setValidator(validator)

        self.label_desired_price = QLabel("Desired Price:")
        self.field_desired_price = QLineEdit()
        self.field_desired_price.setValidator(validator)

        self.label_result = QLabel("Predicted Price: 0")
        self.label_result.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.label_result.setAlignment(Qt.AlignCenter)

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

        layout_desired_price.addWidget(self.label_desired_price)
        layout_desired_price.addWidget(self.field_desired_price)

        layout_result.addWidget(self.label_result)

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
        left_layout.addLayout(layout_desired_price)  # Add the desired price input to the layout

        self.submit_button = QPushButton("Submit")
        left_layout.addWidget(self.submit_button)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        right_layout = QVBoxLayout()
        web_view = QWebEngineView()
        web_view.load(QUrl("http://localhost:5000/"))
        right_layout.addWidget(web_view)
        right_layout.addLayout(layout_result)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        form_and_map_layout.addWidget(left_widget, 2)
        form_and_map_layout.addWidget(right_widget, 3)

        main_layout.addLayout(form_and_map_layout)
        main_layout.addWidget(self.progress_bar)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.submit_button.clicked.connect(self.on_submit)

    def update_price(self, price):
    # Calculează intervalul de preț în jurul prețului prezis
        lower_bound = price * 0.9
        upper_bound = price * 1.1
        
        # Verifică dacă există un preț dorit introdus de utilizator
        if self.field_desired_price.text():
            try:
                desired_price = float(self.field_desired_price.text())
                # Determină dacă prețul dorit este în intervalul ±10% al prețului prezis
                if lower_bound <= desired_price <= upper_bound:
                    self.label_result.setText(f"Predicted Price: {price:.2f} (Desired price {desired_price:.2f} is within a decent range)")
                else:
                    self.label_result.setText(f"Predicted Price: {price:.2f} (Desired price {desired_price:.2f} is out of range), Suggested Range: {lower_bound:.2f} - {upper_bound:.2f}")
            except ValueError:
                # Gestionarea cazului în care inputul pentru prețul dorit nu este un număr valid
                self.label_result.setText(f"Predicted Price: {price:.2f} (Invalid desired price input)")
        else:
            # Afisează prețul prezis și intervalul său dacă nu există un preț dorit introdus
            self.label_result.setText(f"Predicted Price: {price:.2f}, Suggested Range: {lower_bound:.2f} - {upper_bound:.2f}")

    def on_submit(self):
        if not os.path.exists("coordinates.txt"):
            QMessageBox.critical(self, "Error", "Location not chosen - coordinate file does not exist.")
            return
        try:
            with open("coordinates.txt", "r") as file:
                coords = file.read().splitlines()
                if not coords:
                    raise ValueError("Location not chosen - coordinate file is empty.")
                coords = coords[0].split(",")
                coords_x = coords[0]
                coords_y = coords[1]
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        try:
            condition = int(self.field_condition.text())
            grade = int(self.field_grade.text())
            yr_built = int(self.field_yr_built.text()) if self.field_yr_built.text() else None
            yr_renovated = int(self.field_yr_renovated.text()) if self.field_yr_renovated.text() else 0
            if not (1 <= condition <= 5):
                raise ValueError("Condition must be between 1 and 5.")
            if not (1 <= grade <= 12):
                raise ValueError("Grade must be between 1 and 12.")
            if yr_built is not None and not (1500 <= yr_built <= datetime.now().year):
                raise ValueError(f"Year Built must be between 1500 and {datetime.now().year}.")
            if yr_renovated != 0 and (yr_built is None or yr_renovated < yr_built):
                raise ValueError("Year Renovated must be 0 or greater than Year Built.")
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", str(e))
            return
        self.start_processing(coords_x, coords_y)

    def start_processing(self, lat, lon):
        print(f"Starting processing for location ({lat}, {lon})")
        self.thread = WorkerThread(lat, lon, self.field_bedrooms.text(), self.field_bathrooms.text(), self.field_sqm_living.text(), self.field_floors.text(), self.field_condition.text(), self.field_grade.text(), self.field_yr_built.text(), self.field_yr_renovated.text(), self.field_sqm_above.text(), self.field_sqm_basement.text(), self.field_sqm_lot.text())
        self.thread.priceUpdated.connect(self.update_price)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.processing_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def processing_finished(self):
        QMessageBox.information(self, "Processing Complete", "All metrics have been calculated.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
