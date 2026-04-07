# 数学家关系网络搜索系统

## 项目简介

这是一个专门设计用来展示数学家之间的**师承关系**、**合作关系**和**学派传承**的交互式知识库系统。

通过搜索一位数学家的名字，您可以立即获取：
- ✅ 生卒年份和国籍
- ✅ 主要研究领域和成就
- ✅ 师承关系（他的师父）
- ✅ 著名弟子（他培养的学生）
- ✅ 学派归属
- ✅ 关系网络可视化图表

## 项目结构

```
数学家搜索网站/
├── backend/              # Python Flask后端服务
│   ├── app.py           # API服务器（搜索、查询、编辑）
│   ├── init_db.py       # 数据库初始化脚本
│   └── requirements.txt  # Python依赖包
├── frontend/            # Web前端界面
│   └── index.html       # 单页应用（含HTML/CSS/JS）
├── data/                # 数据文件夹
│   └── mathematicians.db # SQLite数据库（自动生成）
└── README.md            # 本文件
```

## 技术栈

| 层次 | 技术 |
|-----|------|
| **后端** | Python 3.8+ + Flask |
| **前端** | HTML5 + CSS3 + JavaScript + D3.js |
| **数据库** | SQLite3 |
| **可视化** | D3.js (关系网络图) |

## 安装步骤

### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
cd backend
python init_db.py
```

这将：
- 创建SQLite数据库
- 初始化表结构（数学家、关系、学派等）
- 导入约20位著名数学家的样本数据

### 3. 启动后端服务

```bash
cd backend
python app.py
```

服务将在 `http://localhost:5000` 上运行

### 4. 打开前端页面

在浏览器中打开：
```
frontend/index.html
```

或者通过简单的HTTP服务器提供：
```bash
# Python 3
cd frontend
python -m http.server 8000
# 然后访问 http://localhost:8000
```

## 使用方法

### 搜索数学家

1. 在左侧边栏的搜索框输入数学家名字（支持中文和英文）
2. 点击"搜索"按钮或按Enter键
3. 查看搜索结果列表

### 查看详细信息

1. 点击搜索结果中的任何数学家
2. 左侧边栏将显示详细信息：
   - 生卒年份、国籍、研究领域、主要成就
   - 师父列表（可继续点击）
   - 弟子列表（可继续点击）
3. 右侧将自动显示关系网络图

### 浏览关系网络

- **中心节点（蓝紫色）**：当前选中的数学家
- **周围节点（紫色）**：与其有直接关系的人物
- **线条**：表示师生或合作关系
- 您可以拖拽节点来调整图表布局
- 点击相关人物可以查看他们的信息

## API 接口文档

### 搜索数学家
```
GET /api/search?q=<query>
```
返回匹配的数学家列表

### 获取数学家详情
```
GET /api/mathematician/<id>
```
返回完整信息，包括师承、弟子、合作者等

### 获取关系图数据
```
GET /api/relationship-graph/<id>
```
返回用于可视化的节点和链接数据

### 添加新数学家
```
POST /api/add-mathematician
```
请求体示例：
```json
{
    "name": "欧拉",
    "birth_year": 1707,
    "death_year": 1783,
    "country": "瑞士",
    "field": "数论、分析",
    "achievements": "欧拉公式、图论"
}
```

### 添加关系
```
POST /api/add-relationship
```
请求体示例：
```json
{
    "source_id": 1,
    "target_id": 2,
    "type": "mentor"
}
```

## 数据库结构

### 表：mathematicians（数学家）
- `id`: 唯一标识符
- `name`: 名字
- `birth_year`: 出生年
- `death_year`: 死亡年
- `country`: 国家/地区
- `field`: 研究领域
- `achievements`: 主要成就
- `school_id`: 所属学派
- `biography`: 传记

### 表：relationships（关系）
- `id`: 唯一标识符
- `teacher_id`: 教师ID
- `student_id`: 学生ID
- `type`: 关系类型 (mentor/collaboration)
- `description`: 描述
- `year`: 年份

### 表：schools（学派）
- `id`: 唯一标识符
- `name`: 学派名称
- `founded_year`: 创立年
- `founder_id`: 创始人ID
- `description`: 描述

## 扩展和定制

### 添加更多数学家数据

编辑 `backend/init_db.py` 中的 `mathematicians` 列表：

```python
mathematicians = [
    ('名字', 出生年, 死亡年, '国家', '领域', '成就'),
    # ... 更多数据
]
```

然后重新运行初始化：
```bash
python init_db.py
```

### 修改前端样式

编辑 `frontend/index.html` 中的 `<style>` 部分

### 自定义搜索和过滤

修改 `backend/app.py` 中的 `/api/search` 端点

## 已包含的数学家（样本数据）

- 毕达哥拉斯、欧几里得、阿基米德 - 古代希腊
- 笛卡尔、牛顿、莱布尼茨、欧拉 - 近代数学
- 高斯、拉格朗日、柯西、黎曼、魏尔施特拉斯、康托尔 - 19世纪
- 希尔伯特、哈迪、冯·诺依曼、魏尔、庞加莱等 - 20世纪

## 浏览器兼容性

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 常见问题

**Q: 如何导入自己的数据？**
A: 修改 `init_db.py` 中的数据列表，或通过 POST API 端点逐个添加。

**Q: 为什么搜索看不到结果？**
A: 确保已运行了 `python init_db.py` 初始化数据库。

**Q: 能否离线使用？**
A: 可以。所有数据存储在本地SQLite数据库中，不需要网络连接。

**Q: 如何删除或修改已有数据？**
A: 直接编辑SQLite数据库文件，或通过Python脚本操作。

## 许可证

MIT License - 自由使用和修改

## 贡献

欢迎提交改进建议或pull requests！

---

**最后更新**：2026年3月
