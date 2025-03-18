from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from datetime import datetime, timedelta
from Parametres import *
from Custom_interface import CustomButton
from kivy.clock import Clock


# --- La classe RappelsScreen reste inchangée ---
class RappelsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanc
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Bouton retour en haut
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
            text="Rappels",
            font_size=80,
            size_hint=(None, None),
            size=(600, 200),
            text_size=(600, None),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        label.pos_hint = {'x': 0.12, 'y': 0.77}

        # Ligne de séparation
        separator = Widget(size_hint=(None, None), size=(Window.width, 2.5), pos_hint={'x': 0, 'y': 0.85})
        with separator.canvas:
            Color(0, 0, 0, 1)
            self.sep_rect = Rectangle(pos=separator.pos, size=separator.size)
        separator.bind(pos=self.update_sep, size=self.update_sep)

        make_rappels = MakeRappels()

        layout.add_widget(back_button)
        layout.add_widget(label)
        layout.add_widget(separator)
        layout.add_widget(make_rappels)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_sep(self, instance, value):
        self.sep_rect.pos = instance.pos
        self.sep_rect.size = instance.size

    def goto_home(self, instance):
        self.manager.current = 'home'


from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from datetime import datetime, timedelta
from Parametres import *
from Custom_interface import CustomButton
from kivy.clock import Clock


# --- La classe RappelsScreen reste inchangée ---
class RappelsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Blanc
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Bouton retour en haut
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
            text="Rappels",
            font_size=80,
            size_hint=(None, None),
            size=(600, 200),
            text_size=(600, None),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        label.pos_hint = {'x': 0.12, 'y': 0.77}

        # Ligne de séparation
        separator = Widget(size_hint=(None, None), size=(Window.width, 2.5), pos_hint={'x': 0, 'y': 0.85})
        with separator.canvas:
            Color(0, 0, 0, 1)
            self.sep_rect = Rectangle(pos=separator.pos, size=separator.size)
        separator.bind(pos=self.update_sep, size=self.update_sep)

        make_rappels = MakeRappels()

        layout.add_widget(back_button)
        layout.add_widget(label)
        layout.add_widget(separator)
        layout.add_widget(make_rappels)

        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_sep(self, instance, value):
        self.sep_rect.pos = instance.pos
        self.sep_rect.size = instance.size

    def goto_home(self, instance):
        self.manager.current = 'home'


class MakeRappels(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout(size_hint=(1, 1))

        # Création du ScrollView centré et avec largeur réduite à 300
        scroll_view = ScrollView(size_hint=(None, None),
                                 width=300,
                                 height=Window.height * 0.85,
                                 pos_hint={"center_x": 0.2, "y": -0.01})

        # Conteneur GridLayout à 1 colonne, dont la hauteur s'ajuste au contenu
        container = GridLayout(cols=1,
                               size_hint_y=None,
                               spacing=10)
        container.bind(minimum_height=container.setter('height'))

        # Liste des présidents
        presidents = [
            ("George Washington", "57", "22 février 1732", "George Washington Jr., John Washington"),
            ("Abraham Lincoln", "56", "12 février 1809", "Robert Todd Lincoln, Edward Baker Lincoln"),
            ("Theodore Roosevelt", "60", "27 octobre 1858", "Alice Roosevelt Longworth, Theodore Roosevelt Jr."),
            ("Franklin D. Roosevelt", "63", "30 janvier 1882", "Anna Roosevelt, James Roosevelt II, Elliott Roosevelt"),
            ("John F. Kennedy", "46", "29 mai 1917", "Caroline Kennedy, John F. Kennedy Jr.")
        ]

        now = datetime.now()  # Heure actuelle
        self.reminders = []  # Liste pour stocker les rappels

        # Création des rappels
        for i in range(15):
            reminder_time = now + timedelta(minutes=i * 15)  # Calcul de l'heure du rappel
            time_str = reminder_time.strftime("%H:%M")  # Formatage de l'heure en HH:MM

            # Calcul du minutage (compte à rebours)
            delta = reminder_time - now
            hours = delta.seconds // 3600  # Nombre d'heures restantes
            minutes = (delta.seconds % 3600) // 60  # Nombre de minutes restantes
            seconds = delta.seconds % 60  # Reste des secondes

            # Formatage de l'heure
            if hours == 0:
                if minutes == 0:
                    countdown = f"{seconds:02d}"  # Si 0h et 0m, afficher uniquement les secondes
                else:
                    countdown = f"{minutes:02d}:{seconds:02d}"  # Si 0h, afficher minutes et secondes
            else:
                countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"  # Afficher heures, minutes et secondes

            # Sélection d'un président (en alternance)
            president = presidents[i % len(presidents)]

            # Description complète
            desc_full = f"Nom: {president[0]}, Âge: {president[1]}, Naissance: {president[2]}, Enfants: {president[3]}"

            # Troncature de la description (50 caractères maximum)
            max_chars = 50
            if len(desc_full) > max_chars:
                desc = desc_full[:max_chars] + "..."
            else:
                desc = desc_full

            # Texte final du rappel
            reminder_text = f"{time_str} - Minuteur: {countdown}\n{desc}"
            reminder_button = Button(
                text=reminder_text,
                size_hint=(None, None),
                width=300,  # Largeur des boutons
                height=120,
                halign='left',
                valign='middle'
            )
            # Pour gérer le texte et l'assurer qu'il soit bien tronqué si nécessaire
            reminder_button.text_size = (reminder_button.width - 20, None)
            container.add_widget(reminder_button)
            self.reminders.append((reminder_button, reminder_time))

        scroll_view.add_widget(container)
        layout.add_widget(scroll_view)

        # Bouton pour ajouter un nouveau rappel
        add_reminder_button = Button(
            text="Ajouter un rappel",
            size_hint=(None, None),
            size=(470, 50),
            pos_hint={"center_x": 0.693, "y": 0.02}
        )
        # Correction ici - lier directement à open_add_reminder_popup au lieu de add_reminder
        add_reminder_button.bind(on_press=self.open_add_reminder_popup)
        layout.add_widget(add_reminder_button)

        self.add_widget(layout)

        # Lancer l'intervalle pour mettre à jour les rappels chaque seconde
        Clock.schedule_interval(self.update_reminders, 1)

    def update_reminders(self, *args):
        now = datetime.now()  # Obtenir l'heure actuelle
        for btn, reminder_time in self.reminders:
            # Calcul du minutage (compte à rebours)
            delta = reminder_time - now
            if delta.total_seconds() <= 0:
                # Le temps est écoulé
                btn.text = "Temps écoulé!"
                continue

            hours = delta.seconds // 3600  # Nombre d'heures restantes
            minutes = (delta.seconds % 3600) // 60  # Nombre de minutes restantes
            seconds = delta.seconds % 60  # Reste des secondes

            # Formatage de l'heure
            if hours == 0:
                if minutes == 0:
                    countdown = f"{seconds:02d}"  # Si 0h et 0m, afficher uniquement les secondes
                else:
                    countdown = f"{minutes:02d}:{seconds:02d}"  # Si 0h, afficher minutes et secondes
            else:
                countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"  # Afficher heures, minutes et secondes

            # Mise à jour du texte du bouton
            original_text = btn.text.split("\n")
            if len(original_text) > 1:
                btn.text = f"{original_text[0].split(' - ')[0]} - Minuteur: {countdown}\n{original_text[1]}"
            else:
                btn.text = f"Minuteur: {countdown}"

    # La méthode add_reminder est conservée mais modifiée pour l'ajout direct sans popup
    def add_reminder(self, time_str, description):
        """ Ajoute un rappel avec l'heure et la description entrées """
        # Analyser l'heure
        try:
            hour, minute = map(int, time_str.split(':'))
            now = datetime.now()
            reminder_time = datetime(now.year, now.month, now.day, hour, minute)

            # Si l'heure est déjà passée pour aujourd'hui, ajouter un jour
            if reminder_time < now:
                reminder_time += timedelta(days=1)

            # Calcul du compte à rebours
            delta = reminder_time - now
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            seconds = delta.seconds % 60

            if hours == 0:
                if minutes == 0:
                    countdown = f"{seconds:02d}"
                else:
                    countdown = f"{minutes:02d}:{seconds:02d}"
            else:
                countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            # Créer le bouton du rappel
            reminder_text = f"{time_str} - Minuteur: {countdown}\n{description}"
            reminder_button = Button(
                text=reminder_text,
                size_hint=(None, None),
                width=300,
                height=120,
                halign='left',
                valign='middle'
            )
            reminder_button.text_size = (reminder_button.width - 20, None)

            # Récupérer le GridLayout contenu dans le ScrollView
            grid_layout = self.children[0].children[-1].children[0]
            grid_layout.add_widget(reminder_button)

            # Ajouter le rappel à la liste des rappels
            self.reminders.append((reminder_button, reminder_time))

            return True
        except (ValueError, IndexError):
            return False

    def open_add_reminder_popup(self, instance):
        """ Ouvre le popup pour ajouter un rappel """
        # Passer self en tant que paramètre parent_screen et non pas parent
        popup = AddReminderPopup(parent_screen=self)
        popup.open()


class AddReminderPopup(Popup):
    def __init__(self, parent=None, **kwargs):
        # Assurez-vous que parent n'est pas passé en tant que parent widget
        # mais plutôt comme une référence à utiliser plus tard
        if 'parent' in kwargs:
            del kwargs['parent']

        super().__init__(**kwargs)
        self.title = "Ajouter un rappel"
        self.size_hint = (0.8, 0.6)
        self.parent_screen = parent

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Champ pour entrer l'heure
        self.time_input = TextInput(hint_text="Entrez l'heure (HH:MM)", size_hint=(1, None), height=40)

        # Champ pour la description
        self.desc_input = TextInput(hint_text="Entrez la description", size_hint=(1, None), height=40)

        # Bouton pour ajouter le rappel
        add_button = Button(text="Ajouter", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        add_button.bind(on_press=self.add_reminder)

        layout.add_widget(Label(text="Heure:"))
        layout.add_widget(self.time_input)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.desc_input)
        layout.add_widget(add_button)

        self.content = layout

    def add_reminder(self, instance):
        """ Ajoute un rappel avec l'heure et la description entrées """
        time_str = self.time_input.text
        description = self.desc_input.text

        # Validation simple du format de l'heure (HH:MM)
        import re
        if not re.match(r'^\d{1,2}:\d{2}$', time_str):
            self.time_input.text = "Format incorrect, veuillez entrer HH:MM"
            return

        # Ajouter le rappel en utilisant la méthode de la classe parente
        if self.parent_screen:
            success = self.parent_screen.add_reminder(time_str, description)

            if success:
                self.dismiss()  # Fermer le popup après l'ajout
            else:
                self.time_input.text = "Format incorrect, veuillez entrer HH:MM"
        else:
            self.dismiss()  # Fermer le popup si pas de parent_screen

    def add_reminder(self, instance):
        """ Ajoute un rappel avec l'heure et la description entrées """
        time_str = self.time_input.text
        description = self.desc_input.text

        # Validation simple du format de l'heure (HH:MM)
        import re
        if not re.match(r'^\d{1,2}:\d{2}$', time_str):
            self.time_input.text = "Format incorrect, veuillez entrer HH:MM"
            return

        # Ajouter le rappel en utilisant la méthode de la classe parente
        success = self.parent_screen.add_reminder(time_str, description)

        if success:
            self.dismiss()  # Fermer le popup après l'ajout
        else:
            self.time_input.text = "Format incorrect, veuillez entrer HH:MM"


class AddReminderPopup(Popup):
    def __init__(self, **kwargs):
        # Extraire parent_screen avant d'appeler super().__init__
        self.parent_screen = kwargs.pop('parent_screen', None)

        # Maintenant on peut appeler super().__init__ sans le paramètre non reconnu
        super().__init__(**kwargs)

        self.title = "Ajouter un rappel"
        self.size_hint = (0.8, 0.6)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Champ pour entrer l'heure
        self.time_input = TextInput(hint_text="Entrez l'heure (HH:MM)", size_hint=(1, None), height=40)

        # Champ pour la description
        self.desc_input = TextInput(hint_text="Entrez la description", size_hint=(1, None), height=40)

        # Bouton pour ajouter le rappel
        add_button = Button(text="Ajouter", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        add_button.bind(on_press=self.add_reminder)

        layout.add_widget(Label(text="Heure:"))
        layout.add_widget(self.time_input)
        layout.add_widget(Label(text="Description:"))
        layout.add_widget(self.desc_input)
        layout.add_widget(add_button)

        self.content = layout

    def add_reminder(self, instance):
        """ Ajoute un rappel avec l'heure et la description entrées """
        time_str = self.time_input.text
        description = self.desc_input.text

        # Validation simple du format de l'heure (HH:MM)
        import re
        if not re.match(r'^\d{1,2}:\d{2}$', time_str):
            self.time_input.text = "Format incorrect, veuillez entrer HH:MM"
            return

        # Ajouter le rappel en utilisant la méthode de la classe parente
        if self.parent_screen:
            success = self.parent_screen.add_reminder(time_str, description)

            if success:
                self.dismiss()  # Fermer le popup après l'ajout
            else:
                self.time_input.text = "Format incorrect, veuillez entrer HH:MM"
        else:
            self.dismiss()  # Fermer le popup si pas de parent_screen