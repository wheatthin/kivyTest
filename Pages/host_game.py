import asyncio
import websockets
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class HostGame(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'host_game'

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
            text="Host Game",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        self.box_layout.add_widget(self.title_label)
        self.username_input = TextInput(
            hint_text="Username",
            size_hint=(1, None),
            height=80,  # Fixed height
            font_size='24sp',
            halign='center',
            padding_y=(10, 10)
        )
        self.username_input.bind(text=self.on_text)
        self.box_layout.add_widget(self.username_input)

        self.match_id_input = TextInput(
            hint_text="Match ID",
            size_hint=(1, None),
            height=80,  # Fixed height
            font_size='24sp',
            halign='center',
            padding_y=(10, 10)
        )
        self.match_id_input.bind(text=self.on_text)
        self.box_layout.add_widget(self.match_id_input)

        self.box_layout.add_widget(Button(
            text="Start Game",
            size_hint=(1, 0.2),
            on_press=self.start_game
        ))
        self.box_layout.add_widget(Button(
            text="Back",
            size_hint=(1, 0.2),
            on_press=self.back_to_main
        ))

        # Add BoxLayout to AnchorLayout
        self.add_widget(self.box_layout)

    def on_text(self, instance, value):
        if len(value) > 15:
            instance.text = value[:15]

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_pre_enter(self, *args):
        self.username_input.text = ''
        self.match_id_input.text = ''

    def back_to_main(self, instance):
        self.manager.current = 'main_menu'

    async def send_create_game(self, username, match_id):
        print(f"testing1")
        try:
            async with websockets.connect("ws://localhost:8765") as websocket:
                print(f"Connected to WebSocket server")
                message = json.dumps({"action": "create_game", "username": username, "match_id": match_id})
                await websocket.send(message)
                print(f"Sent: {message}")
                response = await websocket.recv()
                print(f"Received: {response}")
        except Exception as e:
            print(f"Error in send_create_game: {e}")

    def start_game(self, instance):
        username = self.username_input.text
        match_id = self.match_id_input.text
        if username and match_id:
            # Only schedule sending the create game message
            Clock.schedule_once(lambda dt: asyncio.run(self.send_create_game(username, match_id)))
            self.manager.get_screen('lobby').add_player(username, match_id)  # Update lobby only
            self.manager.current = 'lobby'

    def update_font_size(self, font_size):
        self.title_label.font_size = font_size
        self.username_input.font_size = font_size
        self.username_input.height = 80  # Fixed height
        self.match_id_input.font_size = font_size
        self.match_id_input.height = 80  # Fixed height
        for child in self.box_layout.children:
            if isinstance(child, Button):
                child.font_size = font_size