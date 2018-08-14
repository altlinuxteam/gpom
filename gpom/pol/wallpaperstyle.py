from gpom.common import config, error, warning, info, debug
from gpom.policy import DesktopPolicy

class PolImpl(DesktopPolicy):
    def __init__(self, reg):
        super(PolImpl, self).__init__()
        self.name = 'WallpaperStyle'
