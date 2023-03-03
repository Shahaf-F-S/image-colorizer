# save.py

from image_colorizer.base import suppress, run_silent_command

from specs import main as specs
from document import main as document

def main() -> None:
    """Runs the function to save thew project."""

    commands = [
        (lambda: run_silent_command("python setup.py sdist")),
        specs, lambda: document(location="image_colorizer")
    ]

    for command in commands:
        with suppress():
            command()
        # end suppress
    # end for
# end main

if __name__ == "__main__":
    main()
# end if