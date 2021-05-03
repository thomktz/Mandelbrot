
# %%
import numpy as np
import matplotlib.pyplot as plt
import tqdm
from PIL import Image
import matplotlib
from pathlib import Path

WIDTH = 1000
HEIGHT = 1000
x__min = -2
x__max = 1
y__min = -2
y__max = 2
starting_points = [x__min , x__max, y__min, y__max]

def create_points(x, y, scale_factor, number_steps):
    points = [starting_points]
    for i in range(number_steps):
        A = scale_factor * points[-1][0] + (1- scale_factor) * x
        B = scale_factor * points[-1][1] + (1- scale_factor) * x
        C = scale_factor * points[-1][2] + (1- scale_factor) * y
        D = scale_factor * points[-1][3] + (1- scale_factor) * y
        points.append([A,B,C,D])
    return points


def create_zoom(x, y, resume = 0, scale_factor = 0.80, number_steps = 10):

    points = create_points(x,y,scale_factor, resume + number_steps)
    depth = resume
    for x_min, x_max, y_min, y_max in points[resume:]:
        depth += 1 
        xstep = np.linspace(x_min, x_max, WIDTH)
        ystep = np.linspace(y_min, y_max, HEIGHT)
        C = xstep[:, None] + 1j*ystep.T
        Z = np.zeros((HEIGHT, WIDTH))
        iter = np.zeros((HEIGHT, WIDTH))
        n = 100 + 15 * depth
        for i in tqdm.tqdm(range(n)):
            Z = (np.square(Z) + C).copy()
            filter = np.argwhere(np.absolute(Z)>2).T
            iter[filter[0], filter[1]] = np.sqrt(i+1) - np.log(np.log(np.absolute(Z[filter[0], filter[1]])))
            Z[filter[0], filter[1]] = 0
            C[filter[0], filter[1]] = 0
        iter = iter - np.min(iter)
        iter = iter / np.max(iter)
        im = Image.fromarray((matplotlib.cm.twilight(iter)*255).astype(np.uint8)).convert("RGB")
        Path(f"Zooms\\{x}_{y}").mkdir(parents=True, exist_ok=True)
        im.save(f"Zooms\\{x}_{y}\\depth_{depth}.jpeg")
        print(f"Image n° {depth} saved, dx = {x_max-x_min}")



# %%
#create_zoom(-0.661644125,-0.446924283,0,0.75,100)