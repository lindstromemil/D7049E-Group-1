# D7049E-Group-1
The group consists of 4 people studying D7049E at LTU.

### Games Genre:
3D shooter with focus on aim training similar to [Aim Lab](https://aimlab.gg/)

## Design Idea (Milestone 2)

[UML Overview](https://drive.google.com/file/d/1ZiK6dv3DAgfk3j_JF3WzqF3ae29eIMVa/view?usp=sharing)

[Design Description](https://docs.google.com/document/d/10KdjgH7jCUT3FOrPdMxzWrG1XPnNNLA3hUT4Ol3CqTc/edit?usp=sharing)

Both documents will get updated as the course progresses and are not final.

## Libraries:
**Language**: Python <br />
**3D library**: Ogre <br />
**Physics library**: PyBullet <br />
**Audio library**: OpenAL <br />

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