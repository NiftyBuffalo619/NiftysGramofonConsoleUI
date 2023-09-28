from __future__ import annotations

from functools import partial
from pathlib import Path

from rich.syntax import Syntax

from textual.app import App, ComposeResult
from textual.command import Hit, Hits, Provider
from textual.containers import VerticalScroll, Grid
from textual.widgets import Static, Footer, Header, Input, Label, Button
from textual.screen import Screen, ModalScreen

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
                help="Plays a song by the id provided",
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
    ]
    COMMANDS = App.COMMANDS | {Playsound} | {PlaySong}
    MODES = {
        "main": MainScreen,
        "songmenu": SongSearchScreen,
    }
    CSS_PATH = "style.tcss"
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with VerticalScroll():
            yield Static(id="code", expand=True)
    def do_something(self) -> None:
        self.bell()
    def action_change_theme(self):
        self.dark = not self.dark
    def playsong(self) -> None:
        self.switch_mode("songmenu")
    
    def action_request_quit(self) -> None:
        def check_quit(quit: bool) -> None:
            if quit:
                self.exit()
        
        self.push_screen(QuitScreen(), check_quit)

if __name__ == "__main__":
    app = NiftyhoGramofonUI()
    app.run()