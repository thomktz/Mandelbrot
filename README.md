# Mandelbrot set zoom

### The Mandelbrot set

A faster way to generate Mandelbrot set zooms using extrapolation  

A point `c = a + ib` on the complex plane is in the Mandelbrot set if the sequence defined by

`z_0 = 0`  
`z_n = z_(n-1)^2 + c`  

converges as `n -> +inf`

An important thing to notice is that if at some point `|z_n| > 2`, then the sequence is divergent.

### Colors

If at iteration `i`, `|z_i|` becomes greater than 2, the color value of the point is set as such :

`Col(c) = sqrt(i) + log(log(|z_i|))`

This value is later mapped into a `matplotlib` colormap to make it RGB

### Interpolation

In between two zooms, the interpolation will divide this zoom (usually 120%) as ~10 smaller zooms without having to calculate all points, by cropping and resizing the bigger image by a factor of = ~ 102%  (100% + 20%/10)

### How to use

First, find a point `c = x + iy` near (outside) the set boundaries.  
Then call `create_zoom(x,y)` to generate all zoomed frames, followed by `create_all(x,y)` to interpolate in between frames  
The interpolation allows for a huge speedup, at the cost of a few "jumps" in the rendering.  
Finally, call `create_video`  

### Results :

`c = -0.661644125 -0.446924283 * i` :

https://user-images.githubusercontent.com/60552083/116859732-c03af980-ac00-11eb-9dd2-e1c49968f910.mp4


