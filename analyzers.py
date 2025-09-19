#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
분석 클래스들
Analyzers for Ashley Customer Validation System
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
from config import Config
from utils import setup_logging, calculate_percentage, safe_divide, calculate_correlation
from database_manager import DatabaseManager

class RevisitAnalyzer:
    """재방문율 분석 클래스"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logging()
    
    def calculate_revisit_rate(self, period_days: int = None) -> Dict[str, Any]:
        """재방문율 계산"""
        period_days = period_days or Config.DEFAULT_ANALYSIS_PERIOD_DAYS
        self.logger.info(f"🔄 최근 {period_days}일 재방문율 분석...")
        
        try:
            visits = self.db_manager.get_customer_visits(period_days)
            
            if not visits:
                self.logger.warning("방문 데이터가 없습니다.")
                return self._empty_result(period_days)
            
            # 고객별 방문 횟수 계산
            customer_visits = {}
            for visit in visits:
                customer_id = visit[1]  # customer_id는 두 번째 컬럼
                customer_visits[customer_id] = customer_visits.get(customer_id, 0) + 1
            
            # 재방문율 계산
            total_customers = len(customer_visits)
            repeat_customers = len([count for count in customer_visits.values() if count > 1])
            revisit_rate = calculate_percentage(repeat_customers, total_customers)
            
            # 방문 빈도 분포
            visit_frequency = {}
            for count in customer_visits.values():
                visit_frequency[count] = visit_frequency.get(count, 0) + 1
            
            result = {
                'total_customers': total_customers,
                'repeat_customers': repeat_customers,
                'revisit_rate': revisit_rate,
                'visit_frequency': visit_frequency,
                'period_days': period_days,
                'customer_visits': customer_visits
            }
            
            self.logger.info(f"📊 재방문율 분석 결과:")
            self.logger.info(f"   - 총 고객 수: {total_customers}명")
            self.logger.info(f"   - 재방문 고객: {repeat_customers}명")
            self.logger.info(f"   - 재방문율: {revisit_rate:.1f}%")
            
            return result
            
        except Exception as e:
            self.logger.error(f"재방문율 분석 오류: {e}")
            return self._empty_result(period_days)
    
    def _empty_result(self, period_days: int) -> Dict[str, Any]:
        """빈 결과 반환"""
        return {
            'total_customers': 0,
            'repeat_customers': 0,
            'revisit_rate': 0.0,
            'visit_frequency': {},
            'period_days': period_days,
            'customer_visits': {}
        }

class IngredientAnalyzer:
    """재료 소진율 분석 클래스"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logging()
    
    def analyze_consumption(self) -> Dict[str, Any]:
        """재료 소진율 분석"""
        self.logger.info("🥘 재료 소진율 분석...")
        
        try:
            ingredients = self.db_manager.get_ingredient_inventory()
            
            if not ingredients:
                self.logger.warning("재료 데이터가 없습니다.")
                return self._empty_result()
            
            consumption_data = []
            total_waste_cost = 0
            
            for ingredient in ingredients:
                name, initial, current, unit, expiration, cost = ingredient[1:7]
                
                consumed = initial - current
                consumption_rate = calculate_percentage(consumed, initial)
                remaining_rate = calculate_percentage(current, initial)
                
                # 폐기 비용 계산 (남은 재료의 10%가 폐기된다고 가정)
                waste_amount = current * 0.1
                waste_cost = waste_amount * cost
                
                consumption_data.append({
                    'ingredient': name,
                    'initial_quantity': initial,
                    'current_quantity': current,
                    'consumed_quantity': consumed,
                    'consumption_rate': consumption_rate,
                    'remaining_rate': remaining_rate,
                    'unit': unit,
                    'waste_cost': waste_cost
                })
                
                total_waste_cost += waste_cost
            
            # 위험 재료 식별
            low_consumption = [x for x in consumption_data 
                             if x['consumption_rate'] < Config.get_threshold('low_consumption_rate')]
            high_consumption = [x for x in consumption_data 
                              if x['consumption_rate'] > Config.get_threshold('high_consumption_rate')]
            
            average_consumption_rate = np.mean([x['consumption_rate'] for x in consumption_data])
            
            result = {
                'consumption_data': consumption_data,
                'low_consumption_ingredients': low_consumption,
                'high_consumption_ingredients': high_consumption,
                'total_waste_cost': total_waste_cost,
                'average_consumption_rate': average_consumption_rate
            }
            
            self.logger.info(f"📊 재료 소진율 분석 결과:")
            self.logger.info(f"   - 평균 소진율: {average_consumption_rate:.1f}%")
            self.logger.info(f"   - 예상 폐기 비용: {total_waste_cost:,.0f}원")
            self.logger.info(f"   - 소진율 낮은 재료: {len(low_consumption)}개")
            self.logger.info(f"   - 소진율 높은 재료: {len(high_consumption)}개")
            
            return result
            
        except Exception as e:
            self.logger.error(f"재료 소진율 분석 오류: {e}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, Any]:
        """빈 결과 반환"""
        return {
            'consumption_data': [],
            'low_consumption_ingredients': [],
            'high_consumption_ingredients': [],
            'total_waste_cost': 0.0,
            'average_consumption_rate': 0.0
        }

class DishAnalyzer:
    """접시 분석 클래스"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logging()
    
    def analyze_dish_waste(self) -> Dict[str, Any]:
        """접시 폐기율 분석"""
        self.logger.info("🤖 접시 폐기율 분석...")
        
        try:
            analyses = self.db_manager.get_dish_analysis()
            
            if not analyses:
                self.logger.warning("접시 분석 데이터가 없습니다.")
                return self._empty_result()
            
            # 분석 결과 파싱
            analysis_results = []
            for analysis in analyses:
                try:
                    result_data = json.loads(analysis[4])  # analysis_result 컬럼
                    analysis_results.append(result_data)
                except (json.JSONDecodeError, IndexError):
                    continue
            
            if not analysis_results:
                return self._empty_result()
            
            # 통계 계산
            avg_waste = np.mean([r['waste_percentage'] for r in analysis_results])
            avg_satisfaction = np.mean([r['satisfaction_score'] for r in analysis_results])
            
            # 메뉴별 분석
            dish_stats = {}
            dishes = set(r['dish_name'] for r in analysis_results)
            
            for dish in dishes:
                dish_results = [r for r in analysis_results if r['dish_name'] == dish]
                if dish_results:
                    dish_stats[dish] = {
                        'avg_waste': np.mean([r['waste_percentage'] for r in dish_results]),
                        'avg_satisfaction': np.mean([r['satisfaction_score'] for r in dish_results]),
                        'count': len(dish_results)
                    }
            
            # 상관관계 계산
            waste_scores = [r['waste_percentage'] for r in analysis_results]
            satisfaction_scores = [r['satisfaction_score'] for r in analysis_results]
            correlation = calculate_correlation(waste_scores, satisfaction_scores)
            
            result = {
                'total_dishes_analyzed': len(analysis_results),
                'average_waste_percentage': avg_waste,
                'average_satisfaction': avg_satisfaction,
                'dish_statistics': dish_stats,
                'analysis_results': analysis_results,
                'correlation': correlation
            }
            
            self.logger.info(f"📊 접시 분석 결과:")
            self.logger.info(f"   - 분석된 접시 수: {len(analysis_results)}개")
            self.logger.info(f"   - 평균 폐기율: {avg_waste:.1f}%")
            self.logger.info(f"   - 평균 만족도: {avg_satisfaction:.1f}/5.0")
            self.logger.info(f"   - 폐기율-만족도 상관계수: {correlation:.3f}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"접시 분석 오류: {e}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, Any]:
        """빈 결과 반환"""
        return {
            'total_dishes_analyzed': 0,
            'average_waste_percentage': 0.0,
            'average_satisfaction': 0.0,
            'dish_statistics': {},
            'analysis_results': [],
            'correlation': 0.0
        }

class TrendAnalyzer:
    """트렌드 분석 클래스"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.logger = setup_logging()
    
    def analyze_trends(self, days: int = 30) -> Dict[str, Any]:
        """트렌드 분석"""
        self.logger.info(f"📈 최근 {days}일 트렌드 분석...")
        
        try:
            # 날짜별 데이터 생성 (시뮬레이션)
            dates = [datetime.now() - timedelta(days=i) for i in range(days, 0, -1)]
            
            # 각 지표별 트렌드 데이터 생성
            trends = {
                'dates': [d.strftime('%Y-%m-%d') for d in dates],
                'revisit_rate': self._generate_trend_data(dates, 45, 5, 30, 60),
                'consumption_rate': self._generate_trend_data(dates, 65, 8, 40, 90),
                'waste_percentage': self._generate_trend_data(dates, 15, 3, 5, 25),
                'satisfaction': self._generate_trend_data(dates, 4.2, 0.3, 3.5, 5.0)
            }
            
            # 트렌드 방향 분석
            trend_directions = {}
            for key, values in trends.items():
                if key != 'dates':
                    trend_directions[key] = self._calculate_trend_direction(values)
            
            result = {
                'trends': trends,
                'trend_directions': trend_directions,
                'analysis_period': days
            }
            
            self.logger.info("📊 트렌드 분석 완료")
            return result
            
        except Exception as e:
            self.logger.error(f"트렌드 분석 오류: {e}")
            return {'trends': {}, 'trend_directions': {}, 'analysis_period': days}
    
    def _generate_trend_data(self, dates: List[datetime], mean: float, std: float, 
                           min_val: float, max_val: float) -> List[float]:
        """트렌드 데이터 생성"""
        np.random.seed(42)  # 재현 가능한 결과
        data = np.random.normal(mean, std, len(dates))
        return [max(min_val, min(max_val, val)) for val in data]
    
    def _calculate_trend_direction(self, values: List[float]) -> str:
        """트렌드 방향 계산"""
        if len(values) < 2:
            return "stable"
        
        # 선형 회귀로 트렌드 계산
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "increasing"
        elif slope < -0.1:
            return "decreasing"
        else:
            return "stable"
