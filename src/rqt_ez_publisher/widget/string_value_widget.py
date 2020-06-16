from python_qt_binding import QtWidgets
import value_widget


class StringValueWidget(value_widget.ValueWidget):

    def __init__(self, topic_name, attributes, array_index, publisher, parent, 
                 initial_value=''):
        self._type = str
        self._initial_value = initial_value
        super(StringValueWidget, self).__init__(
            topic_name, attributes, array_index, publisher, parent)

    def input_text(self):
        self.publish_value(str(self._line_edit.text()))

    def setup_ui(self, name):
        self._line_edit = QtWidgets.QLineEdit()
        self._line_edit.setText(self._initial_value)
        self._line_edit.returnPressed.connect(self.input_text)
        self._horizontal_layout.addWidget(self._line_edit)
        self.setLayout(self._horizontal_layout)
