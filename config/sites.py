from src.services.porno365 import porno365
from src.services.sosalkino import sosalkino
from src.services.xvideos import xvideos


SITE_HANDLERS = {
    "sslkn": ("JSON/sslkn.json", sosalkino),
    "porno365": ("JSON/p365.json", porno365),
    "xvideos": ("JSON/xvideos.json", xvideos),
}