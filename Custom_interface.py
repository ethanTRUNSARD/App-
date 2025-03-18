

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal=''
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)

        with self.canvas.before:
            Color(0, 0.5, 1, 1)
            self.rounded_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

        self.bind(size=self.update_rounded_rect, pos=self.update_rounded_rect)


    def update_rounded_rect(self, *args):
        self.rounded_rect.size = self.size
        self.rounded_rect.pos = self.pos

class TimeWheel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 8  # Heure initiale
        self.size = (200, 100)  # Taille du widget

        with self.canvas.before:
            Color(1, 1, 1, 1)  # Fond blanc
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Texte de l'heure au centre
        self.label = Label(text=f'{self.time}:00', size_hint=(None, None), size=(200, 50), pos=self.center)
        self.add_widget(self.label)

        # Bind du mouvement de la molette de la souris pour faire défiler l'heure
        self.bind(on_touch_move=self.scroll_wheel)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.label.center = self.center

    def scroll_wheel(self, instance, touch):
        if self.collide_point(touch.x, touch.y):
            if touch.dy > 0:  # Si on fait défiler vers le bas
                self.time = (self.time + 1) % 24  # Incrémente l'heure (et retourne à 0 après 23)
            elif touch.dy < 0:  # Si on fait défiler vers le haut
                self.time = (self.time - 1) % 24  # Décrémente l'heure (et revient à 23 avant 0)
            self.label.text = f'{self.time}:00'
            return True
        return False


class PopupMakeRappels(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Créer un rappel"
        self.size_hint = (None, None)
        self.size = (400, 350)
        self.auto_dismiss = False  # Empêche la fermeture accidentelle en cliquant en dehors

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Fond blanc et bords arrondis
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Fond blanc
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Champ pour entrer l'heure avec le TimeWheel (roue)
        self.time_wheel = TimeWheel()
        layout.add_widget(self.time_wheel)

        # Champ pour entrer la description du rappel
        description_label = Label(text="Description", size_hint_y=None, height=30, color=(0, 0, 1, 1))
        layout.add_widget(description_label)

        self.description_input = TextInput(
            multiline=True, hint_text="Entrez la description ici...",
            size_hint_y=None, height=100, padding=[10, 10], background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 1, 1)
        )
        layout.add_widget(self.description_input)

        # Bouton de sauvegarde
        save_button = Button(text="Sauvegarder", size_hint_y=None, height=50, background_normal='',
                             background_color=(0, 0, 1, 1))
        save_button.bind(on_press=self.save_rappel)
        layout.add_widget(save_button)

        # Bouton de fermeture
        close_button = Button(text="Fermer", size_hint_y=None, height=50, background_normal='',
                              background_color=(0.9, 0.9, 0.9, 1))
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)

        self.content = layout

    def save_rappel(self, instance):
        time = f"{self.time_wheel.time}:00"
        description = self.description_input.text
        print(f"Rappel enregistré - Heure: {time}, Description: {description}")
        self.dismiss()

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Bouton pour ouvrir le pop-up
        open_popup_button = Button(text="Créer un rappel", size_hint=(None, None), size=(200, 50),
                                   background_normal='', background_color=(0, 0, 1, 1), font_size=18)
        open_popup_button.bind(on_press=self.open_popup)

        main_layout.add_widget(open_popup_button)

        return main_layout

    def open_popup(self, instance):
        popup = PopupMakeRappels()
        popup.open()


# Pour exécuter l'application
if __name__ == "__main__":
    MainApp().run()

