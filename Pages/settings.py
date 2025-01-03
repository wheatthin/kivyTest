from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

class Settings(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'

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
            text="Settings",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        self.box_layout.add_widget(self.title_label)

        # Dropdown for font size
        self.font_size_label = Label(
            text="Font Size",
            font_size="18sp",
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        self.box_layout.add_widget(self.font_size_label)

        self.font_size_dropdown = DropDown()
        for size in ["Small", "Medium", "Large"]:
            btn = Button(text=size, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.font_size_dropdown.select(btn.text))
            self.font_size_dropdown.add_widget(btn)

        self.font_size_main_button = Button(text='Select Font Size', size_hint=(1, 0.2))
        self.font_size_main_button.bind(on_release=self.font_size_dropdown.open)
        self.font_size_dropdown.bind(on_select=self.set_font_size)
        self.box_layout.add_widget(self.font_size_main_button)

        self.box_layout.add_widget(Button(
            text="Back",
            size_hint=(1, 0.2),
            on_press=self.back_to_main
        ))

        # Add BoxLayout to AnchorLayout
        self.add_widget(self.box_layout)

    def set_font_size(self, instance, size):
        font_size_map = {
            "Small": "24sp",
            "Medium": "32sp",
            "Large": "40sp"
        }
        font_size = font_size_map.get(size, "24sp")
        self.manager.get_screen('main_menu').update_font_size(font_size)
        self.manager.get_screen('host_game').update_font_size(font_size)
        self.manager.get_screen('join_game').update_font_size(font_size)
        self.update_font_size(font_size)

    def update_font_size(self, font_size):
        self.title_label.font_size = font_size
        self.font_size_label.font_size = font_size
        self.font_size_main_button.font_size = font_size
        for child in self.box_layout.children:
            if isinstance(child, Button) and child.text != 'Select Font Size':
                child.font_size = font_size

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def back_to_main(self, instance):
        self.manager.current = 'main_menu'