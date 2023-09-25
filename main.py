from textual.app import App
from textual.widgets import Footer, Header, Button, Static
from textual.command import Hit, Hits, Provider
from textual.containers import VerticalScroll
import winsound

class NowPlaying(Static):
    """Some Text"""

class Commands(Provider):
    """Plays a sound"""
    async def startup(self) -> None:
        await self.playsound()

    def playsound():
        return windsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    async def search(self , query: str) -> Hits:
        """"""

class NiftyhoGramofon(App):
    
    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("d", "change_theme", "Change Theme"),
        ("q", "quit", "Quit"),
    ]
    COMMANDS = App.COMMANDS | {Commands}
    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield NowPlaying("Now Playing something", id="now_playing")
    # IMPORTANT there has to be an action_ in it because it is an action method and it's associated with change_theme
    def action_change_theme(self):
        self.dark = not self.dark

if __name__ == "__main__":
    NiftyhoGramofon().run()