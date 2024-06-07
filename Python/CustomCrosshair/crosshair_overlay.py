import tkinter as tk
import ctypes
from tkinter import colorchooser, simpledialog, messagebox, filedialog, OptionMenu
import json
import os

class CrosshairOverlay(tk.Tk):
    CONFIG_FILE = "crosshair_config.json"

    def __init__(self):
        super().__init__()
        # 设置窗口属性：全屏、透明背景、置顶、无边框
        self.attributes("-fullscreen", True)
        self.attributes("-transparentcolor", "black")
        self.attributes("-topmost", True)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        self.overrideredirect(True)

        # 创建一个全屏的画布，背景色为黑色（透明色）
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg='black', highlightthickness=0)
        self.canvas.pack()

        # 加载配置
        self.load_config()

        # 绘制初始的准心
        self.draw_crosshair()

        # 开始监测鼠标右键状态
        self.update_crosshair_visibility()

        # 创建菜单界面
        self.create_menu()

    def draw_crosshair(self):
        # 在屏幕中心绘制一个十字准心
        center_x = self.winfo_screenwidth() // 2
        center_y = self.winfo_screenheight() // 2
        self.canvas.delete("all")

        # 绘制中心样式
        if self.crosshair_shape == "circle":
            self.canvas.create_oval(center_x - self.crosshair_width, center_y - self.crosshair_width,
                                    center_x + self.crosshair_width, center_y + self.crosshair_width,
                                    fill=self.crosshair_color, outline=self.crosshair_color)
        elif self.crosshair_shape == "square":
            self.canvas.create_rectangle(center_x - self.crosshair_width, center_y - self.crosshair_width,
                                         center_x + self.crosshair_width, center_y + self.crosshair_width,
                                         fill=self.crosshair_color, outline=self.crosshair_color)
        elif self.crosshair_shape == "hollow_circle":
            self.canvas.create_oval(center_x - self.crosshair_width, center_y - self.crosshair_width,
                                    center_x + self.crosshair_width, center_y + self.crosshair_width,
                                    outline=self.crosshair_color)
        elif self.crosshair_shape == "hollow_square":
            self.canvas.create_rectangle(center_x - self.crosshair_width, center_y - self.crosshair_width,
                                         center_x + self.crosshair_width, center_y + self.crosshair_width,
                                         outline=self.crosshair_color)
        elif self.crosshair_shape == "triangle":
            self.canvas.create_polygon(center_x, center_y - self.crosshair_width,
                                       center_x - self.crosshair_width, center_y + self.crosshair_width,
                                       center_x + self.crosshair_width, center_y + self.crosshair_width,
                                       fill=self.crosshair_color, outline=self.crosshair_color)

        # 绘制围绕中心点的样式
        if self.crosshair_lines_style == "lines":
            self.crosshair_lines = [
                self.canvas.create_line(center_x - self.crosshair_size - self.crosshair_distance - self.crosshair_gap, center_y,
                                        center_x - self.crosshair_gap, center_y,
                                        fill=self.crosshair_color, width=self.crosshair_width),
                self.canvas.create_line(center_x + self.crosshair_gap, center_y,
                                        center_x + self.crosshair_size + self.crosshair_distance + self.crosshair_gap, center_y,
                                        fill=self.crosshair_color, width=self.crosshair_width),
                self.canvas.create_line(center_x, center_y - self.crosshair_size - self.crosshair_distance - self.crosshair_gap,
                                        center_x, center_y - self.crosshair_gap,
                                        fill=self.crosshair_color, width=self.crosshair_width),
                self.canvas.create_line(center_x, center_y + self.crosshair_gap,
                                        center_x, center_y + self.crosshair_size + self.crosshair_distance + self.crosshair_gap,
                                        fill=self.crosshair_color, width=self.crosshair_width)
            ]
        elif self.crosshair_lines_style == "concentric_circle":
            self.canvas.create_oval(center_x - self.crosshair_size - self.crosshair_distance, center_y - self.crosshair_size - self.crosshair_distance,
                                    center_x + self.crosshair_size + self.crosshair_distance, center_y + self.crosshair_size + self.crosshair_distance,
                                    outline=self.crosshair_color, width=self.crosshair_width)
        elif self.crosshair_lines_style == "concentric_square":
            self.canvas.create_rectangle(center_x - self.crosshair_size - self.crosshair_distance, center_y - self.crosshair_size - self.crosshair_distance,
                                         center_x + self.crosshair_size + self.crosshair_distance, center_y + self.crosshair_size + self.crosshair_distance,
                                         outline=self.crosshair_color, width=self.crosshair_width)

    def hide_crosshair(self):
        # 隐藏准心
        self.canvas.itemconfig("all", state='hidden')

    def show_crosshair_again(self):
        # 显示准心
        self.canvas.itemconfig("all", state='normal')

    def update_crosshair_visibility(self):
        # 获取鼠标右键的状态
        state = ctypes.windll.user32.GetAsyncKeyState(0x02)  # 0x02 是右键的虚拟键码
        if state & 0x8000:  # 如果右键按下
            self.hide_crosshair()
        else:
            self.show_crosshair_again()

        # 每10毫秒检查一次鼠标状态
        self.after(10, self.update_crosshair_visibility)

    def create_menu(self):
        # 创建一个新的Tk窗口作为菜单
        self.menu_window = tk.Toplevel(self)
        self.menu_window.title("Crosshair Settings")
        self.menu_window.geometry("400x700")

        # 创建颜色选择按钮
        color_button = tk.Button(self.menu_window, text="Select Crosshair Color", command=self.select_color)
        color_button.pack(pady=10)

        # 创建形状选择次级菜单
        shape_label = tk.Label(self.menu_window, text="Select Crosshair Shape:")
        shape_label.pack(pady=5)
        self.shape_var = tk.StringVar(value=self.crosshair_shape)
        shapes = ["circle", "square", "hollow_circle", "hollow_square", "triangle"]
        shape_menu = OptionMenu(self.menu_window, self.shape_var, *shapes, command=self.update_shape)
        shape_menu.pack(pady=5)

        # 创建围绕中心点的样式选择次级菜单
        lines_label = tk.Label(self.menu_window, text="Select Lines Style:")
        lines_label.pack(pady=5)
        self.lines_var = tk.StringVar(value=self.crosshair_lines_style)
        lines_styles = ["lines", "concentric_circle", "concentric_square"]
        lines_menu = OptionMenu(self.menu_window, self.lines_var, *lines_styles, command=self.update_lines_style)
        lines_menu.pack(pady=5)

        # 创建尺寸滑动条
        size_label = tk.Label(self.menu_window, text="Crosshair Size:")
        size_label.pack(pady=5)
        self.size_slider = tk.Scale(self.menu_window, from_=1, to=100, orient=tk.HORIZONTAL, command=self.update_size)
        self.size_slider.set(self.crosshair_size)
        self.size_slider.pack(pady=5)

        # 创建宽度滑动条
        width_label = tk.Label(self.menu_window, text="Crosshair Width:")
        width_label.pack(pady=5)
        self.width_slider = tk.Scale(self.menu_window, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_width)
        self.width_slider.set(self.crosshair_width)
        self.width_slider.pack(pady=5)

        # 创建距离滑动条
        self.distance_label = tk.Label(self.menu_window, text="Line Distance from Center:")
        self.distance_label.pack(pady=5)
        self.distance_slider = tk.Scale(self.menu_window, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_distance)
        self.distance_slider.set(self.crosshair_distance)
        self.distance_slider.pack(pady=5)

        # 创建间隙滑动条
        self.gap_label = tk.Label(self.menu_window, text="Gap Between Line and Dot:")
        self.gap_label.pack(pady=5)
        self.gap_slider = tk.Scale(self.menu_window, from_=0, to=50, orient=tk.HORIZONTAL, command=self.update_gap)
        self.gap_slider.set(self.crosshair_gap)
        self.gap_slider.pack(pady=5)

        # 创建保存按钮
        save_button = tk.Button(self.menu_window, text="Save Settings", command=self.save_config)
        save_button.pack(pady=10)

        # 创建加载按钮
        load_button = tk.Button(self.menu_window, text="Load Settings", command=self.load_config_from_file)
        load_button.pack(pady=10)

        # 创建关闭按钮
        close_button = tk.Button(self.menu_window, text="Close", command=self.close_menu)
        close_button.pack(pady=10)

    def select_color(self):
        # 弹出颜色选择对话框
        color = colorchooser.askcolor()[1]
        if color:
            self.crosshair_color = color
            self.redraw_crosshair()

    def update_shape(self, val):
        self.crosshair_shape = self.shape_var.get()
        self.redraw_crosshair()

    def update_lines_style(self, val):
        self.crosshair_lines_style = self.lines_var.get()
        self.redraw_crosshair()

    def update_size(self, val):
        self.crosshair_size = int(val)
        self.redraw_crosshair()

    def update_width(self, val):
        self.crosshair_width = int(val)
        self.redraw_crosshair()

    def update_distance(self, val):
        self.crosshair_distance = int(val)
        self.redraw_crosshair()

    def update_gap(self, val):
        self.crosshair_gap = int(val)
        self.redraw_crosshair()

    def redraw_crosshair(self):
        # 删除旧的准心
        self.canvas.delete("all")
        # 绘制新的准心
        self.draw_crosshair()

    def close_menu(self):
        # 关闭菜单窗口并退出应用程序
        self.menu_window.destroy()
        self.quit_app()

    def quit_app(self):
        self.destroy()

    def load_config(self):
        # 加载配置文件
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)
            self.crosshair_size = config.get('size', 20)
            self.crosshair_color = config.get('color', 'red')
            self.crosshair_width = config.get('width', 2)
            self.crosshair_distance = config.get('distance', 10)
            self.crosshair_gap = config.get('gap', 5)
            self.crosshair_shape = config.get('shape', 'circle')
            self.crosshair_lines_style = config.get('lines_style', 'lines')
        else:
            self.crosshair_size = 20
            self.crosshair_color = 'red'
            self.crosshair_width = 2
            self.crosshair_distance = 10
            self.crosshair_gap = 5
            self.crosshair_shape = 'circle'
            self.crosshair_lines_style = 'lines'

    def load_config_from_file(self):
        # 从文件选择器加载配置文件
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                config = json.load(f)
            self.crosshair_size = config.get('size', 20)
            self.crosshair_color = config.get('color', 'red')
            self.crosshair_width = config.get('width', 2)
            self.crosshair_distance = config.get('distance', 10)
            self.crosshair_gap = config.get('gap', 5)
            self.crosshair_shape = config.get('shape', 'circle')
            self.crosshair_lines_style = config.get('lines_style', 'lines')
            self.redraw_crosshair()

    def save_config(self):
        # 保存配置文件
        config = {
            'size': self.crosshair_size,
            'color': self.crosshair_color,
            'width': self.crosshair_width,
            'distance': self.crosshair_distance,
            'gap': self.crosshair_gap,
            'shape': self.crosshair_shape,
            'lines_style': self.crosshair_lines_style
        }
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        messagebox.showinfo("Settings Saved", "Your crosshair settings have been saved.")

if __name__ == "__main__":
    app = CrosshairOverlay()
    app.mainloop()
