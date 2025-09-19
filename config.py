#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
애슐리 고객검증 시스템 설정 파일
Ashley Customer Validation System Configuration
"""

import os
from typing import Dict, List

class Config:
    """애플리케이션 설정 클래스"""
    
    # 데이터베이스 설정
    DATABASE_PATH = "ashley_customer_validation.db"
    
    # 대시보드 설정
    DASHBOARD_PORT = 8051
    DASHBOARD_HOST = "localhost"
    DASHBOARD_DEBUG = True
    
    # 분석 설정
    DEFAULT_ANALYSIS_PERIOD_DAYS = 30
    SAMPLE_DATA_SIZE = 500
    
    # 한글 폰트 설정
    KOREAN_FONTS = [
        'C:/Windows/Fonts/malgun.ttf',
        'C:/Windows/Fonts/gulim.ttc', 
        'C:/Windows/Fonts/dotum.ttc',
        'C:/Windows/Fonts/batang.ttc'
    ]
    
    # 메뉴 아이템
    MENU_ITEMS = [
        "스테이크", "파스타", "피자", "샐러드", 
        "스프", "빵", "음료", "디저트"
    ]
    
    # 재료 설정
    INGREDIENTS = [
        {"name": "소고기", "initial": 100, "unit": "kg", "cost": 15000},
        {"name": "치킨", "initial": 80, "unit": "kg", "cost": 8000},
        {"name": "파스타면", "initial": 50, "unit": "kg", "cost": 3000},
        {"name": "토마토", "initial": 30, "unit": "kg", "cost": 4000},
        {"name": "치즈", "initial": 25, "unit": "kg", "cost": 12000},
        {"name": "빵", "initial": 40, "unit": "개", "cost": 2000},
        {"name": "야채", "initial": 35, "unit": "kg", "cost": 5000},
        {"name": "소스", "initial": 20, "unit": "L", "cost": 8000}
    ]
    
    # 분석 임계값
    THRESHOLDS = {
        'low_revisit_rate': 50,
        'low_consumption_rate': 30,
        'high_consumption_rate': 80,
        'high_waste_cost': 100000,
        'high_waste_percentage': 20,
        'low_satisfaction': 4.0
    }
    
    # 파일 경로
    OUTPUT_FILES = {
        'report_json': 'ashley_customer_validation_report.json',
        'analysis_image': 'ashley_customer_validation_analysis.png',
        'database': 'ashley_customer_validation.db'
    }
    
    # 색상 테마
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#7f8c8d',
        'success': '#27ae60',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#3498db',
        'light': '#ecf0f1',
        'dark': '#34495e'
    }
    
    # 차트 색상
    CHART_COLORS = {
        'revisit': '#3498db',
        'consumption_low': '#e74c3c',
        'consumption_medium': '#f39c12',
        'consumption_high': '#27ae60',
        'waste': '#e67e22',
        'satisfaction': '#27ae60'
    }
    
    @classmethod
    def get_database_path(cls) -> str:
        """데이터베이스 경로 반환"""
        return cls.DATABASE_PATH
    
    @classmethod
    def get_menu_items(cls) -> List[str]:
        """메뉴 아이템 목록 반환"""
        return cls.MENU_ITEMS.copy()
    
    @classmethod
    def get_ingredients(cls) -> List[Dict]:
        """재료 설정 반환"""
        return cls.INGREDIENTS.copy()
    
    @classmethod
    def get_threshold(cls, key: str) -> float:
        """임계값 반환"""
        return cls.THRESHOLDS.get(key, 0)
    
    @classmethod
    def get_color(cls, key: str) -> str:
        """색상 반환"""
        return cls.COLORS.get(key, '#000000')
    
    @classmethod
    def get_chart_color(cls, key: str) -> str:
        """차트 색상 반환"""
        return cls.CHART_COLORS.get(key, '#000000')
