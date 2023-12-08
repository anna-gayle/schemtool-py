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

        image (Image.Image): The original symbol image.
        tk_image (ImageTk.PhotoImage): The Tkinter-compatible image for displaying on the canvas.
        item (int): The item ID representing the component instance on the canvas.

    Methods:
        __init__(canvas, symbol_name, x, y, schematic_designer): Constructor method.
            Initializes the component instance with the given parameters.

        rotate_on_click(event): Event handler for rotating the component image on a click.
            Rotates the image by 45 degrees on each click.

        load_symbol_image(): Loads the symbol image for the component instance.
            Returns the Tkinter-compatible image, or None if the image is not found.
    """

    def __init__(self, canvas, symbol_name, x, y, schematic_designer):
        """
        Initialize the component instance with the given parameters.

        Parameters:
            canvas (tk.Canvas): The canvas where the component instance is displayed.
            symbol_name (str): The name of the component symbol.
            x (int): The x-coordinate of the component instance on the canvas.
            y (int): The y-coordinate of the component instance on the canvas.
            schematic_designer (SchematicDesigner): The parent schematic designer tool.
        """
        self.canvas = canvas
        self.schematic_designer = schematic_designer
        self.symbol_name = symbol_name
        self.x = x
        self.y = y
        self.rotation_angle = 0  

        # Load the symbol image
        self.image = Image.open(f"assets/component_symbols/{symbol_name}")
        self.image = self.image.resize((120, 60), Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Create the image item on the canvas
        self.item = self.canvas.create_image(x, y, image=self.tk_image, anchor=tk.NW, tags=("clickable",))

        # Bind events for rotation
        self.canvas.tag_bind(self.item, '<Button-1>', self.rotate_on_click)

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
                rotated_image = self.image.rotate(self.rotation_angle, expand=True)
                rotated_tk_image = ImageTk.PhotoImage(rotated_image)

                # Update the image item on the canvas
                self.canvas.itemconfig(self.item, image=rotated_tk_image)
                self.tk_image = rotated_tk_image  # Update the reference to the rotated image

    def load_symbol_image(self):
        """
        Loads the symbol image for the component instance.

        Returns:
            ImageTk.PhotoImage or None: The Tkinter-compatible image,
            or None if the image is not found.
        """
        image_directory = "assets/component_symbols/"
        try:
            image_path = image_directory + self.symbol_name
            tk_symbol_image = Image.open(image_path)
            tk_symbol_image = tk_symbol_image.resize((120, 60), Image.BICUBIC)
            return ImageTk.PhotoImage(tk_symbol_image)
        except FileNotFoundError:
            return None
