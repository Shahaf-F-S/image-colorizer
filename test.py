# test.py

from image_colorizer import Colorizer

def main() -> None:
    """Runs a test program."""

    colorizer = Colorizer("lion.jpg")

    colorizer.save_colorized_image("colorized_lion.jpg")
    colorizer.display_colorized_image()
# end main

if __name__ == "__main__":
    main()
# end if