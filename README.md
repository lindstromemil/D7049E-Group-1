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

Run `sample.py` to start the game engine and the game attached to it.

### All pip installs (so far)
```
pip install PyOpenAL
pip install pybullet
```

### Install Panda3D

if you have python already installed on your device then simply run:
```
pip install panda3d==1.10.13
```
Otherwise download Panda3D [here](https://docs.panda3d.org/1.10/python/introduction/installation-windows)

### Usage

In order to load in assets in the game add any models and textures to be used inside the `models` folder and call upon the `createNewObject()` function from the `render.py` file.
