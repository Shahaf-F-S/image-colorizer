# main.py

import argparse

from image_colorizer import Colorizer

__all__ = [
    "main"
]

def main() -> None:
    """Runs the program to visualize in an image a model."""

    parser = argparse.ArgumentParser(
        description='An image colorizer for black and white images.'
    )

    parser.add_argument(
        'image', metavar='IMAGE_FILE', help='image file to save',
        nargs='?', default="image.png"
    )
    parser.add_argument(
        '--display_org_img', help="display the original image",
        action='store_true', default=False
    )
    parser.add_argument(
        '--display_colorized_img', help="display the colorized image",
        action='store_true', default=False
    )
    parser.add_argument(
        '--save_org_img', help="save the original image in a file",
        type=str, default=False
    )
    parser.add_argument(
        '--save_colorized_img', help="save the colorized image in a file",
        type=str, default=False
    )

    args = parser.parse_args()

    colorizer = Colorizer(args.image)

    colorizer.colorize_image()

    if args.display_org_img:
        colorizer.display_original_image()
    # end if

    if args.display_colorized_img:
        colorizer.display_colorized_image()
    # end if

    if args.save_org_img:
        colorizer.save_original_image(args.save_org_img)
    # end if

    if args.save_colorized_img:
        colorizer.save_colorized_image(args.save_colorized_img)
    # end if
# end main

if __name__ == '__main__':
    main()
# end if