import tkinter as tk
import ctypes
from tkinter import colorchooser, simpledialog

class CrosshairOverlay(tk.Tk):
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

        # 定义准心的尺寸和颜色
        self.crosshair_size = 20
        self.crosshair_color = 'red'
        self.show_crosshair = True

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
        self.crosshair_lines = [
            self.canvas.create_line(center_x - self.crosshair_size, center_y, center_x + self.crosshair_size, center_y, fill=self.crosshair_color, width=2),
            self.canvas.create_line(center_x, center_y - self.crosshair_size, center_x, center_y + self.crosshair_size, fill=self.crosshair_color, width=2)
        ]

    def hide_crosshair(self):
        # 隐藏准心
        for line in self.crosshair_lines:
            self.canvas.itemconfig(line, state='hidden')

    def show_crosshair_again(self):
        # 显示准心
        for line in self.crosshair_lines:
            self.canvas.itemconfig(line, state='normal')

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
        self.menu_window.geometry("300x200")

        # 创建颜色选择按钮
        color_button = tk.Button(self.menu_window, text="Select Crosshair Color", command=self.select_color)
        color_button.pack(pady=10)

        # 创建尺寸选择按钮
        size_button = tk.Button(self.menu_window, text="Set Crosshair Size", command=self.set_size)
        size_button.pack(pady=10)

        # 创建关闭按钮
        close_button = tk.Button(self.menu_window, text="Close", command=self.close_menu)
        close_button.pack(pady=10)

    def select_color(self):
        # 弹出颜色选择对话框
        color = colorchooser.askcolor()[1]
        if color:
            self.crosshair_color = color
            self.redraw_crosshair()

    def set_size(self):
        # 弹出尺寸输入对话框
        size = simpledialog.askinteger("Crosshair Size", "Enter crosshair size:", minvalue=1, maxvalue=100)
        if size:
            self.crosshair_size = size
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

if __name__ == "__main__":
    app = CrosshairOverlay()
    app.mainloop()
