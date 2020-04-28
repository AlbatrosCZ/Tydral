from defaults.install_default import *
from players.install_players import *
from settings.install_settings import *
class instaler:
    def __init__(self, setting = True, players = True, default = True):
        self.setting = setting
        self.players = players
        self.default = default
        self.install()

    def install(self):
        if self.setting:
            install_settings()
        if self.players:
            install_players()
        if self.default:
            install_default()