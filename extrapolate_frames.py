# %%
from mandelbrot import *
from PIL import Image
import cv2
import numpy as np
import glob


def complex2pixel(x,y):
    return (int((x-x__min)/(x__max-x__min)*WIDTH), int((y-y__min)/(y__max-y__min)*HEIGHT))


def create_pixels(x, y, scale_factor, number_steps):
    intermediate_factor = scale_factor ** (1/number_steps)
    points = create_points(x,y,intermediate_factor, number_steps) # [xmin xmax, ymin ymax]
    pixels = [complex2pixel(points[i][0], points[i][2]) + complex2pixel(points[i][1], points[i][3]) for i in range(len(points))]
    return pixels # [xmin, ymin, xmax, ymax]



def extrapolate(big_image_nb, scale_factor, x, y, steps):
    pixels = create_pixels(x,y,scale_factor, steps)
    big_image = Image.open(f"Zooms\\{x}_{y}\\depth_{big_image_nb}.jpeg")

    Path(f"Zooms\\{x}_{y}\\extrapolated_{steps}").mkdir(parents=True, exist_ok=True)
    gif = []
    for i in range(steps):
        (xmin, ymin, xmax, ymax) = pixels[i]
        cropped = Image.fromarray(np.asarray(big_image)[xmin :xmax, ymin:ymax])
        resized = cropped.resize((HEIGHT, WIDTH))
        #gif.append(resized)
        resized.save(f"Zooms\\{x}_{y}\\extrapolated_{steps}\\{i+steps*(big_image_nb-1)}.jpeg")
    return gif


def create_all(x,y):
    gif = []
    for i in tqdm.tqdm(range(101)):
        gif = gif + extrapolate(i+1, 0.75, x,y, 10)
    #gif[0].save(f"Zooms\\{x}_{y}\\out.gif", save_all=True, append_images = gif[1:], loop =0, duration = (1/25)*1000)
    
def create_video(x,y):
    img_array = []
    for filename in tqdm.tqdm([f"Zooms\\{x}_{y}\\extrapolated_{10}\\{i}.jpeg" for i in range(1010)]):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv2.VideoWriter(f"Zooms\\{x}_{y}\\project_60.avi",cv2.VideoWriter_fourcc(*'DIVX'), 60, size)
    for i in tqdm.tqdm(range(len(img_array))):
        out.write(img_array[i])
    out.release()
# %%

# %%
