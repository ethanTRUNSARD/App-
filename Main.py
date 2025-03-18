from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

from Screen.Home_screen import HomeScreen
from Screen.Rappels_screen import RappelsScreen
from Screen.Pronote_screen import PronoteScreen
from Screen.Calendar_screen import CalendarScreen
from Screen.News_screen import NewsFeedScreen

class MainApp(App):
    def build(self):
        Window.clearcolor =(1, 1, 1, 1)
        # Création du gestionnaire de screens
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(NewsFeedScreen(name='news_feed'))
        sm.add_widget(RappelsScreen(name='rappels'))
        sm.add_widget(PronoteScreen(name='pronote'))
        return sm


if __name__ == '__main__':
    MainApp().run()


