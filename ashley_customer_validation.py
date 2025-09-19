#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
애슐리 고객검증 시스템 (리팩토링 버전)
Ashley Customer Validation System (Refactored)

주요 기능:
1. 재방문율 추적 및 분석
2. 재료 소진율 모니터링
3. AI 기반 접시 사진 분석

Author: AI Assistant
Date: 2024
"""

import json
import matplotlib.pyplot as plt
from typing import Dict, List, Any
from config import Config
from utils import setup_logging, setup_korean_font, format_currency, format_percentage
from database_manager import DatabaseManager
from data_generator import DataGenerator
from analyzers import RevisitAnalyzer, IngredientAnalyzer, DishAnalyzer, TrendAnalyzer

class AshleyCustomerValidation:
    """애슐리 고객검증 시스템 클래스 (리팩토링 버전)"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.get_database_path()
        self.logger = setup_logging()
        
        # 컴포넌트 초기화
        self.db_manager = DatabaseManager(self.db_path)
        self.data_generator = DataGenerator()
        
        # 분석기 초기화
        self.revisit_analyzer = RevisitAnalyzer(self.db_manager)
        self.ingredient_analyzer = IngredientAnalyzer(self.db_manager)
        self.dish_analyzer = DishAnalyzer(self.db_manager)
        self.trend_analyzer = TrendAnalyzer(self.db_manager)
        
        # 한글 폰트 설정
        setup_korean_font()
        
    def generate_sample_data(self):
        """샘플 데이터 생성"""
        self.logger.info("📊 애슐리 샘플 데이터 생성 중...")
        
        try:
            # 기존 데이터 삭제
            self.db_manager.clear_all_data()
            
            # 새 데이터 생성
            sample_data = self.data_generator.generate_all_sample_data()
            
            # 데이터베이스에 저장
            self.db_manager.insert_customer_visits(sample_data['customer_visits'])
            self.db_manager.insert_ingredient_inventory(sample_data['ingredient_inventory'])
            self.db_manager.insert_dish_analysis(sample_data['dish_analysis'])
            
            self.logger.info("✅ 샘플 데이터 생성 완료!")
            
        except Exception as e:
            self.logger.error(f"샘플 데이터 생성 오류: {e}")
            raise
        
    def generate_sample_data(self):
        """샘플 데이터 생성"""
        print("📊 애슐리 샘플 데이터 생성 중...")
        
        # 고객 방문 데이터 생성
        np.random.seed(42)
        visit_data = []
        
        # 메뉴 아이템들
        menu_items = [
            "스테이크", "파스타", "피자", "샐러드", "스프", "빵", "음료", "디저트"
        ]
        
        for i in range(500):  # 500번의 방문 기록
            customer_id = f"CUST_{np.random.randint(1000, 9999)}"
            visit_date = datetime.now() - timedelta(days=np.random.randint(0, 90))
            
            # 주문 아이템들 (1-4개)
            num_items = np.random.randint(1, 5)
            order_items = np.random.choice(menu_items, num_items, replace=False)
            
            visit_data.append({
                'customer_id': customer_id,
                'visit_date': visit_date.strftime('%Y-%m-%d'),
                'table_number': np.random.randint(1, 21),
                'order_items': ','.join(order_items),
                'total_amount': np.random.normal(45000, 15000),
                'satisfaction_score': np.random.normal(4.2, 0.6),
                'visit_duration': np.random.randint(60, 180)  # 60-180분
            })
        
        # 재료 재고 데이터 생성
        ingredients = [
            {"name": "소고기", "initial": 100, "unit": "kg", "cost": 15000},
            {"name": "치킨", "initial": 80, "unit": "kg", "cost": 8000},
            {"name": "파스타면", "initial": 50, "unit": "kg", "cost": 3000},
            {"name": "토마토", "initial": 30, "unit": "kg", "cost": 4000},
            {"name": "치즈", "initial": 25, "unit": "kg", "cost": 12000},
            {"name": "빵", "initial": 40, "unit": "개", "cost": 2000},
            {"name": "야채", "initial": 35, "unit": "kg", "cost": 5000},
            {"name": "소스", "initial": 20, "unit": "L", "cost": 8000}
        ]
        
        ingredient_data = []
        for ingredient in ingredients:
            # 현재 재고량 (초기량의 10-90%)
            current_qty = ingredient["initial"] * np.random.uniform(0.1, 0.9)
            
            ingredient_data.append({
                'ingredient_name': ingredient["name"],
                'initial_quantity': ingredient["initial"],
                'current_quantity': current_qty,
                'unit': ingredient["unit"],
                'expiration_date': (datetime.now() + timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d'),
                'cost_per_unit': ingredient["cost"]
            })
        
        # 데이터베이스에 저장
        cursor = self.conn.cursor()
        
        # 고객 방문 데이터 삽입
        for data in visit_data:
            cursor.execute('''
                INSERT INTO customer_visits 
                (customer_id, visit_date, table_number, order_items, total_amount, satisfaction_score, visit_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['customer_id'], data['visit_date'], data['table_number'], 
                  data['order_items'], data['total_amount'], data['satisfaction_score'], data['visit_duration']))
        
        # 재료 재고 데이터 삽입
        for data in ingredient_data:
            cursor.execute('''
                INSERT INTO ingredient_inventory 
                (ingredient_name, initial_quantity, current_quantity, unit, expiration_date, cost_per_unit)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['ingredient_name'], data['initial_quantity'], data['current_quantity'], 
                  data['unit'], data['expiration_date'], data['cost_per_unit']))
        
        self.conn.commit()
        print("✅ 샘플 데이터 생성 완료!")
        
    def calculate_revisit_rate(self, period_days: int = 30) -> Dict:
        """재방문율 계산"""
        print(f"\n🔄 최근 {period_days}일 재방문율 분석...")
        
        cursor = self.conn.cursor()
        
        # 기간 설정
        start_date = (datetime.now() - timedelta(days=period_days)).strftime('%Y-%m-%d')
        
        # 해당 기간 내 방문한 고객들
        cursor.execute('''
            SELECT customer_id, COUNT(*) as visit_count
            FROM customer_visits 
            WHERE visit_date >= ?
            GROUP BY customer_id
        ''', (start_date,))
        
        visit_counts = cursor.fetchall()
        
        # 재방문율 계산
        total_customers = len(visit_counts)
        repeat_customers = len([x for x in visit_counts if x[1] > 1])
        revisit_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0
        
        # 세부 분석
        visit_frequency = {}
        for customer_id, count in visit_counts:
            if count not in visit_frequency:
                visit_frequency[count] = 0
            visit_frequency[count] += 1
        
        result = {
            'total_customers': total_customers,
            'repeat_customers': repeat_customers,
            'revisit_rate': revisit_rate,
            'visit_frequency': visit_frequency,
            'period_days': period_days
        }
        
        print(f"📊 재방문율 분석 결과:")
        print(f"   - 총 고객 수: {total_customers}명")
        print(f"   - 재방문 고객: {repeat_customers}명")
        print(f"   - 재방문율: {revisit_rate:.1f}%")
        
        return result
    
    def analyze_ingredient_consumption(self) -> Dict:
        """재료 소진율 분석"""
        print("\n🥘 재료 소진율 분석...")
        
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ingredient_name, initial_quantity, current_quantity, unit, cost_per_unit
            FROM ingredient_inventory
        ''')
        
        ingredients = cursor.fetchall()
        
        consumption_data = []
        total_waste_cost = 0
        
        for ingredient in ingredients:
            name, initial, current, unit, cost = ingredient
            consumed = initial - current
            consumption_rate = (consumed / initial * 100) if initial > 0 else 0
            remaining_rate = (current / initial * 100) if initial > 0 else 0
            
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
        
        # 위험 재료 식별 (소진율이 낮거나 높은 재료)
        low_consumption = [x for x in consumption_data if x['consumption_rate'] < 30]
        high_consumption = [x for x in consumption_data if x['consumption_rate'] > 80]
        
        result = {
            'consumption_data': consumption_data,
            'low_consumption_ingredients': low_consumption,
            'high_consumption_ingredients': high_consumption,
            'total_waste_cost': total_waste_cost,
            'average_consumption_rate': np.mean([x['consumption_rate'] for x in consumption_data])
        }
        
        print(f"📊 재료 소진율 분석 결과:")
        print(f"   - 평균 소진율: {result['average_consumption_rate']:.1f}%")
        print(f"   - 예상 폐기 비용: {total_waste_cost:,.0f}원")
        print(f"   - 소진율 낮은 재료: {len(low_consumption)}개")
        print(f"   - 소진율 높은 재료: {len(high_consumption)}개")
        
        return result
    
    def analyze_dish_waste_with_ai(self, image_path: str = None) -> Dict:
        """AI 기반 접시 사진 분석 (시뮬레이션)"""
        print("\n🤖 AI 접시 사진 분석...")
        
        # 실제로는 이미지 분석 모델을 사용하지만, 여기서는 시뮬레이션
        if image_path and os.path.exists(image_path):
            # 실제 이미지 분석 로직
            image = cv2.imread(image_path)
            # 여기에 실제 AI 분석 코드가 들어갑니다
            pass
        
        # 시뮬레이션 데이터 생성
        np.random.seed(42)
        analysis_results = []
        
        dishes = ["스테이크", "파스타", "피자", "샐러드"]
        
        for i in range(20):  # 20개 접시 분석
            dish = np.random.choice(dishes)
            waste_percentage = np.random.normal(15, 8)  # 평균 15% 폐기
            waste_percentage = max(0, min(100, waste_percentage))  # 0-100% 범위
            
            satisfaction = 5 - (waste_percentage / 20)  # 폐기율이 높을수록 만족도 낮음
            satisfaction = max(1, min(5, satisfaction))
            
            analysis_results.append({
                'dish_name': dish,
                'waste_percentage': waste_percentage,
                'satisfaction_score': satisfaction,
                'customer_id': f"CUST_{np.random.randint(1000, 9999)}",
                'table_number': np.random.randint(1, 21),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # 분석 결과를 데이터베이스에 저장
        cursor = self.conn.cursor()
        for result in analysis_results:
            cursor.execute('''
                INSERT INTO dish_analysis 
                (customer_id, table_number, dish_name, analysis_result, waste_percentage, satisfaction_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (result['customer_id'], result['table_number'], result['dish_name'], 
                  json.dumps(result), result['waste_percentage'], result['satisfaction_score']))
        
        self.conn.commit()
        
        # 통계 계산
        avg_waste = np.mean([r['waste_percentage'] for r in analysis_results])
        avg_satisfaction = np.mean([r['satisfaction_score'] for r in analysis_results])
        
        # 메뉴별 분석
        dish_stats = {}
        for dish in dishes:
            dish_results = [r for r in analysis_results if r['dish_name'] == dish]
            if dish_results:
                dish_stats[dish] = {
                    'avg_waste': np.mean([r['waste_percentage'] for r in dish_results]),
                    'avg_satisfaction': np.mean([r['satisfaction_score'] for r in dish_results]),
                    'count': len(dish_results)
                }
        
        result = {
            'total_dishes_analyzed': len(analysis_results),
            'average_waste_percentage': avg_waste,
            'average_satisfaction': avg_satisfaction,
            'dish_statistics': dish_stats,
            'analysis_results': analysis_results
        }
        
        print(f"📊 AI 접시 분석 결과:")
        print(f"   - 분석된 접시 수: {len(analysis_results)}개")
        print(f"   - 평균 폐기율: {avg_waste:.1f}%")
        print(f"   - 평균 만족도: {avg_satisfaction:.1f}/5.0")
        
        return result
    
    def generate_comprehensive_report(self) -> Dict:
        """종합 보고서 생성"""
        print("\n📋 애슐리 고객검증 종합 보고서 생성...")
        
        # 각 분석 실행
        revisit_data = self.calculate_revisit_rate()
        consumption_data = self.analyze_ingredient_consumption()
        ai_analysis_data = self.analyze_dish_waste_with_ai()
        
        # 종합 보고서
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'revisit_analysis': revisit_data,
            'ingredient_consumption': consumption_data,
            'ai_dish_analysis': ai_analysis_data,
            'recommendations': self.generate_recommendations(revisit_data, consumption_data, ai_analysis_data)
        }
        
        # JSON 파일로 저장
        with open('ashley_customer_validation_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("✅ 종합 보고서가 'ashley_customer_validation_report.json' 파일로 저장되었습니다!")
        
        return report
    
    def create_visualizations(self):
        """시각화 생성"""
        print("\n📊 시각화 생성...")
        
        # 데이터 로드
        revisit_data = self.calculate_revisit_rate()
        consumption_data = self.analyze_ingredient_consumption()
        ai_data = self.analyze_dish_waste_with_ai()
        
        # 스타일 설정
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('애슐리 고객검증 시스템 분석 결과', fontsize=16, fontweight='bold')
        
        # 한글 폰트 재설정
        try:
            # matplotlib 폰트 캐시 초기화
            fm._rebuild()
            plt.rcParams['font.family'] = korean_font if korean_font else 'Malgun Gothic'
            plt.rcParams['font.size'] = 10
            print(f"matplotlib 폰트 설정: {plt.rcParams['font.family']}")
        except Exception as e:
            print(f"폰트 설정 오류: {e}")
            plt.rcParams['font.family'] = 'DejaVu Sans'
        
        # 1. 재방문율 분포
        visit_freq = revisit_data['visit_frequency']
        axes[0, 0].bar(visit_freq.keys(), visit_freq.values(), color='skyblue')
        axes[0, 0].set_title('방문 빈도별 고객 수')
        axes[0, 0].set_xlabel('방문 횟수')
        axes[0, 0].set_ylabel('고객 수')
        
        # 2. 재료별 소진율
        ingredients = [x['ingredient'] for x in consumption_data['consumption_data']]
        consumption_rates = [x['consumption_rate'] for x in consumption_data['consumption_data']]
        axes[0, 1].bar(ingredients, consumption_rates, color='lightcoral')
        axes[0, 1].set_title('재료별 소진율')
        axes[0, 1].set_ylabel('소진율 (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. 메뉴별 폐기율
        if ai_data['dish_statistics']:
            dishes = list(ai_data['dish_statistics'].keys())
            waste_rates = [ai_data['dish_statistics'][dish]['avg_waste'] for dish in dishes]
            axes[1, 0].bar(dishes, waste_rates, color='lightgreen')
            axes[1, 0].set_title('메뉴별 평균 폐기율')
            axes[1, 0].set_ylabel('폐기율 (%)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. 폐기율 vs 만족도 상관관계
        waste_scores = [x['waste_percentage'] for x in ai_data['analysis_results']]
        satisfaction_scores = [x['satisfaction_score'] for x in ai_data['analysis_results']]
        axes[1, 1].scatter(waste_scores, satisfaction_scores, alpha=0.6, color='purple')
        axes[1, 1].set_title('폐기율 vs 고객 만족도')
        axes[1, 1].set_xlabel('폐기율 (%)')
        axes[1, 1].set_ylabel('만족도 (5점 척도)')
        
        plt.tight_layout()
        plt.savefig('ashley_customer_validation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ 시각화가 'ashley_customer_validation_analysis.png' 파일로 저장되었습니다!")
    
    def generate_recommendations(self, revisit_data: Dict, consumption_data: Dict, ai_data: Dict) -> List[str]:
        """개선 권장사항 생성"""
        recommendations = []
        
        # 재방문율 관련 권장사항
        if revisit_data['revisit_rate'] < 50:
            recommendations.append("재방문율이 낮습니다. 고객 만족도 향상을 위한 메뉴 개선이 필요합니다.")
        
        # 재료 소진율 관련 권장사항
        if len(consumption_data['low_consumption_ingredients']) > 2:
            recommendations.append("소진율이 낮은 재료가 많습니다. 메뉴 구성 재검토가 필요합니다.")
        
        if consumption_data['total_waste_cost'] > 100000:
            recommendations.append("폐기 비용이 높습니다. 재고 관리 시스템 개선이 필요합니다.")
        
        # AI 분석 관련 권장사항
        if ai_data['average_waste_percentage'] > 20:
            recommendations.append("접시 폐기율이 높습니다. 포션 크기 조정을 고려해보세요.")
        
        if ai_data['average_satisfaction'] < 4.0:
            recommendations.append("고객 만족도가 낮습니다. 음식 품질 개선이 필요합니다.")
        
        return recommendations
    
    def create_visualizations(self):
        """시각화 생성"""
        print("\n📊 시각화 생성...")
        
        # 데이터 로드
        revisit_data = self.calculate_revisit_rate()
        consumption_data = self.analyze_ingredient_consumption()
        ai_data = self.analyze_dish_waste_with_ai()
        
        # 차트 생성
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('애슐리 고객검증 시스템 분석 결과', fontsize=16, fontweight='bold')
        
        # 1. 재방문율 차트
        visit_freq = revisit_data['visit_frequency']
        axes[0, 0].bar(visit_freq.keys(), visit_freq.values(), color='skyblue')
        axes[0, 0].set_title('방문 빈도별 고객 수')
        axes[0, 0].set_xlabel('방문 횟수')
        axes[0, 0].set_ylabel('고객 수')
        
        # 2. 재료 소진율 차트
        ingredients = [x['ingredient'] for x in consumption_data['consumption_data']]
        consumption_rates = [x['consumption_rate'] for x in consumption_data['consumption_data']]
        axes[0, 1].bar(ingredients, consumption_rates, color='lightcoral')
        axes[0, 1].set_title('재료별 소진율')
        axes[0, 1].set_ylabel('소진율 (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. AI 분석 - 메뉴별 폐기율
        if ai_data['dish_statistics']:
            dishes = list(ai_data['dish_statistics'].keys())
            waste_rates = [ai_data['dish_statistics'][dish]['avg_waste'] for dish in dishes]
            axes[1, 0].bar(dishes, waste_rates, color='lightgreen')
            axes[1, 0].set_title('메뉴별 평균 폐기율')
            axes[1, 0].set_ylabel('폐기율 (%)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. 만족도 vs 폐기율 상관관계
        waste_scores = [x['waste_percentage'] for x in ai_data['analysis_results']]
        satisfaction_scores = [x['satisfaction_score'] for x in ai_data['analysis_results']]
        axes[1, 1].scatter(waste_scores, satisfaction_scores, alpha=0.6, color='purple')
        axes[1, 1].set_title('폐기율 vs 고객 만족도')
        axes[1, 1].set_xlabel('폐기율 (%)')
        axes[1, 1].set_ylabel('만족도 (5점 척도)')
        
        plt.tight_layout()
        plt.savefig('ashley_customer_validation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ 시각화가 'ashley_customer_validation_analysis.png' 파일로 저장되었습니다!")
    
    def run_complete_analysis(self):
        """전체 분석 실행"""
        print("🚀 애슐리 고객검증 시스템 분석 시작!")
        print("=" * 60)
        
        # 1. 샘플 데이터 생성
        self.generate_sample_data()
        
        # 2. 재방문율 분석
        self.calculate_revisit_rate()
        
        # 3. 재료 소진율 분석
        self.analyze_ingredient_consumption()
        
        # 4. AI 접시 분석
        self.analyze_dish_waste_with_ai()
        
        # 5. 종합 보고서 생성
        self.generate_comprehensive_report()
        
        # 6. 시각화 생성
        self.create_visualizations()
        
        print("\n" + "=" * 60)
        print("🎉 애슐리 고객검증 시스템 분석 완료!")
        print("📁 생성된 파일:")
        print("   - ashley_customer_validation_report.json")
        print("   - ashley_customer_validation_analysis.png")
        print("   - ashley_customer_validation.db")
    
    def close_connection(self):
        """데이터베이스 연결 종료"""
        if self.conn:
            self.conn.close()
            print("✅ 데이터베이스 연결이 종료되었습니다.")


def main():
    """메인 실행 함수"""
    # 애슐리 고객검증 시스템 생성
    validator = AshleyCustomerValidation()
    
    try:
        # 전체 분석 실행
        validator.run_complete_analysis()
    finally:
        # 데이터베이스 연결 종료
        validator.close_connection()


if __name__ == "__main__":
    main()
