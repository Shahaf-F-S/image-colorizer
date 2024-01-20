# image-colorizer

> A program that colorizes black and white images, using an AI model of Artificial Neural Network.
> The program includes a module to use dynamically to colorize black and white images.

```python
from image_colorizer import Colorizer

colorizer = Colorizer("lion.jpg")

colorizer.save_colorized_image("colorized_lion.jpg")
colorizer.display_colorized_image()
```