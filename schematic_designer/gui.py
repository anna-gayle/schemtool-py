import tkinter as tk
import json
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
from tkinter import filedialog
from .component_instance import ComponentInstance
from .tooltip import ToolTip
from .cd_box import CanvasSizeDialog
from .user_guide import UserGuideDialog

class SchematicDesigner:
    """
    SchematicDesigner class for creating a simple schematic designer tool using Tkinter.

    Attributes:
        root (tk.Tk): The root Tkinter window.
        menu_bar (tk.Menu): The menu bar for the application.
        tools_frame (ttk.LabelFrame): The frame containing tool buttons.
        symbol_images (dict): Dictionary to store images for component symbols.
        component_count (int): Counter for the number of components.
        component_instances (list): List to store instances of ComponentInstance.

    Methods:
        __init__(self, root): Initializes the SchematicDesigner instance.
        get_component_instance_by_item(self, item_id): Returns a component instance based on the item ID.
        setup_menu_bar(self): Sets up the menu bar with file and user guide menus.
        setup_tools(self): Sets up the tools frame with tool buttons and tooltips.
        handle_tool_click(self, tool_name): Handles clicks on tool buttons.
        toggle_tool(self, tool_name): Toggles the state of various tools.
        setup_component_library(self): Sets up the component library frame with component buttons and tooltips.
        spawn_symbol(self, symbol_name): Spawns a component symbol on the canvas.
        setup_canvas(self): Sets up the main canvas for drawing.
        setup_events(self): Sets up event bindings for canvas interactions.
        move_tool_arrow_key(self, event, direction): Handles arrow key events for the move tool.
        click_on_item(self, event): Handles clicks on items within the canvas.
        reset_selection(self): Resets the selected item.
        perform_delete_selected_components(self, item_id): Deletes selected components from the canvas.
        draw_grid(self, event=None): Draws a grid on the canvas.
        save(self): Saves the current state of the canvas to a JSON file.
        export_as_png(self): Exports the canvas as a PNG image.
        open_file(self): Opens a JSON file and loads the data onto the canvas.
        reset_canvas(self): Clears the canvas and resets tool-related states.
        load_from_file(self, filename): Loads data from a JSON file onto the canvas.
        open_user_guide(self): Opens the user guide dialog.
        change_canvas_size(self): Opens a dialog to change the canvas size.
        clear_canvas(self): Clears the canvas and resets tool-related states.
        draw(self, event): Handles drawing events based on the selected tool.
        draw_move_tool(self, event): Handles drawing events for the move tool.
        draw_move_tool_start(self, event): Initializes the move tool when the canvas is clicked.
        update_tool_state(self): Updates the visual state of tool buttons.

    """
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Schematic Designer Tool")
        self.setup_menu_bar()
        self.setup_tools()
        self.symbol_images = {}
        self.setup_component_library()
        self.setup_canvas()
        self.setup_events()
        self.prev_x, self.prev_y = None, None
        self.selected_item, self.selected_tool = None, None
        self.grid_enabled, self.delete_enabled, self.selection_active, self.rotation_enabled = False, False, False, False
        self.component_count = 0
        self.component_instances = []

    def get_component_instance_by_item(self, item_id):
        for component_instance in self.component_instances:
            # Convert the item_id to a string for comparison
            if str(component_instance.item) == str(item_id):
                return component_instance
        return None

    def setup_menu_bar(self):
        self.menu_bar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Export as PNG", command=self.export_as_png)
        file_menu.add_command(label="Open...", command=self.open_file)  
        file_menu.add_command(label="Change Canvas Size", command=self.change_canvas_size)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # User Guide menu
        user_guide_menu = tk.Menu(self.menu_bar, tearoff=False)
        user_guide_menu.add_command(label="Open User Guide", command=self.open_user_guide)
        self.menu_bar.add_cascade(label="Help", menu=user_guide_menu)

        self.root.config(menu=self.menu_bar)

    def setup_tools(self):
        # Create and configure the frame for tool buttons
        self.tools_frame = ttk.LabelFrame(self.root, text="Tool Library")
        self.tools_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # List of tool icons to be displayed
        tool_icons = [
            "move.png",
            "delete.png",
            "rotate.png",
            "grid.png",
            "clear.png" 
        ]

        # Dictionary to store tool buttons
        self.tool_buttons = {}
        col_count, row_count = 0, 0

        # Iterate through tool icons and create buttons
        for icon_name in tool_icons:
            # Open and resize tool icon image
            tool_icon = Image.open(f"assets/tool_icons/{icon_name}")
            tool_icon = tool_icon.resize((30, 30), Image.BICUBIC)
            tool_image = ImageTk.PhotoImage(tool_icon)

            # Create tool button with appropriate command
            if icon_name == "clear.png":
                tool_button = ttk.Button(self.tools_frame, image=tool_image, command=self.clear_canvas)
            else:
                tool_button = ttk.Button(self.tools_frame, image=tool_image, command=lambda i=icon_name: self.toggle_tool(i))

            tool_button.image = tool_image
            tool_button.grid(row=row_count, column=col_count, padx=5, pady=5)

            # Store button in the dictionary
            self.tool_buttons[icon_name] = tool_button

            # Create and bind tooltips to tool buttons
            tooltip_text = f"{icon_name[:-4].replace('_', ' ').capitalize()} Tool"
            ToolTip(tool_button, tooltip_text)

            col_count += 1

            # Reset column count and increment row count for a new row
            if col_count > 1:
                col_count, row_count = 0, row_count + 1

    def toggle_tool(self, tool_name):
        # Deselect all tool buttons
        for name, button in self.tool_buttons.items():
            button.state(('!pressed',))

        # Toggle specific tool based on tool_name
        if tool_name == "move.png":
            # Toggle move tool
            self.selection_active = not self.selection_active
            self.selected_tool = tool_name
            self.reset_selection()
            self.update_tool_state()
        elif tool_name == "grid.png":
            # Toggle grid tool
            self.grid_enabled = not self.grid_enabled
            self.selected_tool = tool_name
            self.draw_grid(None) if self.grid_enabled else self.canvas.delete("grid_line")
            self.update_tool_state()
        elif tool_name == "rotate.png":
            # Toggle rotate tool
            self.rotation_enabled = not self.rotation_enabled
            self.selected_tool = tool_name
            self.update_tool_state()
        elif tool_name == "delete.png":
            # Toggle delete tool
            self.delete_enabled = not self.delete_enabled
            self.selected_tool = tool_name
            self.update_tool_state()
        else:
            # Set the selected tool
            self.selected_tool = tool_name
            self.selection_active = False
            self.rotation_enabled = False
            self.update_tool_state()

    def setup_component_library(self):
        # Create and configure Component Library frame
        self.component_library_frame = ttk.LabelFrame(self.root, text="Component Library")
        self.component_library_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # List of component icons
        component_icons = [
            "battery.png", "capacitor.png",
            "diode.png", "fuse.png",
            "ground.png", "inductor.png",
            "led.png", "op_amp.png",
            "potentiometer.png", "resistor.png",
            "switch.png", "transformer.png",
            "transistor.png", "wire.png",
            "lamp.png"
        ]

        col_count, row_count = 0, 0

        for icon_name in component_icons:
            # Load component icon
            component_icon = Image.open(f"assets/component_icons/{icon_name}")
            component_icon = component_icon.resize((30, 30), Image.BICUBIC)
            component_image = ImageTk.PhotoImage(component_icon)

            # Store component image for reference
            self.symbol_images[icon_name] = component_image

            # Create component button
            component_button = ttk.Button(self.component_library_frame, image=component_image,
                                        command=lambda i=icon_name: self.spawn_symbol(i))
            component_button.image = component_image
            component_button.grid(row=row_count, column=col_count, padx=5, pady=5)

            # Tooltip for each component button
            tooltip_text = f"Add {icon_name[:-4].replace('_', ' ')}"
            ToolTip(component_button, tooltip_text.capitalize())

            col_count += 1

            if col_count > 1:
                col_count, row_count = 0, row_count + 1

    def spawn_symbol(self, symbol_name):
        # Get canvas width and height
        canvas_width, canvas_height = self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()

        # Set initial position for the new symbol
        symbol_x, symbol_y = canvas_width - 80, 40

        # Directory containing component symbols
        image_directory = "assets/component_symbols/"

        try:
            # Load the symbol image
            image_path = image_directory + symbol_name
            tk_symbol_image = Image.open(image_path)
            tk_symbol_image = tk_symbol_image.resize((120, 60), Image.BICUBIC)
            tk_symbol_image = ImageTk.PhotoImage(tk_symbol_image)

            # Store the symbol image for reference
            self.symbol_images[symbol_name] = tk_symbol_image
        except FileNotFoundError:
            # If the file is not found, return without creating the component instance
            return

        # Create a new component instance on the canvas
        component_instance = ComponentInstance(self.canvas, symbol_name, symbol_x, symbol_y, self)
        
        # Append the new component instance to the list
        self.component_instances.append(component_instance)

    def setup_canvas(self):
        # Create and configure the canvas frame
        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")

        # Set initial canvas dimensions
        self.canvas_width, self.canvas_height = 800, 600

        # Create the canvas with specified attributes
        self.canvas = tk.Canvas(self.canvas_frame, width=self.canvas_width, height=self.canvas_height, bg="white",
                                bd=3, relief=tk.SUNKEN)

        # Pack and expand the canvas to fill available space
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Configure the root column to expand the canvas
        self.root.grid_columnconfigure(1, weight=1)


    def setup_events(self):
        # Bind mouse events for drawing, clicking, and right-clicking on the canvas
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-1>", lambda event: self.click_on_item(event))
        self.canvas.bind("<Button-3>", self.draw_move_tool_start)
        self.canvas.bind("<Configure>", self.draw_grid)

        # Bind arrow keys for the move tool
        # self.canvas.bind("<Left>", lambda event: self.move_tool_arrow_key(event, "left"))
        # self.canvas.bind("<Right>", lambda event: self.move_tool_arrow_key(event, "right"))
        # self.canvas.bind("<Up>", lambda event: self.move_tool_arrow_key(event, "up"))
        # self.canvas.bind("<Down>", lambda event: self.move_tool_arrow_key(event, "down"))

    '''
    def move_tool_arrow_key(self, event, direction):
        # Handle arrow key presses for the move tool
        if self.selected_tool == "move.png" and self.selection_active and self.selected_item:
            delta_x, delta_y = 0, 0

            if direction == "left":
                delta_x = -5
            elif direction == "right":
                delta_x = 5
            elif direction == "up":
                delta_y = -5
            elif direction == "down":
                delta_y = 5

            # Move the selected item on the canvas
            self.canvas.move(self.selected_item, delta_x, delta_y)
            self.prev_x, self.prev_y = event.x, event.y
    '''

    def click_on_item(self, event):
        # Handle click events based on the selected tool
        if self.rotation_enabled and self.selected_tool == "rotate.png":
            # Rotate the selected component by 90 degrees
            if self.selected_item:
                selected_component = self.get_component_instance_by_item(self.selected_item)
                if selected_component:
                    rotation_angle = 90
                    selected_component.rotate_on_click(rotation_angle)
        elif self.selection_active and self.selected_tool == "move.png":
            # Handle click events for the move tool
            overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
            for item in overlapping_items:
                if self.canvas.type(item) == "image":
                    # Select the clicked item for movement
                    self.reset_selection()
                    self.selected_item = item
                    self.prev_x, self.prev_y = event.x, event.y
        elif self.delete_enabled:
            # Handle click events for the delete tool
            overlapping_items = self.canvas.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)
            for item in overlapping_items:
                if self.canvas.type(item) == "image":
                    # Confirm and delete the selected item
                    result = tk.messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected item?")
                    if result:
                        self.perform_delete_selected_components(item)
        else:
            pass

    def reset_selection(self):
        # Reset the selected item to None
        self.selected_item = None


    def perform_delete_selected_components(self, item_id):
        # Delete the selected component and remove it from the canvas
        selected_component = self.get_component_instance_by_item(item_id)
        if selected_component:
            self.canvas.delete(item_id)
            self.component_instances.remove(selected_component)
            self.reset_selection()

    def draw_grid(self, event=None):
        # Draw grid lines on the canvas if grid is enabled
        if self.grid_enabled:
            self.canvas.delete("grid_line")

            canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()

            # Draw horizontal grid lines
            for i in range(0, canvas_height, 20):
                self.canvas.create_line(0, i, canvas_width, i, fill="gray", tags="grid_line")

            # Draw vertical grid lines
            for i in range(0, canvas_width, 20):
                self.canvas.create_line(i, 0, i, canvas_height, fill="gray", tags="grid_line")


    def save(self):
        # Save schematic data to a JSON file
        save_data = {
            "canvas_size": (self.canvas_width, self.canvas_height),
            "component_instances": [
                {
                    "symbol_name": instance.symbol_name,
                    "x": instance.x,
                    "y": instance.y,
                }
                for instance in self.component_instances
            ],
        }

        filename = "schematic_save.json"
        with open(filename, "w") as file:
            json.dump(save_data, file)


    def export_as_png(self):
        # Export the canvas content as a PNG file
        x = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Ask user for the file path to save the PNG file
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            screenshot.save(file_path, "PNG")

    def open_file(self):
        # Open a JSON file dialog and load data from the selected file
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_from_file(file_path)


    def reset_canvas(self):
        # Reset the canvas by deleting all items and clearing component instances
        self.canvas.delete("all")
        self.component_instances = []


    def load_from_file(self, filename):
        # Load schematic data from a JSON file and create component instances on the canvas
        # Clear the canvas before loading new data
        self.reset_canvas()

        with open(filename, "r") as file:
            data = json.load(file)

            for instance_data in data.get("component_instances", []):
                symbol_name = instance_data.get("symbol_name")
                x = instance_data.get("x")
                y = instance_data.get("y")

                if symbol_name and x is not None and y is not None:
                    component_instance = ComponentInstance(self.canvas, symbol_name, 0, 0, self)
                    
                    # Set the coordinates for the component instance on the canvas
                    self.canvas.coords(component_instance.item, x, y)
                    
                    self.component_instances.append(component_instance)

    def open_user_guide(self):
        # Open a user guide dialog to display information about the Schematic Designer
        user_guide_dialog = UserGuideDialog(self.root)


    def change_canvas_size(self):
        # Open a dialog to change the canvas size and update canvas dimensions if a valid size is provided
        canvas_size_dialog = CanvasSizeDialog(self.root, title="Canvas Size")
        result = canvas_size_dialog.result

        if result is not None:
            new_width, new_height = result
            self.canvas.config(width=new_width, height=new_height)

    def clear_canvas(self):
        # Clear the canvas, disable grid, reset tool states, and update tool buttons
        self.canvas.delete("all")
        self.grid_enabled = False
        self.selection_active = False
        self.rotation_enabled = False
        self.delete_enabled = False
        self.update_tool_state()


    def draw(self, event):
        # Draw based on the selected tool (e.g., move or grid)
        if self.selected_tool == "move.png":
            self.draw_move_tool(event)
        elif self.selected_tool == "grid.png":
            self.draw_grid(event)

    def draw_move_tool(self, event):
        # Move the selected item on the canvas if the move tool is active
        if self.selected_item and self.prev_x is not None and self.prev_y is not None:
            delta_x, delta_y = event.x - self.prev_x, event.y - self.prev_y
            self.canvas.move(self.selected_item, delta_x, delta_y)
            self.prev_x, self.prev_y = event.x, event.y

    def draw_move_tool_start(self, event):
        # Initialize the starting coordinates when the move tool is activated
        if self.selection_active and self.selected_tool == "move.png":
            self.prev_x, self.prev_y = event.x, event.y


    def update_tool_state(self):
        # Update the state of tool buttons based on the active tools
        self.tool_buttons["grid.png"].state(('pressed',) if self.grid_enabled else ('!pressed',))
        self.tool_buttons["move.png"].state(('pressed',) if self.selection_active else ('!pressed',))
        self.tool_buttons["rotate.png"].state(('pressed',) if self.rotation_enabled else ('!pressed',))
        self.tool_buttons["delete.png"].state(('pressed',) if self.delete_enabled else ('!pressed',))

if __name__ == "__main__":
    # Create the main Tkinter window and run the Schematic Designer application
    root = tk.Tk()
    app = SchematicDesigner(root)
    root.mainloop()

