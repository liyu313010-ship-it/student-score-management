import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from student_data import StudentData
from student_analysis import ScoreAnalysis

# 【实例化对象】
db_manager = StudentData()
score_analysis = ScoreAnalysis()

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("学生成绩管理系统")
        self.root.geometry("800x600")
        
        # 设置窗口图标和样式
        self.setup_style()
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建主内容区域
        self.create_main_content()
    
    def setup_style(self):
        """设置界面样式"""
        style = ttk.Style()
        style.configure("TLabel", font=(", 12"))
        style.configure("TButton", font=(", 12"))
        style.configure("TFrame", background="#f0f0f0")
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 成绩管理菜单
        grade_menu = tk.Menu(menubar, tearoff=0)
        grade_menu.add_command(label="录入成绩", command=self.input_score)
        grade_menu.add_command(label="查询成绩", command=self.query_score)
        grade_menu.add_command(label="修改成绩", command=self.update_score)
        grade_menu.add_command(label="删除学生信息", command=self.delete_student)
        menubar.add_cascade(label="成绩管理", menu=grade_menu)
        
        # 统计分析菜单
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(label="成绩排名", command=self.rank_output)
        analysis_menu.add_command(label="计算平均分", command=self.calculate_averages)
        analysis_menu.add_command(label="统计成绩方差", command=self.calculate_variance)
        analysis_menu.add_command(label="分数段分布统计", command=self.score_distribution_analysis)
        menubar.add_cascade(label="统计分析", menu=analysis_menu)
        
        # 关于菜单
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="关于系统", command=self.about)
        menubar.add_cascade(label="关于", menu=about_menu)
        
        # 退出系统菜单项（顶级菜单）
        menubar.add_command(label="退出系统", command=self.root.quit)
        
        self.root.config(menu=menubar)
    
    def create_main_content(self):
        """创建主内容区域"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题标签
        title_label = ttk.Label(main_frame, text="学生成绩管理系统", font=("Arial", 24, "bold"))
        title_label.pack(pady=20)
        
        # 功能按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 创建按钮网格
        buttons = [
            ("录入成绩", self.input_score),
            ("查询成绩", self.query_score),
            ("修改成绩", self.update_score),
            ("删除学生信息", self.delete_student),
            ("成绩排名", self.rank_output),
            ("计算平均分", self.calculate_averages),
            ("统计成绩方差", self.calculate_variance),
            ("分数段分布统计", self.score_distribution_analysis)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, width=15)
            btn.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_var.set("欢迎使用学生成绩管理系统")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.pack(side=tk.BOTTOM, pady=10)
    
    def input_score(self):
        """录入成绩GUI"""
        try:
            # 创建录入窗口
            input_window = tk.Toplevel(self.root)
            input_window.title("录入成绩")
            input_window.geometry("500x500")
            
            # 创建输入表单
            form_frame = ttk.Frame(input_window, padding="20")
            form_frame.pack(fill=tk.BOTH, expand=True)
            
            fields = ["学号", "姓名", "性别", "年龄", "班级", "语文", "数学", "英语", "Python程序设计"]
            entries = {}
            
            for i, field in enumerate(fields):
                label = ttk.Label(form_frame, text=f"{field}:")
                label.grid(row=i, column=0, sticky="w", pady=5)
                
                if field == "性别":
                    # 性别使用下拉菜单
                    combo = ttk.Combobox(form_frame, values=["男", "女"], width=30)
                    combo.grid(row=i, column=1, pady=5)
                    entries[field] = combo
                else:
                    entry = ttk.Entry(form_frame, width=30)
                    entry.grid(row=i, column=1, pady=5)
                    entries[field] = entry
            
            def save_score():
                """保存成绩"""
                try:
                    student_id = entries["学号"].get().strip()
                    name = entries["姓名"].get().strip()
                    gender = entries["性别"].get().strip()
                    age = entries["年龄"].get().strip()
                    grade_class = entries["班级"].get().strip()
                    
                    # 获取成绩
                    scores = {}
                    for subject in ["语文", "数学", "英语", "Python程序设计"]:
                        score_text = entries[subject].get().strip()
                        if not score_text:
                            messagebox.showerror("错误", f"请输入{subject}成绩")
                            return
                        scores[subject] = float(score_text)
                    
                    # 验证输入
                    if not student_id:
                        messagebox.showerror("错误", "请输入学号")
                        return
                    if not name:
                        messagebox.showerror("错误", "请输入姓名")
                        return
                    if gender not in ["男", "女"]:
                        messagebox.showerror("错误", "性别必须是'男'或'女'")
                        return
                    if not age.isdigit():
                        messagebox.showerror("错误", "年龄必须是数字")
                        return
                    
                    # 保存到数据库
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    # 检查学号是否存在
                    cursor.execute("SELECT 学号 FROM students WHERE 学号=%s", (student_id,))
                    if cursor.fetchone():
                        messagebox.showerror("错误", "该学号已存在，请勿重复录入！")
                        return
                    
                    # 插入数据
                    sql = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (student_id, name, gender, age, grade_class, 
                                       scores["语文"], scores["数学"], scores["英语"], scores["Python程序设计"]))
                    conn.commit()
                    
                    messagebox.showinfo("成功", f"恭喜你！学号为{student_id}, 名字为{name}的学生成绩已经录入。")
                    input_window.destroy()
                    self.status_var.set(f"已成功录入学号为{student_id}的学生成绩")
                    
                except Exception as e:
                    messagebox.showerror("错误", f"录入失败: {str(e)}")
                finally:
                    if 'conn' in locals() and conn.is_connected():
                        cursor.close()
                        conn.close()
            
            # 保存按钮
            save_btn = ttk.Button(form_frame, text="保存", command=save_score)
            save_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("错误", f"打开录入窗口失败: {str(e)}")
    
    def query_score(self):
        """查询成绩GUI"""
        try:
            student_id = simpledialog.askstring("查询成绩", "请输入学号:")
            if not student_id:
                return
            
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE 学号=%s", (student_id,))
            result = cursor.fetchone()
            
            if result:
                # 创建结果窗口
                result_window = tk.Toplevel(self.root)
                result_window.title(f"{result[1]}的成绩")
                result_window.geometry("400x300")
                
                frame = ttk.Frame(result_window, padding="20")
                frame.pack(fill=tk.BOTH, expand=True)
                
                fields = ["学号", "姓名", "性别", "年龄", "班级", "语文", "数学", "英语", "Python程序设计"]
                for i, (field, value) in enumerate(zip(fields, result)):
                    ttk.Label(frame, text=f"{field}:", width=15).grid(row=i, column=0, sticky="w", pady=5)
                    ttk.Label(frame, text=value).grid(row=i, column=1, sticky="w", pady=5)
                
                self.status_var.set(f"已查询学号为{student_id}的学生成绩")
            else:
                messagebox.showinfo("提示", "未找到该学号的学生记录")
        except Exception as e:
            messagebox.showerror("错误", f"查询失败: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def update_score(self):
        """修改成绩GUI"""
        try:
            student_id = simpledialog.askstring("修改成绩", "请输入要修改的学号:")
            if not student_id:
                return
            
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE 学号=%s", (student_id,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showinfo("提示", "未找到该学号的学生记录")
                return
            
            # 创建修改窗口
            update_window = tk.Toplevel(self.root)
            update_window.title(f"修改{result[1]}的成绩")
            update_window.geometry("500x500")
            
            frame = ttk.Frame(update_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            fields = ["学号", "姓名", "性别", "年龄", "班级", "语文", "数学", "英语", "Python程序设计"]
            entries = {}
            
            for i, (field, value) in enumerate(zip(fields, result)):
                ttk.Label(frame, text=f"{field}:", width=15).grid(row=i, column=0, sticky="w", pady=5)
                
                if field == "性别":
                    combo = ttk.Combobox(frame, values=["男", "女"], width=30)
                    combo.set(value)
                    combo.grid(row=i, column=1, pady=5)
                    entries[field] = combo
                elif field == "学号":
                    # 学号不可修改
                    entry = ttk.Entry(frame, width=30)
                    entry.insert(0, value)
                    entry.config(state="disabled")
                    entry.grid(row=i, column=1, pady=5)
                    entries[field] = entry
                else:
                    entry = ttk.Entry(frame, width=30)
                    entry.insert(0, value)
                    entry.grid(row=i, column=1, pady=5)
                    entries[field] = entry
            
            def save_update():
                """保存修改"""
                try:
                    update_data = {}
                    for field in fields:
                        if field == "学号":
                            continue
                        if field == "性别":
                            value = entries[field].get().strip()
                        else:
                            value = entries[field].get().strip()
                        
                        if not value:
                            messagebox.showerror("错误", f"请输入{field}")
                            return
                        
                        # 验证数值字段
                        if field in ["年龄", "语文", "数学", "英语", "Python程序设计"]:
                            if field == "年龄":
                                int(value)
                            else:
                                float(value)
                        
                        update_data[field] = value
                    
                    # 执行更新
                    for field, value in update_data.items():
                        sql = f"UPDATE students SET {field}=%s WHERE 学号=%s"
                        cursor.execute(sql, (value, student_id))
                    
                    conn.commit()
                    messagebox.showinfo("成功", f"修改成功！")
                    update_window.destroy()
                    self.status_var.set(f"已成功修改学号为{student_id}的学生信息")
                except Exception as e:
                    messagebox.showerror("错误", f"修改失败: {str(e)}")
            
            # 保存按钮
            save_btn = ttk.Button(frame, text="保存修改", command=save_update)
            save_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("错误", f"修改失败: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def delete_student(self):
        """删除学生信息GUI"""
        try:
            student_id = simpledialog.askstring("删除学生信息", "请输入要删除的学号:")
            if not student_id:
                return
            
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 姓名 FROM students WHERE 学号=%s", (student_id,))
            res = cursor.fetchone()
            
            if not res:
                messagebox.showinfo("提示", "未找到该学生")
                return
            
            if messagebox.askyesno("确认删除", f"确定要删除【{res[0]}】吗？"):
                cursor.execute("DELETE FROM students WHERE 学号=%s", (student_id,))
                conn.commit()
                messagebox.showinfo("成功", "删除成功")
                self.status_var.set(f"已成功删除学号为{student_id}的学生信息")
        except Exception as e:
            messagebox.showerror("错误", f"删除失败: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    
    def rank_output(self):
        """成绩排名GUI"""
        try:
            # 获取学生数据
            df = score_analysis.get_data_from_db()
            if df is None:
                messagebox.showinfo("提示", "数据库中暂无学生数据，请先录入成绩。")
                return
            
            # 创建排名选择窗口
            rank_window = tk.Toplevel(self.root)
            rank_window.title("成绩排名")
            rank_window.geometry("600x500")
            
            frame = ttk.Frame(rank_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            # 排名科目选择
            ttk.Label(frame, text="请选择要查看的排名科目：", font=("Arial", 12)).pack(pady=10)
            
            subjects = score_analysis.score_fields + ["总分"]
            subject_var = tk.StringVar()
            subject_var.set(subjects[0])
            
            # 创建科目选择下拉菜单
            subject_combo = ttk.Combobox(frame, textvariable=subject_var, values=subjects, width=20)
            subject_combo.pack(pady=10)
            
            def show_rank():
                """显示排名结果"""
                target_subject = subject_var.get()
                
                # 执行排序并取前十名学生
                ranked_df = df.sort_values(by=target_subject, ascending=False).head(10).copy()
                ranked_df['排名'] = range(1, len(ranked_df) + 1)
                
                # 清空之前的结果
                for widget in result_frame.winfo_children():
                    widget.destroy()
                
                # 创建表格显示排名结果
                columns = ['排名', '学号', '姓名', '班级', target_subject]
                tree = ttk.Treeview(result_frame, columns=columns, show='headings')
                
                # 设置表头
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)
                
                # 添加数据
                for _, row in ranked_df.iterrows():
                    tree.insert('', tk.END, values=[row['排名'], row['学号'], row['姓名'], row['班级'], row[target_subject]])
                
                tree.pack(fill=tk.BOTH, expand=True)
                
                # 滚动条
                scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 显示排名按钮
            show_btn = ttk.Button(frame, text="显示排名", command=show_rank)
            show_btn.pack(pady=10)
            
            # 结果显示区域
            ttk.Label(frame, text="排名结果（前10名）：", font=("Arial", 12)).pack(pady=10)
            result_frame = ttk.Frame(frame, padding="10", relief=tk.SUNKEN)
            result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            
            self.status_var.set("已生成成绩排名")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成排名失败: {str(e)}")
    
    def calculate_averages(self):
        """计算平均分GUI"""
        try:
            # 获取学生数据
            df = score_analysis.get_data_from_db()
            if df is None:
                messagebox.showinfo("提示", "数据库中暂无学生数据，请先录入成绩。")
                return
            
            # 创建结果窗口
            avg_window = tk.Toplevel(self.root)
            avg_window.title("平均分统计")
            avg_window.geometry("400x300")
            
            frame = ttk.Frame(avg_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="平均分统计结果", font=("Arial", 14, "bold")).pack(pady=10)
            
            # 计算平均分
            averages = df[score_analysis.score_fields].mean()
            total_avg = df['总分'].mean()
            
            # 显示结果
            result_frame = ttk.Frame(frame, padding="10")
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            for i, (subject, avg) in enumerate(averages.items()):
                ttk.Label(result_frame, text=f"{subject} 平均分:", width=15, anchor="w").grid(row=i, column=0, sticky="w", pady=5)
                ttk.Label(result_frame, text=f"{avg:.2f}", width=10, anchor="e").grid(row=i, column=1, sticky="e", pady=5)
            
            # 总分平均分
            ttk.Label(result_frame, text="总分平均分:", width=15, anchor="w", font=("Arial", 10, "bold")).grid(row=len(averages), column=0, sticky="w", pady=10)
            ttk.Label(result_frame, text=f"{total_avg:.2f}", width=10, anchor="e", font=("Arial", 10, "bold")).grid(row=len(averages), column=1, sticky="e", pady=10)
            
            self.status_var.set("已计算平均分")
            
        except Exception as e:
            messagebox.showerror("错误", f"计算平均分失败: {str(e)}")
    
    def calculate_variance(self):
        """统计成绩方差GUI"""
        try:
            # 获取学生数据
            df = score_analysis.get_data_from_db()
            if df is None:
                messagebox.showinfo("提示", "数据库中暂无学生数据，请先录入成绩。")
                return
            
            # 创建结果窗口
            var_window = tk.Toplevel(self.root)
            var_window.title("成绩方差统计")
            var_window.geometry("400x350")
            
            frame = ttk.Frame(var_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="成绩方差统计结果", font=("Arial", 14, "bold")).pack(pady=10)
            
            # 计算方差
            variances = df[score_analysis.score_fields + ['总分']].var()
            
            # 显示结果
            result_frame = ttk.Frame(frame, padding="10")
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            for i, (subject, var) in enumerate(variances.items()):
                ttk.Label(result_frame, text=f"{subject} 方差:", width=15, anchor="w").grid(row=i, column=0, sticky="w", pady=5)
                ttk.Label(result_frame, text=f"{var:.2f}", width=10, anchor="e").grid(row=i, column=1, sticky="e", pady=5)
            
            # 添加方差说明
            ttk.Label(frame, text="", font=("Arial", 8)).pack(pady=5)
            ttk.Label(frame, text="方差说明：方差用于衡量成绩的离散程度，", font=("Arial", 8)).pack(pady=2)
            ttk.Label(frame, text="值越大表示成绩分布越分散，值越小表示成绩分布越集中。", font=("Arial", 8)).pack(pady=2)
            
            self.status_var.set("已统计成绩方差")
            
        except Exception as e:
            messagebox.showerror("错误", f"统计方差失败: {str(e)}")
    
    def score_distribution_analysis(self):
        """分数段分布统计GUI"""
        try:
            # 获取学生数据
            df = score_analysis.get_data_from_db()
            if df is None:
                messagebox.showinfo("提示", "数据库中暂无学生数据，请先录入成绩。")
                return
            
            # 计算每个学生的平均分
            df['平均分'] = df[score_analysis.score_fields].mean(axis=1)

            # 定义分数段划分标准
            bins = [0, 60, 70, 80, 90, 101]
            labels = ['0-60(不及格)', '60-70(及格)', '70-80(中等)', '80-90(良好)', '90-100(优秀)']
            
            # 将平均分划分到不同的分数段
            df['分数段'] = pd.cut(df['平均分'], bins=bins, labels=labels, right=False)
            
            # 统计各分数段的人数
            dist_counts = df['分数段'].value_counts().sort_index()
            # 计算总人数
            total_count = len(df)
            
            # 创建结果窗口
            dist_window = tk.Toplevel(self.root)
            dist_window.title("分数段分布统计")
            dist_window.geometry("500x400")
            
            frame = ttk.Frame(dist_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="分数段比例统计结果", font=("Arial", 14, "bold")).pack(pady=10)
            
            # 显示文字统计结果
            result_frame = ttk.Frame(frame, padding="10")
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            for i, (label, count) in enumerate(dist_counts.items()):
                percentage = (count / total_count) * 100
                ttk.Label(result_frame, text=f"{label}: ", width=15, anchor="w").grid(row=i, column=0, sticky="w", pady=5)
                ttk.Label(result_frame, text=f"{count}人 ", width=10, anchor="e").grid(row=i, column=1, sticky="e", pady=5)
                ttk.Label(result_frame, text=f"({percentage:.2f}%)", width=10, anchor="e").grid(row=i, column=2, sticky="e", pady=5)
            
            # 显示柱状图按钮
            def show_chart():
                """显示柱状图"""
                score_analysis._draw_distribution_chart(dist_counts, total_count)
            
            chart_btn = ttk.Button(frame, text="显示柱状图", command=show_chart)
            chart_btn.pack(pady=20)
            
            self.status_var.set("已生成分数段分布统计")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成分数段分布统计失败: {str(e)}")
    
    def about(self):
        """关于系统"""
        messagebox.showinfo("关于学生成绩管理系统", "学生成绩管理系统\n版本：1.0\n开发：Python实习项目")
