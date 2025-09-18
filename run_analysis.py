#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시장조사 분석 실행 스크립트
Market Research Analysis Execution Script

Author: AI Assistant
Date: 2024
"""

import os
import sys
import argparse
from datetime import datetime
from market_research_analyzer import MarketResearchAnalyzer

def check_requirements():
    """필요한 패키지 설치 확인"""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'plotly', 'dash', 'scikit-learn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 다음 패키지가 설치되지 않았습니다:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n다음 명령어로 설치하세요:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 모든 필요한 패키지가 설치되어 있습니다.")
    return True

def create_sample_data():
    """샘플 데이터 파일 생성"""
    print("📊 샘플 데이터 파일 생성 중...")
    
    # 고객 데이터 생성
    import pandas as pd
    import numpy as np
    
    np.random.seed(42)
    n_customers = 1000
    
    customer_data = pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'age': np.random.normal(32, 8, n_customers).astype(int),
        'gender': np.random.choice(['남성', '여성'], n_customers),
        'visit_time': np.random.choice(['점심시간', '오후', '저녁', '주말'], n_customers, p=[0.4, 0.3, 0.2, 0.1]),
        'purchase_amount': np.random.normal(8500, 2000, n_customers),
        'visit_frequency': np.random.choice(['일주일 1-2회', '월 1-2회', '가끔'], n_customers, p=[0.3, 0.4, 0.3]),
        'satisfaction': np.random.normal(3.5, 0.8, n_customers),
        'waiting_time': np.random.normal(12, 5, n_customers),
        'segment': np.random.choice(['점심시간커피러', '스터디이용자', '모임이용자', '일상커피러'], 
                                  n_customers, p=[0.4, 0.3, 0.2, 0.1])
    })
    
    # 매출 데이터 생성
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    sales_data = pd.DataFrame({
        'date': dates,
        'daily_sales': np.random.normal(2500000, 500000, len(dates)),
        'customer_count': np.random.normal(300, 50, len(dates)),
        'avg_purchase': np.random.normal(8500, 1000, len(dates))
    })
    
    # 파일 저장
    customer_data.to_csv('sample_customer_data.csv', index=False, encoding='utf-8-sig')
    sales_data.to_csv('sample_sales_data.csv', index=False, encoding='utf-8-sig')
    
    print("✅ 샘플 데이터 파일 생성 완료:")
    print("   - sample_customer_data.csv")
    print("   - sample_sales_data.csv")

def run_analysis(brand_name, use_real_data=False, customer_file=None, sales_file=None):
    """분석 실행"""
    print(f"🚀 {brand_name} 시장조사 분석 시작!")
    print("=" * 60)
    
    # 분석기 생성
    analyzer = MarketResearchAnalyzer(brand_name)
    
    # 데이터 로드
    if use_real_data and customer_file and sales_file:
        print("📁 실제 데이터 로드 중...")
        try:
            analyzer.customer_data = pd.read_csv(customer_file)
            analyzer.sales_data = pd.read_csv(sales_file)
            analyzer.sales_data['date'] = pd.to_datetime(analyzer.sales_data['date'])
            print("✅ 실제 데이터 로드 완료!")
        except Exception as e:
            print(f"❌ 데이터 로드 오류: {e}")
            print("샘플 데이터로 대체합니다.")
            analyzer.load_sample_data()
    else:
        print("📊 샘플 데이터 로드 중...")
        analyzer.load_sample_data()
    
    # 분석 실행
    try:
        # 고객 세그먼트 분석
        print("\n🎯 고객 세그먼트 분석...")
        analyzer.analyze_customer_segments()
        
        # 문제점 식별
        print("\n🚨 문제점 식별...")
        problems = analyzer.identify_problems()
        
        # 인사이트 도출
        print("\n💡 인사이트 도출...")
        insights = analyzer.generate_insights()
        
        # 전략 수립
        print("\n🎯 전략 수립...")
        strategies = analyzer.create_strategy()
        
        # 실행 계획 수립
        print("\n🚀 실행 계획 수립...")
        execution_plan = analyzer.create_execution_plan()
        
        # KPI 설정
        print("\n📊 KPI 설정...")
        kpis = analyzer.set_kpis()
        
        # 보고서 생성
        print("\n📋 종합 보고서 생성...")
        report = analyzer.generate_report()
        
        # 시각화 생성
        print("\n📊 시각화 생성...")
        analyzer.create_visualizations()
        
        print("\n" + "=" * 60)
        print("🎉 분석 완료!")
        print("📁 생성된 파일:")
        print(f"   - {brand_name.replace(' ', '_')}_분석보고서.json")
        print(f"   - {brand_name.replace(' ', '_')}_분석결과.png")
        
        return True
        
    except Exception as e:
        print(f"❌ 분석 중 오류 발생: {e}")
        return False

def run_dashboard(port=8050):
    """대시보드 실행"""
    print(f"🚀 대시보드 시작 중...")
    print(f"브라우저에서 http://localhost:{port} 를 열어주세요.")
    
    try:
        from dashboard_app import DashboardApp
        app = DashboardApp()
        app.run(debug=False, port=port)
    except Exception as e:
        print(f"❌ 대시보드 실행 오류: {e}")
        print("다음 명령어로 직접 실행해보세요:")
        print("python dashboard_app.py")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='시장조사 분석 실행 스크립트')
    parser.add_argument('--brand', '-b', default='스타벅스 강남점', 
                       help='분석할 브랜드명 (기본값: 스타벅스 강남점)')
    parser.add_argument('--mode', '-m', choices=['analysis', 'dashboard', 'both'], 
                       default='both', help='실행 모드 (기본값: both)')
    parser.add_argument('--port', '-p', type=int, default=8050, 
                       help='대시보드 포트 (기본값: 8050)')
    parser.add_argument('--real-data', action='store_true', 
                       help='실제 데이터 사용')
    parser.add_argument('--customer-file', '-c', 
                       help='고객 데이터 CSV 파일 경로')
    parser.add_argument('--sales-file', '-s', 
                       help='매출 데이터 CSV 파일 경로')
    parser.add_argument('--create-sample', action='store_true', 
                       help='샘플 데이터 파일 생성')
    
    args = parser.parse_args()
    
    print("📊 시장조사 기반 비즈니스 문제해결 프로젝트")
    print("=" * 60)
    
    # 필요한 패키지 확인
    if not check_requirements():
        return
    
    # 샘플 데이터 생성
    if args.create_sample:
        create_sample_data()
        return
    
    # 분석 실행
    if args.mode in ['analysis', 'both']:
        success = run_analysis(
            brand_name=args.brand,
            use_real_data=args.real_data,
            customer_file=args.customer_file,
            sales_file=args.sales_file
        )
        
        if not success:
            print("❌ 분석 실행 실패")
            return
    
    # 대시보드 실행
    if args.mode in ['dashboard', 'both']:
        if args.mode == 'both':
            print("\n" + "=" * 60)
            print("🚀 대시보드 시작...")
            print("브라우저에서 대시보드를 확인하세요.")
            print("분석을 종료하려면 Ctrl+C를 누르세요.")
            print("=" * 60)
        
        run_dashboard(args.port)

if __name__ == "__main__":
    main()
