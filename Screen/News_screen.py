from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from Parametres import *
from Custom_interface import (CustomButton)

class NewsFeedScreen(Screen):
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
            text="Pronote",
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

        layout.add_widget(back_button)
        layout.add_widget(label)
        layout.add_widget(separator)

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
