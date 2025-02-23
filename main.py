from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PySide6.QtCore import Qt

class SliderDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sliders avec Couleurs Personnalisées")
        self.setFixedSize(300, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Slider orange
        self.slider_orange = QSlider(Qt.Horizontal, self)
        self.slider_orange.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #ddd;
            }
            QSlider::handle:horizontal {
                background: orange;
                border: 1px solid #555;
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        layout.addWidget(self.slider_orange)

        # Slider rouge
        self.slider_rouge = QSlider(Qt.Horizontal, self)
        self.slider_rouge.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #ddd;
            }
            QSlider::handle:horizontal {
                background: red;
                border: 1px solid #555;
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        layout.addWidget(self.slider_rouge)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = SliderDemo()
    window.show()
    app.exec()
