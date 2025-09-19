#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
애슐리 고객검증 시스템 유틸리티 함수
Ashley Customer Validation System Utilities
"""

import logging
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from typing import Optional, List, Dict, Any
import numpy as np
from datetime import datetime, timedelta

# 로깅 설정
def setup_logging(level: str = "INFO") -> logging.Logger:
    """로깅 설정"""
    logger = logging.getLogger("ashley_validation")
    logger.setLevel(getattr(logging, level.upper()))
    
    # 핸들러가 이미 있으면 제거
    if logger.handlers:
        logger.handlers.clear()
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # 포맷터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger

def setup_korean_font() -> Optional[str]:
    """한글 폰트 설정"""
    from config import Config
    
    font_paths = Config.KOREAN_FONTS
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                plt.rcParams['font.family'] = font_name
                plt.rcParams['axes.unicode_minus'] = False
                return font_name
            except Exception:
                continue
    
    # 폰트를 찾지 못한 경우 기본 설정
    plt.rcParams['font.family'] = ['Malgun Gothic', 'Gulim', 'Dotum', 'Batang', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return None

def format_currency(amount: float) -> str:
    """통화 형식으로 포맷팅"""
    return f"{amount:,.0f}원"

def format_percentage(value: float, decimals: int = 1) -> str:
    """퍼센트 형식으로 포맷팅"""
    return f"{value:.{decimals}f}%"

def format_date(date_obj: datetime) -> str:
    """날짜 형식으로 포맷팅"""
    return date_obj.strftime('%Y-%m-%d')

def format_datetime(datetime_obj: datetime) -> str:
    """날짜시간 형식으로 포맷팅"""
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

def calculate_percentage(part: float, total: float) -> float:
    """퍼센트 계산"""
    if total == 0:
        return 0.0
    return (part / total) * 100

def clamp(value: float, min_val: float, max_val: float) -> float:
    """값을 범위 내로 제한"""
    return max(min_val, min(max_val, value))

def generate_customer_id() -> str:
    """고객 ID 생성"""
    return f"CUST_{np.random.randint(1000, 9999)}"

def generate_random_date(days_back: int = 90) -> datetime:
    """랜덤 날짜 생성"""
    return datetime.now() - timedelta(days=np.random.randint(0, days_back))

def calculate_correlation(x: List[float], y: List[float]) -> float:
    """상관계수 계산"""
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    
    correlation_matrix = np.corrcoef(x, y)
    return correlation_matrix[0, 1] if not np.isnan(correlation_matrix[0, 1]) else 0.0

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """안전한 나눗셈"""
    if denominator == 0:
        return default
    return numerator / denominator

def validate_data(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """데이터 유효성 검사"""
    return all(key in data for key in required_keys)

def create_directory_if_not_exists(directory: str) -> None:
    """디렉토리가 없으면 생성"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_size_mb(file_path: str) -> float:
    """파일 크기 (MB) 반환"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0.0

def clean_filename(filename: str) -> str:
    """파일명 정리 (특수문자 제거)"""
    import re
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

class DataValidator:
    """데이터 검증 클래스"""
    
    @staticmethod
    def validate_satisfaction_score(score: float) -> bool:
        """만족도 점수 검증 (1-5 범위)"""
        return 1.0 <= score <= 5.0
    
    @staticmethod
    def validate_percentage(percentage: float) -> bool:
        """퍼센트 값 검증 (0-100 범위)"""
        return 0.0 <= percentage <= 100.0
    
    @staticmethod
    def validate_positive_number(value: float) -> bool:
        """양수 검증"""
        return value >= 0.0
    
    @staticmethod
    def validate_customer_id(customer_id: str) -> bool:
        """고객 ID 형식 검증"""
        import re
        pattern = r'^CUST_\d{4}$'
        return bool(re.match(pattern, customer_id))

class ColorUtils:
    """색상 유틸리티 클래스"""
    
    @staticmethod
    def get_consumption_color(rate: float) -> str:
        """소진율에 따른 색상 반환"""
        from config import Config
        
        if rate < Config.get_threshold('low_consumption_rate'):
            return Config.get_chart_color('consumption_low')
        elif rate < 70:
            return Config.get_chart_color('consumption_medium')
        else:
            return Config.get_chart_color('consumption_high')
    
    @staticmethod
    def get_waste_color(percentage: float) -> str:
        """폐기율에 따른 색상 반환"""
        from config import Config
        
        if percentage > Config.get_threshold('high_waste_percentage'):
            return Config.get_color('danger')
        elif percentage > 10:
            return Config.get_color('warning')
        else:
            return Config.get_color('success')
    
    @staticmethod
    def get_satisfaction_color(score: float) -> str:
        """만족도에 따른 색상 반환"""
        from config import Config
        
        if score < Config.get_threshold('low_satisfaction'):
            return Config.get_color('danger')
        elif score < 4.5:
            return Config.get_color('warning')
        else:
            return Config.get_color('success')
