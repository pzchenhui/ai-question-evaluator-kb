#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 生成的中小学考试题目质量评价工具（知识库增强版）
基于教育测量理论 + 学科知识库，从 8 个维度全面评估题目质量

作者：AI Education Lab
版本：1.1.0 (知识库增强版)
"""

import json
import re
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path

try:
    import jieba
    JIEBA_AVAILABLE = True
except ImportError:
    JIEBA_AVAILABLE = False


class KnowledgeBase:
    """学科知识库"""
    
    def __init__(self, kb_path: str = None):
        """初始化知识库"""
        if kb_path is None:
            kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base")
        self.kb_path = Path(kb_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)
        
        # 加载知识库
        self.curriculum_standards = self._load_kb("curriculum_standards.json")
        self.knowledge_points = self._load_kb("knowledge_points.json")
        self.common_errors = self._load_kb("common_errors.json")
        self.example_questions = self._load_kb("example_questions.json")
        self.cognitive_requirements = self._load_kb("cognitive_requirements.json")
        self.difficulty_reference = self._load_kb("difficulty_reference.json")
        
    def _load_kb(self, filename: str) -> Dict:
        """加载知识库文件"""
        filepath = self.kb_path / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 创建默认知识库
            default_data = self._create_default_kb(filename)
            self._save_kb(filename, default_data)
            return default_data
    
    def _save_kb(self, filename: str, data: Dict):
        """保存知识库文件"""
        filepath = self.kb_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _create_default_kb(self, filename: str) -> Dict:
        """创建默认知识库"""
        
        if filename == "curriculum_standards.json":
            return self._create_curriculum_standards()
        elif filename == "knowledge_points.json":
            return self._create_knowledge_points()
        elif filename == "common_errors.json":
            return self._create_common_errors()
        elif filename == "example_questions.json":
            return self._create_example_questions()
        elif filename == "cognitive_requirements.json":
            return self._create_cognitive_requirements()
        elif filename == "difficulty_reference.json":
            return self._create_difficulty_reference()
        else:
            return {}
    
    def _create_curriculum_standards(self) -> Dict:
        """创建课程标准知识库"""
        return {
            "数学": {
                "小学一年级": {
                    "数与代数": ["20 以内数的认识", "20 以内加减法", "认识钟表"],
                    "图形与几何": ["认识长方体、正方体、圆柱、球", "辨认上下前后左右"],
                    "统计与概率": ["简单分类", "象形统计图"],
                    "认知要求": "以直观认识为主，避免抽象概念"
                },
                "小学三年级": {
                    "数与代数": ["万以内数的认识", "两位数乘除法", "分数初步"],
                    "图形与几何": ["长方形正方形周长", "面积初步"],
                    "统计与概率": ["条形统计图", "平均数"],
                    "认知要求": "开始培养抽象思维，但仍需具体情境支持"
                },
                "初中二年级": {
                    "数与代数": ["一次函数", "整式乘除", "因式分解", "分式"],
                    "图形与几何": ["三角形全等", "平行四边形", "勾股定理"],
                    "统计与概率": ["数据分析", "概率初步"],
                    "认知要求": "培养逻辑推理和抽象思维能力"
                }
            },
            "物理": {
                "初中一年级": {
                    "力学": ["长度测量", "运动描述", "力的概念"],
                    "热学": ["温度", "物态变化"],
                    "认知要求": "以观察和实验为主，建立物理概念"
                },
                "初中二年级": {
                    "力学": ["压强", "浮力", "简单机械"],
                    "能量": ["功和机械能", "能量转化"],
                    "认知要求": "理解物理规律，能进行简单计算"
                }
            },
            "地理": {
                "小学三年级": {
                    "地球与地图": ["地球形状", "简单地图识别"],
                    "中国地理": ["省级行政区", "主要山脉河流"],
                    "认知要求": "建立空间概念，认识家乡和祖国"
                },
                "初中一年级": {
                    "地球与地图": ["经纬网", "地球运动"],
                    "世界地理": ["大洲大洋", "主要国家"],
                    "认知要求": "理解地理现象的成因和分布规律"
                }
            },
            "语文": {
                "小学三年级": {
                    "识字与写字": ["累计认识 2500 字", "会写 1600 字"],
                    "阅读": ["理解词句意思", "初步把握文章内容"],
                    "写作": ["乐于书面表达", "学习修改习作"],
                    "认知要求": "培养阅读兴趣，打好语文基础"
                },
                "初中二年级": {
                    "阅读": ["理解主要内容", "体会作者情感", "了解表达方式"],
                    "写作": ["写记叙文", "表达真情实感", "45 分钟完成 500 字"],
                    "认知要求": "提高阅读理解能力，规范书面表达"
                }
            }
        }
    
    def _create_knowledge_points(self) -> Dict:
        """创建知识点体系"""
        return {
            "数学": {
                "初中二年级": [
                    {"name": "一次函数", "level": "核心", "prerequisites": ["平面直角坐标系", "函数概念"]},
                    {"name": "三角形全等", "level": "核心", "prerequisites": ["三角形概念", "角的性质"]},
                    {"name": "勾股定理", "level": "重要", "prerequisites": ["直角三角形", "平方运算"]},
                    {"name": "平行四边形", "level": "重要", "prerequisites": ["平行线", "四边形"]},
                    {"name": "因式分解", "level": "核心", "prerequisites": ["整式乘法", "乘法公式"]}
                ]
            },
            "物理": {
                "初中二年级": [
                    {"name": "压强", "level": "核心", "prerequisites": ["力的概念", "面积计算"]},
                    {"name": "浮力", "level": "核心", "prerequisites": ["力的平衡", "密度"]},
                    {"name": "杠杆", "level": "重要", "prerequisites": ["力的概念", "力臂"]},
                    {"name": "功", "level": "重要", "prerequisites": ["力", "距离"]},
                    {"name": "机械能", "level": "重要", "prerequisites": ["动能", "势能"]}
                ]
            },
            "地理": {
                "初中一年级": [
                    {"name": "经纬网", "level": "核心", "prerequisites": ["地球形状", "角度概念"]},
                    {"name": "地球运动", "level": "核心", "prerequisites": ["自转", "公转"]},
                    {"name": "大洲大洋", "level": "基础", "prerequisites": ["地图识别"]},
                    {"name": "气候类型", "level": "重要", "prerequisites": ["气温", "降水"]}
                ]
            }
        }
    
    def _create_common_errors(self) -> Dict:
        """创建常见错误知识库"""
        return {
            "数学": {
                "概念错误": [
                    {"error": "混淆周长和面积", "example": "求边长 4cm 的正方形周长，学生计算 4×4=16cm²", "correction": "周长是边长之和，面积是边长乘积"},
                    {"error": "函数概念不清", "example": "认为 y=x²+1 不是函数", "correction": "对于每个 x 值，y 有唯一确定值，就是函数"},
                    {"error": "全等条件混淆", "example": "用 SSA 判定三角形全等", "correction": "SSA 不能判定全等，应为 SAS、ASA、AAS、SSS"}
                ],
                "计算错误": [
                    {"error": "符号错误", "example": "(-2)² = -4", "correction": "(-2)² = 4，负数的偶次幂为正"},
                    {"error": "去括号错误", "example": "-(a-b) = -a-b", "correction": "-(a-b) = -a+b，括号前是负号要变号"},
                    {"error": "分式运算错误", "example": "1/a + 1/b = 1/(a+b)", "correction": "1/a + 1/b = (a+b)/(ab)，需要通分"}
                ],
                "审题错误": [
                    {"error": "忽略单位换算", "example": "题目给 cm，答案写 m", "correction": "注意题目要求的单位，必要时进行换算"},
                    {"error": "漏看条件", "example": "忽略'非负数'限制", "correction": "仔细阅读所有条件，圈画关键词"}
                ]
            },
            "物理": {
                "概念错误": [
                    {"error": "混淆质量和重力", "example": "认为质量随位置变化", "correction": "质量是物体属性，不随位置变化；重力随位置变化"},
                    {"error": "浮力方向错误", "example": "认为浮力方向与物体运动方向有关", "correction": "浮力方向始终竖直向上"}
                ],
                "公式错误": [
                    {"error": "压强公式滥用", "example": "用 p=F/S 计算液体压强", "correction": "液体压强用 p=ρgh，固体压强用 p=F/S"},
                    {"error": "功的公式错误", "example": "W=Fs 中 s 不是力方向上的距离", "correction": "s 必须是力方向上移动的距离"}
                ]
            },
            "地理": {
                "概念错误": [
                    {"error": "混淆经线和纬线", "example": "认为经线指示东西方向", "correction": "经线指示南北，纬线指示东西"},
                    {"error": "季节判断错误", "example": "认为北半球夏季时南半球也是夏季", "correction": "南北半球季节相反"}
                ]
            }
        }
    
    def _create_example_questions(self) -> Dict:
        """创建典型例题知识库"""
        return {
            "数学": {
                "初中二年级": {
                    "一次函数": [
                        {
                            "question": "已知一次函数 y=kx+b 的图象经过点 (1,3) 和 (2,5)，求这个函数的解析式。",
                            "answer": "解：将两点代入得：3=k+b, 5=2k+b，解得 k=2, b=1，所以 y=2x+1",
                            "analysis": "考查待定系数法求一次函数解析式",
                            "difficulty": 0.65,
                            "bloom_level": "应用"
                        }
                    ],
                    "三角形全等": [
                        {
                            "question": "如图，在△ABC 和△DEF 中，AB=DE，∠B=∠E，BC=EF。求证：△ABC≌△DEF。",
                            "answer": "证明：在△ABC 和△DEF 中，AB=DE，∠B=∠E，BC=EF，根据 SAS 判定定理，△ABC≌△DEF。",
                            "analysis": "考查三角形全等的 SAS 判定",
                            "difficulty": 0.70,
                            "bloom_level": "理解"
                        }
                    ]
                }
            },
            "物理": {
                "初中二年级": {
                    "压强": [
                        {
                            "question": "一个重 500N 的人，每只脚与地面的接触面积为 200cm²，求他站立时对地面的压强。",
                            "answer": "解：F=G=500N，S=2×200cm²=400cm²=0.04m²，p=F/S=500N/0.04m²=12500Pa",
                            "analysis": "考查压强公式 p=F/S 的应用，注意单位换算和受力面积",
                            "difficulty": 0.60,
                            "bloom_level": "应用"
                        }
                    ]
                }
            }
        }
    
    def _create_cognitive_requirements(self) -> Dict:
        """创建认知层次要求"""
        return {
            "小学": {
                "记忆": "能回忆基本概念、公式、定义",
                "理解": "能解释简单概念，说明基本原理",
                "应用": "能在熟悉情境中运用所学知识解决简单问题",
                "分析": "初步培养，能区分简单事实",
                "评价": "不要求",
                "创造": "不要求"
            },
            "初中": {
                "记忆": "能准确回忆知识点",
                "理解": "能解释概念，说明原理，进行转换",
                "应用": "能在新情境中运用知识解决问题",
                "分析": "能分析因果关系，区分事实与观点",
                "评价": "初步培养，能进行简单判断",
                "创造": "初步培养，能提出简单方案"
            },
            "高中": {
                "记忆": "熟练掌握知识体系",
                "理解": "深入理解概念本质和内在联系",
                "应用": "灵活运用知识解决复杂问题",
                "分析": "能进行系统分析和综合",
                "评价": "能进行批判性评价和论证",
                "创造": "能提出创新性解决方案"
            }
        }
    
    def _create_difficulty_reference(self) -> Dict:
        """创建难度参考"""
        return {
            "小学": {
                "容易": {"range": "0.85-0.95", "description": "基础题，大多数学生能做对"},
                "中等": {"range": "0.65-0.85", "description": "中档题，需要一定思考"},
                "困难": {"range": "0.45-0.65", "description": "较难题，区分优秀学生"}
            },
            "初中": {
                "容易": {"range": "0.75-0.90", "description": "基础题，考查基本概念"},
                "中等": {"range": "0.55-0.75", "description": "中档题，需要综合运用"},
                "困难": {"range": "0.35-0.55", "description": "较难题，考查思维能力"}
            },
            "高中": {
                "容易": {"range": "0.65-0.85", "description": "基础题"},
                "中等": {"range": "0.45-0.65", "description": "中档题"},
                "困难": {"range": "0.25-0.45", "description": "较难题"}
            }
        }
    
    def get_curriculum_standard(self, subject: str, grade: str) -> Dict:
        """获取课程标准"""
        return self.curriculum_standards.get(subject, {}).get(grade, {})
    
    def get_knowledge_points(self, subject: str, grade: str) -> List:
        """获取知识点列表"""
        return self.knowledge_points.get(subject, {}).get(grade, [])
    
    def check_common_error(self, subject: str, question: str) -> List:
        """检查是否涉及常见错误"""
        errors = []
        subject_errors = self.common_errors.get(subject, {})
        
        for error_type, error_list in subject_errors.items():
            for error_info in error_list:
                # 简单关键词匹配
                if any(kw in question for kw in error_info.get("example", "").split()[:3]):
                    errors.append({
                        "type": error_type,
                        "error": error_info["error"],
                        "correction": error_info["correction"]
                    })
        
        return errors
    
    def get_example_questions(self, subject: str, grade: str, knowledge_point: str = None) -> List:
        """获取典型例题"""
        examples = self.example_questions.get(subject, {}).get(grade, {})
        if knowledge_point and knowledge_point in examples:
            return examples[knowledge_point]
        # 返回所有例题
        result = []
        for kp_examples in examples.values():
            result.extend(kp_examples)
        return result
    
    def get_cognitive_requirement(self, school_level: str, bloom_level: str) -> str:
        """获取认知层次要求"""
        return self.cognitive_requirements.get(school_level, {}).get(bloom_level, "未知")
    
    def get_difficulty_range(self, school_level: str, difficulty_level: str) -> Dict:
        """获取难度范围"""
        return self.difficulty_reference.get(school_level, {}).get(difficulty_level, {})
    
    def search(self, keyword: str, subject: str = None, kb_type: str = None) -> List:
        """搜索知识库"""
        results = []
        
        # 搜索所有知识库
        kb_dict = {
            "curriculum_standards": self.curriculum_standards,
            "knowledge_points": self.knowledge_points,
            "common_errors": self.common_errors,
            "example_questions": self.example_questions
        }
        
        for kb_name, kb_data in kb_dict.items():
            if kb_type and kb_name != kb_type:
                continue
            
            # 简单搜索
            kb_str = json.dumps(kb_data, ensure_ascii=False)
            if keyword in kb_str:
                results.append({
                    "kb_type": kb_name,
                    "matched": True
                })
        
        return results
    
    def add_knowledge(self, kb_type: str, content: Dict) -> bool:
        """添加知识到知识库"""
        if kb_type == "curriculum_standards":
            self.curriculum_standards.update(content)
            self._save_kb("curriculum_standards.json", self.curriculum_standards)
        elif kb_type == "knowledge_points":
            self.knowledge_points.update(content)
            self._save_kb("knowledge_points.json", self.knowledge_points)
        elif kb_type == "common_errors":
            self.common_errors.update(content)
            self._save_kb("common_errors.json", self.common_errors)
        elif kb_type == "example_questions":
            self.example_questions.update(content)
            self._save_kb("example_questions.json", self.example_questions)
        else:
            return False
        return True


class QuestionEvaluatorKB:
    """AI 生成题目质量评价器（知识库增强版）"""
    
    EVALUATION_DIMENSIONS = {
        "科学性": {"weight": 0.20, "description": "知识内容是否准确、科学，无知识性错误"},
        "适切性": {"weight": 0.15, "description": "难度是否符合年级水平，符合课程标准"},
        "认知层次": {"weight": 0.15, "description": "布鲁姆分类是否合理，思维层次清晰"},
        "区分度": {"weight": 0.12, "description": "能否区分不同水平学生，梯度合理"},
        "语言表达": {"weight": 0.12, "description": "表述是否清晰、简洁、无歧义"},
        "规范性": {"weight": 0.10, "description": "格式是否符合命题规范，要素完整"},
        "公平性": {"weight": 0.08, "description": "是否存在文化、性别、地域偏见"},
        "创新性": {"weight": 0.08, "description": "情境设计是否新颖，贴近生活实际"}
    }
    
    BLOOM_TAXONOMY = {
        "记忆": {"level": 1, "keywords": ["是什么", "定义", "列举", "说出", "写出", "回忆"]},
        "理解": {"level": 2, "keywords": ["解释", "说明", "理解", "概括", "归纳", "比较"]},
        "应用": {"level": 3, "keywords": ["应用", "运用", "计算", "解决", "使用", "操作"]},
        "分析": {"level": 4, "keywords": ["分析", "区分", "组织", "推断", "对比", "剖析"]},
        "评价": {"level": 5, "keywords": ["评价", "评判", "判断", "评估", "论证", "辩护"]},
        "创造": {"level": 6, "keywords": ["设计", "创造", "构建", "提出", "规划", "创作"]}
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化评价器"""
        self.config = config or {}
        self.subject = self.config.get("subject", "数学")
        self.grade = self.config.get("grade", "初中二年级")
        self.question_type = self.config.get("question_type", "选择题")
        self.enable_kb = self.config.get("enable_kb", True)
        
        # 初始化知识库
        if self.enable_kb:
            self.kb = KnowledgeBase(self.config.get("kb_path"))
        else:
            self.kb = None
    
    def evaluate(self, question: str, answer: str = "", subject: str = None, 
                 grade: str = None, question_type: str = None, 
                 enable_kb: bool = None) -> Dict:
        """评价单道题目（知识库增强版）"""
        
        # 更新配置
        if subject:
            self.subject = subject
        if grade:
            self.grade = grade
        if question_type:
            self.question_type = question_type
        if enable_kb is not None:
            self.enable_kb = enable_kb
        
        # 执行各维度评价
        dimension_scores = {}
        dimension_feedback = {}
        
        for dimension in self.EVALUATION_DIMENSIONS:
            if self.enable_kb and dimension in ["科学性", "适切性", "认知层次"]:
                # 使用知识库增强评价
                score, feedback = self._evaluate_with_kb(dimension, question, answer)
            else:
                score, feedback = self._evaluate_dimension(dimension, question, answer)
            dimension_scores[dimension] = score
            dimension_feedback[dimension] = feedback
        
        # 计算综合得分
        total_score = self._calculate_total_score(dimension_scores)
        
        # 识别认知层次
        bloom_level = self._identify_bloom_level(question)
        
        # 预估难度
        estimated_difficulty = self._estimate_difficulty(question)
        
        # 知识点检查（知识库增强）
        knowledge_check = None
        if self.enable_kb:
            knowledge_check = self._check_knowledge_coverage(question)
        
        # 常见错误检查（知识库增强）
        error_warnings = None
        if self.enable_kb:
            error_warnings = self.kb.check_common_error(self.subject, question)
        
        # 生成改进建议
        improvements = self._generate_improvements(dimension_scores, dimension_feedback, error_warnings)
        
        # 生成评价报告
        report = {
            "基本信息": {
                "学科": self.subject,
                "年级": self.grade,
                "题型": self.question_type,
                "评价时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "知识库增强": self.enable_kb
            },
            "题目内容": question[:200] + "..." if len(question) > 200 else question,
            "参考答案": answer if answer else "未提供",
            "综合得分": round(total_score, 1),
            "等级": self._score_to_grade(total_score),
            "维度得分": dimension_scores,
            "维度反馈": dimension_feedback,
            "认知层次": bloom_level,
            "预估难度": estimated_difficulty,
            "知识点覆盖": knowledge_check,
            "常见错误预警": error_warnings,
            "改进建议": improvements,
            "总体评价": self._generate_summary(total_score, dimension_scores)
        }
        
        return report
    
    def _evaluate_with_kb(self, dimension: str, question: str, answer: str) -> Tuple[float, str]:
        """使用知识库增强评价"""
        
        if dimension == "科学性":
            return self._evaluate_science_kb(question, answer)
        elif dimension == "适切性":
            return self._evaluate_appropriateness_kb(question)
        elif dimension == "认知层次":
            return self._evaluate_cognitive_level_kb(question)
        else:
            return self._evaluate_dimension(dimension, question, answer)
    
    def _evaluate_science_kb(self, question: str, answer: str) -> Tuple[float, str]:
        """评价科学性（知识库增强）"""
        score = 1.0
        issues = []
        
        # 基础检查
        error_patterns = [
            (r"地球是平的", "科学错误：地球是球体"),
            (r"太阳绕地球转", "科学错误：地球绕太阳转"),
            (r"1+1=3", "数学错误：1+1=2"),
            (r"水的化学式是 HO", "科学错误：水的化学式是 H2O"),
        ]
        
        for pattern, error_msg in error_patterns:
            if re.search(pattern, question, re.IGNORECASE):
                issues.append(error_msg)
                score -= 0.3
        
        # 知识库检查：常见错误
        if self.kb:
            errors = self.kb.check_common_error(self.subject, question)
            for error in errors:
                issues.append(f"可能涉及常见错误：{error['error']}")
                score -= 0.1
        
        # 知识库检查：知识点准确性
        if self.kb:
            kp_list = self.kb.get_knowledge_points(self.subject, self.grade)
            # 简单检查知识点名称是否匹配
            for kp in kp_list:
                kp_name = kp.get("name", "")
                if kp_name in question:
                    # 知识点在范围内，加分
                    score = min(1.0, score + 0.05)
                    break
        
        feedback = "科学性良好" if not issues else "; ".join(issues)
        return max(0.1, score), feedback
    
    def _evaluate_appropriateness_kb(self, question: str) -> Tuple[float, str]:
        """评价适切性（知识库增强）"""
        score = 0.85
        issues = []
        
        # 获取课程标准
        if self.kb:
            standard = self.kb.get_curriculum_standard(self.subject, self.grade)
            if standard:
                # 检查是否超纲
                cognitive_req = standard.get("认知要求", "")
                if cognitive_req:
                    # 简单检查题目复杂度是否符合认知要求
                    if "小学" in self.grade and len(question) > 200:
                        issues.append(f"题干过长，{cognitive_req}")
                        score -= 0.15
                    elif "初中" in self.grade and len(question) > 300:
                        issues.append(f"题干过长，{cognitive_req}")
                        score -= 0.1
        
        # 难度检查
        if self.kb:
            difficulty_range = self.kb.get_difficulty_range(
                "小学" if "小学" in self.grade else ("高中" if "高中" in self.grade else "初中"),
                "中等"
            )
            if difficulty_range:
                # 预估难度是否在合理范围
                estimated = self._estimate_difficulty_simple(question)
                range_str = difficulty_range.get("range", "0.55-0.75")
                try:
                    min_d, max_d = map(float, range_str.split("-"))
                    if estimated < min_d - 0.15 or estimated > max_d + 0.15:
                        issues.append(f"预估难度{estimated:.2f}，可能偏离{range_str}范围")
                        score -= 0.1
                except:
                    pass
        
        feedback = "难度适切" if not issues else "; ".join(issues)
        return max(0.3, score), feedback
    
    def _evaluate_cognitive_level_kb(self, question: str) -> Tuple[float, str]:
        """评价认知层次（知识库增强）"""
        detected_levels = []
        
        for level_name, level_info in self.BLOOM_TAXONOMY.items():
            for keyword in level_info["keywords"]:
                if keyword in question:
                    detected_levels.append((level_name, level_info["level"]))
                    break
        
        if not detected_levels:
            if "计算" in question or "求解" in question:
                detected_levels.append(("应用", 3))
            elif "为什么" in question or "说明" in question:
                detected_levels.append(("理解", 2))
            else:
                detected_levels.append(("记忆", 1))
        
        detected_levels.sort(key=lambda x: x[1], reverse=True)
        bloom_level = detected_levels[0][0]
        bloom_rank = detected_levels[0][1]
        
        score = 0.85
        feedback = f"认知层次：{bloom_level}（第{bloom_rank}级）"
        
        # 知识库检查：认知要求是否合理
        if self.kb:
            school_level = "小学" if "小学" in self.grade else ("高中" if "高中" in self.grade else "初中")
            expected_max = {"小学": 3, "初中": 4, "高中": 6}.get(school_level, 4)
            
            if bloom_rank > expected_max:
                score -= 0.15
                feedback += f"（对{school_level}可能偏高，建议不超过{expected_max}级）"
            elif bloom_rank < expected_max - 2:
                score -= 0.1
                feedback += f"（对{school_level}可能偏低）"
        
        return score, feedback
    
    def _check_knowledge_coverage(self, question: str) -> Dict:
        """检查知识点覆盖"""
        if not self.kb:
            return {"status": "知识库未启用"}
        
        kp_list = self.kb.get_knowledge_points(self.subject, self.grade)
        matched_kps = []
        
        for kp in kp_list:
            kp_name = kp.get("name", "")
            if kp_name in question:
                matched_kps.append({
                    "name": kp_name,
                    "level": kp.get("level", "未知"),
                    "prerequisites": kp.get("prerequisites", [])
                })
        
        return {
            "status": "已检查",
            "matched_count": len(matched_kps),
            "matched_points": matched_kps,
            "total_points": len(kp_list),
            "coverage": f"{len(matched_kps)/len(kp_list)*100:.1f}%" if kp_list else "0%"
        }
    
    def _estimate_difficulty_simple(self, question: str) -> float:
        """简单难度估计"""
        base = 0.65
        
        # 长度因素
        if len(question) > 200:
            base += 0.05
        elif len(question) < 50:
            base -= 0.05
        
        # 题型因素
        type_diff = {"选择题": -0.05, "填空题": 0, "判断题": -0.1, "简答题": 0.1, "应用题": 0.1}
        base += type_diff.get(self.question_type, 0)
        
        return max(0.3, min(0.95, base))
    
    # 以下方法继承自基础版本
    def _evaluate_dimension(self, dimension: str, question: str, answer: str) -> Tuple[float, str]:
        """评价单个维度（基础版）"""
        if dimension == "科学性":
            return self._evaluate_science(question, answer)
        elif dimension == "适切性":
            return self._evaluate_appropriateness(question)
        elif dimension == "认知层次":
            return self._evaluate_cognitive_level(question)
        elif dimension == "区分度":
            return self._evaluate_discrimination(question, answer)
        elif dimension == "语言表达":
            return self._evaluate_language(question)
        elif dimension == "规范性":
            return self._evaluate_standardization(question, answer)
        elif dimension == "公平性":
            return self._evaluate_fairness(question)
        elif dimension == "创新性":
            return self._evaluate_innovation(question)
        return 0.5, "未知评价维度"
    
    def _evaluate_science(self, question: str, answer: str) -> Tuple[float, str]:
        """评价科学性（基础版）"""
        issues = []
        score = 1.0
        error_patterns = [
            (r"地球是平的", "科学错误：地球是球体"),
            (r"太阳绕地球转", "科学错误：地球绕太阳转"),
            (r"1+1=3", "数学错误：1+1=2"),
        ]
        for pattern, error_msg in error_patterns:
            if re.search(pattern, question, re.IGNORECASE):
                issues.append(error_msg)
                score -= 0.3
        if answer and self.question_type == "选择题":
            options = re.findall(r'[A-D][.、:：]', question)
            if len(options) < 4:
                issues.append("选择题选项不完整")
                score -= 0.1
        feedback = "科学性良好" if not issues else "; ".join(issues)
        return max(0.1, score), feedback
    
    def _evaluate_appropriateness(self, question: str) -> Tuple[float, str]:
        """评价适切性（基础版）"""
        score = 0.8
        issues = []
        sentences = re.split(r'[。！？.!?]', question)
        avg_sentence_len = sum(len(s) for s in sentences if s) / max(len(sentences), 1)
        if avg_sentence_len > 50:
            issues.append("题干过长")
            score -= 0.15
        feedback = "难度适切" if not issues else "; ".join(issues)
        return max(0.3, score), feedback
    
    def _evaluate_cognitive_level(self, question: str) -> Tuple[float, str]:
        """评价认知层次（基础版）"""
        detected_levels = []
        for level_name, level_info in self.BLOOM_TAXONOMY.items():
            for keyword in level_info["keywords"]:
                if keyword in question:
                    detected_levels.append((level_name, level_info["level"]))
                    break
        if not detected_levels:
            detected_levels.append(("记忆", 1))
        detected_levels.sort(key=lambda x: x[1], reverse=True)
        return 0.85, f"认知层次：{detected_levels[0][0]}"
    
    def _evaluate_discrimination(self, question: str, answer: str) -> Tuple[float, str]:
        """评价区分度"""
        score = 0.75
        issues = []
        if self.question_type == "选择题":
            options = re.findall(r'[A-D][.、:：][^\n]+', question)
            if len(options) == 4:
                option_lengths = [len(opt) for opt in options]
                if max(option_lengths) - min(option_lengths) > 30:
                    issues.append("选项长度差异过大")
                    score -= 0.15
            else:
                issues.append("选择题应有 4 个选项")
                score -= 0.2
        feedback = "区分度良好" if not issues else "; ".join(issues)
        return max(0.3, score), feedback
    
    def _evaluate_language(self, question: str) -> Tuple[float, str]:
        """评价语言表达"""
        score = 0.9
        issues = []
        if not question.endswith(("?", "?", "。", ".", "）", ")")):
            issues.append("题目缺少结束标点")
            score -= 0.05
        if len(question) > 300:
            issues.append("题目过长")
            score -= 0.1
        feedback = "语言表达规范" if not issues else "; ".join(issues)
        return max(0.4, score), feedback
    
    def _evaluate_standardization(self, question: str, answer: str) -> Tuple[float, str]:
        """评价规范性"""
        score = 0.85
        issues = []
        if self.question_type == "选择题":
            if not re.search(r'[A-D][.、:：]', question):
                issues.append("选择题缺少选项标记")
                score -= 0.2
        if not answer and self.question_type in ["选择题", "填空题", "判断题"]:
            issues.append("客观题应提供参考答案")
            score -= 0.15
        feedback = "格式基本规范" if not issues else "; ".join(issues)
        return max(0.4, score), feedback
    
    def _evaluate_fairness(self, question: str) -> Tuple[float, str]:
        """评价公平性"""
        score = 0.9
        issues = []
        bias_words = ["城市", "农村", "有钱", "贫困"]
        for word in bias_words:
            if word in question:
                issues.append(f"包含敏感词'{word}'")
                score -= 0.1
                break
        feedback = "公平性良好" if not issues else "; ".join(issues)
        return max(0.5, score), feedback
    
    def _evaluate_innovation(self, question: str) -> Tuple[float, str]:
        """评价创新性"""
        score = 0.7
        positive_features = []
        innovation_keywords = [("人工智能", "AI"), ("环保", "绿色"), ("航天", "科技")]
        for keyword, category in innovation_keywords:
            if keyword in question:
                positive_features.append(f"融入{category}情境")
                score += 0.1
        feedback = "创新性良好：" + "; ".join(positive_features) if positive_features else "情境设计较为常规"
        return min(1.0, score), feedback
    
    def _calculate_total_score(self, dimension_scores: Dict[str, float]) -> float:
        """计算综合得分"""
        total = sum(dimension_scores[dim] * self.EVALUATION_DIMENSIONS[dim]["weight"] 
                    for dim in dimension_scores)
        return total * 100
    
    def _score_to_grade(self, score: float) -> str:
        """分数转等级"""
        if score >= 90: return "优秀"
        elif score >= 80: return "良好"
        elif score >= 70: return "中等"
        elif score >= 60: return "及格"
        else: return "待改进"
    
    def _identify_bloom_level(self, question: str) -> Dict:
        """识别布鲁姆认知层次"""
        for level_name, level_info in self.BLOOM_TAXONOMY.items():
            for keyword in level_info["keywords"]:
                if keyword in question:
                    return {"层次": level_name, "等级": level_info["level"]}
        return {"层次": "记忆", "等级": 1}
    
    def _estimate_difficulty(self, question: str) -> Dict:
        """预估难度"""
        estimated = self._estimate_difficulty_simple(question)
        return {"预估值": round(estimated, 2), "说明": "难度值越低表示题目越难"}
    
    def _generate_improvements(self, dimension_scores: Dict, dimension_feedback: Dict, 
                                error_warnings: List = None) -> List[Dict]:
        """生成改进建议"""
        improvements = []
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1])
        for dimension, score in sorted_dims:
            if score < 0.8:
                suggestions = {
                    "科学性": "核对知识点准确性，查阅教材和课程标准",
                    "适切性": "参考同年级真题难度，调整题目复杂度",
                    "认知层次": "根据年级特点调整思维要求",
                    "区分度": "优化选项设计或增加评分细则",
                    "语言表达": "精简题干，避免歧义表述",
                    "规范性": "补充题目分值、答题要求等要素",
                    "公平性": "避免文化、性别、地域偏见",
                    "创新性": "融入生活情境、时事热点或跨学科元素"
                }
                improvements.append({
                    "维度": dimension,
                    "当前得分": round(score * 100, 1),
                    "问题": dimension_feedback[dimension],
                    "建议": suggestions.get(dimension, "请根据具体问题分析改进"),
                    "优先级": "高" if score < 0.6 else "中"
                })
        
        # 添加常见错误预警
        if error_warnings:
            for error in error_warnings:
                improvements.append({
                    "维度": "科学性",
                    "类型": "常见错误预警",
                    "问题": error["error"],
                    "建议": error["correction"],
                    "优先级": "高"
                })
        
        return improvements
    
    def _generate_summary(self, total_score: float, dimension_scores: Dict) -> str:
        """生成总体评价"""
        if total_score >= 90:
            return f"该题目质量优秀（{total_score:.1f}分），各维度表现均衡，可直接使用。"
        elif total_score >= 80:
            weak_dims = [d for d, s in dimension_scores.items() if s < 0.75]
            if weak_dims:
                return f"该题目质量良好（{total_score:.1f}分），建议在{','.join(weak_dims)}方面稍作改进后使用。"
            return f"该题目质量良好（{total_score:.1f}分），可直接使用。"
        elif total_score >= 70:
            weak_dims = [d for d, s in dimension_scores.items() if s < 0.7]
            return f"该题目质量中等（{total_score:.1f}分），建议在{','.join(weak_dims)}方面改进后使用。"
        else:
            return f"该题目质量待改进（{total_score:.1f}分），建议重新审视题目设计。"


def print_report(report: Dict):
    """格式化打印评价报告"""
    print("\n" + "=" * 70)
    print("📊 AI 生成题目质量评价报告（知识库增强版）")
    print("=" * 70)
    
    print("\n【基本信息】")
    for k, v in report["基本信息"].items():
        print(f"  {k}: {v}")
    
    print(f"\n【题目内容】")
    print(f"  {report['题目内容']}")
    
    if report["参考答案"] != "未提供":
        print(f"\n【参考答案】")
        print(f"  {report['参考答案']}")
    
    print(f"\n【综合评价】")
    print(f"  综合得分：{report['综合得分']}分（{report['等级']}）")
    print(f"  认知层次：{report['认知层次']['层次']}（第{report['认知层次']['等级']}级）")
    print(f"  预估难度：{report['预估难度']['预估值']}")
    
    if report.get("知识点覆盖"):
        print(f"\n【知识点覆盖】")
        kc = report["知识点覆盖"]
        print(f"  匹配知识点：{kc.get('matched_count', 0)}/{kc.get('total_points', 0)} ({kc.get('coverage', '0%')})")
        for kp in kc.get("matched_points", [])[:3]:
            print(f"    - {kp['name']} ({kp['level']})")
    
    if report.get("常见错误预警"):
        print(f"\n【常见错误预警】")
        for err in report["常见错误预警"][:3]:
            print(f"  ⚠️  {err['error']}")
            print(f"     建议：{err['correction']}")
    
    print(f"\n【维度得分】")
    for dim, score in report["维度得分"].items():
        weight = QuestionEvaluatorKB.EVALUATION_DIMENSIONS[dim]["weight"]
        bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
        print(f"  {dim:8s} ({weight:.0%}): [{bar}] {score*100:.1f}分")
    
    if report["改进建议"]:
        print(f"\n【改进建议】")
        for i, imp in enumerate(report["改进建议"][:5], 1):
            print(f"  {i}. [{imp['优先级']}] {imp.get('类型', imp['维度'])}: {imp['建议']}")
    
    print(f"\n【总体评价】")
    print(f"  {report['总体评价']}")
    
    print("\n" + "=" * 70)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 生成题目质量评价工具（知识库增强版）")
    parser.add_argument("--question", "-q", type=str, help="题目内容")
    parser.add_argument("--answer", "-a", type=str, default="", help="参考答案")
    parser.add_argument("--subject", "-s", type=str, default="数学", help="学科")
    parser.add_argument("--grade", "-g", type=str, default="初中二年级", help="年级")
    parser.add_argument("--type", "-t", type=str, default="选择题", help="题型")
    parser.add_argument("--no-kb", action="store_true", help="禁用知识库增强")
    parser.add_argument("--file", "-f", type=str, help="批量评价文件路径")
    
    args = parser.parse_args()
    
    config = {
        "subject": args.subject,
        "grade": args.grade,
        "question_type": args.type,
        "enable_kb": not args.no_kb
    }
    evaluator = QuestionEvaluatorKB(config)
    
    if args.question:
        report = evaluator.evaluate(question=args.question, answer=args.answer)
        print_report(report)
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        results = []
        for q in questions:
            result = evaluator.evaluate(
                question=q.get("question", ""),
                answer=q.get("answer", "")
            )
            results.append(result)
        print(f"\n✅ 完成{len(results)}道题目的评价")
        avg_score = sum(r["综合得分"] for r in results) / len(results)
        print(f"📊 平均得分：{avg_score:.1f}分")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
