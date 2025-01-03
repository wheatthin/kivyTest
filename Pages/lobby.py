import asyncio
import websockets
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

class Lobby(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'lobby'
        self.players = []

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
        self.match_id_label = Label(
            text="Match ID: ",
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        self.box_layout.add_widget(self.match_id_label)

        self.players_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.6)
        )
        self.box_layout.add_widget(self.players_box)

        self.box_layout.add_widget(Button(
            text="Back",
            size_hint=(1, 0.2),
            on_press=self.back_to_main
        ))

        # Add BoxLayout to AnchorLayout
        self.add_widget(self.box_layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def add_player(self, username, match_id):
        self.match_id_label.text = f"Match ID: {match_id}"
        self.players.append(username)
        self.update_players_list()
        Clock.schedule_once(lambda dt: asyncio.run(self.receive_updates(match_id)))

    def update_players_list(self):
        self.players_box.clear_widgets()
        for player in self.players:
            self.players_box.add_widget(Label(
                text=player,
                font_size="20sp",
                color=(1, 1, 1, 1),
                size_hint=(1, None),
                height=30
            ))

    def back_to_main(self, instance):
        self.manager.current = 'main_menu'

    async def receive_updates(self, match_id):
        async with websockets.connect("ws://localhost:8765") as websocket:
            async for message in websocket:
                data = json.loads(message)
                if data.get("action") == "update_lobby" and data.get("match_id") == match_id:
                    self.players = data["players"]
                    self.update_players_list()