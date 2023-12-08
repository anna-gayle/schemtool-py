import tkinter as tk
from schematic_designer.gui import SchematicDesigner

if __name__ == "__main__":
    """
    Main script to launch the Schematic Designer application.

    This script creates a Tkinter window, sets up the Schematic Designer GUI, and starts the main event loop.

    Note:
        Ensure that the SchematicDesigner class is imported from the 'schematic_designer.gui' module.

    Example:
        Run this script to launch the Schematic Designer application.

    """
    root = tk.Tk()
    root.title("Schematic Designer")

    schematic_designer_frame = tk.Frame(root)
    schematic_designer_frame.grid(row=0, column=0, sticky="nsew")

    app = SchematicDesigner(root)

    root.mainloop()
