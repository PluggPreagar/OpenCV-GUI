from PySide6.QtWidgets import QComboBox, QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from stepslider import StepSlider

MAXIMUM_HEIGHT = 65

class MenuWithText(QFrame):
    def __init__(self, menu_parameters, index, event_to_call):
        super().__init__()
        self.setMaximumHeight(MAXIMUM_HEIGHT)

        self.parameters = menu_parameters

        self.menu = QComboBox()
        self.menu.addItems(menu_parameters['menu_item'].keys())
        self.menu.setCurrentIndex(index)
        self.menu.currentIndexChanged.connect(self.update_value_changed)
        self.menu.currentIndexChanged.connect(event_to_call)

        self.value = list(menu_parameters['menu_item'].values())[0]

        self.variable_name = self.parameters['variable_name']


        self.label = QLabel()
        self.label.setText(menu_parameters['name'])

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.menu)


    def update_value_changed(self):
        current_index_menu = self.menu.currentIndex()
        self.value = list(self.parameters['menu_item'].values())[current_index_menu]