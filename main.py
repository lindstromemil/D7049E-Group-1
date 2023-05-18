from render_module.render import Render

def main():
    game_engine = Render()
    game_engine.setup()
    #This is where you do configurations to fit your game
    game_engine.loadMap("render_module/models/square.egg.pz")
    game_engine.setClock(60)
    game_engine.setFullscreen(True)
    game_engine.addTitle("GunAimLab")
    game_engine.addMusic("glitch-blue-moon.wav")
    game_engine.run()

if __name__ == "__main__":
    main()