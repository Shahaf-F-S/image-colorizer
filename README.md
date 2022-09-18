# image-colorizer
> A program that colorizes black and white images, using an AI model of Artificial Neural Network.
> The program includes a module to use dynamically to colorize black and white images.

first of all
------------

#### Hi there, I'm Shahaf Frank-Shapir

Just a bit about me...

- I just launched my complete python application for stock prediction, sentiment analysis and trading advisor!
- I’m currently learning biology, software engineering and systems engineering.
- I’m looking to collaborate with other content topics.
- 2021 Goals: Contribute more to privet projects.
- Fun fact: I love to draw and paint, sculpt, program (of course) play the piano and make origami.

#### credits:

- writen and owned by:
  Shahaf Frank-Shapir

- all the rights are saved for:
  Shahaf Frank-Shapir

- program version:
  1.4.2

- programming language:
  python 3.8.6 (100%)

before we start
---------------

#### description:

- A program that colorizes black and white images, using an AI model of Artificial Neural Network.
- 
- The program includes a module to use dynamically to colorize black and white images.

#### dependencies:

- opening:
  As for this is a really complex program, which uses a lot of modules, there are required dependencies needed
  in order to run the program. keep in mined the program was writen in python 3.8.6, so any python version lower
  than 3.6.1 might not work properly. Moreover, built-in python modules are being used, so keep that in mind.

- the modules are:
  > - opencv-python==4.5.3.56
>
- to install manually the required none-built-in python modules in command line:
  write in the project command line:
- install the dependencies manually by writing the following list to the command line in the project directory:
````
pip install opencv-python==4.5.3.56
````
- install app dependencies by writing the "-r" option to install the requirements
  writen in a file, and write the following line in the project directory:
````
pip install -r requirements.txt
````

run the app
-----------

#### run from windows command line (inside the project directory)
- run with python (3.6.0 or higher) by writing to the command line in the project directory:
````
python object_detection/test.py
````

use the module
--------------

#### imports the module main object to use the Speech-Recognition system
- uses the module in a closed loop:
````python
from image_colorizer import Colorizer  # imports the colorizing object

def main(img_path, saving_path) -> "np.ndarray":  # defines the main function of the script
    # this function is the main function that runs the program

    colorizer = Colorizer(img_path)  # creates the colorization object
    
    colorizer.colorize_image()  # calls the method to colorize the image
    colorizer.display_org_image()  # calls the method to display the original image
    colorizer.display_colorized_image()  # calls the method to display the colorized image
    colorizer.save_colorized_image(saving_path)  # calls the method to display the image
# end main

if __name__ == "__main__":  # for a main function in the script
    # calls the main function
    main("<BLACK & WHITE IMAGE PATH>", "<SAVING COLORIZED IMAGE PATH>")
# end if
````