import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, \
    QGraphicsView, QGraphicsItem, QDialog, QFileDialog
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt
from builder_interface import Ui_MainWindow
from json_settings import Ui_Dialog
import uuid
import json


class JsonSettings(QDialog, Ui_Dialog):

    def __init__(self, parent):
        self.parent = parent
        super(JsonSettings, self).__init__()
        self.setupUi(self)
        self.show()
        self.raise_()
        self.setWindowModality(Qt.ApplicationModal)
        self.textEdit.setText(json.dumps(self.parent.created_environment, indent=4))
        self.buttonBox.accepted.connect(self.save)

    def save(self):
        self.parent.created_environment = json.loads(self.textEdit.toPlainText())


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_intersection.clicked.connect(self.create_intersection)
        self.add_road.clicked.connect(self.create_road)
        self.rotate90.clicked.connect(self.rotate90f)
        self.rotate_90.clicked.connect(self.rotate_90f)
        self.del_object.clicked.connect(self.delete_element)
        self.parse_items.triggered.connect(self.parse)
        self.json_settings.triggered.connect(self.open_modal)
        self.save_json.clicked.connect(self.save_file)

        self.scene = QGraphicsScene(self.centralwidget)

        self.graphicsView = QGraphicsView(self.scene, self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 1, 2, 8, 3)

        self.roads = []
        self.intersections = []

        self.brush = QBrush(Qt.blue)
        self.inter_pen = QPen(Qt.red)
        self.inter_pen.setWidth(6)
        self.road_pen = QPen(Qt.darkGreen)
        self.road_pen.setWidth(10)

        self.created_environment = None
        self.settings_window = None

    def open_modal(self):
        self.settings_window = JsonSettings(self)

    def create_road(self):
        road = self.scene.addLine(0, 0, 0, 75)
        road.setPen(self.road_pen)
        road.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        road.json_id = str(uuid.uuid4())
        road.setZValue(5)
        self.roads.append(road)

    def create_intersection(self):
        intersection = self.scene.addEllipse(0, 0, 45, 45)
        intersection.setPen(self.inter_pen)
        intersection.setBrush(self.brush)
        intersection.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        intersection.json_id = str(uuid.uuid4())
        intersection.setZValue(1)
        self.intersections.append(intersection)

    def rotate90f(self):
        items = self.scene.selectedItems()
        for item in items:
            item.setRotation(item.rotation() + 90)

    def rotate_90f(self):
        items = self.scene.selectedItems()
        for item in items:
            item.setRotation(item.rotation() - 90)

    def delete_element(self):
        items = self.scene.selectedItems()
        for item in items:
            if item in self.roads:
                self.roads.remove(item)
            else:
                self.intersections.remove(item)
            self.scene.removeItem(item)
            del item

    def parse(self):
        new_environment = {"roads": {}, "intersections": {}, "destinations_list": []}
        for road in self.roads:
            connected_roads = [item.json_id for item in road.collidingItems() if item in self.roads]
            if len(connected_roads) <= 3:
                new_environment["destinations_list"].append(road.json_id)
            connected_intersections = [item.json_id for item in road.collidingItems() if item in self.intersections]
            road_p = {
                "intersections": connected_intersections,
                "connected_roads": connected_roads
            }
            new_environment["roads"][road.json_id] = road_p
        for intersection in self.intersections:
            roads = [item.json_id for item in intersection.collidingItems() if item in self.roads]
            roads_x = [item.json_id for item in intersection.collidingItems() if item.rotation() % 90 == 0 and
                       item.rotation() != 0]
            roads_y = [item.json_id for item in intersection.collidingItems() if item.json_id not in roads_x]
            inter_p = {
                "roads": roads,
                "roads_x": roads_x,
                "roads_y": roads_y
            }
            new_environment["intersections"][intersection.json_id] = inter_p

        self.created_environment = new_environment

        with open("temp.json", "w") as f:
            json.dump(new_environment, f)

    def save_file(self):
        name = QFileDialog.getSaveFileName(self, 'Save file', filter="JSON (*.json)")[0]
        with open(name, "w") as f:
            json.dump(self.created_environment, f)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
