from __future__ import annotations

from functools import partial
from pathlib import Path

from rich.syntax import Syntax
from rich.text import Text

from textual.app import App, ComposeResult
from textual.command import Hit, Hits, Provider
from textual.containers import VerticalScroll, Grid
from textual.widgets import Static, Footer, Header, Input, Label, Button, LoadingIndicator
from textual.screen import Screen, ModalScreen
from textual.worker import Worker, get_current_worker
from textual import work
import requests
from urllib.request import Request , urlopen, HTTPError
from urllib.error import URLError
import base64
import json
from config import Config
import os
from credentials import credentials
from textual.timer import Timer
from textual import on

class QuitScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )
    def on_button_press(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)

# COMMANDS
class PlaySong(Provider):
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, NiftyhoGramofonUI)
        command = f"play"
        score = matcher.match(command)
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(command),
                partial(app.playsong),
                help=f"Plays a song by the id provided",
            )
class Playsound(Provider):
    async def search(self, query: str) -> Hits:  
        matcher = self.matcher(query)  

        app = self.app
        assert isinstance(app, NiftyhoGramofonUI)
        command = f"playtest"
        score = matcher.match(command)  
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(command),  
                partial(app.do_something),
                help="Plays a test sound",
            )
class RefreshMusic(Provider):
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, NiftyhoGramofonUI)
        command = f"refresh"
        score = matcher.match(command)
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(command),
                partial(app.update_music),
                help="Refreshes a song"
            )

# SCREENS
class MainScreen(Screen):
    def compose(self) -> MainScreen:
        yield Label("Main Screen")
        yield Header()
        yield Footer()

class SongSearchScreen(Screen):
    BINDINGS = [
        ("a", "switch_mode('main')", "Main"),
        ("d", "change_theme", "Change Theme"),
        ("q", "quit", "Quit"),
    ]
    def compose(self) -> SongSearchScreen:
        yield Input(placeholder="Type a song you want to play")
        yield Footer()
    def action_change_theme(self):
        self.dark = not self.dark

# MAIN APP
class NiftyhoGramofonUI(App):
    BINDINGS = [
        ("d", "change_theme", "Change Theme"),
        ("q", "quit", "Quit"),
        ("s", "stop_audio", "Stop Audio"),
        ("r", "pause_audio", "Pause Audio"),
        ("t", "unpause_audio", "Unpause Audio"),
    ]
    COMMANDS = App.COMMANDS | {Playsound} | {PlaySong} | {RefreshMusic}
    MODES = {
        "main": MainScreen,
        "songmenu": SongSearchScreen,
    }
    CSS_PATH = "main.css"
    paused = False
    @on(Button.Pressed, "#pause")
    def on_button_pressed(self, event: Button.Pressed):
        self.add_class("paused")
        if event.button.id == "pause":
            if self.paused == False:
                self.action_pause_audio()
                event.button.variant = "error"
                #event.button.border_title = "Unpause"
                event.button.label = "Unpause"
                self.paused = True
            else:
                self.action_unpause_audio()
                event.button.variant = "primary"
                event.button.label = "Pause"
                self.paused = False
    def compose(self) -> ComposeResult:
        self.notify("The credentials aren't encrypted", title="Warning", severity="warning", timeout=6.9)
        yield Header()
        yield Footer()
        self.channelJoined = Static("🟢Operational", id="status")
        yield self.channelJoined
        self.widget = Static("Refreshing", id="now_playing")
        yield self.widget
        with VerticalScroll():
            yield Static(id="code", expand=True)
        yield Button("Pause", variant="primary", id="pause")
    def do_something(self) -> None:
        self.bell()
    def action_change_theme(self):
        self.dark = not self.dark
    
    def action_stop_audio(self):
        config = Config(os.path.abspath("config.json"))
        try:
            url = "http://localhost/api/stopaudio"
            credentials = f"{config.username}:{config.password}"
            credentials_bytes = credentials.encode("utf-8")
            base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")
            headers = {
                "Authorization": f"Basic {base64_credentials}"
            }
            request = requests.post(url, headers=headers)
            self.notify("Successfully stopped",title="Information", severity="information", timeout=3.0)
            self.update_music()
        except HTTPError as error:
            self.notify("HTTP Status Code " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except URLError as error:
            self.notify("An error has occured while stopping the music " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except Exception as error:
            self.notify("An error has occured while stopping the music " + str(error.args), title="Error", severity="error", timeout=10.0)
            self.bell()
    
    def action_pause_audio(self):
        config = Config(os.path.abspath("config.json"))
        try:
            url = "http://localhost/api/pause"
            credentials = f"{config.username}:{config.password}"
            credentials_bytes = credentials.encode("utf-8")
            base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")
            headers = {
                "Authorization": f"Basic {base64_credentials}"
            }
            request = requests.post(url, headers=headers)
            self.notify("Successfully paused",title="Information", severity="information", timeout=3.0)
            self.update_music()
        except HTTPError as error:
            self.notify("HTTP Status Code " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except URLError as error:
            self.notify("An error has occured while stopping the music " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except Exception as error:
            self.notify("An error has occured while stopping the music " + str(error.args), title="Error", severity="error", timeout=10.0)
            self.bell()
    def action_unpause_audio(self):
        config = Config(os.path.abspath("config.json"))
        try:
            url = "http://localhost/api/unpause"
            credentials = f"{config.username}:{config.password}"
            credentials_bytes = credentials.encode("utf-8")
            base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")
            headers = {
                "Authorization": f"Basic {base64_credentials}"
            }
            request = requests.post(url, headers=headers)
            self.notify("Successfully unpaused",title="Information", severity="information", timeout=3.0)
            self.update_music()
        except HTTPError as error:
            self.notify("HTTP Status Code " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except URLError as error:
            self.notify("An error has occured while stopping the music " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except Exception as error:
            self.notify("An error has occured while stopping the music " + str(error.args), title="Error", severity="error", timeout=10.0)
            self.bell()
    def playsong(self) -> None:
        self.switch_mode("songmenu")
    
    def action_request_quit(self) -> None:
        def check_quit(quit: bool) -> None:
            if quit:
                self.exit()
        
        self.push_screen(QuitScreen(), check_quit)
    def on_mount(self) -> None:
        self.widget.border_title = "Now Playing"
        self.update_music()
        timer = Timer(self.update_music,interval=5.0, repeat=None)
        
    @work(exclusive=True, thread=True)
    def update_music(self):
        config = Config(os.path.abspath("config.json"))
        try:
            music_widget = self.query_one("#now_playing")
            worker = get_current_worker()
            url = "http://localhost/api/song"
            credentials = f"{config.username}:{config.password}"
            credentials_bytes = credentials.encode("utf-8")
            base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")
            headers = {
                "Authorization": f"Basic {base64_credentials}"
            }
            request = Request(url, headers=headers)
            response_text = urlopen(request).read().decode("utf-8")
            music = Text.from_ansi(response_text)
            if not worker.is_cancelled:
                if not response_text:
                    self.call_from_thread(music_widget, "Nothing is being played right now")
                music_object = json.loads(response_text)
                name = music_object["name"]
                description = music_object["description"]
                self.call_from_thread(music_widget.update, f"🎵{name} \n📝[bold]Description[/bold]: {description}")
                self.notify("The music has been successfully refreshed",title="Information", severity="information", timeout=3.0)
        except HTTPError as error:
            self.notify("HTTP Status Code " + str(error.reason), title="[bold]Error[/bold]", severity="error", timeout=10.0)
            self.bell()
        except URLError as error:
            self.notify("An error has occured while updating the music " + str(error.reason), title="Error", severity="error", timeout=10.0)
            self.bell()
        except Exception as error:
            self.notify("An error has occured while updating the music " + str(error.args), title="Error", severity="error", timeout=10.0)
            self.bell()
    @work(exclusive=True, thread=True)
    def update_status(self):
        try:
            status_widget = self.query_one("#status")
            worker = get_current_worker()
            url = "http://localhost/status"
            config = Config(os.path.abspath("config.json"))
            credentials = f"{config.username}:{config.password}"
            credentials_bytes = credentials.encode("utf-8")
            base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")
            headers = {
                "Authorization" : f"Basic {base64_credentials}"
            }
            request = Request(url, headers=headers)
            response_text = urlopen(request).read().decode("utf-8")
            response = Text.from_ansi(response_text)
            if not worker.is_cancelled:
                if not response_text:
                    self.call_from_thread(status_widget, "")
                music_object = json.loads(response_text)
                name = music_object["name"]
                description = music_object["description"]
                self.call_from_thread(status_widget, f"Operational")
                self.notify("Successfully refreshed status",title="Information", severity="information", timeout=5.0)
        except HTTPError as error:
            self.notify("HTTP Status Code " + str(error.reason), title="[bold]Error[/bold]", severity="error", timeout=10.0)

if __name__ == "__main__":
    app = NiftyhoGramofonUI()
    app.run()