from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from Custom_interface import CustomButton  # Assurez-vous que CustomButton est bien défini dans ce module

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Dessin du fond avec canvas
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Fond blanc
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Création des boutons
        calendar_button = CustomButton(
            text="Calendrier",
            font_size=24,
            size_hint=(None, None),
            size=(300, 100),
            background_normal='',
            background_color=(0, 0.5, 1, 1)
        )
        news_feed_button = CustomButton(
            text="Fil d'Actualité",
            font_size=24,
            size_hint=(None, None),
            size=(300, 100),
            background_normal='',
            background_color=(0, 0.5, 1, 1)
        )
        pronote_button = CustomButton(
            text="Pronote",
            font_size=24,
            size_hint=(None, None),
            size=(300, 100),
            background_normal='',
            background_color=(0, 0.5, 1, 1)
        )
        rappels_button = CustomButton(
            text="Rappels",
            font_size=24,
            size_hint=(None, None),
            size=(300, 100),
            background_normal='',
            background_color=(0, 0.5, 1, 1)
        )

        # Lier les boutons aux fonctions de navigation
        calendar_button.bind(on_press=self.goto_calendar)
        news_feed_button.bind(on_press=self.goto_news_feed)
        pronote_button.bind(on_press=self.goto_pronote)
        rappels_button.bind(on_press=self.goto_rappels)

        # Création de la grille pour les boutons
        button_grid = GridLayout(cols=2, spacing=20, padding=50)

        # Ajout des widgets au layout
        layout.add_widget(Widget(size_hint_y=1))  # Espace vide en haut
        layout.add_widget(button_grid)
        layout.add_widget(Widget(size_hint_y=0.5))  # Espace en bas

        # Ajout des boutons à la grille
        button_grid.add_widget(calendar_button)
        button_grid.add_widget(pronote_button)
        button_grid.add_widget(news_feed_button)
        button_grid.add_widget(rappels_button)

        # Ajout du layout à l'écran
        self.add_widget(layout)

    def goto_calendar(self, instance):
        self.manager.current = 'calendar'

    def goto_news_feed(self, instance):
        self.manager.current = 'news_feed'

    def goto_pronote(self, instance):
        self.manager.current = 'pronote'

    def goto_rappels(self, instance):
        self.manager.current = 'rappels'

    def update_rect(self, *args):
        # Mettre à jour la taille et la position du rectangle
        self.rect.size = self.size
        self.rect.pos = self.pos
