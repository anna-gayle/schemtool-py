import tkinter as tk
from PIL import Image, ImageTk

class ComponentInstance:
    """
    Represents an instance of a component on the canvas in a schematic designer tool.

    Attributes:
        canvas (tk.Canvas): The canvas where the component instance is displayed.
        schematic_designer (SchematicDesigner): The parent schematic designer tool.
        symbol_name (str): The name of the component symbol.
        x (int): The x-coordinate of the component instance on the canvas.
        y (int): The y-coordinate of the component instance on the canvas.
        rotation_angle (int): The rotation angle of the component image (in degrees).

        tk_symbol_image (ImageTk.PhotoImage): The Tkinter-compatible image for displaying on the canvas.
        item (int): The item ID representing the component instance on the canvas.

    Methods:
        __init__(self, canvas, symbol_name, x, y, schematic_designer): Constructor method.
            Initializes the component instance with the given parameters.

        rotate_on_click(self, event): Event handler for rotating the component image on a click.
            Rotates the image by 45 degrees on each click.

        load_symbol_image(self): Loads the symbol image for the component instance.
            Returns the Tkinter-compatible image, or None if the image is not found.
    """

    def __init__(self, canvas, symbol_name, x, y, schematic_designer):
        self.canvas = canvas
        self.schematic_designer = schematic_designer
        self.symbol_name = symbol_name
        self.x = x
        self.y = y
        self.rotation_angle = 0

        # Load the symbol image
        self.original_image = self.load_symbol_image()

        if self.original_image:
            # Create the image item on the canvas
            self.tk_symbol_image = ImageTk.PhotoImage(self.original_image)
            self.item = self.canvas.create_image(x, y, image=self.tk_symbol_image, anchor=tk.NW, tags=("clickable",))

            # Bind events for rotation
            self.canvas.tag_bind(self.item, '<Button-1>', self.rotate_on_click)
        else:
            # If the image loading fails, print a warning
            print(f"Warning: Failed to load symbol image for {symbol_name}")

    def rotate_on_click(self, event):
        """
        Event handler for rotating the component image on a click.

        Rotates the image by 45 degrees on each click.

        Parameters:
            event (tk.Event): The Tkinter event object.
        """
        if self.schematic_designer.selected_tool == "rotate.png":
            # Update the rotation angle
            selected_component = self.schematic_designer.get_component_instance_by_item(self.item)
            if selected_component:
                self.rotation_angle += 45
                self.rotation_angle %= 360  # Ensure the angle is within [0, 360)

                # Rotate the image
                rotated_image = self.original_image.rotate(self.rotation_angle, expand=True)
                self.tk_symbol_image = ImageTk.PhotoImage(rotated_image)

                # Update the image item on the canvas
                self.canvas.itemconfig(self.item, image=self.tk_symbol_image)

    def load_symbol_image(self):
        """
        Loads the symbol image for the component instance.

        Returns:
            Image or None: The original PIL Image,
            or None if the image is not found.
        """
        image_directory = "assets/component_symbols/"
        try:
            image_path = image_directory + self.symbol_name
            tk_symbol_image = Image.open(image_path)
            tk_symbol_image = tk_symbol_image.resize((120, 60), Image.BICUBIC)
            return tk_symbol_image
        except FileNotFoundError:
            return None
