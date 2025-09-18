#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
실행 코드 예시
Execution Code Examples

Author: AI Assistant
Date: 2024
"""

import pandas as pd
import numpy as np
from market_research_analyzer import MarketResearchAnalyzer

def example_1_basic_analysis():
    """예시 1: 기본 분석 실행"""
    print("🔸 예시 1: 기본 분석 실행")
    print("-" * 40)
    
    # 분석기 생성
    analyzer = MarketResearchAnalyzer("스타벅스 강남점")
    
    # 전체 분석 실행
    analyzer.run_complete_analysis()
    
    print("✅ 기본 분석 완료!")

def example_2_custom_brand():
    """예시 2: 다른 브랜드 분석"""
    print("\n🔸 예시 2: 다른 브랜드 분석")
    print("-" * 40)
    
    # 다른 브랜드로 분석
    brands = ["메가커피 강남점", "투썸플레이스 강남점", "이디야 강남점"]
    
    for brand in brands:
        print(f"\n📊 {brand} 분석 중...")
        analyzer = MarketResearchAnalyzer(brand)
        analyzer.load_sample_data()
        analyzer.analyze_customer_segments()
        analyzer.identify_problems()
        print(f"✅ {brand} 분석 완료!")

def example_3_step_by_step():
    """예시 3: 단계별 분석"""
    print("\n🔸 예시 3: 단계별 분석")
    print("-" * 40)
    
    analyzer = MarketResearchAnalyzer("스타벅스 강남점")
    
    # 1단계: 데이터 로드
    print("1단계: 데이터 로드")
    analyzer.load_sample_data()
    
    # 2단계: 고객 세그먼트 분석
    print("2단계: 고객 세그먼트 분석")
    segments = analyzer.analyze_customer_segments()
    
    # 3단계: 문제점 식별
    print("3단계: 문제점 식별")
    problems = analyzer.identify_problems()
    
    # 4단계: 인사이트 도출
    print("4단계: 인사이트 도출")
    insights = analyzer.generate_insights()
    
    # 5단계: 전략 수립
    print("5단계: 전략 수립")
    strategies = analyzer.create_strategy()
    
    print("✅ 단계별 분석 완료!")

def example_4_real_data():
    """예시 4: 실제 데이터 사용"""
    print("\n🔸 예시 4: 실제 데이터 사용")
    print("-" * 40)
    
    # 실제 데이터 로드 함수
    def load_real_data(analyzer, customer_file, sales_file):
        """실제 데이터 로드"""
        try:
            # 고객 데이터 로드
            analyzer.customer_data = pd.read_csv(customer_file, encoding='utf-8-sig')
            
            # 매출 데이터 로드
            analyzer.sales_data = pd.read_csv(sales_file, encoding='utf-8-sig')
            analyzer.sales_data['date'] = pd.to_datetime(analyzer.sales_data['date'])
            
            print("✅ 실제 데이터 로드 완료!")
            return True
        except Exception as e:
            print(f"❌ 데이터 로드 오류: {e}")
            return False
    
    # 분석기 생성
    analyzer = MarketResearchAnalyzer("실제 브랜드")
    
    # 실제 데이터 로드 (파일이 있는 경우)
    customer_file = "sample_customer_data.csv"  # 실제 파일 경로로 변경
    sales_file = "sample_sales_data.csv"        # 실제 파일 경로로 변경
    
    if load_real_data(analyzer, customer_file, sales_file):
        # 분석 실행
        analyzer.analyze_customer_segments()
        analyzer.identify_problems()
        analyzer.generate_insights()
        print("✅ 실제 데이터 분석 완료!")
    else:
        print("샘플 데이터로 대체합니다.")
        analyzer.load_sample_data()
        analyzer.run_complete_analysis()

def example_5_custom_analysis():
    """예시 5: 커스텀 분석"""
    print("\n🔸 예시 5: 커스텀 분석")
    print("-" * 40)
    
    analyzer = MarketResearchAnalyzer("커스텀 브랜드")
    analyzer.load_sample_data()
    
    # 커스텀 분석 1: 연령대별 분석
    print("연령대별 분석:")
    age_groups = pd.cut(analyzer.customer_data['age'], 
                       bins=[0, 25, 35, 45, 100], 
                       labels=['20대', '30대', '40대', '50대+'])
    age_analysis = analyzer.customer_data.groupby(age_groups).agg({
        'purchase_amount': 'mean',
        'satisfaction': 'mean',
        'waiting_time': 'mean'
    }).round(2)
    print(age_analysis)
    
    # 커스텀 분석 2: 성별 분석
    print("\n성별 분석:")
    gender_analysis = analyzer.customer_data.groupby('gender').agg({
        'purchase_amount': 'mean',
        'satisfaction': 'mean',
        'waiting_time': 'mean'
    }).round(2)
    print(gender_analysis)
    
    # 커스텀 분석 3: 방문시간대별 분석
    print("\n방문시간대별 분석:")
    time_analysis = analyzer.customer_data.groupby('visit_time').agg({
        'purchase_amount': 'mean',
        'satisfaction': 'mean',
        'waiting_time': 'mean'
    }).round(2)
    print(time_analysis)
    
    print("✅ 커스텀 분석 완료!")

def example_6_export_results():
    """예시 6: 결과 내보내기"""
    print("\n🔸 예시 6: 결과 내보내기")
    print("-" * 40)
    
    analyzer = MarketResearchAnalyzer("스타벅스 강남점")
    analyzer.load_sample_data()
    analyzer.analyze_customer_segments()
    problems = analyzer.identify_problems()
    insights = analyzer.generate_insights()
    
    # Excel 파일로 내보내기
    with pd.ExcelWriter('분석결과.xlsx', engine='openpyxl') as writer:
        # 고객 데이터
        analyzer.customer_data.to_excel(writer, sheet_name='고객데이터', index=False)
        
        # 매출 데이터
        analyzer.sales_data.to_excel(writer, sheet_name='매출데이터', index=False)
        
        # 세그먼트 분석 결과
        segment_df = pd.DataFrame(analyzer.customer_segments).T
        segment_df.to_excel(writer, sheet_name='세그먼트분석')
        
        # 문제점 분석 결과
        problems_df = pd.DataFrame(problems).T
        problems_df.to_excel(writer, sheet_name='문제점분석')
    
    print("✅ Excel 파일로 내보내기 완료: 분석결과.xlsx")
    
    # CSV 파일로 내보내기
    analyzer.customer_data.to_csv('고객데이터.csv', index=False, encoding='utf-8-sig')
    analyzer.sales_data.to_csv('매출데이터.csv', index=False, encoding='utf-8-sig')
    
    print("✅ CSV 파일로 내보내기 완료:")
    print("   - 고객데이터.csv")
    print("   - 매출데이터.csv")

def example_7_batch_analysis():
    """예시 7: 배치 분석"""
    print("\n🔸 예시 7: 배치 분석")
    print("-" * 40)
    
    # 여러 브랜드 배치 분석
    brands = ["스타벅스 강남점", "메가커피 강남점", "투썸플레이스 강남점"]
    results = {}
    
    for brand in brands:
        print(f"\n📊 {brand} 분석 중...")
        analyzer = MarketResearchAnalyzer(brand)
        analyzer.load_sample_data()
        
        # 핵심 지표만 추출
        segments = analyzer.analyze_customer_segments()
        problems = analyzer.identify_problems()
        
        # 결과 저장
        results[brand] = {
            'total_customers': len(analyzer.customer_data),
            'avg_satisfaction': analyzer.customer_data['satisfaction'].mean(),
            'avg_purchase': analyzer.customer_data['purchase_amount'].mean(),
            'avg_waiting': analyzer.customer_data['waiting_time'].mean(),
            'main_problems': list(problems.keys())
        }
    
    # 배치 결과 요약
    print("\n📋 배치 분석 결과 요약:")
    summary_df = pd.DataFrame(results).T
    print(summary_df.round(2))
    
    # 결과를 Excel로 저장
    summary_df.to_excel('배치분석결과.xlsx')
    print("✅ 배치 분석 결과 저장: 배치분석결과.xlsx")

def main():
    """메인 실행 함수"""
    print("🚀 시장조사 분석 실행 코드 예시")
    print("=" * 60)
    
    # 예시 실행
    example_1_basic_analysis()
    example_2_custom_brand()
    example_3_step_by_step()
    example_4_real_data()
    example_5_custom_analysis()
    example_6_export_results()
    example_7_batch_analysis()
    
    print("\n" + "=" * 60)
    print("🎉 모든 예시 실행 완료!")
    print("\n📚 사용 가능한 예시:")
    print("1. example_1_basic_analysis() - 기본 분석")
    print("2. example_2_custom_brand() - 다른 브랜드 분석")
    print("3. example_3_step_by_step() - 단계별 분석")
    print("4. example_4_real_data() - 실제 데이터 사용")
    print("5. example_5_custom_analysis() - 커스텀 분석")
    print("6. example_6_export_results() - 결과 내보내기")
    print("7. example_7_batch_analysis() - 배치 분석")

if __name__ == "__main__":
    main()
