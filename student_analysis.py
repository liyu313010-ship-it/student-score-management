import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from mysql.connector import Error
# 导入warnings模块，用于处理警告信息
import warnings
# 忽略UserWarning类型的警告，避免影响程序运行时的输出
warnings.filterwarnings("ignore", category=UserWarning)


class ScoreAnalysis:
    """学生成绩分析类：实现成绩排名、平均分计算及方差统计等功能
    """
    
    def __init__(self):
        """类的初始化方法
        """
        # 数据库连接配置信息
        self.db_config = {
            'host': 'localhost',      
            'user': 'root',           
            'password': '123456',   
            'database': 'student_grade_management',  
            'charset': 'utf8mb4'     
        }
        # 定义需要分析的成绩科目字段（列表形式存储）
        self.score_fields = ["语文", "数学", "英语", "python程序设计"]

    def get_data_from_db(self):
        """从数据库读取所有学生数据并转换为DataFrame格式
        """
        try:
            # 建立数据库连接，使用self.db_config中的配置信息
            conn = mysql.connector.connect(**self.db_config)
            query = "SELECT * FROM students"
            # 使用pandas的read_sql函数读取SQL查询结果，转换为DataFrame
            df = pd.read_sql(query, conn)
            
            if df.empty:
                print("数据库中暂无学生数据，请先录入成绩。")
                return None
            
            '''
            计算每个学生的总分，
            从 DataFrame 中选择所有属于成绩字段的列（只保留成绩数据）
            axis=1表示按行求和（对每个学生的各科成绩求和）
            '''
            df['总分'] = df[self.score_fields].sum(axis=1)
            return df
        except Error as e:
            print(f"读取数据失败: {e}")
            return None
        finally:
            # 无论是否发生异常，都会执行finally块的代码
            # 检查conn变量是否存在于当前局部变量中
            if 'conn' in locals():
                if conn.is_connected():
                    conn.close()

    def rank_output(self):
        """根据用户选择的科目或总分，输出前十名排名
        """
        # 调用get_data_from_db方法获取学生数据
        df = self.get_data_from_db()
        # 如果数据为空（返回None），直接退出函数
        if df is None: return

        print("\n--- 排名查询选择 ---")
        options = self.score_fields + ["总分"]
        # 遍历选项列表，打印序号和对应的科目名称
        for i, opt in enumerate(options):
            print(f"{i + 1}. 查看 {opt} 排名")
        
        # 获取用户输入的选择
        choice = input("请输入您想查看的排名编号 (1-5)，按其他键返回: ")
        
        # 验证用户输入是否为有效数字且在有效范围内
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            print("已返回分析菜单。")
            return

        # 2. 确定用户选择的目标科目
        target_subject = options[int(choice) - 1]

        # 3. 执行排序并取前十名学生
        print(f"\n" + "="*25 + f" 【{target_subject}】成绩前十名 " + "="*25)
        # 根据选择的科目降序排列（ascending=False表示从高到低），取前10名
        ranked_df = df.sort_values(by=target_subject, ascending=False).head(10).copy()
        
        # 4. 为排名结果添加"排名"列
        ranked_df['排名'] = range(1, len(ranked_df) + 1)
        
        # 5. 格式化输出排名结果
        # 定义要显示的列：排名、学号、姓名、班级和该科目分数
        display_columns = ['排名', '学号', '姓名', '班级', target_subject]
        # 使用to_string方法将DataFrame转换为字符串输出，index=False表示不显示行索引
        print(ranked_df[display_columns].to_string(index=False))
        print("="*65)

    def calculate_averages(self):
        """计算各科及总分的平均分并输出结果
        """
        # 获取学生数据
        df = self.get_data_from_db()
        # 如果数据为空，直接返回
        if df is None: return

        # 打印平均分统计标题
        print("\n" + "="*20 + " 平均分统计 " + "="*20)
        # 计算各科目的平均分，mean()方法默认计算每列的平均值
        averages = df[self.score_fields].mean()
        # 遍历输出各科目的平均分，保留两位小数
        #items--将字典中的键值对转换为元组，并把这些元祖放在一个列表中返回
        for sub, avg in averages.items():
            print(f"{sub} 平均分: {avg:.2f}")
        
        # 计算总分的平均分
        total_avg = df['总分'].mean()
        # 输出总分平均分，保留两位小数
        print(f"总分平均分: {total_avg:.2f}")

    def calculate_variance(self):
        """
        统计每门功课及总分的方差并输出结果
        
        方差：方差用于衡量成绩的离散程度，值越大表示成绩分布越分散，值越小表示成绩分布越集中。
        """
        # 获取学生数据
        df = self.get_data_from_db()
        # 如果数据为空，直接返回
        if df is None: return

        # 打印方差统计标题
        print("\n" + "="*20 + " 成绩方差统计 " + "="*20)
        # 计算各科目及总分的方差，var()方法用于计算方差
        variances = df[self.score_fields + ['总分']].var()
        # 遍历输出各科目及总分的方差，保留两位小数
        for sub, var in variances.items():
            print(f"{sub} 方差: {var:.2f}")

    def score_distribution_analysis(self):
        """计算分数段人数及比例，并显示柱状图
        """
        # 获取学生数据
        df = self.get_data_from_db()
        # 如果数据为空，直接返回
        if df is None: return
        
        # 计算每个学生的平均分，axis=1表示按行求平均
        df['平均分'] = df[self.score_fields].mean(axis=1)

        # 1. 定义分数段划分标准
        # bins是分数段的边界值，需要比标签多一个边界值
        # 101是为了包含100分的情况（因为right=False表示左闭右开区间）
        bins = [0, 60, 70, 80, 90, 101]
        # 定义每个分数段对应的标签
        labels = ['0-60(不及格)', '60-70(及格)', '70-80(中等)', '80-90(良好)', '90-100(优秀)']
        
        # 2. 使用pd.cut函数将平均分划分到不同的分数段
        # right=False表示区间是左闭右开的，例如[0,60)表示0≤分数<60
        df['分数段'] = pd.cut(df['平均分'], bins=bins, labels=labels, right=False)
        
        # 统计各分数段的人数，value_counts()用于统计每个标签出现的次数
        # sort_index()确保按分数段顺序显示结果
        dist_counts = df['分数段'].value_counts().sort_index()
        # 计算总人数
        total_count = len(df)

        # 3. 控制台输出文字报表
        print("\n" + "="*15 + " 分数段比例统计 " + "="*15)
        # 遍历每个分数段的统计结果
        for label, count in dist_counts.items():
            # 计算该分数段人数占总人数的百分比
            percentage = (count / total_count) * 100
            # 格式化输出，保留两位小数
            print(f"{label: <12}: {count: >2}人 | 占比: {percentage:.2f}%")

        # 4. 调用内部方法绘制可视化柱状图
        self._draw_distribution_chart(dist_counts, total_count)

    def _draw_distribution_chart(self, dist_counts, total_count):
        """
        参数：
            dist_counts: pandas.Series，各分数段的人数统计
            total_count: int，总人数
        
        """
        # 设置中文字体（解决Matplotlib中文乱码问题）
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        # 设置坐标轴负号显示正常
        plt.rcParams['axes.unicode_minus'] = False

        # 创建一个新的图形对象，设置图的大小为12x8英寸，分辨率为100
        plt.figure(figsize=(12, 8), dpi=100)
        # 设置x轴为分数段标签
        x = dist_counts.index
        # 设置y轴为各分数段的人数
        y = dist_counts.values

        # 为不同分数段设置不同颜色
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        # 绘制柱状图，设置柱子宽度为0.6
        bars = plt.bar(x, y, color=colors, edgecolor='black', alpha=0.8, width=0.6)

        # 在每个柱子顶部标注具体人数和百分比
        for i, bar in enumerate(bars):
            # 获取柱子的高度（即该分数段的人数）
            height = bar.get_height()
            # 计算百分比
            percent = (height / total_count) * 100
            # 在柱子顶部添加文本
            # bar.get_x() + bar.get_width()/2. 表示柱子的中心位置
            # height + 0.1 表示文本的y坐标（在柱子顶部上方一点）
            # ha='center'表示水平居中，va='bottom'表示垂直方向底部对齐
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1, 
                    f'{int(height)}人\n({percent:.1f}%)', 
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        # 设置图表标题，字体大小16，粗体
        plt.title('学生总分分数段分布情况', fontsize=16, fontweight='bold', pad=20)
        # 设置x轴标签，字体大小14
        plt.xlabel('分数区间', fontsize=14, labelpad=15)
        # 设置y轴标签，字体大小14
        plt.ylabel('人数', fontsize=14, labelpad=15)
        # 设置x轴刻度字体大小12
        plt.xticks(fontsize=12, rotation=15)
        # 设置y轴刻度字体大小12
        plt.yticks(fontsize=12)
        # 显示y轴网格线，linestyle='--'表示虚线，alpha=0.6表示透明度，线宽0.8
        plt.grid(axis='y', linestyle='--', alpha=0.6, linewidth=0.8)
        # 添加图例
        plt.legend(['分数段分布'], loc='upper right', fontsize=12)
        # 添加总人数注释
        plt.text(0.95, 0.95, f'总人数: {total_count}', transform=plt.gca().transAxes,
                fontsize=12, fontweight='bold', ha='right', va='top',
                bbox=dict(facecolor='lightyellow', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.5'))
        # 调整图表边距
        plt.tight_layout()
        # 显示图表
        plt.show()

    def show_menu(self):
        """控制台交互菜单
        """
        while True:
            print("\n" + "*"*30)
            print("   学生成绩数据分析系统")
            print("*"*30)
            print("1. 输出各项成绩排名 (含个人详情)")
            print("2. 计算平均分数")
            print("3. 统计成绩方差")
            print("4. 分数段分布统计(柱状图)")
            print("0. 退出")
            print("*"*30)
            
            
            choice = input("尊敬的管理员！请选择您的操作需求: ")
            if choice == '1':
                self.rank_output()
            elif choice == '2':
                self.calculate_averages()
            elif choice == '3':
                self.calculate_variance()
            elif choice == '4':
                self.score_distribution_analysis()
            elif choice == '0':
                break
            else:
                # 处理无效输入
                print("输入有误，请输入数字 0-4 进行选择！")

# 主程序入口（当直接运行这个Python文件时，以下代码会被执行）
if __name__ == "__main__":
    # 创建ScoreAnalysis类的实例（对象）
    analysis = ScoreAnalysis()
    # 调用show_menu方法启动交互式菜单
    analysis.show_menu()