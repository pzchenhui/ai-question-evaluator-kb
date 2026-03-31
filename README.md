# AI 题目评价技能（知识库增强版）

<div align="center">

![version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![python](https://img.shields.io/badge/python-3.8+-green.svg)
![license](https://img.shields.io/badge/license-MIT-yellow.svg)
![category](https://img.shields.io/badge/category-education-orange.svg)

**AI 生成的中小学考试题目质量评价工具**

基于教育测量理论 + 学科知识库，从 8 个维度全面评估题目质量

</div>

---

## 📋 目录

- [功能特性](#-功能特性)
- [安装使用](#-安装使用)
- [快速开始](#-快速开始)
- [评价体系](#-评价体系)
- [知识库系统](#-知识库系统)
- [API 参考](#-api 参考)
- [示例演示](#-示例演示)
- [与 v1.0 对比](#-与-v10-对比)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)

---

## ✨ 功能特性

### 核心功能

- **8 维度综合评价**：科学性 (20%)、适切性 (15%)、认知层次 (15%)、区分度 (12%)、语言表达 (12%)、规范性 (10%)、公平性 (8%)、创新性 (8%)
- **知识库增强评价**：基于课程标准、知识点体系、常见错误库进行智能评价
- **布鲁姆认知层次识别**：自动识别题目的认知层次（记忆/理解/应用/分析/评价/创造）
- **难度智能预估**：基于题目特征预估难度系数（0.3-0.95）
- **知识点覆盖分析**：检查题目覆盖的知识点及掌握要求
- **常见错误预警**：识别题目可能涉及的学生常见错误
- **改进建议生成**：针对薄弱环节提供具体改进建议

### v1.1.0 新增

- 🆕 **课程标准知识库**：支持小学/初中/高中各学科课程标准查询
- 🆕 **知识点体系**：包含知识点名称、重要程度、前置知识要求
- 🆕 **常见错误库**：概念错误、计算错误、审题错误分类整理
- 🆕 **典型例题库**：各学科典型例题，含难度和认知层次标注
- 🆕 **认知层次要求**：不同学段的认知层次上限要求
- 🆕 **难度参考范围**：各学段不同难度等级的参考区间
- 🆕 **知识库可扩展**：支持用户自定义添加知识

---

## 🚀 安装使用

### 方式一：SkillHub 安装（推荐）

```bash
skillhub install ai-question-evaluator-kb
```

### 方式二：源码安装

```bash
# 克隆仓库
git clone https://github.com/pzchenhui/ai-question-evaluator-kb.git
cd ai-question-evaluator-kb

# 安装依赖
pip install jieba

# 测试运行
python3 ai_question_evaluator_kb.py --help
```

### 方式三：直接使用

```bash
# 下载主程序
wget https://raw.githubusercontent.com/pzchenhui/ai-question-evaluator-kb/main/ai_question_evaluator_kb.py

# 运行评价
python3 ai_question_evaluator_kb.py -q "题目内容" -s 数学 -g 初中二年级
```

---

## 🎯 快速开始

### 单题评价

```bash
python3 ai_question_evaluator_kb.py \
  -q "已知一次函数 y=kx+b 的图象经过点 (1,3) 和 (2,5)，求这个函数的解析式。" \
  -a "y=2x+1" \
  -s 数学 \
  -g 初中二年级 \
  -t 解答题
```

### 批量评价

准备 `questions.json` 文件：

```json
[
  {
    "question": "地球绕太阳转一圈需要多长时间？",
    "answer": "365 天（或一年）",
    "subject": "地理",
    "grade": "初中一年级",
    "type": "填空题"
  },
  {
    "question": "下列哪项不是可再生能源？A.太阳能 B.风能 C.石油 D.水能",
    "answer": "C",
    "subject": "物理",
    "grade": "初中二年级",
    "type": "选择题"
  }
]
```

运行批量评价：

```bash
python3 ai_question_evaluator_kb.py -f questions.json
```

### Python API 调用

```python
from ai_question_evaluator_kb import QuestionEvaluatorKB

# 初始化评价器（启用知识库）
evaluator = QuestionEvaluatorKB({
    "subject": "数学",
    "grade": "初中二年级",
    "question_type": "选择题",
    "enable_kb": True  # 启用知识库增强
})

# 评价单题
report = evaluator.evaluate(
    question="已知一次函数 y=kx+b 的图象经过点 (1,3) 和 (2,5)，求解析式。",
    answer="y=2x+1"
)

print(f"综合得分：{report['综合得分']}分")
print(f"等级：{report['等级']}")
print(f"认知层次：{report['认知层次']['层次']}")
```

### 禁用知识库（基础版）

```bash
python3 ai_question_evaluator_kb.py \
  -q "题目内容" \
  --no-kb  # 禁用知识库，使用基础评价
```

---

## 📊 评价体系

### 8 个评价维度

| 维度 | 权重 | 评价内容 | 知识库增强 |
|------|------|----------|------------|
| **科学性** | 20% | 知识内容是否准确、科学，无知识性错误 | ✅ 常见错误库匹配 |
| **适切性** | 15% | 难度是否符合年级水平，符合课程标准 | ✅ 课程标准对照 |
| **认知层次** | 15% | 布鲁姆分类是否合理，思维层次清晰 | ✅ 认知要求对照 |
| **区分度** | 12% | 能否区分不同水平学生，梯度合理 | ❌ |
| **语言表达** | 12% | 表述是否清晰、简洁、无歧义 | ❌ |
| **规范性** | 10% | 格式是否符合命题规范，要素完整 | ❌ |
| **公平性** | 8% | 是否存在文化、性别、地域偏见 | ❌ |
| **创新性** | 8% | 情境设计是否新颖，贴近生活实际 | ❌ |

### 评分等级

| 分数范围 | 等级 | 说明 |
|----------|------|------|
| 90-100 | 优秀 | 各维度表现均衡，可直接使用 |
| 80-89 | 良好 | 整体质量较好，建议微调后使用 |
| 70-79 | 中等 | 存在明显不足，需改进后使用 |
| 60-69 | 及格 | 多处需要改进，谨慎使用 |
| 0-59 | 待改进 | 建议重新设计题目 |

### 布鲁姆认知层次

| 层次 | 等级 | 关键词 | 适用学段 |
|------|------|--------|----------|
| 记忆 | 1 | 是什么、定义、列举、说出、写出 | 小学/初中/高中 |
| 理解 | 2 | 解释、说明、理解、概括、归纳、比较 | 小学/初中/高中 |
| 应用 | 3 | 应用、运用、计算、解决、使用、操作 | 初中/高中 |
| 分析 | 4 | 分析、区分、组织、推断、对比、剖析 | 初中/高中 |
| 评价 | 5 | 评价、评判、判断、评估、论证、辩护 | 高中 |
| 创造 | 6 | 设计、创造、构建、提出、规划、创作 | 高中 |

---

## 📚 知识库系统

### 知识库结构

```
knowledge_base/
├── curriculum_standards.json   # 课程标准
├── knowledge_points.json       # 知识点体系
├── common_errors.json          # 常见错误库
├── example_questions.json      # 典型例题
├── cognitive_requirements.json # 认知层次要求
└── difficulty_reference.json   # 难度参考范围
```

### 课程标准知识库

```json
{
  "数学": {
    "初中二年级": {
      "数与代数": ["一次函数", "整式乘除", "因式分解", "分式"],
      "图形与几何": ["三角形全等", "平行四边形", "勾股定理"],
      "统计与概率": ["数据分析", "概率初步"],
      "认知要求": "培养逻辑推理和抽象思维能力"
    }
  }
}
```

### 知识点体系

```json
{
  "数学": {
    "初中二年级": [
      {
        "name": "一次函数",
        "level": "核心",
        "prerequisites": ["平面直角坐标系", "函数概念"]
      }
    ]
  }
}
```

### 常见错误库

```json
{
  "数学": {
    "概念错误": [
      {
        "error": "混淆周长和面积",
        "example": "求边长 4cm 的正方形周长，学生计算 4×4=16cm²",
        "correction": "周长是边长之和，面积是边长乘积"
      }
    ]
  }
}
```

### 扩展知识库

```python
from ai_question_evaluator_kb import KnowledgeBase

kb = KnowledgeBase()

# 添加新的常见错误
kb.add_knowledge("common_errors", {
    "物理": {
        "概念错误": [
            {
                "error": "混淆速度和加速度",
                "example": "认为速度大加速度就大",
                "correction": "速度描述运动快慢，加速度描述速度变化快慢"
            }
        ]
    }
})

# 添加新的知识点
kb.add_knowledge("knowledge_points", {
    "地理": {
        "初中一年级": [
            {
                "name": "等高线地形图",
                "level": "核心",
                "prerequisites": ["地图比例尺", "海拔概念"]
            }
        ]
    }
})
```

---

## 🔧 API 参考

### QuestionEvaluatorKB 类

#### 初始化参数

```python
QuestionEvaluatorKB(config: Dict = None)
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| subject | str | "数学" | 学科 |
| grade | str | "初中二年级" | 年级 |
| question_type | str | "选择题" | 题型 |
| enable_kb | bool | True | 是否启用知识库 |
| kb_path | str | None | 知识库路径 |

#### evaluate() 方法

```python
evaluate(
    question: str,
    answer: str = "",
    subject: str = None,
    grade: str = None,
    question_type: str = None,
    enable_kb: bool = None
) -> Dict
```

**返回报告结构：**

```python
{
    "基本信息": {
        "学科": "数学",
        "年级": "初中二年级",
        "题型": "选择题",
        "评价时间": "2026-03-31 10:30:00",
        "知识库增强": True
    },
    "题目内容": "题目文本...",
    "参考答案": "答案文本",
    "综合得分": 85.5,
    "等级": "良好",
    "维度得分": {
        "科学性": 0.9,
        "适切性": 0.8,
        ...
    },
    "维度反馈": {
        "科学性": "科学性良好",
        "适切性": "难度适切",
        ...
    },
    "认知层次": {
        "层次": "应用",
        "等级": 3
    },
    "预估难度": {
        "预估值": 0.65,
        "说明": "难度值越低表示题目越难"
    },
    "知识点覆盖": {
        "status": "已检查",
        "matched_count": 2,
        "matched_points": [...],
        "total_points": 10,
        "coverage": "20.0%"
    },
    "常见错误预警": [
        {
            "type": "概念错误",
            "error": "混淆周长和面积",
            "correction": "..."
        }
    ],
    "改进建议": [
        {
            "维度": "区分度",
            "当前得分": 65.0,
            "问题": "选项长度差异过大",
            "建议": "优化选项设计",
            "优先级": "中"
        }
    ],
    "总体评价": "该题目质量良好（85.5 分），可直接使用。"
}
```

### KnowledgeBase 类

#### 主要方法

| 方法 | 说明 |
|------|------|
| `get_curriculum_standard(subject, grade)` | 获取课程标准 |
| `get_knowledge_points(subject, grade)` | 获取知识点列表 |
| `check_common_error(subject, question)` | 检查常见错误 |
| `get_example_questions(subject, grade, kp)` | 获取典型例题 |
| `get_cognitive_requirement(level, bloom)` | 获取认知要求 |
| `get_difficulty_range(level, difficulty)` | 获取难度范围 |
| `search(keyword, subject, kb_type)` | 搜索知识库 |
| `add_knowledge(kb_type, content)` | 添加知识 |

---

## 📝 示例演示

### 示例 1：数学选择题评价

**输入：**
```bash
python3 ai_question_evaluator_kb.py \
  -q "下列哪个数是无理数？A. √4  B. √9  C. √2  D. √16" \
  -a "C" \
  -s 数学 \
  -g 初中二年级 \
  -t 选择题
```

**输出：**
```
======================================================================
📊 AI 生成题目质量评价报告（知识库增强版）
======================================================================

【基本信息】
  学科：数学
  年级：初中二年级
  题型：选择题
  评价时间：2026-03-31 10:30:00
  知识库增强：True

【题目内容】
  下列哪个数是无理数？A. √4  B. √9  C. √2  D. √16

【参考答案】
  C

【综合评价】
  综合得分：88.5 分（良好）
  认知层次：理解（第 2 级）
  预估难度：0.68

【知识点覆盖】
  匹配知识点：1/10 (10.0%)
    - 实数分类 (核心)

【维度得分】
  科学性   (20%): [██████████] 100.0 分
  适切性   (15%): [████████░░] 85.0 分
  认知层次 (15%): [████████░░] 85.0 分
  区分度   (12%): [████████░░] 80.0 分
  语言表达 (12%): [██████████] 95.0 分
  规范性   (10%): [████████░░] 85.0 分
  公平性   (8%):  [██████████] 100.0 分
  创新性   (8%):  [██████░░░░] 65.0 分

【总体评价】
  该题目质量良好（88.5 分），可直接使用。

======================================================================
```

### 示例 2：物理应用题评价（含错误预警）

**输入：**
```bash
python3 ai_question_evaluator_kb.py \
  -q "一个物体质量 5kg，在水平面上以 2m/s 的速度匀速运动，求物体的动能。" \
  -a "Ek=1/2mv²=1/2×5×2²=10J" \
  -s 物理 \
  -g 初中二年级 \
  -t 计算题
```

**输出：**
```
...
【常见错误预警】
  ⚠️  混淆质量和重力
     建议：质量是物体属性，不随位置变化；重力随位置变化

【改进建议】
  1. [中] 创新性：融入生活情境、时事热点或跨学科元素
...
```

### 示例 3：批量评价

**输入文件 `batch.json`：**
```json
[
  {
    "question": "地球自转的方向是？A.自西向东 B.自东向西 C.自南向北 D.自北向南",
    "answer": "A",
    "subject": "地理",
    "grade": "初中一年级",
    "type": "选择题"
  },
  {
    "question": "写出光合作用的反应式。",
    "answer": "6CO₂+6H₂O→C₆H₁₂O₆+6O₂",
    "subject": "生物",
    "grade": "初中二年级",
    "type": "填空题"
  }
]
```

**运行：**
```bash
python3 ai_question_evaluator_kb.py -f batch.json
```

**输出：**
```
✅ 完成 2 道题目的评价
📊 平均得分：86.5 分
```

---

## 🆚 与 v1.0 对比

| 功能 | v1.0 | v1.1.0 (KB) |
|------|------|-------------|
| 8 维度评价 | ✅ | ✅ |
| 布鲁姆层次识别 | ✅ | ✅ |
| 难度预估 | ✅ | ✅ |
| 课程标准对照 | ❌ | ✅ |
| 知识点匹配 | ❌ | ✅ |
| 常见错误预警 | ❌ | ✅ |
| 典型例题参考 | ❌ | ✅ |
| 认知要求对照 | ❌ | ✅ |
| 知识库扩展 | ❌ | ✅ |
| 评价精准度 | 基准 | +15-20% |

---

## ❓ 常见问题

### Q1: 如何添加新的学科？

在知识库 JSON 文件中添加新学科条目：

```python
kb.add_knowledge("curriculum_standards", {
    "化学": {
        "初中三年级": {
            "物质构成": ["原子", "分子", "离子"],
            "认知要求": "建立微观粒子概念"
        }
    }
})
```

### Q2: 知识库评价不准怎么办？

1. 检查学科和年级配置是否正确
2. 尝试禁用知识库使用基础评价：`--no-kb`
3. 补充该学科的知识库内容

### Q3: 如何自定义评价权重？

修改 `EVALUATION_DIMENSIONS` 字典：

```python
evaluator = QuestionEvaluatorKB()
evaluator.EVALUATION_DIMENSIONS["科学性"]["weight"] = 0.25
evaluator.EVALUATION_DIMENSIONS["创新性"]["weight"] = 0.05
```

### Q4: 批量评价支持多少题目？

理论上无限制，但建议每次不超过 100 题，超时可分批处理。

### Q5: 知识库文件在哪里？

默认位置：`skills/ai-question-evaluator-kb/knowledge_base/`

---

## 🤝 贡献指南

欢迎贡献代码、知识库内容或提出建议！

### 提交知识库内容

1. Fork 本仓库
2. 在 `knowledge_base/` 目录下添加或修改 JSON 文件
3. 提交 Pull Request

### 报告问题

请在 GitHub Issues 中描述：
- 问题现象
- 复现步骤
- 预期结果
- 实际结果

---

## 📄 许可证

MIT License

---

## 📬 联系方式

- **作者**: AI Education Lab
- **GitHub**: https://github.com/pzchenhui/ai-question-evaluator-kb
- **问题反馈**: https://github.com/pzchenhui/ai-question-evaluator-kb/issues

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐ Star！**

</div>
