import tkinter as tk

class ToolTip:
    """
    Provides a tooltip for a Tkinter widget.

    Attributes:
        widget (tk.Widget): The widget for which the tooltip is displayed.
        text (str): The text content of the tooltip.
        tooltip (tk.Toplevel): The Toplevel window containing the tooltip.

    Methods:
        __init__(widget, text): Constructor method.
            Initializes the tooltip with the given widget and text.

        show_tooltip(event): Displays the tooltip on widget enter.
            Creates and positions the Toplevel window with the tooltip text.

        hide_tooltip(_): Hides the tooltip on widget leave.
            Destroys the Toplevel window containing the tooltip.
    """

    def __init__(self, widget, text):
        """
        Initialize the tooltip with the given widget and text.

        Parameters:
            widget (tk.Widget): The widget for which the tooltip is displayed.
            text (str): The text content of the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        """
        Displays the tooltip on widget enter.

        Creates and positions the Toplevel window with the tooltip text.

        Parameters:
            event (tk.Event): The Tkinter event object.
        """
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, justify="left", background="#ffffe0", relief="solid", borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tooltip(self, _):
        """
        Hides the tooltip on widget leave.

        Destroys the Toplevel window containing the tooltip.

        Parameters:
            _ (tk.Event): The Tkinter event object (not used).
        """
        if self.tooltip:
            self.tooltip.destroy()
