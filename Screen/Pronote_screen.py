from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.scrollview import ScrollView, DampedScrollEffect
from kivy.uix.floatlayout import FloatLayout
import json
from Custom_interface import CustomButton
from Parametres import *



# Couleurs associées aux statuts des devoirs
homework_status_colors = {
    "Fait": "#008000",    # Vert
    "Non Fait": "#FF0000"   # Rouge
}

# =========================
# Fonctions et Widgets Personnalisés
# =========================

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i+lv//3], 16)/255 for i in range(0, lv, lv//3))

class ColorCircle(Widget):
    def __init__(self, hex_color, **kwargs):
        super(ColorCircle, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (CIRCLE_DIAMETER, CIRCLE_DIAMETER)
        self.hex_color = hex_color
        self.rgb = hex_to_rgb(hex_color)
        with self.canvas:
            Color(*self.rgb)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self.update_circle, size=self.update_circle)
    def update_circle(self, *args):
        self.circle.pos = self.pos
        self.circle.size = self.size

class PlusColorCircle(FloatLayout):
    def __init__(self, hex_color, **kwargs):
        super(PlusColorCircle, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (CIRCLE_DIAMETER, CIRCLE_DIAMETER)
        self.circle = ColorCircle(hex_color)
        self.add_widget(self.circle)
        self.plus_label = Label(text="+", font_size=PLUS_FONT_SIZE, color=(1,1,1,1),
                                size_hint=(None, None), size=(CIRCLE_DIAMETER, CIRCLE_DIAMETER),
                                halign='center', valign='middle')
        self.plus_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        self.add_widget(self.plus_label)

class SeparatorLine(Widget):
    def __init__(self, **kwargs):
        super(SeparatorLine, self).__init__(**kwargs)
        self.size_hint_y = None
        self.height = LINE_HEIGHT
        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# =========================
# Chargement des Données JSON
# =========================
with open("C:/Users/Ethan/Desktop/Maison/python/App/donnés/extracted_data.json", "r", encoding="utf8") as file:
    data = json.load(file)
homework_data = data.get("homework", [])
notes_data = data.get("notes", [])

# =========================
# Classes de l'Application
# =========================

class PronoteScreen(Screen):
    def __init__(self, **kwargs):
        super(PronoteScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        back_button = CustomButton(
            text="Retour",
            font_size=30,
            size_hint=(None, None),
            size=(112.5, 75),
            pos_hint={'top': 0.95, 'right': 0.95}
        )
        back_button.bind(on_press=self.goto_home)
        title_label = Label(
            text="Pronote",
            font_size=80,
            size_hint=(None, None),
            size=(600, 200),
            text_size=(600, None),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)
        )
        title_label.pos_hint = {'x': 0.12, 'y': 0.77}
        separator = Widget(size_hint=(None, None), size=(Window.width, LINE_HEIGHT), pos_hint={'x': 0, 'y': 0.85})
        with separator.canvas:
            Color(0, 0, 0, 1)
            self.sep_rect = Rectangle(pos=separator.pos, size=separator.size)
        separator.bind(pos=self.update_sep, size=self.update_sep)
        main_widget = MainWidget()
        layout.add_widget(back_button)
        layout.add_widget(title_label)
        layout.add_widget(separator)
        layout.add_widget(main_widget)
        self.add_widget(layout)
    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
    def update_sep(self, instance, value):
        self.sep_rect.pos = instance.pos
        self.sep_rect.size = instance.size
    def goto_home(self, instance):
        self.manager.current = 'home'

class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = BOX_SPACING
        self.padding = BOX_PADDING

        # ----------------------------
        # ScrollView pour les devoirs (groupés par date)
        # ----------------------------
        scrollview_left = ScrollView(
            size_hint=(None, None),
            size=(Window.width * SCROLLVIEW_LEFT_WIDTH_RATIO, SCROLLVIEW_HEIGHT),
            pos_hint={'x': 0.05, 'top': 0.85},
            do_scroll_x=False
        )
        box_layout_left = BoxLayout(
            orientation='vertical',
            padding=(BOX_PADDING, BOX_PADDING, BOX_PADDING, BOX_PADDING),
            spacing=5,
            size_hint_y=None
        )
        box_layout_left.bind(minimum_height=box_layout_left.setter('height'))

        # Regroupement des devoirs par date
        ordered_grouped_homework = {}
        for hw in homework_data:
            date_str = hw.get("date", "").strip()
            if date_str == "":
                date_str = "Date inconnue"
            # Correction "Pourdemain" → "Pour demain"
            if date_str.lower().startswith("pour") and len(date_str) > 4 and date_str[4] != " ":
                date_str = "Pour " + date_str[4:]
            ordered_grouped_homework.setdefault(date_str, []).append(hw)

        # Pour chaque groupe, affichage de la date et des devoirs
        for date_str, hw_list in ordered_grouped_homework.items():
            # Affichage de la date en gras
            date_label = Label(
                text=f"[b]{date_str}[/b]",
                markup=True,
                font_size=18,
                color=(0, 0, 0, 1),
                size_hint_y=None
            )
            # Laisser le label calculer sa hauteur
            date_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
            date_label.halign = 'left'
            date_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
            box_layout_left.add_widget(date_label)

            # Pour chaque devoir du groupe, création d'une ligne horizontale
            for hw in hw_list:
                # Créer un layout horizontal pour la ligne
                homework_line = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    spacing=5
                )
                # Layout vertical pour le texte (matière et description)
                text_layout = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None
                )
                text_layout.bind(minimum_height=text_layout.setter('height'))
                subject = hw.get("subject", "Inconnu")
                description = hw.get("description", "Aucune description")
                if ":" in description:
                    description = description.split(":", 1)[1].strip()
                subject_label = Label(
                    text=f"[b]{subject}[/b]",
                    markup=True,
                    font_size=14,
                    color=(0, 0, 0, 1),
                    halign='left',
                    size_hint_y=None
                )
                subject_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
                subject_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
                description_label = Label(
                    text=description,
                    font_size=12,
                    color=(0, 0, 0, 1),
                    halign='left',
                    size_hint_y=None
                )
                description_label.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1]))
                description_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
                text_layout.add_widget(subject_label)
                text_layout.add_widget(description_label)
                homework_line.add_widget(text_layout)

                # Ajout du cercle de statut
                status = hw.get("status", "")
                circle_color = homework_status_colors.get(status, "#808080")
                circle = ColorCircle(circle_color)
                homework_line.add_widget(circle)

                # Une fois les enfants ajoutés, ajuster la hauteur de la ligne
                def update_line_height(instance, value):
                    # Hauteur égale à la hauteur du text_layout + une marge
                    homework_line.height = text_layout.height if text_layout.height > CIRCLE_DIAMETER else CIRCLE_DIAMETER
                    homework_line.height += ADDITIONAL_LINE_MARGIN
                text_layout.bind(height=update_line_height)
                update_line_height(None, None)
                box_layout_left.add_widget(homework_line)
            # Espace entre les groupes
            box_layout_left.add_widget(Widget(size_hint_y=None, height=5))
        scrollview_left.add_widget(box_layout_left)

        # ----------------------------
        # ScrollView pour les notes
        # ----------------------------
        scrollview_right = ScrollView(
            size_hint=(None, None),
            size=(Window.width * SCROLLVIEW_RIGHT_WIDTH_RATIO, SCROLLVIEW_HEIGHT),
            pos_hint={'right': 0.95, 'top': 0.85},
            do_scroll_x=False,
            effect_cls=DampedScrollEffect
        )
        box_layout_right = BoxLayout(
            orientation='vertical',
            padding=(BOX_PADDING, BOX_PADDING, BOX_PADDING, BOX_PADDING),
            spacing=BOX_SPACING,
            size_hint_y=None
        )
        box_layout_right.bind(minimum_height=box_layout_right.setter('height'))
        for idx, note in enumerate(notes_data):
            course_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=NOTE_BOX_HEIGHT,
                padding=(10, 10, 10, 10),
                spacing=10
            )
            date_label = Label(
                text=note.get("date", "Date inconnue"),
                font_size=18,
                bold=True,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=LABEL_HEIGHT_DATE
            )
            date_label.halign = 'left'
            date_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
            course_layout.add_widget(date_label)
            subject_label = Label(
                text=note.get("subject", "Matière inconnue"),
                font_size=16,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=LABEL_HEIGHT_SUBJECT
            )
            subject_label.halign = 'left'
            subject_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
            course_layout.add_widget(subject_label)
            evaluations = note.get("evaluations", [])
            for evaluation in evaluations:
                eval_layout = BoxLayout(
                    orientation='horizontal',
                    size_hint_y=None,
                    height=EVAL_HEIGHT,
                    spacing=10
                )
                eval_text = evaluation.get("title", "")
                if ":" in eval_text:
                    eval_text = eval_text.split(":", 1)[1].strip()
                eval_suffix = evaluation.get("text", "").strip()
                if eval_suffix != "+":
                    eval_text += " " + eval_suffix
                color_code = evaluation.get("color", "")
                if color_code:
                    if eval_suffix == "+":
                        circle_widget = PlusColorCircle(color_code)
                    else:
                        circle_widget = ColorCircle(color_code)
                    eval_layout.add_widget(circle_widget)
                eval_label = Label(
                    text=eval_text,
                    font_size=14,
                    color=(0, 0, 0, 1),
                    size_hint_y=None,
                    height=EVAL_HEIGHT
                )
                eval_label.halign = 'left'
                eval_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
                eval_layout.add_widget(eval_label)
                course_layout.add_widget(eval_layout)
            box_layout_right.add_widget(course_layout)
            if idx != len(notes_data) - 1:
                box_layout_right.add_widget(SeparatorLine())
        scrollview_right.add_widget(box_layout_right)

        self.add_widget(scrollview_left)
        self.add_widget(scrollview_right)


