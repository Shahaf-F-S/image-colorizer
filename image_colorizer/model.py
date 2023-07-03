# model.py

import datetime as dt
import shutil
from dataclasses import dataclass
from typing import Optional, List, Union
import os

import cv2
import numpy as np

from represent import represent

from image_colorizer.base import models

__all__ = [
    "ModelsLocations",
    "build_model",
    "load_model",
    "Colorizer"
]

def split(data: bytes, fractions: int) -> List[bytes]:
    """
    Splits the data into different parts.

    :param data: The data to split.
    :param fractions: The amount of fractions.

    :returns: The list of data fractions.
    """

    payload = []

    size = len(data) // fractions

    for _ in range(0, len(data), size):
        payload.append(data[:size])

        data = data[size:]
    # end for

    if len(data) > 0:
        payload.append(data)
    # end if

    return payload
# end split

def join(data: List[bytes]) -> bytes:
    """
    Joins the data fractions into one data fragment.

    :param data: The data fractions to join.

    :returns: The joined data.
    """

    payload = b''

    for fraction in data:
        payload += fraction
    # end for

    return payload
# end join

@dataclass(repr=False, slots=True)
@represent
class ModelsLocations:
    """A class to represent a model locator."""

    model: str
    prototext: str
    kernel: str
# end ModelsLocator

def load_model() -> ModelsLocations:
    """
    Builds the models files.

    :returns: The model locator object.
    """

    root = models()

    model_path = f"{root}/colorization.caffemodel"

    if not os.path.exists(model_path):
        payload = []

        for i in range(len(os.listdir(f"{root}/caffemodel"))):
            with open(f"{root}/caffemodel/{i}.weight", "rb") as file:
                payload.append(file.read())
            # end open
        # end for

        with open(f"{root}/colorization.caffemodel", "wb") as file:
            file.write(join(payload))
        # end open
    # end if

    working_directory = os.path.split(
        os.path.dirname(os.path.abspath(__file__))
    )[0] + "/models"

    if not os.path.exists(working_directory):
        shutil.copytree(root, working_directory)
        shutil.rmtree(f"{working_directory}/caffemodel")
    # end if

    prototext_path = f"{working_directory}/colorization.prototxt"
    model_path = f"{working_directory}/colorization.caffemodel"
    kernel_path = f"{working_directory}/points.npy"

    prototext_path = os.path.relpath(prototext_path)
    model_path = os.path.relpath(model_path)

    return ModelsLocations(
        model=model_path, prototext=prototext_path,
        kernel=kernel_path
    )
# end load_model

def build_model(locator: ModelsLocations) -> cv2.dnn.readNetFromCaffe:
    """
    Loads the network model.

    :returns: The network model.
    """

    prototext_path = locator.prototext
    model_path = locator.model
    kernel_path = locator.kernel

    net = cv2.dnn.readNetFromCaffe(prototext_path, model_path)

    points = np.load(kernel_path)
    points = points.transpose().reshape(2, 313, 1, 1)

    net.getLayer(net.getLayerId("class8_ab")).blobs = [
        points.astype(np.float32)
    ]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [
        np.full([1, 313], 2.606, dtype="float32")
    ]

    return net
# end build_model

def create_model() -> cv2.dnn.readNetFromCaffe:
    """
    Builds the network model.

    :returns: The network model.
    """

    return build_model(load_model())
# end create_model

@represent
class Colorizer:
    """
    A class to represent an image colorization model.

    The instances of this class are objects for black-and-white images colorization.
    Automatically accelerated with GPU connected, the colorization process
    is generally quick, as well as on a CPU.

    In the colorization process the instance uses a deep Neural Network,
    trained to colorize black-and-white images.

    The constractor parameters:

    - image:
        A path to an image file, or a numpy array of the image to colorize.

    >>> from image_colorizer import Colorizer
    >>>
    >>> colorizer = Colorizer("<PATH TO B&W IMAGE>")
    >>> colorizer.save_colorized_image("<PATH TO COLORIZED IMAGE>")
    """

    model = None

    DELAY = 0

    def __init__(self, image: Union[np.array, str]) -> None:
        """
        Processes the image input as a file path or an image array

        :param image: The path to the image file or the image object
        """

        if Colorizer.model is None:
            Colorizer.model = create_model()
        # end if

        self.colorized_img = None

        self.bw_img = self.configure_image(image)

        self.delay = self.DELAY
    # end __init__

    def colorize_image(self) -> np.array:
        """
        Colorizes the image using the image colorization.

        :returns: The colorized image object.
        """

        normalized_img = self.bw_img.astype("float32") / 255.0
        lab_img = cv2.cvtColor(normalized_img, cv2.COLOR_BGR2LAB)
        resized_img = cv2.resize(lab_img, (224, 224))
        light_img = cv2.split(resized_img)[0] - 50

        self.model.setInput(cv2.dnn.blobFromImage(light_img))

        ab = self.model.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (self.bw_img.shape[1], self.bw_img.shape[0]))

        light_img = cv2.split(lab_img)[0]

        colorized_img = np.concatenate((light_img[:, :, np.newaxis], ab), axis=2)
        colorized_img = cv2.cvtColor(colorized_img, cv2.COLOR_LAB2BGR)

        self.colorized_img = (255 * colorized_img).astype("uint8")

        return self.colorized_img
    # end colorize_image

    @staticmethod
    def configure_image(image: Union[np.array, str]) -> np.array:
        """
        Processes the image input as a file path or an image array

        :param image: The path to the image file or the image object
        """

        if isinstance(image, str) and os.path.exists(image):
            return cv2.imread(image)

        elif isinstance(image, np.ndarray):
            return image
        # end if
    # end configure_image

    @staticmethod
    def save_image(image: np.array, path: str) -> None:
        """
        Saves the given image object into a file by the file path

        :param path: The file path to save the image in.
        :param image: The path to the image file or the image object
        """

        if location := os.path.split(path)[0]:
            os.makedirs(location, exist_ok=True)
        # end if

        cv2.imwrite(path, image)
    # end save_image

    def configure_colorized_image(self) -> np.array:
        """
        Configures the colorized image existing state.

        :returns: The colorized image array.
        """

        if self.colorized_img is None:
            self.colorized_img = self.colorize_image()
        # end if

        return self.colorized_img
    # end configure_colorized_image

    def display_image(
            self,
            image: np.array,
            delay: Optional[Union[int, float, dt.timedelta]] = None,
            title: Optional[str] = "image"
    ) -> None:
        """
        Displays the given image.

        :param image: The image object ot display.
        :param delay: The amount of seconds to show the window.
        :param title: The title of the image window.
        """

        if delay is None:
            delay = self.delay
        # end if

        if isinstance(delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        cv2.imshow(title or "", self.configure_image(image))
        cv2.waitKey(delay * 1000)
    # end display_image

    def display_original_image(
            self,
            delay: Optional[Union[int, float, dt.timedelta]] = None,
            title: Optional[str] = "original image"
    ) -> None:
        """
        Displays the given image.

        :param delay: The amount of seconds to show the window.
        :param title: The title of the image window.
        """

        self.display_image(
            image=self.bw_img,
            delay=delay or self.delay, title=title
        )
    # end display_original_image

    def display_colorized_image(
            self,
            delay: Optional[Union[int, float, dt.timedelta]] = None,
            title: Optional[str] = "colorized image"
    ) -> None:
        """
        Displays the given image.

        :param delay: The amount of seconds to show the window.
        :param title: The title of the image window.
        """

        self.configure_colorized_image()

        self.display_image(
            image=self.colorized_img,
            delay=delay or self.delay, title=title
        )
    # end display_colorized_image

    def save_original_image(self, path: str) -> None:
        """
        Saves the given image object into a file by the file path

        :param path: The file path to save the image in.
        """

        self.save_image(image=self.bw_img, path=path)
    # end save_original_image

    def save_colorized_image(self, path: str) -> None:
        """
        Saves the given image object into a file by the file path

        :param path: The file path to save the image in.
        """

        self.configure_colorized_image()

        self.save_image(image=self.colorized_img, path=path)
    # end save_colorized_image
# end Colorizer