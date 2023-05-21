# D7049E-Group-1
The group consists of 4 people studying D7049E at LTU.

### Games Genre:
3D shooter with focus on aim training similar to [Aim Lab](https://aimlab.gg/)

## Implementation (Milestone 3)
During implementation we realised that OGRE for Python was quite outdated and the docs were deprecated. Because of this we will use Panda3D for our rendering instead.
Aside from that implemenation is going as planned, we only have to implement graphics and physics to have it done at the moment.

## Design Idea (Milestone 2)

[UML Overview](https://drive.google.com/file/d/1ZiK6dv3DAgfk3j_JF3WzqF3ae29eIMVa/view?usp=sharing)

[Design Description](https://docs.google.com/document/d/10KdjgH7jCUT3FOrPdMxzWrG1XPnNNLA3hUT4Ol3CqTc/edit?usp=sharing)

Both documents will get updated as the course progresses and are not final.

## Libraries:
**Language**: Python <br />
**3D library**: Panda3D <br />
**Physics library**: PyBullet <br />
**Audio library**: PyOpenAL <br />

## Prioritized Attributes:
* Responsive camera <br />
* Forgiving physics <br />
* High fidelity animations

## Setup

Run `sample.py` and it will generate the config files in `/Documents/PySample` on your main drive. Do the following inside `/PySample`: 

Add a folder named `Meshes` where the mesh, material and skeleton files will be. Add a file named `resources.cfg` and insert
```
[General] 
FileSystem=../PySample/Meshes
```

### All pip installs (so far)
```
pip install PyOpenAL
pip install pynput
pip install pybullet

Install Panda3D
```

### Usage

Adding assets into the game is done by moving the desired 3d models and textures into the models folder and then calling the `createNewObject()` function from `render.py`
