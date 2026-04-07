"""初始化数据库并导入样本数据"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, '..', 'data', 'mathematicians.db')

def init_database():
    """创建数据库表结构"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # 重新构建数据库，避免 Render 上保留旧表和旧关系数据
    cursor.execute('DROP TABLE IF EXISTS relationships')
    cursor.execute('DROP TABLE IF EXISTS mathematicians')
    cursor.execute('DROP TABLE IF EXISTS schools')
    
    # 创建学派表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            founded_year INTEGER,
            founder_id INTEGER,
            description TEXT
        )
    ''')
    
    # 创建数学家表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mathematicians (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            english_name TEXT,
            birth_year INTEGER,
            death_year INTEGER,
            country TEXT,
            field TEXT,
            achievements TEXT,
            school_id INTEGER,
            biography TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (school_id) REFERENCES schools(id)
        )
    ''')
    
    # 创建关系表（师生关系、合作关系等）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER,
            target_id INTEGER,
            teacher_id INTEGER,
            student_id INTEGER,
            type TEXT NOT NULL,
            description TEXT,
            year INTEGER,
            FOREIGN KEY (source_id) REFERENCES mathematicians(id),
            FOREIGN KEY (target_id) REFERENCES mathematicians(id),
            FOREIGN KEY (teacher_id) REFERENCES mathematicians(id),
            FOREIGN KEY (student_id) REFERENCES mathematicians(id)
        )
    ''')
    
    db.commit()
    db.close()
    print("数据库创建成功！")

def import_sample_data():
    """导入样本数据"""
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    # 清空现有数据
    cursor.execute('DELETE FROM relationships')
    cursor.execute('DELETE FROM mathematicians')
    cursor.execute('DELETE FROM schools')
    
    # 添加学派
    schools = [
        ('欧几里得几何学派', None, None, '古代希腊'),
        ('牛顿学派', 1687, None, '微积分学派'),
        ('莱布尼茨学派', 1675, None, '微积分和单子论'),
        ('高斯学派', 1800, None, '数论和高等数学'),
        ('柏林学派', 1850, None, '严格的分析基础'),
        ('法国学派', 1900, None, '现代数学发展'),
    ]
    
    school_ids = {}
    for name, year, founder, desc in schools:
        cursor.execute(
            'INSERT INTO schools (name, founded_year, description) VALUES (?, ?, ?)',
            (name, year, desc)
        )
        school_ids[name] = cursor.lastrowid
    
    # 添加数学家
    mathematicians = [
        # 古代/中世纪
        ('毕达哥拉斯', -580, -500, '古希腊', '几何学', '毕达哥拉斯定理', None),
        ('欧几里得', -325, -265, '古希腊', '几何学', '《几何原本》', None),
        ('阿基米德', -287, -212, '古希腊/西西里', '几何、物理', '圆周率近似、杠杆原理', None),
        ('丢番图', 200, 284, '古罗马', '代数、数论', '丢番图方程', None),
        
        # 中世纪伊斯兰
        ('花拉子米', 780, 850, '波斯', '代数、算术', '代数学之父、算法', None),
        ('卡尔达诺', 1501, 1576, '意大利', '代数', '三次方程求解公式', None),
        
        # 近代早期
        ('笛卡尔', 1596, 1650, '法国', '几何、代数', '解析几何、笛卡尔坐标系', None),
        ('费马', 1601, 1665, '法国', '数论', '费马大定理、费马点', None),
        ('帕斯卡', 1623, 1662, '法国', '概率、几何', '帕斯卡三角形、概率论基础', None),
        ('沃利斯', 1616, 1703, '英国', '分析', '沃利斯乘积、积分', None),
        ('牛顿', 1643, 1727, '英国', '微积分、物理', '牛顿三定律、微积分', None),
        ('莱布尼茨', 1646, 1716, '德国', '微积分、哲学', '微积分记号、单子论', None),
        ('雅各布·伯努利', 1654, 1705, '瑞士', '分析、概率', '伯努利数、伯努利不等式、概率论', None),
        ('约翰·伯努利', 1667, 1748, '瑞士', '分析、力学', '变分法、指数函数、L洛必达法则', None),
        ('丹尼尔·伯努利', 1700, 1782, '瑞士', '流体力学、概率', '伯努利原理、大数定律', None),
        
        # 18世纪
        ('欧拉', 1707, 1783, '瑞士', '数论、分析', '图论、欧拉公式、多产的数学家', None),
        ('达朗贝尔', 1717, 1783, '法国', '分析、力学', '达朗贝尔原理、偏微分方程', None),
        ('拉格朗日', 1736, 1813, '意大利/法国', '分析、力学', '拉格朗日乘数法、分析力学', None),
        ('勒让德', 1752, 1833, '法国', '数论、分析', '勒让德多项式、数论进展', None),
        ('拉普拉斯', 1749, 1827, '法国', '分析、天体力学', '拉普拉斯变换、拉普拉斯方程', None),
        
        # 19世纪早期
        ('高斯', 1777, 1855, '德国', '数论、几何', '高斯消元法、最小二乘法、高斯分布', None),
        ('柯西', 1789, 1857, '法国', '分析、数论', '极限理论、实分析基础、复分析', None),
        ('傅里叶', 1768, 1830, '法国', '分析、物理', '傅里叶级数、傅里叶变换、偏微分方程', None),
        ('泊松', 1781, 1840, '法国', '分析、概率', '泊松方程、泊松分布、泊松比', None),
        ('波尔查诺', 1781, 1848, '捷克', '分析', '严格极限定义、介值定理', None),
        
        # 19世纪中期
        ('黎曼', 1826, 1866, '德国', '分析、几何', '黎曼积分、黎曼几何、黎曼假设', None),
        ('魏尔施特拉斯', 1815, 1897, '德国', '分析', '严格分析基础、一致连续', None),
        ('康托尔', 1845, 1918, '德国', '集合论、分析', '集合论、超越数、无穷集合论', None),
        ('克罗内克', 1823, 1891, '德国', '数论', '克罗内克符号、整数分解', None),
        ('德德金', 1831, 1916, '德国', '数论、分析', '戴德金割、理想论、整数环', None),
        
        # 19世纪晚期
        ('希尔伯特', 1862, 1943, '德国', '几何、泛函分析', '希尔伯特空间、23个问题、形式主义', None),
        ('闵可夫斯基', 1864, 1909, '波兰/德国', '几何、数论', '闵可夫斯基不等式、闵可夫斯基时空', None),
        ('庞加莱', 1854, 1912, '法国', '拓扑、几何、物理', '庞加莱猜想、相对论、混沌', None),
        ('阿达玛', 1865, 1963, '法国', '分析、数论', '素数定理、阿达玛矩阵', None),
        
        # 20世纪早期
        ('希尔伯特弟子-冯诺依曼', 1903, 1957, '匈牙利/美国', '泛函分析、计算机', '冯诺依曼代数、计算机之父', None),
        ('魏尔', 1885, 1955, '德国', '几何、群论', '对称性、李群、群表示论、量子力学', None),
        ('布劳威尔', 1881, 1966, '荷兰', '拓扑、直觉主义', '直觉主义逻辑、不动点定理', None),
        ('哈迪', 1877, 1947, '英国', '数论、分析', '数论、哈迪不等式、纯数学', None),
        ('拉马努金', 1887, 1920, '印度', '数论', '分割函数、mock theta函数、天才数学家', None),
        ('狄利克雷', 1805, 1859, '德国', '数论、分析', '狄利克雷函数、素数定理', None),
        ('切比雪夫', 1821, 1894, '俄国', '数论、分析', '切比雪夫多项式、素数分布', None),
        ('埃尔米特', 1822, 1901, '法国', '分析、代数', '埃尔米特多项式、埃尔米特矩阵、椭圆函数', None),  # 新增：庞加莱和赫尔曼.韦尔的导师
        ('伦德尔', 1862, 1918, '德国', '函数论', '黎曼假设相关研究', None),
        
        # 20世纪中期
        ('勒贝格', 1875, 1941, '法国', '分析', '勒贝格积分、测度论', None),
        ('希尔伯特学生-范德瓦尔登', 1903, 1996, '荷兰', '代数', '《现代代数》作者、范德瓦尔登永久猜想', None),
        ('埃米·诺特', 1882, 1935, '德国/美国', '抽象代数', '诺特环、理想论、物理与对称性', None),
        ('考瑟坦', 1901, 1976, '奥地利', '数学逻辑', '哥德尔不完全定理', None),
        ('图灵', 1912, 1954, '英国', '计算论、逻辑', '图灵机、计算可計性论', None),
        ('安德烈·魏勒', 1906, 1998, '法国', '数论、几何', '魏勒猜想、L-函数', None),
        ('布尔巴基学派', 1935, 2000, '法国', '现代数学', '结构主义数学、集合论基础', None),
        
        # 中国古代数学家
        ('刘徽', 220, 280, '古代中国', '几何、代数', '《九章算术》注解、割圆术、刘徽模', '欧几里得几何学派'),
        ('祖冲之', 429, 500, '中国', '数学、天文', '圆周率精确值（355/113）、球体积计算', None),
        ('杨辉', 1238, 1298, '中国', '代数、组合', '杨辉三角、大衍总术、对数表早期形式', None),
        ('祖暅', 450, 520, '中国', '数学、天文', '祖率（圆周率近似）、球体积公式', None),
        
        # 现代中国数学家
        ('华罗庚', 1910, 1985, '中国', '数论、分析', '华罗庚型函数、优选法', None),
        ('苏步青', 1902, 1983, '中国', '微分几何', '苏步青曲线、微分几何', None),
        ('陈省身', 1911, 2004, '中国', '微分几何', '陈类、陈-西蒙斯理论', None),
        ('丘成桐', 1949, None, '中国/美国', '微分几何', '卡拉比-丘成桐定理、菲尔茨奖', None),
        
        # 19世纪补充数学家
        ('阿贝尔', 1802, 1829, '挪威', '代数、分析', '阿贝尔定理、阿贝尔群、椭圆函数', None),
        ('伽罗瓦', 1811, 1832, '法国', '代数', '伽罗瓦理论、伽罗瓦群、方程论', None),
        ('雅可比', 1804, 1851, '普鲁士', '椭圆函数、分析', '雅可比行列式、椭圆函数', None),
        ('凯利', 1821, 1895, '英国', '代数、矩阵论', '凯利定理、矩阵代数、不变量论', None),
        ('西尔维斯特', 1814, 1897, '英国', '代数、矩阵论', '矩阵论、惯性定律、行列式', None),
        
        # 20世纪中国数学家补充
        ('陈景润', 1933, 1996, '中国', '数论', '哥德巴赫猜想、1+2证明、筛法', None),
        ('王元', 1930, 2015, '中国', '数论', '筛法、哥德巴赫猜想、素数分布', None),
    ]
    
    math_ids = {}
    math_meta = {}
    names_seen = set()
    for name, birth, death, country, field, achievements, school_id in mathematicians:
        if name in names_seen:
            print(f"ERROR: Duplicated name: {name}")
        else:
            names_seen.add(name)
        math_meta[name] = {'birth_year': birth, 'death_year': death}
        cursor.execute('''
            INSERT INTO mathematicians 
            (name, birth_year, death_year, country, field, achievements, school_id, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, birth, death, country, field, achievements, school_id, None))
        math_ids[name] = cursor.lastrowid
    
    # 不使用外部图片URL（维基百科直链被阻止），前端会使用fallback方案生成头像
    db.commit()

    # 仅保留时间线上成立且较有把握的直接师承关系，避免出现明显错误
    confirmed_mentor_relationships = {
        ('约翰·伯努利', '欧拉'),
        ('约翰·伯努利', '丹尼尔·伯努利'),
        ('高斯', '黎曼'),
        ('高斯', '狄利克雷'),
        ('高斯', '德德金'),  # 新增：戴德金是高斯的最后一名学生（1852年获博士学位）
        ('埃尔米特', '庞加莱'),  # 新增：庞加莱在巴黎综合工科学校学习埃尔米特数学（1873-1875）
        ('魏尔施特拉斯', '康托尔'),
        ('希尔伯特', '魏尔'),
        ('哈迪', '拉马努金'),
        ('华罗庚', '陈景润'),
        ('华罗庚', '王元'),
        ('苏步青', '陈省身'),
        ('陈省身', '丘成桐'),
    }

    candidate_relationships = [
        ('约翰·伯努利', '欧拉', 'mentor'),
        ('约翰·伯努利', '丹尼尔·伯努利', 'mentor'),
        ('高斯', '黎曼', 'mentor'),
        ('高斯', '狄利克雷', 'mentor'),
        ('高斯', '德德金', 'mentor'),  # 新增：威基百科确认戴德金是高斯的学生
        ('埃尔米特', '庞加莱', 'mentor'),  # 新增：庞加莱的导师（巴黎综合工科学校）
        ('魏尔施特拉斯', '康托尔', 'mentor'),
        ('希尔伯特', '魏尔', 'mentor'),
        ('哈迪', '拉马努金', 'mentor'),
        ('华罗庚', '陈景润', 'mentor'),
        ('华罗庚', '王元', 'mentor'),
        ('苏步青', '陈省身', 'mentor'),
        ('陈省身', '丘成桐', 'mentor'),
    ]

    inserted_relationships = 0
    skipped_relationships = 0
    for teacher_name, student_name, rel_type in candidate_relationships:
        teacher = math_meta.get(teacher_name)
        student = math_meta.get(student_name)
        if not teacher or not student:
            skipped_relationships += 1
            continue

        teacher_birth = teacher['birth_year']
        teacher_death = teacher['death_year']
        student_birth = student['birth_year']

        if (
            teacher_birth is None
            or student_birth is None
            or teacher_birth >= student_birth
            or (teacher_death is not None and teacher_death < student_birth)
        ):
            print(f"跳过时间上不成立的关系: {teacher_name} -> {student_name}")
            skipped_relationships += 1
            continue

        if (teacher_name, student_name) not in confirmed_mentor_relationships:
            print(f"跳过未核实的关系: {teacher_name} -> {student_name}")
            skipped_relationships += 1
            continue

        try:
            cursor.execute('''
                INSERT INTO relationships 
                (teacher_id, student_id, type, description)
                VALUES (?, ?, ?, ?)
            ''', (math_ids[teacher_name], math_ids[student_name], rel_type, f'{teacher_name}的学生'))
            inserted_relationships += 1
        except Exception as e:
            print(f"添加关系失败 {teacher_name} -> {student_name}: {e}")

    db.commit()
    db.close()
    print(f"样本数据导入成功！共添加了{inserted_relationships}个师生关系，跳过{skipped_relationships}个未核实/时间不成立的候选关系")

if __name__ == '__main__':
    # 创建数据文件夹
    os.makedirs(os.path.join(BASE_DIR, '..', 'data'), exist_ok=True)
    init_database()
    import_sample_data()
    print("数据库初始化完成！")
