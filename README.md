<p align="center">
   <h2 align="center">Pyticles</h2>
   <p align="center">
      A short library for easy to use particles in Pygame based on <a href="" target="blank">DaFluffyPotato's</a> particle system.
   </p>
</p>

# Installation

1. Clone the repo
   ```bash
    git clone https://github.com/grimmigerFuchs/Pyticles.git
   ```
2. Go into the directory
   ```bash
   cd Pyticles/
   ```
3. Run `setup.py`
   ```bash
   python3 setup.py install
   ```

# Usage

This is a short example of how to use this library. Others can be found in the [`examples`](examples) folder.

## Needed variables / instances

```python
particles = []  # particles are instantiated in here
shape = pyticles.Shape()  # variables of the class Shape are being passed into the "shape" argument of Particle
```

## Particle creation

```python
particles.append(pyticles.Particle(position=pygame.mouse.get_pos(),       # get mouse pos
                                   velocity=(random.uniform(-1, 1), -3),  # x and y velocity
                                   gravity=0.009,                         # gravity (pulls particles down)
                                   radius=random.randint(2, 25),          # size of particles
                                   delta_radius=0.048,                    # decreases radius every frame
                                   color=random.randint(210, 255),        # rgb or greyscale color
                                   shape=shape.circle))                   # shapes: circle or rect
```

## Updating positions and drawing the particles

```python
removes = []  # list of particles to remove because of to small radius
for particle in particles:
    particle.update(delta_time=delta_time)  # update particle positions and radii; delta time is optional
if particle.to_remove(): removes.append(particle)  # check if radius size is valid -> remove particle if not

# remove invalid particles
for i in range(len(removes)):
    particles.remove(removes[i])

# draw particles
for particle in particles:
    particle.draw(screen)
```

The shown code was taken from the example program [`examples/example.py`](examples/example.py).

![Gif of example program being executed](https://media.giphy.com/media/uz3Ypx10Ib9C8amkfc/giphy.gif)

# License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/). See [`LICENSE`](LICENSE) for mor information.

# Contact

grimmigerFuchs - [grimmigerfuchs@gmail.com](mailto:grimmigerFuchs)\
Project Link: [https://github.com/grimmigerFuchs/Pyticles](https://github.com/grimmigerFuchs/Pyticles)