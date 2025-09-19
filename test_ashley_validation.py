#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
애슐리 고객검증 시스템 테스트
Test Suite for Ashley Customer Validation System
"""

import unittest
import tempfile
import os
from ashley_customer_validation_refactored import AshleyCustomerValidation
from config import Config
from utils import DataValidator, ColorUtils

class TestAshleyCustomerValidation(unittest.TestCase):
    """애슐리 고객검증 시스템 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        # 임시 데이터베이스 파일 생성
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # 테스트용 검증 시스템 생성
        self.validator = AshleyCustomerValidation(self.temp_db.name)
    
    def tearDown(self):
        """테스트 정리"""
        # 임시 파일 삭제
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_initialization(self):
        """초기화 테스트"""
        self.assertIsNotNone(self.validator.db_manager)
        self.assertIsNotNone(self.validator.data_generator)
        self.assertIsNotNone(self.validator.revisit_analyzer)
        self.assertIsNotNone(self.validator.ingredient_analyzer)
        self.assertIsNotNone(self.validator.dish_analyzer)
        self.assertIsNotNone(self.validator.trend_analyzer)
    
    def test_sample_data_generation(self):
        """샘플 데이터 생성 테스트"""
        self.validator.generate_sample_data()
        
        # 데이터베이스 통계 확인
        stats = self.validator.get_database_stats()
        self.assertGreater(stats['customer_visits'], 0)
        self.assertGreater(stats['ingredients'], 0)
        self.assertGreater(stats['dish_analyses'], 0)
    
    def test_revisit_rate_calculation(self):
        """재방문율 계산 테스트"""
        self.validator.generate_sample_data()
        revisit_data = self.validator.calculate_revisit_rate()
        
        self.assertIn('total_customers', revisit_data)
        self.assertIn('repeat_customers', revisit_data)
        self.assertIn('revisit_rate', revisit_data)
        self.assertIn('visit_frequency', revisit_data)
        
        self.assertGreaterEqual(revisit_data['revisit_rate'], 0)
        self.assertLessEqual(revisit_data['revisit_rate'], 100)
    
    def test_ingredient_consumption_analysis(self):
        """재료 소진율 분석 테스트"""
        self.validator.generate_sample_data()
        consumption_data = self.validator.analyze_ingredient_consumption()
        
        self.assertIn('consumption_data', consumption_data)
        self.assertIn('total_waste_cost', consumption_data)
        self.assertIn('average_consumption_rate', consumption_data)
        
        self.assertGreaterEqual(consumption_data['average_consumption_rate'], 0)
        self.assertLessEqual(consumption_data['average_consumption_rate'], 100)
    
    def test_dish_analysis(self):
        """접시 분석 테스트"""
        self.validator.generate_sample_data()
        ai_data = self.validator.analyze_dish_waste_with_ai()
        
        self.assertIn('total_dishes_analyzed', ai_data)
        self.assertIn('average_waste_percentage', ai_data)
        self.assertIn('average_satisfaction', ai_data)
        
        self.assertGreaterEqual(ai_data['average_waste_percentage'], 0)
        self.assertLessEqual(ai_data['average_waste_percentage'], 100)
        self.assertGreaterEqual(ai_data['average_satisfaction'], 1)
        self.assertLessEqual(ai_data['average_satisfaction'], 5)
    
    def test_trend_analysis(self):
        """트렌드 분석 테스트"""
        self.validator.generate_sample_data()
        trend_data = self.validator.analyze_trends()
        
        self.assertIn('trends', trend_data)
        self.assertIn('trend_directions', trend_data)
        self.assertIn('analysis_period', trend_data)
    
    def test_comprehensive_report(self):
        """종합 보고서 생성 테스트"""
        self.validator.generate_sample_data()
        report = self.validator.generate_comprehensive_report()
        
        self.assertIn('report_date', report)
        self.assertIn('revisit_analysis', report)
        self.assertIn('ingredient_consumption', report)
        self.assertIn('ai_dish_analysis', report)
        self.assertIn('recommendations', report)
        self.assertIn('database_stats', report)
    
    def test_recommendations_generation(self):
        """권장사항 생성 테스트"""
        # 테스트 데이터
        revisit_data = {'revisit_rate': 30}  # 낮은 재방문율
        consumption_data = {
            'low_consumption_ingredients': [1, 2, 3],  # 많은 낮은 소진율 재료
            'total_waste_cost': 150000  # 높은 폐기 비용
        }
        ai_data = {
            'average_waste_percentage': 25,  # 높은 폐기율
            'average_satisfaction': 3.5  # 낮은 만족도
        }
        
        recommendations = self.validator.generate_recommendations(
            revisit_data, consumption_data, ai_data
        )
        
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)


class TestDataValidator(unittest.TestCase):
    """데이터 검증 클래스 테스트"""
    
    def test_satisfaction_score_validation(self):
        """만족도 점수 검증 테스트"""
        self.assertTrue(DataValidator.validate_satisfaction_score(3.5))
        self.assertTrue(DataValidator.validate_satisfaction_score(1.0))
        self.assertTrue(DataValidator.validate_satisfaction_score(5.0))
        
        self.assertFalse(DataValidator.validate_satisfaction_score(0.5))
        self.assertFalse(DataValidator.validate_satisfaction_score(5.5))
    
    def test_percentage_validation(self):
        """퍼센트 값 검증 테스트"""
        self.assertTrue(DataValidator.validate_percentage(50.0))
        self.assertTrue(DataValidator.validate_percentage(0.0))
        self.assertTrue(DataValidator.validate_percentage(100.0))
        
        self.assertFalse(DataValidator.validate_percentage(-1.0))
        self.assertFalse(DataValidator.validate_percentage(101.0))
    
    def test_positive_number_validation(self):
        """양수 검증 테스트"""
        self.assertTrue(DataValidator.validate_positive_number(10.5))
        self.assertTrue(DataValidator.validate_positive_number(0.0))
        
        self.assertFalse(DataValidator.validate_positive_number(-5.0))
    
    def test_customer_id_validation(self):
        """고객 ID 검증 테스트"""
        self.assertTrue(DataValidator.validate_customer_id("CUST_1234"))
        self.assertTrue(DataValidator.validate_customer_id("CUST_9999"))
        
        self.assertFalse(DataValidator.validate_customer_id("CUST_123"))
        self.assertFalse(DataValidator.validate_customer_id("CUST_12345"))
        self.assertFalse(DataValidator.validate_customer_id("CUST_ABCD"))


class TestColorUtils(unittest.TestCase):
    """색상 유틸리티 클래스 테스트"""
    
    def test_consumption_color(self):
        """소진율 색상 테스트"""
        low_color = ColorUtils.get_consumption_color(20)
        medium_color = ColorUtils.get_consumption_color(50)
        high_color = ColorUtils.get_consumption_color(85)
        
        self.assertIsInstance(low_color, str)
        self.assertIsInstance(medium_color, str)
        self.assertIsInstance(high_color, str)
    
    def test_waste_color(self):
        """폐기율 색상 테스트"""
        low_color = ColorUtils.get_waste_color(5)
        medium_color = ColorUtils.get_waste_color(15)
        high_color = ColorUtils.get_waste_color(25)
        
        self.assertIsInstance(low_color, str)
        self.assertIsInstance(medium_color, str)
        self.assertIsInstance(high_color, str)
    
    def test_satisfaction_color(self):
        """만족도 색상 테스트"""
        low_color = ColorUtils.get_satisfaction_color(3.0)
        medium_color = ColorUtils.get_satisfaction_color(4.0)
        high_color = ColorUtils.get_satisfaction_color(4.8)
        
        self.assertIsInstance(low_color, str)
        self.assertIsInstance(medium_color, str)
        self.assertIsInstance(high_color, str)


class TestConfig(unittest.TestCase):
    """설정 클래스 테스트"""
    
    def test_config_values(self):
        """설정 값 테스트"""
        self.assertIsNotNone(Config.get_database_path())
        self.assertIsInstance(Config.get_menu_items(), list)
        self.assertIsInstance(Config.get_ingredients(), list)
        
        # 임계값 테스트
        self.assertGreater(Config.get_threshold('low_revisit_rate'), 0)
        self.assertGreater(Config.get_threshold('high_waste_cost'), 0)
        
        # 색상 테스트
        self.assertIsInstance(Config.get_color('primary'), str)
        self.assertIsInstance(Config.get_chart_color('revisit'), str)


def run_tests():
    """테스트 실행"""
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    
    # 테스트 클래스들 추가
    test_classes = [
        TestAshleyCustomerValidation,
        TestDataValidator,
        TestColorUtils,
        TestConfig
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 애슐리 고객검증 시스템 테스트 시작...")
    success = run_tests()
    
    if success:
        print("\n✅ 모든 테스트가 성공적으로 완료되었습니다!")
    else:
        print("\n❌ 일부 테스트가 실패했습니다.")
