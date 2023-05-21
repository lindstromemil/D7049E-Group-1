from render_module.render import Render

def main():
    game_engine = Render()
    game_engine.setup()


    # This is where you do configurations to fit your game
    game_engine.loadMap("render_module/models/square.egg.pz")
    game_engine.setClock(60)
    game_engine.setFullscreen(True)
    game_engine.addTitle("GunAimLab")

    # Credit to Glitch for allowing us to use this song in our game!
    game_engine.addMusic("glitch-blue-moon.wav")

    game_engine.run()

if __name__ == "__main__":
    main()


""" Documentation 

    We have the player and plane spawn in when you run the game engine

    To create an object you must first create a class that
    implements the Action class. That is what you send into
    game_engine.createNewObject()

    Create new object in both rendering and physics -> game_engine.createNewObject()
    Add music to game -> game_engine.addMusic() 
    Set fullscreen -> game_engine.setFullscreen()
    Set runtime clock -> game_engine.setClock()
    Load map -> game_engine.loadMap()
    Add title -> game_engine.addTitle()
"""