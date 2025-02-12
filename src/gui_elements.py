import tkinter as tk

class GUIManager:
    # Manages GUI elements and their creation for the application
    def __init__(self, root):
        # Initialize the GUI manager
        # Args:
        #     root: The root Tkinter window
        self.root = root
        self.font_default = ("Arial", 10)
        self.font_button = ("Arial", 12)

    def create_label_with_background(self, canvas, text, x, y, width, height, font=None):
        # Create a label with a semi-transparent background
        # Args:
        #     canvas: The Tkinter canvas to draw on
        #     text (str): Text to display in the label
        #     x (int): X coordinate for the label
        #     y (int): Y coordinate for the label
        #     width (int): Width of the label background
        #     height (int): Height of the label background
        #     font (tuple): Font tuple (family, size), defaults to self.font_default
        # Returns:
        #     tuple: (label, rectangle) The created label and its background rectangle
        if font is None:
            font = self.font_default
            
        rectangle = canvas.create_rectangle(
            x, y, x + width, y + height,
            fill="black",
            outline=""
        )
        label = tk.Label(self.root, text=text, font=font, bg="black", fg="white")
        label_window = canvas.create_window(x + 5, y + height // 2, anchor="w", window=label)
        return label, rectangle

    def create_continue_button(self, command):
        # Create a styled continue button
        # Args:
        #     command: Callback function for button click
        # Returns:
        #     Button: The created continue button
        button = tk.Button(
            self.root,
            text="Continue Hunt",
            command=command,
            font=self.font_button,
            bg="green",
            fg="white"
        )
        return button
