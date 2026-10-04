import mysql.connector
from mysql.connector import Error

class StudentData:
    """学生成绩数据库管理类：负责所有与 MySQL 数据库相关的交互"""

    def __init__(self):
        """构造函数：实例化对象时自动运行"""
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'student_grade_management',
            'charset': 'utf8mb4'
        }
        self.init_database() #进行数据库连接、执行sql语句、定义表结构

    def get_connection(self):
        """建立并返回一个数据库连接对象"""
        return mysql.connector.connect(**self.db_config) #使用字典解包语法，将配置参数传递给连接函数

    def init_database(self):
        """初始化数据库：仅在表不存在时创建表结构"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor() #创建数据库的游标对象，执行SQL语句
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    学号 VARCHAR(50) PRIMARY KEY,
                    姓名 VARCHAR(20),
                    性别 VARCHAR(5),
                    年龄 INT,
                    班级 VARCHAR(20),
                    语文 DECIMAL(4,1),
                    数学 DECIMAL(4,1),
                    英语 DECIMAL(4,1),
                    python程序设计 DECIMAL(4,1)
                )
            """)
            conn.commit()
        except Error as e:
            print(f"检查数据库时出错: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def get_valid_score(self, subject):
        """通用的成绩验证逻辑：包含3次机会提示"""
        frequency_num = 3
        frequency = 0
        while frequency < frequency_num:
            error_msg = "" #在每次输入尝试开始时，将 error_msg 重置为空字符串
            try:
                score_input = input(f"请输入{subject}成绩: ")
                score = float(score_input)
                if 0 <= score <= 100:
                    return score
                error_msg = "分数超出范围(0-100), 请重新输入"
            except ValueError:
                error_msg = "输入的格式有误，请输入数字"
            
            # 只要触发错误，立即增加计次并提示
            frequency += 1
            print(error_msg)
            attempt_remaining = frequency_num - frequency
            if attempt_remaining > 0:
                print(f"尊敬的管理员！您还有{attempt_remaining}次机会输入{subject}成绩")
        
        print(f"尊敬的管理员！您的3次输入机会已经用完了！")
        return 0

    def input_score(self):
        """录入学生成绩"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            while True:
                student_id = input("\n请输入学号 (输入quit退出): ")
                if student_id.lower() == 'quit':
                    break

                cursor.execute("SELECT 学号 FROM students WHERE 学号=%s", (student_id,))
                if cursor.fetchone(): #fetchone() 是 Cursor 对象的一个方法，用于从数据库中获取查询结果的下一行数据。Cursor 是由连接对象返回的
                    print("错误：该学号已存在，请勿重复录入！")
                    continue

                name = input("请输入姓名: ")
                while True:
                    gender = input("请输入性别: ")
                    if gender in ['男', '女']:
                        break
                    print("尊敬的管理员！性别输入错误哦，请输入“男”或“女”")

                age = input("请输入年龄: ")
                grade_class = input("请输入班级: ")
                print(f"尊敬的管理员！您录入成绩时每门科目有3次机会")

                # 调用提取后的验证方法
                chinese = self.get_valid_score("语文")
                math = self.get_valid_score("数学")
                english = self.get_valid_score("英语")
                python_project = self.get_valid_score("Python程序设计")

                sql = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (student_id, name, gender, age,
                               grade_class, chinese, math, english, python_project))
                conn.commit()
                print(f"恭喜你！学号为{student_id}, 名字为{name}的学生成绩已经录入。")

        except Error as e:
            print(f"录入失败: {e}")
        finally:
            cursor.close()
            conn.close()

    def query_score(self):
        """查询学生的成绩"""
        # 连接数据库
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            student_id = input("\n请输入学号 (输入quit退出): ")
            if student_id.lower() == 'quit':
                return

            sql = "SELECT * FROM students WHERE 学号=%s"
            cursor.execute(sql, (student_id,))
            result = cursor.fetchone()

            if result:
                #索引数据库对应的字段，打印学生信息
                print(f"学号: {result[0]}, 姓名: {result[1]}, 性别: {result[2]}, 年龄: {result[3]}, 班级: {result[4]}")
                print(f"语文: {result[5]}, 数学: {result[6]}, 英语: {result[7]}, Python程序设计: {result[8]}")
            else:
                print("尊敬的管理员！未找到该学号的学生记录")
        except Error as e:
            print(f"查询失败: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_score(self):
        """修改学生的信息：包含查询、列表展示、修改及反馈"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            student_id = input("\n请输入要修改的学号或者姓名 (输入quit退出): ")
            if student_id.lower() == 'quit':
                return

            # 执行查询支持姓名或学号
            sql_find = "SELECT * FROM students WHERE 学号=%s OR 姓名=%s"
            cursor.execute(sql_find, (student_id, student_id))
            result = cursor.fetchone()
            
            if not result:
                print("尊敬的管理员！未找到该学生记录")
                return

            print(f"--------尊敬的管理员！学生信息如下--------")
            fields = ["学号", "姓名", "性别", "年龄", "班级", "语文", "数学", "英语", "Python程序设计"]
            for i in range(len(fields)):
                print(f"{i+1}. {fields[i]}: {result[i]}")

            choice = input("\n请输入要修改的项目编号(1-9)，输入其他则退出: ")
            if not choice.isdigit() or not (1 <= int(choice) <= 9): #检测字符串是否只包含数字字符
                print("尊敬的管理员！操作已取消。")
                return

            idx = int(choice) - 1
            field_name = fields[idx]
            old_value = result[idx]

            print(f"当前《{field_name}》为：{old_value}")
            
            # 如果修改的是成绩项(编号6-9)，使用计次验证逻辑
            if idx >= 5:
                new_value = self.get_valid_score(field_name)
            else:
                new_value = input(f"请输入新的《{field_name}》内容：")

            # 执行更新：修复参数匹配问题，仅用学号(result[0])作为条件
            sql_update = f"UPDATE students SET {field_name}=%s WHERE 学号=%s"
            cursor.execute(sql_update, (new_value, result[0]))
            conn.commit()
            
            print(f"✅ 修改成功！学号为{result[0]}, 名字为{result[1]}的学生，《{field_name}》已从'{old_value}'修改为'{new_value}'")

        except Error as e:
            print(f"❌ 修改失败: {e}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def delete_student(self):
        """删除功能：增加确认机制"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            sid = input("\n请输入要删除的学号: ")
            cursor.execute("SELECT 姓名 FROM students WHERE 学号=%s", (sid,))
            res = cursor.fetchone()
            if not res:
                print("未找到该学生")
                return
            
            confirm = input(f"确定要删除【{res[0]}】吗？(y/n): ")
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM students WHERE 学号=%s", (sid,))
                conn.commit()
                print("删除成功")
        finally:
            cursor.close()
            conn.close()

