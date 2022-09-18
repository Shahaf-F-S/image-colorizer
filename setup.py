# setup.py

from setuptools import setup  # imports the setup function

def main() -> None:
    # this function is the main function to run the setup of the package

    name = 'image-colorizer'  # defines the package name
    version = '1.0.2'  # defines the package version
    license = 'MIT'  # defines the license type
    author = "Shahaf Frank-Shapir"  # defines the author name
    author_email = 'shahaffrs@gmail.com'  # defines the author email
    # defines the package description
    description = "A program that colorizes black and white images,\n" \
                  "using an AI model of Artificial Neural Network.\n"
    long_description = open('README.txt', "r").read()  # defines the package long description
    url = 'https://github.com/Shahaf-F-S/image-colorizer'  # defines the creator url

    packages = ['image_colorizer']  # defines the modules list for the package
    # defines the required packages list to install for the package
    install_requires = [
        "opencv-python==4.5.3.56"
    ]

    # defines the additional files to include in the package
    package_data = {"image_colorizer": ['models/*.*']}

    # calls the function to create the package from the project
    setup(
        name=name, version=version, description=description, license=license,
        packages=packages, author=author, author_email=author_email,
        package_data=package_data, url=url, install_requires=install_requires,
        long_description=long_description
    )
# end main

if __name__ == "__main__":  # if the file is executed:
    # runs the section when the file is executed
    main()  # calls the main function to run the setup
# end if