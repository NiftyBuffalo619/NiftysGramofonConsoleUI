from textual.app import App
from textual.widgets import Footer, Header, Button, Static
from textual.command import Hit, Hits, Provider
from textual.containers import VerticalScroll
import winsound
from functools import partial

class NowPlaying(Static):
    """Some Text"""
class AnotherCommand(Provider):
    async def search(self, query:str) -> Hits:
        matcher = self.matcher(query)
        
        command = "play"
        score = matcher.match(command)
        yield Hit(
                score,
                matcher.highlight(command),  
                partial(),
                help="Plays a test sound",
            )
class Commands(Provider):
    list = ["FNAF"]
    
    """Plays a sound"""
    
    def read_url(self) -> []:
        return list
    async def startup(self) -> None:
        await self.playsound()
    async def search(self, query: str) -> Hits:
        """Search"""
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app , NiftyhoGramofon)
        for url in list:
            command = f"connect {str(url)}"
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),  
                    partial(),
                    help="Connect to FNAF",
                )
    def playsound():
        return windsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
        """"""

class NiftyhoGramofon(App):
    
    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("d", "change_theme", "Change Theme"),
        ("q", "quit", "Quit"),
    ]
    COMMANDS = App.COMMANDS | {Commands, AnotherCommand}
    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield NowPlaying("Now Playing something", id="now_playing")
    # IMPORTANT there has to be an action_ in it because it is an action method and it's associated with change_theme
    def action_change_theme(self):
        self.dark = not self.dark
    def action_playsound(self):
        self.bell()

if __name__ == "__main__":
    NiftyhoGramofon().run()