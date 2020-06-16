from python_qt_binding import QtCore
from python_qt_binding import QtWidgets
import value_widget


class DoubleValueWidget(value_widget.ValueWidget):

    LCD_HEIGHT = 35

    def __init__(self, topic_name, attributes, array_index, publisher, parent,
                 label_text=None, initial_value=0.0):
        self._type = float
        self._initial_value = initial_value
        super(DoubleValueWidget, self).__init__(
            topic_name, attributes, array_index, publisher, parent,
            label_text=label_text)

    def set_value(self, value):
        self._lcd.display(value)
        self.publish_value(value)

    def value_to_slider(self, value):
        return (value - self._min_spin_box.value()) / (
            (self._max_spin_box.value() - self._min_spin_box.value())) * 100.0

    def slider_to_value(self, val):
        return self._min_spin_box.value() + (
            (self._max_spin_box.value() -
             self._min_spin_box.value()) / 100.0 * val)

    def slider_changed(self, val):
        self.set_value(self.slider_to_value(val))

    def setup_ui(self, name, max_value=10000.0, min_value=-10000.0, 
                 default_max_value = 10.0, default_min_value = -10.0):
        self._min_spin_box = QtWidgets.QDoubleSpinBox()
        self._min_spin_box.setMaximum(max_value)
        self._min_spin_box.setMinimum(min_value)
        self._min_spin_box.setValue(default_min_value)
        self._slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self._slider.valueChanged.connect(self.slider_changed)
        self._max_spin_box = QtWidgets.QDoubleSpinBox()
        self._max_spin_box.setMaximum(max_value)
        self._max_spin_box.setMinimum(min_value)
        self._max_spin_box.setValue(default_max_value)
        self._lcd = QtWidgets.QLCDNumber()
        self._lcd.setMaximumHeight(self.LCD_HEIGHT)
        self._slider.setValue(self.value_to_slider(self._initial_value))
        zero_button = QtWidgets.QPushButton('reset')
        zero_button.clicked.connect(
            lambda x: self._slider.setValue(self.value_to_slider(0.0)))
        self._horizontal_layout.addWidget(self._min_spin_box)
        self._horizontal_layout.addWidget(self._slider)
        self._horizontal_layout.addWidget(self._max_spin_box)
        self._horizontal_layout.addWidget(self._lcd)
        self._horizontal_layout.addWidget(zero_button)

        self.setLayout(self._horizontal_layout)


    def get_range(self):
        return (self._min_spin_box.value(), self._max_spin_box.value())

    def set_range(self, min_max):
        self._min_spin_box.setValue(min_max[0])
        self._max_spin_box.setValue(min_max[1])
