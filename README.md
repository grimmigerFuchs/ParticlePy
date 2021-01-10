<p align="center">
   <h2 align="center">ParticlePy</h2>
   <p align="center">
      A short library for easy to use particles in Pygame based on <a href="http://dafluffypotato.com/" target="blank">DaFluffyPotato's</a> particle system.
   </p>
</p>

# Installation

## Dependencies

- Pygame ~= 2.0.1

## Pip
```bash
pip install particlepy
```
or
```bash
pip install git+https://github.com/grimmigerFuchs/ParticlePy.git
```

## Manually

1. Clone the repo
   ```bash
    git clone https://github.com/grimmigerFuchs/ParticlePy.git
   ```
2. Go into the directory
   ```bash
   cd ParticlePy/
   ```
3. Run `setup.py`
   ```bash
   python setup.py install
   ```

# Usage

This is a short example of how to use this library. Others can be found in the [`examples`](examples) folder.\
Note the standard FPS in the example was set to 60.

## Imports

```python
import pygame
import particlepy as par
import random
```

## Needed classes

```python
# particle system with grouped functions
particles = par.particle.ParticleSystem(remove_particles_batched=False)  # particle system; argument: no batched removals
```

## Particle creation

### Circle

```python
particles.create(par.particle.Circle(position=pygame.mouse.get_pos(),                                # get mouse pos
                                     velocity=(random.uniform(0, 1) * random.choice((-1, 1)), -3),   # x and y velocity
                                     size=random.randint(2, 25),                                     # size of particles
                                     delta_size=random.uniform(0.035, 0.050),                        # decreases size every frame
                                     color=(255, 255, 255),                                          # rgb
                                     alpha=255,                                                      # optional transparency
                                     antialiasing=True))                                             # aa normally turned off
```

### Rectangle

```python
# almost same as circles but for rects aa is not an option
particles.create(par.particle.Rect(position=pygame.mouse.get_pos(),
                                   velocity=(random.uniform(0, 1) * random.choice((-1, 1)), -3),
                                   size=random.randint(2, 25),
                                   delta_size=random.uniform(0.035, 0.050),
                                   color=random.randint(210, 255),
                                   alpha=255))
```

## Updating positions and drawing the particles with particle systems

```python
# update position and size
particles.update(delta_time=delta_time, gravity=0.009)  # both arguments are optional; gravity pulls particles down

# draw particles
particles.draw(surface=screen)  # draw particles on given surface
```

The shown code was taken from the example program [`examples/example.py`](examples/example.py).

![Gif of example program being executed](https://media.giphy.com/media/961YhKg8e59t0Y9eUu/giphy.gif)

# License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/). See [`LICENSE`](LICENSE) for more
information.

# Contact

grimmigerFuchs - [grimmigerfuchs@gmail.com](mailto:grimmigerFuchs)\
Project Link: [https://github.com/grimmigerFuchs/Pyticles](https://github.com/grimmigerFuchs/Pyticles)
