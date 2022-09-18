# setup.py

from setuptools import setup

def main() -> None:
    """Runs the program to distribute the package."""

    name = 'image-colorizer'
    version = '1.7.3'
    license = 'MIT'
    author = "Shahaf Frank-Shapir"
    author_email = 'shahaffrs@gmail.com'
    description = "A program that colorizes black and white images,\n" \
                  "using an AI model of Artificial Neural Network.\n"
    long_description = open('README.txt', "r").read()
    url = 'https://github.com/Shahaf-F-S/image-colorizer'

    packages = ['image_colorizer']
    install_requires = ["opencv-python==4.5.3.56"]

    package_data = {"image_colorizer": ['models/*.*', 'assets/icon/*.*']}

    setup(
        name=name, version=version, description=description, license=license,
        packages=packages, author=author, author_email=author_email,
        package_data=package_data, url=url, install_requires=install_requires,
        long_description=long_description
    )
# end main

if __name__ == "__main__":
    main()
# end if