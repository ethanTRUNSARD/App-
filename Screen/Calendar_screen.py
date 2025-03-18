
import json
from kivy.app import App

from Parametres import *
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from Custom_interface import CustomButton


# --- Vos données JSON ---
with open("C:/Users/Ethan/Desktop/Maison/python/App/donnés/extracted_data.json", "r", encoding="utf8") as file:
    json_data = json.load(file)
schedule_data = json_data["schedule"]

# --- Écran Calendrier ---
class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanc
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Création du bouton retour en haut
        back_button = CustomButton(
            text="Retour",
            font_size=30,
            size_hint=(None, None),
            size=(112.5, 75),
            pos_hint={'top': horizontale_button_retour, 'right': vertical_button_retour}
        )

        back_button.bind(on_press=self.goto_home)

        # Titre
        label = Label(
            text="Calendrier",
            font_size=80,
            size_hint=(None, None),
            size=(600, 200),
            text_size=(600, None),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        label.pos_hint = {'x': 0.12, 'y': 0.77}

        # Ajouter une ligne de séparation (couvrant toute la largeur de l'écran)
        separator = Widget(size_hint=(None, None), size=(Window.width, 2.5), pos_hint={'x': 0, 'y': 0.85})
        with separator.canvas:
            Color(0, 0, 0, 1)  # Noir
            self.sep_rect = Rectangle(pos=separator.pos, size=separator.size)
        separator.bind(pos=self.update_sep, size=self.update_sep)

        # Tableau des horaires
        schedule_table = ScheduleTable(schedule_data,
                                       size_hint=(1, None),  # Taille dynamique
                                       height=Window.height * 0.6,  # Limiter la hauteur à 60%
                                       pos_hint={'x': 0, 'y': 0.1})  # Placer le tableau avec un peu d'espace

        # Assurer que le texte du tableau est noir
        schedule_table.color = (0, 0, 0, 1)  # Texte du tableau en noir

        layout.add_widget(back_button)
        layout.add_widget(label)
        layout.add_widget(separator)
        layout.add_widget(schedule_table)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_sep(self, instance, value):
        # Met à jour la position et la taille du rectangle de séparation
        self.sep_rect.pos = instance.pos
        self.sep_rect.size = instance.size

    def goto_home(self, instance):
        self.manager.current = 'home'
























# --- Création du tableau du planning ---
class ScheduleTable(GridLayout):
    def __init__(self, schedule, **kwargs):
        super().__init__(**kwargs)
        self.cols = 5  # Une colonne pour chaque champ sauf "Couleur"
        self.spacing = 5
        self.padding = 5

        # Ligne d'entête
        headers = ["Horaire", "Matière", "Professeur", "Salle", "Statut"]
        for header in headers:
            header_label = Label(text=header, bold=True, size_hint_y=None, height=40, color=(0, 0, 0, 1))
            self.add_widget(header_label)

        # Ajout des horaires pour chaque cours
        for item in schedule:
            # Combiner les colonnes Début et Fin en une seule colonne avec "de ... à ..."
            time_range = f"de {item['start_time']} à {item['end_time']}"
            self.add_widget(Label(text=time_range, size_hint_y=None, height=40, color=(0, 0, 0, 1)))
            self.add_widget(Label(text=item['subject'], size_hint_y=None, height=40, color=(0, 0, 0, 1)))
            self.add_widget(Label(text=item['teacher'], size_hint_y=None, height=40, color=(0, 0, 0, 1)))

            # Vérifier si la salle est "[305_MEDIA]", et l'enlever si c'est le cas
            room = item['room']
            if "[305_MEDIA]" in room:
                room = ""  # On ne l'affiche pas dans la colonne "Salle"

            # Affichage de la salle (si différente de "[305_MEDIA]")
            self.add_widget(Label(text=room, size_hint_y=None, height=40, color=(0, 0, 0, 1)))

            # Affichage du statut, si présent (dans ce cas, salle 211 est dans le statut)
            status = item['status']
            self.add_widget(Label(text=status, size_hint_y=None, height=40, color=(0, 0, 0, 1)))