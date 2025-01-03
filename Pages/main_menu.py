from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main_menu'

        # Background Color
        with self.canvas.before:
            Color(0.1, 0.2, 0.5, 1)  # Dark blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Centered Box Layout
        self.box_layout = BoxLayout(
            orientation="vertical",
            size_hint=(0.6, 0.6),  # Centralized smaller box
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Add Widgets
        self.title_label = Label(
            text="Welcome to Bohnanza!",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        self.box_layout.add_widget(self.title_label)
        self.box_layout.add_widget(Button(
            text="Host Game",
            size_hint=(1, 0.2),
            on_press=self.host_game
        ))
        self.box_layout.add_widget(Button(
            text="Join Game",
            size_hint=(1, 0.2),
            on_press=self.join_game
        ))
        self.box_layout.add_widget(Button(
            text="Settings",
            size_hint=(1, 0.2),
            on_press=self.settings
        ))

        # Add BoxLayout to AnchorLayout
        self.add_widget(self.box_layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def host_game(self, instance):
        self.manager.current = 'host_game'

    def join_game(self, instance):
        self.manager.current = 'join_game'

    def settings(self, instance):
        self.manager.current = 'settings'

    def update_font_size(self, font_size):
        self.title_label.font_size = font_size
        for child in self.box_layout.children:
            if isinstance(child, Button):
                child.font_size = font_size