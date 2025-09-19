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
    
    def calculate_revisit_rate(self, period_days: int = None) -> Dict[str, Any]:
        """재방문율 계산"""
        return self.revisit_analyzer.calculate_revisit_rate(period_days)
    
    def analyze_ingredient_consumption(self) -> Dict[str, Any]:
        """재료 소진율 분석"""
        return self.ingredient_analyzer.analyze_consumption()
    
    def analyze_dish_waste_with_ai(self) -> Dict[str, Any]:
        """AI 기반 접시 사진 분석"""
        return self.dish_analyzer.analyze_dish_waste()
    
    def analyze_trends(self, days: int = 30) -> Dict[str, Any]:
        """트렌드 분석"""
        return self.trend_analyzer.analyze_trends(days)
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """종합 보고서 생성"""
        self.logger.info("📋 애슐리 고객검증 종합 보고서 생성...")
        
        try:
            # 각 분석 실행
            revisit_data = self.calculate_revisit_rate()
            consumption_data = self.analyze_ingredient_consumption()
            ai_analysis_data = self.analyze_dish_waste_with_ai()
            trend_data = self.analyze_trends()
            
            # 종합 보고서
            report = {
                'report_date': self._get_current_datetime(),
                'revisit_analysis': revisit_data,
                'ingredient_consumption': consumption_data,
                'ai_dish_analysis': ai_analysis_data,
                'trend_analysis': trend_data,
                'recommendations': self.generate_recommendations(revisit_data, consumption_data, ai_analysis_data),
                'database_stats': self.db_manager.get_database_stats()
            }
            
            # JSON 파일로 저장
            report_file = Config.OUTPUT_FILES['report_json']
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"✅ 종합 보고서가 '{report_file}' 파일로 저장되었습니다!")
            
            return report
            
        except Exception as e:
            self.logger.error(f"종합 보고서 생성 오류: {e}")
            raise
    
    def create_visualizations(self):
        """시각화 생성"""
        self.logger.info("📊 시각화 생성...")
        
        try:
            # 데이터 로드
            revisit_data = self.calculate_revisit_rate()
            consumption_data = self.analyze_ingredient_consumption()
            ai_data = self.analyze_dish_waste_with_ai()
            
            # 차트 생성
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('애슐리 고객검증 시스템 분석 결과', fontsize=16, fontweight='bold')
            
            # 1. 재방문율 차트
            self._create_revisit_chart(axes[0, 0], revisit_data)
            
            # 2. 재료 소진율 차트
            self._create_consumption_chart(axes[0, 1], consumption_data)
            
            # 3. AI 분석 - 메뉴별 폐기율
            self._create_waste_chart(axes[1, 0], ai_data)
            
            # 4. 만족도 vs 폐기율 상관관계
            self._create_correlation_chart(axes[1, 1], ai_data)
            
            plt.tight_layout()
            
            # 이미지 저장
            image_file = Config.OUTPUT_FILES['analysis_image']
            plt.savefig(image_file, dpi=300, bbox_inches='tight')
            plt.show()
            
            self.logger.info(f"✅ 시각화가 '{image_file}' 파일로 저장되었습니다!")
            
        except Exception as e:
            self.logger.error(f"시각화 생성 오류: {e}")
            raise
    
    def _create_revisit_chart(self, ax, revisit_data):
        """재방문율 차트 생성"""
        visit_freq = revisit_data['visit_frequency']
        if visit_freq:
            ax.bar(visit_freq.keys(), visit_freq.values(), color=Config.get_chart_color('revisit'))
            ax.set_title('방문 빈도별 고객 수')
            ax.set_xlabel('방문 횟수')
            ax.set_ylabel('고객 수')
        else:
            ax.text(0.5, 0.5, '데이터 없음', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('방문 빈도별 고객 수')
    
    def _create_consumption_chart(self, ax, consumption_data):
        """재료 소진율 차트 생성"""
        consumption_data_list = consumption_data['consumption_data']
        if consumption_data_list:
            ingredients = [x['ingredient'] for x in consumption_data_list]
            consumption_rates = [x['consumption_rate'] for x in consumption_data_list]
            
            # 색상 설정 (소진율에 따라)
            colors = []
            for rate in consumption_rates:
                if rate < Config.get_threshold('low_consumption_rate'):
                    colors.append(Config.get_chart_color('consumption_low'))
                elif rate < 70:
                    colors.append(Config.get_chart_color('consumption_medium'))
                else:
                    colors.append(Config.get_chart_color('consumption_high'))
            
            ax.bar(ingredients, consumption_rates, color=colors)
            ax.set_title('재료별 소진율')
            ax.set_ylabel('소진율 (%)')
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, '데이터 없음', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('재료별 소진율')
    
    def _create_waste_chart(self, ax, ai_data):
        """폐기율 차트 생성"""
        dish_stats = ai_data['dish_statistics']
        if dish_stats:
            dishes = list(dish_stats.keys())
            waste_rates = [dish_stats[dish]['avg_waste'] for dish in dishes]
            
            ax.bar(dishes, waste_rates, color=Config.get_chart_color('waste'))
            ax.set_title('메뉴별 평균 폐기율')
            ax.set_ylabel('폐기율 (%)')
            ax.tick_params(axis='x', rotation=45)
        else:
            ax.text(0.5, 0.5, '데이터 없음', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('메뉴별 평균 폐기율')
    
    def _create_correlation_chart(self, ax, ai_data):
        """상관관계 차트 생성"""
        analysis_results = ai_data['analysis_results']
        if analysis_results:
            waste_scores = [x['waste_percentage'] for x in analysis_results]
            satisfaction_scores = [x['satisfaction_score'] for x in analysis_results]
            
            ax.scatter(waste_scores, satisfaction_scores, alpha=0.6, 
                      color=Config.get_chart_color('satisfaction'))
            ax.set_title('폐기율 vs 고객 만족도')
            ax.set_xlabel('폐기율 (%)')
            ax.set_ylabel('만족도 (5점 척도)')
        else:
            ax.text(0.5, 0.5, '데이터 없음', ha='center', va='center', transform=ax.transAxes)
            ax.set_title('폐기율 vs 고객 만족도')
    
    def generate_recommendations(self, revisit_data: Dict, consumption_data: Dict, 
                               ai_data: Dict) -> List[str]:
        """개선 권장사항 생성"""
        recommendations = []
        
        # 재방문율 관련 권장사항
        if revisit_data['revisit_rate'] < Config.get_threshold('low_revisit_rate'):
            recommendations.append("재방문율이 낮습니다. 고객 만족도 향상을 위한 메뉴 개선이 필요합니다.")
        
        # 재료 소진율 관련 권장사항
        if len(consumption_data['low_consumption_ingredients']) > 2:
            recommendations.append("소진율이 낮은 재료가 많습니다. 메뉴 구성 재검토가 필요합니다.")
        
        if consumption_data['total_waste_cost'] > Config.get_threshold('high_waste_cost'):
            recommendations.append("폐기 비용이 높습니다. 재고 관리 시스템 개선이 필요합니다.")
        
        # AI 분석 관련 권장사항
        if ai_data['average_waste_percentage'] > Config.get_threshold('high_waste_percentage'):
            recommendations.append("접시 폐기율이 높습니다. 포션 크기 조정을 고려해보세요.")
        
        if ai_data['average_satisfaction'] < Config.get_threshold('low_satisfaction'):
            recommendations.append("고객 만족도가 낮습니다. 음식 품질 개선이 필요합니다.")
        
        return recommendations
    
    def run_complete_analysis(self):
        """전체 분석 실행"""
        self.logger.info("🚀 애슐리 고객검증 시스템 분석 시작!")
        self.logger.info("=" * 60)
        
        try:
            # 1. 샘플 데이터 생성
            self.generate_sample_data()
            
            # 2. 재방문율 분석
            self.calculate_revisit_rate()
            
            # 3. 재료 소진율 분석
            self.analyze_ingredient_consumption()
            
            # 4. AI 접시 분석
            self.analyze_dish_waste_with_ai()
            
            # 5. 트렌드 분석
            self.analyze_trends()
            
            # 6. 종합 보고서 생성
            self.generate_comprehensive_report()
            
            # 7. 시각화 생성
            self.create_visualizations()
            
            self.logger.info("\n" + "=" * 60)
            self.logger.info("🎉 애슐리 고객검증 시스템 분석 완료!")
            self.logger.info("📁 생성된 파일:")
            self.logger.info(f"   - {Config.OUTPUT_FILES['report_json']}")
            self.logger.info(f"   - {Config.OUTPUT_FILES['analysis_image']}")
            self.logger.info(f"   - {Config.OUTPUT_FILES['database']}")
            
        except Exception as e:
            self.logger.error(f"전체 분석 실행 오류: {e}")
            raise
    
    def get_database_stats(self) -> Dict[str, int]:
        """데이터베이스 통계 조회"""
        return self.db_manager.get_database_stats()
    
    def _get_current_datetime(self) -> str:
        """현재 날짜시간 반환"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def close_connection(self):
        """데이터베이스 연결 종료"""
        # DatabaseManager는 컨텍스트 매니저를 사용하므로 별도 종료 불필요
        self.logger.info("✅ 데이터베이스 연결이 종료되었습니다.")


def main():
    """메인 실행 함수"""
    # 애슐리 고객검증 시스템 생성
    validator = AshleyCustomerValidation()
    
    try:
        # 전체 분석 실행
        validator.run_complete_analysis()
    except Exception as e:
        validator.logger.error(f"실행 오류: {e}")
    finally:
        # 데이터베이스 연결 종료
        validator.close_connection()


if __name__ == "__main__":
    main()
