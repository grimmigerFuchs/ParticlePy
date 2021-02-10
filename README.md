<p align="center">
	<h2 align="center">ParticlePy</h2>
	<p align="center">
    	<img src="https://raw.githubusercontent.com/grimmigerFuchs/ParticlePy/master/img/logo.svg" width=90>   
	</p>
  <!-- badges-->
	<p align="center">
        <a href='https://particlepy.readthedocs.io/en/latest/?badge=latest' target="_blank">
            <img src='https://readthedocs.org/projects/particlepy/badge/?version=latest' alt='Documentation Status' />
        </a>
       	<a href="https://pypi.org/project/particlepy/" target="_blank">
            <img src="https://img.shields.io/badge/PyPi-1.0.4-blue" alt="PyPi Latest Stable" />
      	</a>
	</p>
    <h5 align="center">
        <a href="https://github.com/grimmigerFuchs/ParticlePy/tree/master/examples">Examples</a>
        &bull;
        <a href="https://particlepy.readthedocs.io/en/latest/">Documentation</a>
        &bull;
        <a href="https://pypi.org/project/particlepy/">PyPi</a>
    </h5>
	<p align="center">
		A short library for easy to use particles in Pygame based on <a href="http://dafluffypotato.com/" target="blank">DaFluffyPotato's</a> particle system.
	</p>
</p>





# Installation



## Dependencies

- pygame

- *setuptools*

- *Sphinx*

- *sphinx_rtd_theme*

  


## **Versions**

### *Latest*

#### Pip

```bash
pip install --upgrade particlepy
```


### Git

```bash
git clone https://github.com/grimmigerFuchs/ParticlePy.git
cd ParticlePy/
pip install -r requirements.txt
python3 setup.py install
```



# Usage

This is a short example of how to use this library. Examples can be found in the [`examples`](https://github.com/grimmigerFuchs/ParticlePy/tree/master/examples) folder.

```python
#!/usr/bin/env python3
# example.py

import pygame
import particlepy
import sys
import time
import random

pygame.init()

# pygame config
SIZE = 800, 800
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("ParticlePy example program")
pygame.mouse.set_visible(False)

# timing
clock = pygame.time.Clock()
FPS = 60

# delta time
old_time = time.time()
delta_time = 0

# particle system to manage particles
particle_system = particlepy.particle.ParticleSystem()

# main loop
while True:
    # quit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # delta time
    now = time.time()
    delta_time = now - old_time
    old_time = now

    # get mouse position
    mouse_pos = pygame.mouse.get_pos()

    for _ in range(5):
        particle_system.emit(
            particlepy.particle.Particle(shape=particlepy.shape.Rect(radius=16,
                                                                     angle=random.randint(0, 360),
                                                                     color=(3, 80, 111),
                                                                     alpha=255),
                                         position=mouse_pos,
                                         velocity=(random.uniform(-150, 150), random.uniform(-150, 150)),
                                         delta_radius=0.2))

    # update particle properties
    particle_system.update(delta_time=delta_time)

    # color manipulation
    for particle in particle_system.particles:
        particle.shape.color = particlepy.math.fade_color(particle=particle,
                                                          color=(83, 150, 181),
                                                          progress=particle.inverted_progress)

    # render shapes
    particle_system.make_shape()

    # post shape creation manipulation
    for particle in particle_system.particles:
        particle.shape.angle += 5

    # render particles
    particle_system.render(surface=screen)

    # update display
    pygame.display.update()
    screen.fill((13, 17, 23))
    clock.tick(FPS)
```

![Gif of particle simulation](https://media.giphy.com/media/961YhKg8e59t0Y9eUu/giphy.gif)



# License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/). See [`LICENSE`](https://github.com/grimmigerFuchs/ParticlePy/blob/master/LICENSE) for more
information.



# Contact

grimmigerFuchs - [grimmigerfuchs@gmail.com](mailto:grimmigerFuchs@gmail.com)\
Github Repository: [https://github.com/grimmigerFuchs/ParticlePy](https://github.com/grimmigerFuchs/ParticlePy)\
PyPi Project: [https://pypi.org/project/particlepy/](https://pypi.org/project/particlepy/)
