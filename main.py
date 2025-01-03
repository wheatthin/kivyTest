from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Pages.main_menu import MainMenu
from Pages.host_game import HostGame
from Pages.join_game import JoinGame
from Pages.settings import Settings
from Pages.lobby import Lobby

class BohnanzaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(HostGame(name='host_game'))
        sm.add_widget(JoinGame(name='join_game'))
        sm.add_widget(Settings(name='settings'))
        sm.add_widget(Lobby(name='lobby'))
        return sm

if __name__ == "__main__":
    BohnanzaApp().run()