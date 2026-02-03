from utils.app import WormholeApp
from utils.common import init_config

def run():
    app = WormholeApp()
    app.run()


if __name__ == "__main__":
    init_config()
    run()
