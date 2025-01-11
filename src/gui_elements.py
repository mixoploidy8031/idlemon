import tkinter as tk

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.font_default = ("Arial", 10)
        self.font_button = ("Arial", 12)

    def create_label_with_background(self, canvas, text, x, y, width, height, font=None):
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
        button = tk.Button(
            self.root,
            text="Continue Hunt",
            command=command,
            font=self.font_button,
            bg="green",
            fg="white"
        )
        return button
