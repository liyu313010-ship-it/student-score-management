from student_gui import StudentManagementGUI
import tkinter as tk

# 主程序入口
if __name__ == "__main__":
    # 创建GUI窗口
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()
