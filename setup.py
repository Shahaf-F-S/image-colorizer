# setup.py

import codecs

with codecs.open('build.py', 'r') as build_file:
    build_source = build_file.read()

source = dict()

exec(build_source, source)

setup = source['setup']

def main() -> None:
    """Runs the function to distribute the package."""

    setup(
        package="image_colorizer",
        project="pyproject.toml",
        exclude=[
            "__pycache__",
            "image_colorizer/source/models/colorization.caffemodel",
            "*.pyc"
        ],
        include=[
            "image_colorizer/source/assets/",
            "image_colorizer/source/dependencies/",
            "image_colorizer/source/models/caffemodel",
            "image_colorizer/source/models/colorization.prototxt",
            "image_colorizer/source/models/points.npy",
            "test.py"
        ],
        requirements="requirements.txt",
        dev_requirements="requirements-dev.txt",
        name='image-colorizer',
        version='0.0.0',
        description=(
            "A program that colorizes black and white images, "
            "using an AI model of Artificial Neural Network."
            "The program includes a module to use dynamically "
            "to colorize black and white images."
        ),
        license='MIT',
        author="Shahaf Frank-Shapir",
        author_email='shahaffrs@gmail.com',
        url='https://github.com/Shahaf-F-S/image-colorizer',
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Operating System :: OS Independent"
        ]
    )
# end main

if __name__ == "__main__":
    main()
# end if