import tkinter as tk
from tkinter import messagebox

class UserGuideDialog(tk.Toplevel):
    """
    UserGuideDialog provides a dialog displaying the user guide for the Schematic Designer application.

    Attributes:
        parent (tk.Tk): The parent Tkinter window for the dialog.

    Methods:
        __init__(parent): Constructor method.
            Initializes the UserGuideDialog with the given parent window.

    Note:
        The dialog contains information about tool buttons, component libraries, menu options, and future developments.
        It also includes an "OK" button to close the dialog.
    """

    def __init__(self, parent):
        """
        Initialize the UserGuideDialog with the given parent window.

        Parameters:
            parent (tk.Tk): The parent Tkinter window for the dialog.
        """
        super().__init__(parent)
        self.title("User Guide")

        text = (
            "Welcome to the Schematic Designer User Guide!\n\n"
            "Tool Buttons:\n"
            "- Move Tool: Toggling this button will allow users to move items in the canvas.\n"
            "- Grid Tool: Toggle grid lines on/off for better alignment.\n"
            "- Rotate Tool: Toggling this button will rotate selected components by clicking on them.\n"
            "- Delete Tool: Toggling this button will delete selected components.\n\n"
            "- Clear Tool: Click to clear canvas.\n\n"
            "Note: Toggle buttons may be a little finicky, and might require toggling it again or another button. \n"
            "Try to keep one button toggled at a time.\n\n"
            "Component Libraries:\n"
            "- Basic Components: Contains essential components like resistors, capacitors, LEDs, etc.\n"
            "- Power Components: Includes power-related components like batteries, transformers, etc.\n"
            "- Advanced Components: Provides advanced components like op-amps, transistors, etc.\n"
            "- Wires: Offers symbols for connecting components using wires.\n\n"
            "Menu Options:\n"
            "- File -> Save: Save the current schematic.\n"
            "- File -> Export as PNG: Export the schematic as a PNG file.\n"
            "- File -> Change Canvas Size: Adjust the size of the canvas.\n"
            "- File -> Exit: Close the application.\n\n"
            "Coming Soon:\n"
            "- Snap functionality\n"
            "- More tools\n"
            "- Bug fixes\n"
            "- More schematic symbols\n"
            "- Optimization improvements\n"
            "- Quality of life improvements\n"
        )

        label = tk.Label(self, text=text, padx=10, pady=10)
        label.pack()

