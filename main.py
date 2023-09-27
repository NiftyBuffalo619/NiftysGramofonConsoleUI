from __future__ import annotations

from functools import partial
from pathlib import Path

from rich.syntax import Syntax

from textual.app import App, ComposeResult
from textual.command import Hit, Hits, Provider
from textual.containers import VerticalScroll
from textual.widgets import Static, Footer, Header, Input


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

class NiftyhoGramofonUI(App):
    BINDINGS = [
        ("d", "change_theme", "Change Theme"),
        ("q", "quit", "Quit"),
    ]
    COMMANDS = App.COMMANDS | {Playsound} | {PlaySong}
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
        yield Input(placeholder="Type a song you want to play")

if __name__ == "__main__":
    app = NiftyhoGramofonUI()
    app.run()