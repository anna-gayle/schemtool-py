import tkinter as tk
from tkinter.simpledialog import Dialog

class CanvasSizeDialog(Dialog):
    """
    A dialog window for entering new canvas dimensions.

    Attributes:
        width_entry (tk.Entry): Entry widget for the new canvas width.
        height_entry (tk.Entry): Entry widget for the new canvas height.

    Methods:
        body(master): Override of the Dialog class method.
            Creates the body of the dialog, including labels and entry widgets.

        apply(): Override of the Dialog class method.
            Validates and sets the result as a tuple of new canvas width and height.
    """

    def body(self, master):
        """
        Create the body of the dialog, including labels and entry widgets.

        Parameters:
            master (tk.Tk): The master window.

        Returns:
            tk.Entry: The entry widget for the new canvas width (initial focus).
        """
        tk.Label(master, text="Enter new canvas width:").grid(row=0, sticky="e")
        tk.Label(master, text="Enter new canvas height:").grid(row=1, sticky="e")

        self.width_entry = tk.Entry(master)
        self.height_entry = tk.Entry(master)

        self.width_entry.grid(row=0, column=1)
        self.height_entry.grid(row=1, column=1)

        return self.width_entry  # Initial focus

    def apply(self):
        """
        Validate and set the result as a tuple of new canvas width and height.

        If the input values are valid positive integers, sets the result.
        Otherwise, sets the result to None.

        Returns:
            None
        """
        new_width = self.width_entry.get()
        new_height = self.height_entry.get()

        try:
            new_width = int(new_width)
            new_height = int(new_height)

            if new_width > 0 and new_height > 0:
                self.result = new_width, new_height
            else:
                self.result = None
        except ValueError:
            self.result = None
