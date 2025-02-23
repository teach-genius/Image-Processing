from PySide6.QtWidgets import QWidget, QFileDialog, QPushButton, QLabel, QVBoxLayout, QMainWindow, QSlider
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt
import cv2
from queue import Queue
import cv2
import numpy as np
from PIL import Image
from PySide6.QtWidgets import QApplication,QMainWindow
from PySide6.QtGui import QPixmap,QIcon
import sys
from PySide6.QtGui import QPixmap,QFont, QFontDatabase,QImage

activity=Queue()
load_image_save=None
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self._pan_title = QLabel("Filtrage",self)
        self._pan_title.setGeometry(713,123,72,15)
        self.image_charge = None
        self.image_current= None
        activity.put(self.image_current)
        # Background view
        back_view = QLabel(self)
        back_view.setPixmap(QPixmap("packages/icons/back_projet1.png").scaled(900, 600))
        back_view.setGeometry(0, 0, 900, 600)
        font_id = QFontDatabase.addApplicationFont('C:/Users/farya/Desktop/OpenCv_2K25_Plate/packages/fonts/Manrope-VariableFont_wght.ttf')
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.label()
        self.panel_gauche()
        self.btn_prev_next()
        self.btn_top()
        self.fun()
        self.load_lateral_droit()
        self.replace_widget(Filtrage(self))
        
        self.selected_btn = self.font2
    
    def update_info(self,title,shape):
        self.titre_view1.setText(title)
        self.titre_view2.setText(title)
        self.titre_view3.setText(title)
        self.shape.setText(shape)

    def label(self):
        self.title = QLabel("ImageLab Pro", self)
        self.title.setGeometry(725, 92, 80, 15)
        self.title.setStyleSheet("color:rgba(160, 159, 166, 1);")

        self.titre_view1 = QLabel("title_image.png", self)
        self.titre_view1.setGeometry(85, 10, 95, 19)
        self.titre_view1.setStyleSheet("color:rgba(30, 30, 30, 1);")

        self.dimension_view = QLabel("Dimension", self)
        self.dimension_view.setStyleSheet("color:rgba(160, 159, 166, 1);")
        self.dimension_view.setGeometry(22, 51, 89, 14)

        self.shape = QLabel("790x515", self)
        self.shape.setStyleSheet("color:rgba(30, 30, 30, 1);font-size:9px;")
        self.shape.setGeometry(113, 51, 39, 14)

        self.titre_view2 = QLabel("title_image.png", self)
        self.titre_view2.setGeometry(381, 45, 95, 19)
        self.titre_view2.setStyleSheet("color:rgba(160, 159, 166, 1);")

        self.titre_view3 = QLabel("title_image.png", self)
        self.titre_view3.setGeometry(122, 147, 95, 19)
        self.titre_view3.setStyleSheet("color:rgba(160, 159, 166, 1);")

        self.View_image = QLabel(self)
        self.View_image.setPixmap(QPixmap("Projet1/icons/main.png").scaled(538, 265))
        self.View_image.setGeometry(133, 168, 538, 265)
        self.View_image.setAlignment(Qt.AlignCenter)

    def fun(self):
        self.top_load = QPushButton("Télécharger", self)
        self.top_load .setCursor(Qt.PointingHandCursor)
        self.top_load.setIcon(QIcon("Projet1/icons/tel.png"))
        self.top_load.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:5px;")
        self.top_load.setGeometry(757, 26, 110, 28)
        self.top_load.clicked.connect(self.save_image)

        self.annul = QPushButton("Annuler", self)
        self.annul.setCursor(Qt.PointingHandCursor)
        self.annul.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:10px;")
        self.annul.setGeometry(745, 548, 109, 27)
        self.annul.clicked.connect(self.back_)

    def back_(self):
        # Vérifier si l'activité n'est pas vide
        if not activity.empty():  # Correction ici : "empty()" au lieu de "isempty()"
            # Récupérer l'image de la queue
            self.image_current = activity.get()
            load_image_save = self.image_current 
            # Vérifier si l'image récupérée n'est pas None
            if self.image_current is not None:
                # Convertir l'image de BGR (OpenCV) à RGB
                frame_rgb = cv2.cvtColor(self.image_current, cv2.COLOR_BGR2RGB)
                # Obtenir les dimensions de l'image
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                # Créer un QImage à partir de l'image RGB
                img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                # Créer un QPixmap à partir du QImage
                pixmap = QPixmap.fromImage(img)
                # Afficher l'image dans le QLabel
                self.View_image.setPixmap(pixmap.scaled(538, 265, Qt.KeepAspectRatio))  
    
    def load_changed(self, frame_rgb):
        h, w, ch = frame_rgb.shape if len(frame_rgb.shape) == 3 else (frame_rgb.shape[0], frame_rgb.shape[1], 1)
        if ch == 3:
            bytes_per_line = ch * w
            img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # Si l'image est en noir et blanc (grayscale)
        elif ch == 1:
            bytes_per_line = w  # Pour une image en niveaux de gris, le nombre de bytes par ligne est égal à la largeur
            img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        # Créer un QPixmap à partir du QImage
        pixmap = QPixmap.fromImage(img)
        # Afficher l'image dans le QLabel, avec le redimensionnement tout en gardant les proportions
        self.View_image.setPixmap(pixmap.scaled(538, 265, Qt.KeepAspectRatio))  # Ajout du KeepAspectRatio pour garder les proportions
        self.View_image.setAlignment(Qt.AlignCenter)
    
    def panel_gauche(self):
        # Création des boutons
        self.font1 = QPushButton(self)
        self.font1.setCursor(Qt.PointingHandCursor)
        self.font1.setGeometry(9, 219, 53, 37)
        self.font1.setStyleSheet("background:transparent;")
        self.font1.setIcon(QIcon("Projet1/icons/3.svg"))
        
        self.font2 = QPushButton(self)
        self.font2.setCursor(Qt.PointingHandCursor)
        self.font2.setGeometry(9, 116, 53, 37)
        self.font2.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:9px;")
        self.font2.setIcon(QIcon("Projet1/icons/1.svg"))

        self.font3 = QPushButton(self)
        self.font3.setCursor(Qt.PointingHandCursor)
        self.font3.setGeometry(9, 168, 53, 37)
        self.font3.setStyleSheet("background:transparent;")
        self.font3.setIcon(QIcon("Projet1/icons/2.svg"))

        self.font4 = QPushButton(self)
        self.font4.setCursor(Qt.PointingHandCursor)
        self.font4.setGeometry(9, 270, 53, 37)
        self.font4.setStyleSheet("background:transparent;")
        self.font4.setIcon(QIcon("Projet1/icons/4.svg"))

        self.font5 = QPushButton(self)
        self.font5.setCursor(Qt.PointingHandCursor)
        self.font5.setGeometry(9, 321, 53, 37)
        self.font5.setStyleSheet("background:transparent;")
        self.font5.setIcon(QIcon("Projet1/icons/5.svg"))
        
        # Connexion des boutons aux méthodes correspondantes
        self.font1.clicked.connect(self.view_hist)
        self.font2.clicked.connect(self.view_filt)
        self.font3.clicked.connect(self.view_morp)
        self.font4.clicked.connect(self.view_dete)
        self.font5.clicked.connect(self.view_segment)

    def replace_widget(self, new_wid):
        """Remplacer le widget actuel par le nouveau widget"""
        # Vider le layout actuel
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Supprimer le widget du layout
                
        # Ajouter le nouveau widget au layout
        self.layout.addWidget(new_wid)

    def view_hist(self):
        self._pan_title.setText("Histogramme")
        self.selected_btn.setStyleSheet("background:transparent;")
        self.replace_widget(Histograme(self))  # Remplacer par Histograme
        self.selected_btn = self.font1
        self.font1.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:9px;")
        
    def view_filt(self):
        self._pan_title.setText("Filtrage")
        self.selected_btn.setStyleSheet("background:transparent;")
        self.replace_widget(Filtrage(self))  # Remplacer par Filtrage
        self.selected_btn = self.font2
        self.font2.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:9px;")
        
    def view_morp(self):
        self._pan_title.setText("Morphologie Mathématique")
        self.selected_btn.setStyleSheet("background:transparent;")
        self.replace_widget(Morphologie(self))  # Remplacer par Morphologie
        self.selected_btn = self.font3
        self.font3.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:9px;")
        
    def view_dete(self):
        self._pan_title.setText("Détection des contours")
        self.selected_btn.setStyleSheet("background:transparent;")
        self.replace_widget(DetectionContours(self))  # Remplacer par DetectionContours
        self.selected_btn = self.font4
        self.font4.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:9px;")
        
    def view_segment(self):
        self._pan_title.setText("Segmentation")
        self.selected_btn.setStyleSheet("background:transparent;")
        self.replace_widget(Segmentation(self))  # Remplacer par DetectionContours
        self.selected_btn = self.font5
        self.font5.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:9px;")
    
    def btn_prev_next(self):
        self.btn_prev = QPushButton("Avant", self)
        self.btn_prev.setCursor(Qt.PointingHandCursor)
        self.btn_prev.setStyleSheet("border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);color:rgba(160, 159, 166, 1);")
        self.btn_next = QPushButton("Après", self)
        self.btn_next.setCursor(Qt.PointingHandCursor)
        self.btn_next.setStyleSheet("background:rgba(245, 123, 56, 1);border-radius:5px;color:white;")
        self.btn_prev.setGeometry(303, 484, 78, 27)
        self.btn_next.setGeometry(416, 484, 78, 27)

    def btn_top(self):
        self.btn_load = QPushButton("Charger", self)
        self.btn_load.setCursor(Qt.PointingHandCursor)
        self.btn_load.setIcon(QIcon("Projet1/icons/load.png"))
        self.btn_load.setStyleSheet("border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);color:rgba(30, 30, 30, 1);")
        self.btn_load.clicked.connect(self.load_image)
        self.btn_delete = QPushButton("Supprimer", self)
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_load.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setIcon(QIcon("Projet1/icons/dele.png"))
        self.btn_delete.clicked.connect(self.deleteimg)
        self.btn_delete.setStyleSheet("border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);color:rgba(30, 30, 30, 1);")
        self.btn_load.setGeometry(271, 109, 110, 28)
        self.btn_delete.setGeometry(435, 109, 110, 28)

    def load_lateral_droit(self):
        # Créer le layout principal
        self.lat = QWidget(self)
        self._pan_title = QLabel("Filtrage",self.lat)
        self._pan_title.setGeometry(5,0,200,15)
        self._pan_title.setStyleSheet("color:rgba(52, 64, 84, 1);")
        self.layout = QVBoxLayout(self.lat)
        self.lat.setGeometry(698, 120, 202, 413)
        
        
    def load_image(self):
        # Ouvrir un dialogue pour sélectionner une image
        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.image_charge = cv2.imread(file_name)
            self.image_current=self.image_charge
            load_image_save  = self.image_charge
            activity.put(self.image_current)
            self.update_info(file_name,f"{self.image_charge.shape[0]}x{self.image_charge.shape[1]}")
            # Charger et afficher l'image si un fichier est sélectionné
            self.View_image.setPixmap(QPixmap(file_name).scaled(538, 265, Qt.KeepAspectRatio))
            

    def save_image(self):
        # Vérifier si une image est chargée
        if load_image_save is not None:
            # Ouvrir un dialogue pour choisir le dossier et le nom du fichier
            file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder l'image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)")
            
            if file_name:
                # Sauvegarder l'image au chemin sélectionné
                cv2.imwrite(file_name,load_image_save)
        else:
            print("Aucune image à sauvegarder.")

    def deleteimg(self):
        if self.image_current is not None:
            self.image_current=None
            load_image_save=None
            self.View_image.setPixmap(QPixmap("Projet1/icons/main.png").scaled(538, 265))
            self.update_info("title_image.png","790x515")

class Histograme(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # Bouton Égalisation
        egalisation = QPushButton("Égalisation", self)
        egalisation .setCursor(Qt.PointingHandCursor)
        egalisation.setGeometry(10, 20, 157, 26)
        egalisation.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        egalisation.clicked.connect(self.filtre_egalisation)
        
        # Bouton Étirement
        etirement = QPushButton("Étirement", self)
        etirement.setCursor(Qt.PointingHandCursor)
        etirement.setGeometry(10, 56, 157, 26)
        etirement.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        etirement.clicked.connect(self.filtre_etirrement)
        
        # Bouton Gamma
        gamma_button = QPushButton("Gamma", self)
        gamma_button.setCursor(Qt.PointingHandCursor)
        gamma_button.setGeometry(10, 90, 157, 26)
        gamma_button.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        gamma_button.clicked.connect(self.filtre_gamma)
        
        # Bouton Beta
        beta_button = QPushButton("Beta", self)
        beta_button.setCursor(Qt.PointingHandCursor)
        beta_button.setGeometry(10, 125, 157, 26)
        beta_button.setStyleSheet("color:rgba(245, 123, 56, 1);border-radius:5px;border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);")
        beta_button.clicked.connect(self.filtre_beta)
        
        # Label Gamma
        gamma_lab = QLabel("Gamma", self)
        gamma_lab.setGeometry(10, 200, 50, 15)
        gamma_lab.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        self.gamma_index = QLabel("0.3", self)
        self.gamma_index.setAlignment(Qt.AlignCenter)
        self.gamma_index.setGeometry(120, 200, 27, 15)
        self.gamma_index.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        # Label Beta
        beta_lab = QLabel("Beta", self)
        beta_lab.setGeometry(10, 240, 50, 15)
        beta_lab.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        self.beta_index = QLabel("0.1", self)
        self.beta_index.setAlignment(Qt.AlignCenter)
        self.beta_index.setGeometry(120, 240, 27, 15)
        self.beta_index.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        # Slider Gamma
        self.slider_orange = QSlider(Qt.Horizontal, self)
        self.slider_orange.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: orange;
                border: 1px solid rgba(104, 191, 255, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_orange.setGeometry(10, 220, 164, 20)
        self.slider_orange.setMinimum(1)
        self.slider_orange.setMaximum(100)
        self.slider_orange.valueChanged.connect(self.update_gamma_label)

        # Slider Beta
        self.slider_rouge = QSlider(Qt.Horizontal, self)
        self.slider_rouge.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: red;
                border: 1px solid rgba(245, 123, 56, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_rouge.setGeometry(10, 260, 164, 20)
        self.slider_rouge.setMinimum(1)
        self.slider_rouge.setMaximum(100)
        self.slider_rouge.valueChanged.connect(self.update_beta_label)

    def update_gamma_label(self, value):
        self.gamma_index.setText(f"{value / 100:.2f}")

    def update_beta_label(self, value):
        self.beta_index.setText(f"{value / 100:.2f}")

    def filtre_egalisation(self):
        if self.parent.image_current is not None:
            f = Histogram_(self.parent.image_current)
            h=f.egalisation_histogramme()
            load_image_save = h
            self.parent.load_changed(h)

    def filtre_etirrement(self):
        if self.parent.image_current is not None:
            f = Histogram_(self.parent.image_current)
            e=f.etirement_histogramme()
            load_image_save = e
            self.parent.load_changed(e)
            
    def filtre_gamma(self):
        if self.parent.image_current is not None:
            f = Histogram_(self.parent.image_current)
            t = f.transformation_gamma(float(self.gamma_index.text()))
            load_image_save = t
            self.parent.load_changed(t)

    def filtre_beta(self):
        if self.parent.image_current is not None:
            f = Histogram_(self.parent.image_current)
            l=f.transformation_beta(float(self.beta_index.text()))
            load_image_save = l
            self.parent.load_changed()

        
class Filtrage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # Bouton Moyenneur
        moyenneur = QPushButton("Moyenneur", self)
        moyenneur.setCursor(Qt.PointingHandCursor)
        moyenneur.clicked.connect(self.filtre_moyen)
        moyenneur.setGeometry(10, 20, 157, 26)
        moyenneur.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        
        # Bouton Médian
        median = QPushButton("Médian", self)
        median.setCursor(Qt.PointingHandCursor)
        median.clicked.connect(self.filtre_median)
        median.setGeometry(10, 56, 157, 26)
        median.setStyleSheet("border:1px solid rgba(245, 123, 56, 1);color:rgba(245, 123, 56, 1);border-radius:5px;background:rgba(245, 245, 245, 1);")
        
        # Label Noyau
        noyau = QLabel("Noyau", self)
        noyau.setGeometry(10, 110, 50, 15)
        noyau.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        # Label Index
        self.index = QLabel("3", self)
        self.index.setAlignment(Qt.AlignCenter)
        self.index.setGeometry(130, 110, 27, 15)
        self.index.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        # Slider
        self.slider_orange = QSlider(Qt.Horizontal, self)
        self.slider_orange.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: orange;
                border: 1px solid rgba(104, 191, 255, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_orange.setGeometry(10, 140, 164, 20)  
        self.slider_orange.setMinimum(3)  
        self.slider_orange.setMaximum(11)  
        self.slider_orange.setSingleStep(2)  
         

        # Connecter l'événement de changement de valeur
        self.slider_orange.valueChanged.connect(self.update_label)

    def filtre_moyen(self):
        if self.parent.image_current is not None:
            f = Filtrage_(self.parent.image_current, self.slider_orange.value())
            self.parent.load_changed(f.moyenneur())

    def filtre_median(self):
        if self.parent.image_current is not None:
            f = Filtrage_(self.parent.image_current, self.slider_orange.value())
            self.parent.load_changed(f.median())

    def update_label(self, value):
        # Mettre à jour le label avec la valeur actuelle du slider
        self.index.setText(str(value))


class Morphologie(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # Initialisation des boutons
        self.init_ui()

    def init_ui(self):
        erosion = QPushButton("Érosion", self)
        erosion.setCursor(Qt.PointingHandCursor)
        erosion.setGeometry(10, 20, 157, 26)
        erosion.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        erosion.clicked.connect(self.filtre_erosion)
        
        dilatation = QPushButton("Dilatation", self)
        dilatation.setCursor(Qt.PointingHandCursor)
        dilatation.setGeometry(10, 60, 157, 26)
        dilatation.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        dilatation.clicked.connect(self.filtre_dilatation)
        
        ouverture = QPushButton("Ouverture", self)
        ouverture.setCursor(Qt.PointingHandCursor)
        ouverture.setGeometry(10, 100, 157, 26)
        ouverture.setStyleSheet("color:rgba(160, 159, 166, 1);border-radius:5px;border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);")
        ouverture.clicked.connect(self.filtre_ouverture)
        
        fermeture = QPushButton("Fermeture", self)
        fermeture.setCursor(Qt.PointingHandCursor)
        fermeture.setGeometry(10, 140, 157, 26)
        fermeture.setStyleSheet("color:rgba(245, 123, 56, 1);border-radius:5px;border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);")
        fermeture.clicked.connect(self.filtre_fermeture)
        
        contour_ex = QPushButton("Contour Externe", self)
        contour_ex.setCursor(Qt.PointingHandCursor)
        contour_ex.setGeometry(10, 180, 157, 26)
        contour_ex.setStyleSheet("color:rgba(245, 123, 56, 1);border-radius:5px;border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);")
        contour_ex.clicked.connect(self.filtre_contour_ex)
        
        contour_in = QPushButton("Contour Interne", self)
        contour_in.setCursor(Qt.PointingHandCursor)
        contour_in.setGeometry(10, 220, 157, 26)
        contour_in.setStyleSheet("color:rgba(245, 123, 56, 1);border-radius:5px;border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);")
        contour_in.clicked.connect(self.filtre_contour_in)
        
        contour_grad = QPushButton("Contour Gradient", self)
        contour_grad.setCursor(Qt.PointingHandCursor)
        contour_grad.setGeometry(10, 260, 157, 26)
        contour_grad.setStyleSheet("color:rgba(245, 123, 56, 1);border-radius:5px;border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);")
        contour_grad.clicked.connect(self.filtre_contour_grad)
        
        kernel = QLabel("Taille", self)
        kernel.setGeometry(10, 300, 50, 15)
        kernel.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        self.index = QLabel("3", self)
        self.index.setAlignment(Qt.AlignCenter)
        self.index.setGeometry(120, 300, 27, 15)
        self.index.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        self.slider_orange = QSlider(Qt.Horizontal, self)
        self.slider_orange.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: orange;
                border: 1px solid rgba(104, 191, 255, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_orange.setGeometry(10, 320, 164, 20)
        self.slider_orange.setMinimum(3)
        self.slider_orange.setMaximum(11)
        self.slider_orange.setSingleStep(2)
        self.slider_orange.valueChanged.connect(self.update_label)

    def update_label(self, value):
        # Mettre à jour le label avec la valeur actuelle du slider
        self.index.setText(str(value))
        

    def get_kernel_size(self):
        return int(self.index.text())

    def filtre_erosion(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.erosion())

    def filtre_dilatation(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.dilatation())
        
    def filtre_ouverture(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.ouverture())
        
    def filtre_fermeture(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.fermeture())
                
    def filtre_contour_ex(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.contour_morphologique())
        
    def filtre_contour_in(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.contour_morphologique())
        
    def filtre_contour_grad(self):
        if self.parent.image_current is not None:
            f = Morphologie_(self.parent.image_current,self.get_kernel_size())
            self.parent.load_changed(f.contour_morphologique())

                
                
class DetectionContours(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # Bouton Prewitt
        self.prewitt_button = QPushButton("Prewitt", self)
        self.prewitt_button.setCursor(Qt.PointingHandCursor)
        self.prewitt_button.setGeometry(10, 20, 157, 26)
        self.prewitt_button.setStyleSheet(
            "color:rgba(160, 159, 166, 1);border-radius:5px;"
            "border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);"
        )
        self.prewitt_button.clicked.connect(self.filtre_prewitt)

        # Bouton Sobel
        self.sobel_button = QPushButton("Sobel", self)
        self.sobel_button.setCursor(Qt.PointingHandCursor)
        self.sobel_button.setGeometry(10, 60, 157, 26)
        self.sobel_button.setStyleSheet(
            "color:rgba(160, 159, 166, 1);border-radius:5px;"
            "border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);"
        )
        self.sobel_button.clicked.connect(self.filtre_sobel)

        # Bouton Robert
        self.robert_button = QPushButton("Robert", self)
        self.robert_button.setCursor(Qt.PointingHandCursor)
        self.robert_button.setGeometry(10, 100, 157, 26)
        self.robert_button.setStyleSheet(
            "color:rgba(160, 159, 166, 1);border-radius:5px;"
            "border:1px solid rgba(160, 159, 166, 1);background:rgba(245, 245, 245, 1);"
        )
        self.robert_button.clicked.connect(self.filtre_robert)

        # Bouton Robinson
        self.robinson_button = QPushButton("Robinson", self)
        self.robinson_button.setCursor(Qt.PointingHandCursor)
        self.robinson_button.setGeometry(10, 140, 157, 26)
        self.robinson_button.setStyleSheet(
            "color:rgba(245, 123, 56, 1);border-radius:5px;"
            "border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);"
        )
        self.robinson_button.clicked.connect(self.filtre_robinson)

        # Bouton Laplacien
        self.laplacien_button = QPushButton("Laplacien", self)
        self.laplacien_button.setCursor(Qt.PointingHandCursor)
        self.laplacien_button.setGeometry(10, 180, 157, 26)
        self.laplacien_button.setStyleSheet(
            "color:rgba(245, 123, 56, 1);border-radius:5px;"
            "border:1px solid rgba(245, 123, 56, 1);background:rgba(245, 245, 245, 1);"
        )
        self.laplacien_button.clicked.connect(self.filtre_laplacien)

        # Labels et slider pour le seuillage
        laplacien_lab = QLabel("Laplacien", self)
        laplacien_lab.setGeometry(10, 215, 50, 15)
        laplacien_lab.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")

        self.index = QLabel("0", self)
        self.index.setGeometry(120, 225, 27, 15)
        self.index.setStyleSheet(
            "color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);"
        )

        seuillage = QLabel("Seuillage", self)
        seuillage.setGeometry(10, 230, 80, 15)
        seuillage.setStyleSheet("color:rgba(160, 159, 166, 1);font-size:10px;")

        self.slider_orange = QSlider(Qt.Horizontal, self)
        self.slider_orange.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: orange;
                border: 1px solid rgba(104, 191, 255, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_orange.setGeometry(10, 250, 164, 20)
        self.slider_orange.setMinimum(0)
        self.slider_orange.setMaximum(100)
        self.slider_orange.setSingleStep(1)
        self.slider_orange.valueChanged.connect(self.update_label)

    def update_label(self, value):
        # Mettre à jour le label avec la valeur actuelle du slider
        self.index.setText(str(value))

    def filtre_prewitt(self):
        if self.parent.image_current is not None:
            f = DetectionContours_(self.parent.image_current)
            h=f.prewitt()
            load_image_save=h
            self.parent.load_changed(h)

    def filtre_sobel(self):
        if self.parent.image_current is not None:
            f = DetectionContours_(self.parent.image_current)
            r=f.sobel()
            load_image_save=r
            self.parent.load_changed(r)

    def filtre_robert(self):
        if self.parent.image_current is not None:
            f = DetectionContours_(self.parent.image_current)
            r=f.roberts()
            load_image_save=r
            self.parent.load_changed(r)

    def filtre_robinson(self):
        if self.parent.image_current is not None:
            f = DetectionContours_(self.parent.image_current)
            r=f.robinson()
            load_image_save=r
            self.parent.load_changed(r)

    def filtre_laplacien(self):
        if self.parent.image_current is not None:
            f = DetectionContours_(self.parent.image_current)
            d=f.laplacian(float(self.slider_orange.value()))
            load_image_save=d
            self.parent.load_changed(d)


class Filtrage_:
    def __init__(self, image, kernel_size):
        self.image = self._load_image(image)
        self.kernel_size = int(kernel_size)  # Assurez-vous que kernel_size est un entier

    def _load_image(self, image):
        if isinstance(image, str):
            # Charger l'image à partir d'un chemin
            return cv2.imread(image)
        elif isinstance(image, Image.Image):
            # Convertir un objet Pillow en NumPy array
            return np.array(image)
        elif isinstance(image, np.ndarray):
            # Si c'est déjà un NumPy array
            return image
        else:
            raise ValueError("Format d'image non supporté")

    def median(self):
        return cv2.medianBlur(self.image, self.kernel_size)

    def moyenneur(self):
        kernel = np.ones((self.kernel_size, self.kernel_size), np.float32) / (self.kernel_size ** 2)
        return cv2.filter2D(self.image, -1, kernel)




class Histogram_:
    def __init__(self, image):
        self.image = self._process_input_image(image)

    def _process_input_image(self, image):
        if isinstance(image, str):  # Si c'est un chemin de fichier
            image = cv2.imread(image)
        elif isinstance(image, Image.Image):  # Si c'est une image PIL
            image = np.array(image)
        elif isinstance(image, np.ndarray):
            image=image
            
        # Vérifier si l'image est couleur ou niveaux de gris et la convertir
        if len(image.shape) == 3:  # Image couleur
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image  # Déjà en niveaux de gris



    def egalisation_histogramme(self):
        return cv2.equalizeHist(self.image)

    def etirement_histogramme(self):
        min_val = np.min(self.image)
        max_val = np.max(self.image)
        stretched = ((self.image - min_val) / (max_val - min_val) * 255).astype(np.uint8)
        return stretched


    def transformation_gamma(self, gamma):
        #fais varier gamma=[0.1,5]

        normalized = self.image / 255.0
        transformed = np.power(normalized, gamma) * 255
        return np.clip(transformed, 0, 255).astype(np.uint8)


    def transformation_beta(self, beta):
        #fais varier beta=[0.1,5]
        normalized = self.image / 255.0
        transformed = 255 * (1 - np.power(1 - normalized, beta))
        return np.clip(transformed, 0, 255).astype(np.uint8)



class Morphologie_:
    def __init__(self,image,kernel):
        self.image = self._process_input_image(image)
        #Taille doit etre impair
        self.kernel= self._create_kernel(int(kernel)) 

    def _process_input_image(self, image):
        if isinstance(image, str):  # Si c'est un chemin de fichier
            image = cv2.imread(image)
        elif isinstance(image, Image.Image):  # Si c'est une image PIL
            image = np.array(image)
        elif isinstance(image, np.ndarray):
            image=image

        # Vérifier si l'image est couleur ou niveaux de gris et la convertir
        if len(image.shape) == 3:  # Image couleur
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image  # Déjà en niveaux de gris


    def _create_kernel(self, kernel):
        return cv2.getStructuringElement(cv2.MORPH_RECT, (kernel, kernel))

    def dilatation(self):
        return cv2.dilate(self.image, self.kernel)

    def erosion(self):
        return cv2.erode(self.image,self.kernel)

    def fermeture(self):
        return cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, self.kernel)

    def ouverture(self):
        return cv2.morphologyEx(self.image, cv2.MORPH_OPEN,self.kernel)

    def contour_morphologique(self):
        dilated = self.dilatation()
        eroded = self.erosion()
        return cv2.subtract(dilated, eroded)



class DetectionContours_:
    def __init__(self, image):
        self.image = self._process_input_image(image)

    def _process_input_image(self, image):
        if isinstance(image, str):  # Si c'est un chemin de fichier
            image = cv2.imread(image)
        elif isinstance(image, Image.Image):  # Si c'est une image PIL
            image = np.array(image)
        elif isinstance(image, np.ndarray):  # Si c'est déjà un tableau NumPy
            pass

        # Conversion en niveaux de gris si l'image est en couleur
        if len(image.shape) == 3:  # Image couleur
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image  # Retourner l'image en niveaux de gris


    def _seuillage(self, image, threshold):
        _, seuillee = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        return seuillee

    def roberts(self):
        kernel_roberts_x = np.array([[1, 0], [0, -1]], dtype=float)
        kernel_roberts_y = np.array([[0, 1], [-1, 0]], dtype=float)

        grad_x = cv2.filter2D(self.image, -1, kernel_roberts_x)
        grad_y = cv2.filter2D(self.image, -1, kernel_roberts_y)

        # Calcul de la magnitude du gradient
        magnitude = np.hypot(grad_x, grad_y)
        magnitude = np.uint8(np.clip(magnitude, 0, 255))  # Normalisation de l'intensité

        return magnitude

    def sobel(self):
        grad_x = cv2.Sobel(self.image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(self.image, cv2.CV_64F, 0, 1, ksize=3)
        grad = cv2.magnitude(grad_x, grad_y)
        return np.uint8(np.clip(grad, 0, 255))

 
    def prewitt(self):
        
        # Définir les noyaux de Prewitt
        kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float) / 3
        kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float) / 3
        # Appliquer les noyaux sur l'image
        grad_x = cv2.filter2D(self.image, -1, kernel_x)
        grad_y = cv2.filter2D(self.image, -1, kernel_y)
        
        # Calculer la magnitude du gradient
        grad = np.sqrt(grad_x**2 + grad_y**2)
        # Convertir grad en float32 pour cv2.normalize
        grad = grad.astype(np.float32)
        # Normaliser la magnitude du gradient pour qu'elle s'étende de 0 à 255
        grad = cv2.normalize(grad, None, 0, 255, cv2.NORM_MINMAX)
        # Convertir en entier non signé 8 bits
        grad = np.uint8(grad)
        return self._seuillage(grad,50)
        

    def robinson(self):
        masques = [
            np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]]),  # Nord
            np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]]),   # Nord-Est
            np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),   # Est
            np.array([[-1, -1, 0], [-1, 0, 1], [0, 1, 1]]),   # Sud-Est
            np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),   # Sud
            np.array([[0, 1, 1], [-1, 0, 1], [-1, -1, 0]]),   # Sud-Ouest
            np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]]),   # Ouest
            np.array([[1, 1, 0], [1, 0, -1], [0, -1, -1]])    # Nord-Ouest
        ]
    
        g = [cv2.filter2D(self.image, -1,masque) for masque in masques]
        # Combine les résultats en prenant le maximum de chaque direction pour avoir les contours finaux
        sortie = np.max(g, axis=0)
        sortie = np.clip(sortie, 0, 255).astype(np.uint8)
        return sortie


    def laplacian(self, threshold):
        grad = cv2.Laplacian(self.image, cv2.CV_64F)
        grad = np.abs(grad) 
        
        # Appliquer le seuillage [0,100]
        return self._seuillage(grad, threshold)
class Segmentation(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
        # Label Gamma (x)
        gamma_lab = QLabel("Germe x", self)
        gamma_lab.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        # Slider Gamma (x)
        self.slider_gamma_x = QSlider(Qt.Horizontal, self)
        self.slider_gamma_x.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: orange;
                border: 1px solid rgba(104, 191, 255, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_gamma_x.setMinimum(0)
        self.slider_gamma_x.setSingleStep(1)
        self.slider_gamma_x.setMaximum(100)
        self.slider_gamma_x.valueChanged.connect(self.update_gamma_x_label)

        self.gamma_x_label = QLabel("0", self)
        self.gamma_x_label.setAlignment(Qt.AlignCenter)
        self.gamma_x_label.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        # Label Beta (y)
        beta_lab = QLabel("Germe y", self)
        beta_lab.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        # Slider Beta (y)
        self.slider_gamma_y = QSlider(Qt.Horizontal, self)
        self.slider_gamma_y.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: red;
                border: 1px solid rgba(245, 123, 56, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_gamma_y.setMinimum(0)
        self.slider_gamma_y.setSingleStep(1)
        self.slider_gamma_y.setMaximum(100)
        self.slider_gamma_y.valueChanged.connect(self.update_gamma_y_label)

        self.gamma_y_label = QLabel("0", self)
        self.gamma_y_label.setAlignment(Qt.AlignCenter)
        self.gamma_y_label.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        # Label Seuil (Threshold)
        seuil_lab = QLabel("Seuil", self)
        seuil_lab.setStyleSheet("color:rgba(52, 64, 84, 1);background:transparent;")
        
        # Slider Seuil
        self.slider_seuil = QSlider(Qt.Horizontal, self)
        self.slider_seuil.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(217, 217, 217, 1);
            }
            QSlider::handle:horizontal {
                background: pink;
                border: 1px solid rgba(245, 123, 56, 1);
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        self.slider_seuil.setMinimum(0)
        self.slider_seuil.setMaximum(255)
        self.slider_seuil.valueChanged.connect(self.update_seuil_label)

        self.seuil_label = QLabel("0", self)
        self.seuil_label.setAlignment(Qt.AlignCenter)
        self.seuil_label.setStyleSheet("color:rgba(0, 0, 0, 1);border-radius:5px;background:rgba(217, 217, 217, 1);")
        
        
        # Button Segmentation
        self.segmentation_button = QPushButton("Segmentation", self)
        self.segmentation_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(245, 123, 56, 1);
                color: black;
                border-radius:5px;
            }
            QPushButton:pressed {
                background-color: rgba(245, 123, 56, 1);
            }
            QPushButton:hover {
                background-color: rgba(245, 123, 56, 0.5);
            }
        """)
        self.segmentation_button.setFixedHeight(36)
        self.segmentation_button.clicked.connect(self.run_segmentation)
        self.segmentation_button.setCursor(Qt.PointingHandCursor)
        
        # Layout (alignement vertical)
        layout = QVBoxLayout()
        
        layout.addWidget(gamma_lab)
        layout.addWidget(self.slider_gamma_x)
        layout.addWidget(self.gamma_x_label)
        
        layout.addWidget(beta_lab)
        layout.addWidget(self.slider_gamma_y)
        layout.addWidget(self.gamma_y_label)
        
        layout.addWidget(seuil_lab)
        layout.addWidget(self.slider_seuil)
        layout.addWidget(self.seuil_label)
        
        layout.addWidget(self.segmentation_button)

        self.setLayout(layout)

    def update_gamma_x_label(self, value):
        self.gamma_x_label.setText(f"{value}")
        

    def update_gamma_y_label(self, value):
        self.gamma_y_label.setText(f"{value}")
        

    def update_seuil_label(self, value):
        self.seuil_label.setText(f"{value}")
        

    def run_segmentation(self):
        # Appel de la segmentation avec les paramètres mis à jour
        if self.parent.image_current is not None:
            gamma_x = int(self.gamma_x_label.text())  # Utiliser la valeur du slider gamma X
            gamma_y = int(self.gamma_y_label.text())  # Utiliser la valeur du slider gamma Y
            seuil = float(self.seuil_label.text())  # Utiliser la valeur du seuil
            segmentation = Segmentation_(self.parent.image_current, gamma_x, gamma_y, seuil)
            self.parent.load_changed(segmentation.segment())

class Segmentation_:
    def __init__(self, image, germ_x, germ_y, threshold):
        self.image = self._process_input_image(image)
        self.germ_x = germ_x
        self.germ_y = germ_y
        self.threshold = threshold

    def _process_input_image(self, image):
        if isinstance(image, str):  # Si c'est un chemin de fichier
            image = cv2.imread(image)
        elif isinstance(image, np.ndarray):  # Si c'est une image numpy array
            image = image
        elif isinstance(image, Image.Image):  # Si c'est une image PIL
            image = np.array(image)
        
        # Conversion en niveaux de gris si l'image est couleur
        if len(image.shape) == 3:  # Image couleur
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image  # Déjà en niveaux de gris

    def segment(self):
        # Créer une image de masque (région de segmentation)
        mask = np.zeros_like(self.image, dtype=np.uint8)

        # Liste des pixels à traiter (initialement le germe)
        pixels_to_process = [(self.germ_x, self.germ_y)]

        # Valeur du pixel du germe (pour comparaison)
        germ_value = self.image[self.germ_y, self.germ_x]

        while pixels_to_process:
            x, y = pixels_to_process.pop()
            # Si le pixel est déjà dans le masque, on passe au suivant
            if mask[y, x] == 255:
                continue
            # Ajouter le pixel au masque
            mask[y, x] = 255

            # Vérifier les voisins dans les 8 directions (voisinage de 3x3)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    # Vérifier les limites de l'image
                    if 0 <= nx < self.image.shape[1] and 0 <= ny < self.image.shape[0]:
                        # Si le pixel voisin n'est pas encore dans le masque et est similaire
                        if mask[ny, nx] == 0 and abs(int(self.image[ny, nx]) - int(germ_value)) <= self.threshold:
                            pixels_to_process.append((nx, ny))

        return mask


class Connexion(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.central_widget = Dashboard()
        self.setFixedSize(900, 600)
        self.setWindowIcon(QIcon(QPixmap("packages/icons/icon_logo.svg")))
        self.setframe(self.central_widget)
         
    def setframe(self, fen):
        self.setCentralWidget(fen)
        
    def set_win_title(self,title):
        self.setWindowTitle(title)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Connexion()
    window.show()
    sys.exit(app.exec())
