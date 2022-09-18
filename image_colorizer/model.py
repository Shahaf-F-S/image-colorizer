# model.py

import shutil
from typing import Optional, List, Union
import os

import cv2
import numpy as np

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

class ModelsLocator:
    """A class to represent a model locator."""

    def __init__(self, model: str, prototext: str, kernel: str):
        """
        Defines the class attributes.

        :param model: The model path.
        :param prototext: The prototext path.
        :param kernel: The kernel path.
        """

        self.model = model
        self.prototext = prototext
        self.kernel = kernel
    # end __init__
# end ModelsLocator

def build_model() -> ModelsLocator:
    """
    Builds the models files.

    :returns: The model locator object.
    """

    working_directory = "/".join(
        os.path.split(os.path.dirname(os.path.abspath(__file__)))
    ) + "/models"

    venv = (
            os.environ['VIRTUAL_ENV'].split('\\')[-1] +
            "/Lib/site-packages/image_colorizer/models"
    )

    if not os.path.exists(venv):
        venv = working_directory
    # end if

    model_path = f"{venv}/colorization.caffemodel"

    if not os.path.exists(model_path):
        payload = []

        for i in range(len(os.listdir(f"{venv}/caffemodel"))):
            with open(f"{venv}/caffemodel/{i}.weight", "rb") as file:
                payload.append(file.read())
            # end open
        # end for

        with open(f"{venv}/colorization.caffemodel", "wb") as file:
            file.write(join(payload))
        # end open
    # end if

    working_directory = os.path.split(
        os.path.dirname(os.path.abspath(__file__))
    )[0] + "/models"

    if not os.path.exists(working_directory):
        shutil.copytree(venv, working_directory)
        shutil.rmtree(f"{working_directory}/caffemodel")
    # end if

    prototext_path = f"{working_directory}/colorization.prototxt"
    model_path = f"{working_directory}/colorization.caffemodel"
    kernel_path = f"{working_directory}/points.npy"

    prototext_path = os.path.relpath(prototext_path)
    model_path = os.path.relpath(model_path)

    return ModelsLocator(
        model=model_path, prototext=prototext_path,
        kernel=kernel_path
    )
# end build_model

def load_model(locator: ModelsLocator) -> cv2.dnn.readNetFromCaffe:
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
# end load_model

class Colorizer:
    """An image colorization class"""

    net = load_model(build_model())

    def __init__(self, image: Union[np.array, str]):
        """
        Processes the image input as a file path or an image array

        :param image: The path to the image file or the image object
        """

        self.colorized_img = None

        self.bw_img = self.configure_image(image)
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

        self.net.setInput(cv2.dnn.blobFromImage(light_img))

        ab = self.net.forward()[0, :, :, :].transpose((1, 2, 0))
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

    def configure_colorized_image(self) -> np.array:
        """
        Configures the colorized image existing state.

        :returns: The colorized image array.
        """

        if self.colorized_img is None:
            self.colorized_img = self.colorize_image()
        # end if

        return self.colorized_img
    # end configure_image

    def display_image(
            self, image: np.array, interval: Optional[int] = 0,
            title: Optional[str] = "image"
    ) -> None:
        """
        Displays the given image.

        :param image: The image object ot display.
        :param interval: The amount of seconds to show the window.
        :param title: The title of the image window.
        """

        cv2.imshow(title, self.configure_image(image))
        cv2.waitKey(interval)
    # end _display_image

    def display_org_image(
            self, interval: Optional[int] = 0, title: Optional[str] = "original image"
    ) -> None:
        """
        Displays the given image.

        :param interval: The amount of seconds to show the window.
        :param title: The title of the image window.
        """

        self.display_image(
            image=self.bw_img, interval=interval, title=title
        )
    # end display_image

    def display_colorized_image(
            self, interval: Optional[int] = 0, title: Optional[str] = "colorized image"
    ) -> None:
        """
        Displays the given image.

        :param interval: The amount of seconds to show the window.
        :param title: The title of the image window.
        """

        self.configure_colorized_image()

        self.display_image(
            image=self.colorized_img, interval=interval, title=title
        )
    # end display_colorized_image

    @staticmethod
    def save_image(image: np.array, saving_path: str) -> None:
        """
        Saves the given image object into a file by the file path

        :param image: The image object ot display.
        :param saving_path: The file path to save the image in.
        """

        cv2.imwrite(saving_path, image)
    # end save_image

    def save_org_image(self, saving_path: str) -> None:
        """
        Saves the given image object into a file by the file path

        :param saving_path: The file path to save the image in.
        """

        cv2.imwrite(saving_path, self.bw_img)
    # end save_image

    def save_colorized_image(self, saving_path: str) -> None:
        """
        Saves the given image object into a file by the file path

        :param saving_path: The file path to save the image in.
        """

        self.configure_colorized_image()

        cv2.imwrite(saving_path, self.colorized_img)
    # end save_image
# end Colorizer