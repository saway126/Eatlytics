#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 생성 클래스
Data Generator for Ashley Customer Validation System
"""

import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config import Config
from utils import setup_logging, generate_customer_id, generate_random_date, format_date

class DataGenerator:
    """샘플 데이터 생성 클래스"""
    
    def __init__(self):
        self.logger = setup_logging()
        np.random.seed(42)  # 재현 가능한 결과를 위한 시드 설정
    
    def generate_customer_visits(self, count: int = None) -> List[Dict[str, Any]]:
        """고객 방문 데이터 생성"""
        count = count or Config.SAMPLE_DATA_SIZE
        self.logger.info(f"📊 {count}개의 고객 방문 데이터 생성 중...")
        
        visits = []
        menu_items = Config.get_menu_items()
        
        for i in range(count):
            customer_id = generate_customer_id()
            visit_date = generate_random_date()
            
            # 주문 아이템들 (1-4개)
            num_items = np.random.randint(1, 5)
            order_items = np.random.choice(menu_items, num_items, replace=False)
            
            visits.append({
                'customer_id': customer_id,
                'visit_date': format_date(visit_date),
                'table_number': np.random.randint(1, 21),
                'order_items': ','.join(order_items),
                'total_amount': np.random.normal(45000, 15000),
                'satisfaction_score': np.random.normal(4.2, 0.6),
                'visit_duration': np.random.randint(60, 180)  # 60-180분
            })
        
        self.logger.info(f"✅ {len(visits)}개의 고객 방문 데이터 생성 완료")
        return visits
    
    def generate_ingredient_inventory(self) -> List[Dict[str, Any]]:
        """재료 재고 데이터 생성"""
        self.logger.info("🥘 재료 재고 데이터 생성 중...")
        
        ingredients = []
        ingredient_configs = Config.get_ingredients()
        
        for ingredient_config in ingredient_configs:
            # 현재 재고량 (초기량의 10-90%)
            current_qty = ingredient_config["initial"] * np.random.uniform(0.1, 0.9)
            
            ingredients.append({
                'ingredient_name': ingredient_config["name"],
                'initial_quantity': ingredient_config["initial"],
                'current_quantity': current_qty,
                'unit': ingredient_config["unit"],
                'expiration_date': format_date(
                    datetime.now() + timedelta(days=np.random.randint(1, 30))
                ),
                'cost_per_unit': ingredient_config["cost"]
            })
        
        self.logger.info(f"✅ {len(ingredients)}개의 재료 재고 데이터 생성 완료")
        return ingredients
    
    def generate_dish_analysis(self, count: int = 20) -> List[Dict[str, Any]]:
        """접시 분석 데이터 생성 (시뮬레이션)"""
        self.logger.info(f"🤖 {count}개의 접시 분석 데이터 생성 중...")
        
        analyses = []
        dishes = ["스테이크", "파스타", "피자", "샐러드"]
        
        for i in range(count):
            dish = np.random.choice(dishes)
            waste_percentage = np.random.normal(15, 8)  # 평균 15% 폐기
            waste_percentage = max(0, min(100, waste_percentage))  # 0-100% 범위
            
            satisfaction = 5 - (waste_percentage / 20)  # 폐기율이 높을수록 만족도 낮음
            satisfaction = max(1, min(5, satisfaction))
            
            analysis_result = {
                'dish_name': dish,
                'waste_percentage': waste_percentage,
                'satisfaction_score': satisfaction,
                'customer_id': generate_customer_id(),
                'table_number': np.random.randint(1, 21),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            analyses.append({
                'customer_id': analysis_result['customer_id'],
                'table_number': analysis_result['table_number'],
                'dish_name': dish,
                'analysis_result': json.dumps(analysis_result, ensure_ascii=False),
                'waste_percentage': waste_percentage,
                'satisfaction_score': satisfaction
            })
        
        self.logger.info(f"✅ {len(analyses)}개의 접시 분석 데이터 생성 완료")
        return analyses
    
    def generate_all_sample_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """모든 샘플 데이터 생성"""
        self.logger.info("🚀 전체 샘플 데이터 생성 시작...")
        
        data = {
            'customer_visits': self.generate_customer_visits(),
            'ingredient_inventory': self.generate_ingredient_inventory(),
            'dish_analysis': self.generate_dish_analysis()
        }
        
        self.logger.info("✅ 전체 샘플 데이터 생성 완료!")
        return data
    
    def update_ingredient_consumption(self, ingredients: List[Dict[str, Any]], 
                                     consumption_rate: float = 0.1) -> List[Dict[str, Any]]:
        """재료 소비 시뮬레이션"""
        self.logger.info(f"🔄 재료 소비 시뮬레이션 (소비율: {consumption_rate:.1%})")
        
        updated_ingredients = []
        for ingredient in ingredients:
            current_qty = ingredient['current_quantity']
            consumed = current_qty * consumption_rate
            new_qty = max(0, current_qty - consumed)
            
            updated_ingredient = ingredient.copy()
            updated_ingredient['current_quantity'] = new_qty
            updated_ingredients.append(updated_ingredient)
        
        return updated_ingredients
    
    def simulate_daily_operations(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """일일 운영 시뮬레이션"""
        self.logger.info(f"📅 {days}일간 운영 시뮬레이션...")
        
        all_visits = []
        all_analyses = []
        
        for day in range(days):
            # 하루 방문 수 (평균 20-40명)
            daily_visits = np.random.randint(20, 41)
            daily_analyses = np.random.randint(5, 16)
            
            # 해당 날짜의 방문 데이터 생성
            day_visits = self.generate_customer_visits(daily_visits)
            day_analyses = self.generate_dish_analysis(daily_analyses)
            
            # 날짜 설정
            visit_date = datetime.now() - timedelta(days=day)
            for visit in day_visits:
                visit['visit_date'] = format_date(visit_date)
            
            for analysis in day_analyses:
                analysis_result = json.loads(analysis['analysis_result'])
                analysis_result['analysis_date'] = visit_date.strftime('%Y-%m-%d %H:%M:%S')
                analysis['analysis_result'] = json.dumps(analysis_result, ensure_ascii=False)
            
            all_visits.extend(day_visits)
            all_analyses.extend(day_analyses)
        
        self.logger.info(f"✅ {days}일간 시뮬레이션 완료 (총 방문: {len(all_visits)}, 분석: {len(all_analyses)})")
        
        return {
            'customer_visits': all_visits,
            'dish_analysis': all_analyses
        }
