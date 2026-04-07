from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os
from init_db import init_database, import_sample_data

# 配置前端目录
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# 获取数据库的正确路径
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
DATABASE = os.path.join(DB_DIR, 'mathematicians.db')

# 确保数据文件夹存在
os.makedirs(DB_DIR, exist_ok=True)

print(f"数据库路径: {DATABASE}")
print(f"数据库文件存在: {os.path.exists(DATABASE)}")

def initialize_database():
    """启动时重建并导入经过核实的数据库内容。"""
    init_database()
    import_sample_data()

# 在应用启动时初始化数据库（确保Render上也能执行）
try:
    if not os.path.exists(DATABASE):
        print("数据库不存在，初始化中...")
        initialize_database()
except Exception as e:
    print(f"数据库初始化错误: {e}")

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# 主页路由
@app.route('/')
def index():
    """提供主页"""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """提供静态文件"""
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/api/search', methods=['GET'])
def search():
    """搜索数学家"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': '请输入搜索内容'}), 400
    
    # 英文名称到中文名称的映射
    english_to_chinese = {
        'Euler': '欧拉',
        'Gauss': '高斯',
        'Newton': '牛顿',
        'Leibniz': '莱布尼茨',
        'Lagrange': '拉格朗日',
        'Cauchy': '柯西',
        'Riemann': '黎曼',
        'Weierstrass': '魏尔施特拉斯',
        'Cantor': '康托尔',
        'Hilbert': '希尔伯特',
        'Hardy': '哈迪',
        'Ramanujan': '拉马努金',
        'Descartes': '笛卡尔',
        'Pascal': '帕斯卡',
        'Fourier': '傅里叶',
        'Dirichlet': '狄利克雷',
        'Chebyshev': '切比雪夫',
        'Poincare': '庞加莱',
        'Hadamard': '阿达玛',
        'Weyl': '魏尔',
        'Turing': '图灵',
        'Lebesgue': '勒贝格',
        'Noether': '埃米·诺特',
        'Bourbaki': '布尔巴基学派',
        'Hua': '华罗庚',
        'Chern': '陈省身',
        'Yau': '丘成桐',
    }
    
    # 如果输入是英文，尝试转换
    search_query = english_to_chinese.get(query, query)
    
    db = get_db()
    cursor = db.cursor()
    
    # 搜索匹配的数学家
    cursor.execute('''
        SELECT id, name, birth_year, death_year, country, field, image_url 
        FROM mathematicians 
        WHERE name LIKE ? OR name LIKE ? OR name LIKE ?
        LIMIT 20
    ''', (f'%{search_query}%', f'{search_query}%', f'%{search_query}'))
    
    results = [dict(row) for row in cursor.fetchall()]
    db.close()
    
    return jsonify({'results': results})

@app.route('/api/mathematician/<int:math_id>', methods=['GET'])
def get_mathematician(math_id):
    """获取数学家详细信息"""
    db = get_db()
    cursor = db.cursor()
    
    # 获取基本信息
    cursor.execute('''
        SELECT * FROM mathematicians WHERE id = ?
    ''', (math_id,))
    
    math_info = cursor.fetchone()
    if not math_info:
        db.close()
        return jsonify({'error': '未找到该数学家'}), 404
    
    math_dict = dict(math_info)
    
    # 获取师承关系
    cursor.execute('''
        SELECT m.id, m.name, m.birth_year, m.death_year, m.country
        FROM mathematicians m
        JOIN relationships r ON m.id = r.teacher_id
        WHERE r.student_id = ? AND r.type = 'mentor'
    ''', (math_id,))
    math_dict['teachers'] = [dict(row) for row in cursor.fetchall()]
    
    # 获取著名弟子
    cursor.execute('''
        SELECT m.id, m.name, m.birth_year, m.death_year, m.country
        FROM mathematicians m
        JOIN relationships r ON m.id = r.student_id
        WHERE r.teacher_id = ? AND r.type = 'mentor'
    ''', (math_id,))
    math_dict['students'] = [dict(row) for row in cursor.fetchall()]
    
    # 获取合作者
    cursor.execute('''
        SELECT m.id, m.name, m.birth_year, m.death_year, m.country
        FROM mathematicians m
        JOIN relationships r ON m.id = r.target_id
        WHERE r.source_id = ? AND r.type = 'collaboration'
    ''', (math_id,))
    math_dict['collaborators'] = [dict(row) for row in cursor.fetchall()]
    
    # 获取学派
    cursor.execute('''
        SELECT id, name FROM schools WHERE id = ?
    ''', (math_dict['school_id'],))
    school = cursor.fetchone()
    math_dict['school'] = dict(school) if school else None
    
    db.close()
    return jsonify(math_dict)

@app.route('/api/relationship-graph/<int:math_id>', methods=['GET'])
def get_relationship_graph(math_id):
    """获取关系图数据，用于可视化"""
    db = get_db()
    cursor = db.cursor()
    
    # 获取中心节点
    cursor.execute('SELECT id, name, birth_year, death_year FROM mathematicians WHERE id = ?', (math_id,))
    center = cursor.fetchone()
    if not center:
        db.close()
        return jsonify({'error': '未找到该数学家'}), 404
    
    center_dict = dict(center)
    nodes = [{'id': math_id, 'name': center_dict['name'], 'type': 'center'}]
    links = []
    node_ids = {math_id}
    
    # 获取直接相关的人物（师生关系）
    cursor.execute('''
        SELECT student_id, teacher_id FROM relationships 
        WHERE (teacher_id = ? OR student_id = ?) AND type = 'mentor'
    ''', (math_id, math_id))
    
    relationships = cursor.fetchall()
    for row in relationships:
        if row[1] == math_id:  # math_id是老师
            related_id = row[0]  # 学生
            link_type = 'student'
        else:  # math_id是学生
            related_id = row[1]  # 老师
            link_type = 'teacher'
        
        if related_id not in node_ids:
            cursor.execute('SELECT id, name FROM mathematicians WHERE id = ?', (related_id,))
            related = cursor.fetchone()
            if related:
                related_dict = dict(related)
                nodes.append({'id': related_id, 'name': related_dict['name'], 'type': 'related'})
                node_ids.add(related_id)
        
        links.append({'source': math_id, 'target': related_id, 'type': link_type})
    
    db.close()
    return jsonify({'nodes': nodes, 'links': links})

@app.route('/api/add-mathematician', methods=['POST'])
def add_mathematician():
    """添加新的数学家（需要验证）"""
    data = request.json
    
    required_fields = ['name', 'birth_year', 'country']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必需字段'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO mathematicians 
            (name, birth_year, death_year, country, field, achievements, school_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['birth_year'],
            data.get('death_year'),
            data['country'],
            data.get('field'),
            data.get('achievements'),
            data.get('school_id')
        ))
        db.commit()
        new_id = cursor.lastrowid
        db.close()
        return jsonify({'id': new_id, 'message': '数学家信息已添加'}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/add-relationship', methods=['POST'])
def add_relationship():
    """添加师承或合作关系"""
    data = request.json
    
    if 'source_id' not in data or 'target_id' not in data or 'type' not in data:
        return jsonify({'error': '缺少必需字段'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        if data['type'] == 'mentor':
            cursor.execute('''
                INSERT INTO relationships (teacher_id, student_id, type)
                VALUES (?, ?, ?)
            ''', (data['source_id'], data['target_id'], 'mentor'))
        else:
            cursor.execute('''
                INSERT INTO relationships (source_id, target_id, type)
                VALUES (?, ?, ?)
            ''', (data['source_id'], data['target_id'], data['type']))
        
        db.commit()
        db.close()
        return jsonify({'message': '关系已添加'}), 201
    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    initialize_database()
    # 从环境变量读取端口，默认 5000
    port = int(os.environ.get('PORT', 5000))
    # 生产环境不使用 debug 模式
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
