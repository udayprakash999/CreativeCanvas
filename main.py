import tkinter as tk
from tkinter import ttk, colorchooser

class Whiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Whiteboard")
        
        self.brush_color = "black"
        self.brush_size = 3
        self.is_erasing = False
        self.current_tool = "free_draw"
        self.eraser_id = None
        
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<Button-1>', self.start_draw)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_draw)
        
        self.create_buttons()
        
        self.start_x, self.start_y = None, None
        self.current_shape_id = None

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        
        color_button = ttk.Button(button_frame, text="🎨 Change Color", command=self.change_color, style="Accent.TButton")
        color_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="🗑️ Clear", command=self.clear_canvas, style="Danger.TButton")
        clear_button.pack(side=tk.LEFT, padx=5)
        
        eraser_button = ttk.Button(button_frame, text="🧹 Eraser", command=self.use_eraser, style="Accent.TButton")
        eraser_button.pack(side=tk.LEFT, padx=5)
        
        line_button = ttk.Button(button_frame, text="📏 Line", command=lambda: self.select_tool("line"), style="Accent.TButton")
        line_button.pack(side=tk.LEFT, padx=5)
        
        rect_button = ttk.Button(button_frame, text="▭ Rectangle", command=lambda: self.select_tool("rectangle"), style="Accent.TButton")
        rect_button.pack(side=tk.LEFT, padx=5)
        
        oval_button = ttk.Button(button_frame, text="⚪ Oval", command=lambda: self.select_tool("oval"), style="Accent.TButton")
        oval_button.pack(side=tk.LEFT, padx=5)
        
        free_draw_button = ttk.Button(button_frame, text="✏️ Free Draw", command=lambda: self.select_tool("free_draw"), style="Accent.TButton")
        free_draw_button.pack(side=tk.LEFT, padx=5)
        
        brush_size_label = tk.Label(button_frame, text="🖌️ Brush Size:", bg="#f0f0f0", font=("Helvetica", 12, "bold"))
        brush_size_label.pack(side=tk.LEFT, padx=5)
        
        self.brush_size_slider = tk.Scale(button_frame, from_=1, to=20, orient=tk.HORIZONTAL, command=self.change_brush_size, bg="#f0f0f0")
        self.brush_size_slider.set(self.brush_size)
        self.brush_size_slider.pack(side=tk.LEFT, padx=5)
        
    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.current_tool in ["line", "rectangle", "oval"]:
            self.current_shape_id = None

    def draw(self, event):
        x, y = event.x, event.y
        
        if self.is_erasing:
            self.display_eraser(x, y)
            self.canvas.create_oval(
                x - self.brush_size // 2, y - self.brush_size // 2, 
                x + self.brush_size // 2, y + self.brush_size // 2, 
                fill=self.canvas['bg'], outline=self.canvas['bg']
            )
        elif self.current_tool == "free_draw":
            if self.start_x is not None and self.start_y is not None:
                self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND, smooth=True)
            self.start_x, self.start_y = x, y
        elif self.current_tool in ["line", "rectangle", "oval"]:
            if self.current_shape_id:
                self.canvas.delete(self.current_shape_id)
            if self.current_tool == "line":
                self.current_shape_id = self.canvas.create_line(self.start_x, self.start_y, x, y, fill=self.brush_color, width=self.brush_size)
            elif self.current_tool == "rectangle":
                self.current_shape_id = self.canvas.create_rectangle(self.start_x, self.start_y, x, y, outline=self.brush_color, width=self.brush_size)
            elif self.current_tool == "oval":
                self.current_shape_id = self.canvas.create_oval(self.start_x, self.start_y, x, y, outline=self.brush_color, width=self.brush_size)

    def stop_draw(self, event):
        self.start_x, self.start_y = None, None

    def change_color(self):
        color = colorchooser.askcolor(title="Choose a color")[1]
        if color:
            self.brush_color = color
            self.is_erasing = False
    
    def use_eraser(self):
        self.brush_color = self.canvas['bg']
        self.is_erasing = True
        self.select_tool("free_draw")

    def change_brush_size(self, size):
        self.brush_size = int(size)

    def clear_canvas(self):
        self.canvas.delete('all')

    def select_tool(self, tool):
        self.current_tool = tool
        self.is_erasing = False

    def display_eraser(self, x, y):
        if self.eraser_id:
            self.canvas.delete(self.eraser_id)
        self.eraser_id = self.canvas.create_oval(
            x - self.brush_size // 2, y - self.brush_size // 2, 
            x + self.brush_size // 2, y + self.brush_size // 2, 
            outline="gray", width=2
        )

if __name__ == "__main__":
    root = tk.Tk()
    whiteboard = Whiteboard(root)
    root.mainloop()
