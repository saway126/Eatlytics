#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시장조사 기반 비즈니스 문제해결 프로젝트
Market Research Based Business Problem Solving Project

Author: AI Assistant
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class MarketResearchAnalyzer:
    """시장조사 데이터 분석 및 문제해결 클래스"""
    
    def __init__(self, brand_name: str = "스타벅스 강남점"):
        self.brand_name = brand_name
        self.customer_data = None
        self.sales_data = None
        self.competitor_data = None
        self.customer_segments = {}
        self.insights = {}
        
    def load_sample_data(self):
        """샘플 데이터 생성 및 로드"""
        print(f"📊 {self.brand_name} 샘플 데이터 생성 중...")
        
        # 고객 데이터 생성
        np.random.seed(42)
        n_customers = 1000
        
        self.customer_data = pd.DataFrame({
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
        self.sales_data = pd.DataFrame({
            'date': dates,
            'daily_sales': np.random.normal(2500000, 500000, len(dates)),
            'customer_count': np.random.normal(300, 50, len(dates)),
            'avg_purchase': np.random.normal(8500, 1000, len(dates))
        })
        
        # 경쟁사 데이터 생성
        self.competitor_data = pd.DataFrame({
            'competitor': ['메가커피', '투썸플레이스', '이디야', '카페베네', '할리스'],
            'market_share': [15, 12, 10, 8, 6],
            'avg_price': [4500, 6000, 4000, 5000, 5500],
            'customer_satisfaction': [3.8, 4.1, 3.6, 3.9, 4.0]
        })
        
        print("✅ 샘플 데이터 생성 완료!")
        
    def analyze_customer_segments(self):
        """고객 세그먼트 분석"""
        print("\n🎯 고객 세그먼트 분석 시작...")
        
        segment_analysis = {}
        
        for segment in self.customer_data['segment'].unique():
            segment_data = self.customer_data[self.customer_data['segment'] == segment]
            
            analysis = {
                'count': len(segment_data),
                'percentage': len(segment_data) / len(self.customer_data) * 100,
                'avg_age': segment_data['age'].mean(),
                'avg_purchase': segment_data['purchase_amount'].mean(),
                'avg_satisfaction': segment_data['satisfaction'].mean(),
                'avg_waiting_time': segment_data['waiting_time'].mean(),
                'gender_distribution': segment_data['gender'].value_counts().to_dict(),
                'visit_time_distribution': segment_data['visit_time'].value_counts().to_dict()
            }
            
            segment_analysis[segment] = analysis
            
        self.customer_segments = segment_analysis
        
        # 결과 출력
        print("\n📊 고객 세그먼트 분석 결과:")
        for segment, data in segment_analysis.items():
            print(f"\n🔸 {segment}:")
            print(f"   - 고객 수: {data['count']}명 ({data['percentage']:.1f}%)")
            print(f"   - 평균 연령: {data['avg_age']:.1f}세")
            print(f"   - 평균 구매금액: {data['avg_purchase']:,.0f}원")
            print(f"   - 평균 만족도: {data['avg_satisfaction']:.1f}/5.0")
            print(f"   - 평균 대기시간: {data['avg_waiting_time']:.1f}분")
            
        return segment_analysis
    
    def identify_problems(self):
        """문제점 식별 및 분석"""
        print("\n🚨 문제점 식별 및 분석...")
        
        problems = {}
        
        # 문제 1: 점심시간 대기시간 문제
        lunch_segment = self.customer_data[self.customer_data['segment'] == '점심시간커피러']
        avg_waiting_lunch = lunch_segment['waiting_time'].mean()
        
        problems['점심시간_대기시간'] = {
            'current_state': f"{avg_waiting_lunch:.1f}분",
            'target_state': "10분 이하",
            'gap': f"{avg_waiting_lunch - 10:.1f}분",
            'impact': '높음',
            'affected_customers': len(lunch_segment),
            'revenue_impact': len(lunch_segment) * lunch_segment['purchase_amount'].mean() * 0.2  # 20% 매출 영향
        }
        
        # 문제 2: 재구매율 문제
        frequent_customers = self.customer_data[self.customer_data['visit_frequency'] == '일주일 1-2회']
        repurchase_rate = len(frequent_customers) / len(self.customer_data) * 100
        
        problems['재구매율'] = {
            'current_state': f"{repurchase_rate:.1f}%",
            'target_state': "70% 이상",
            'gap': f"{70 - repurchase_rate:.1f}%",
            'impact': '높음',
            'affected_customers': len(self.customer_data) - len(frequent_customers),
            'revenue_impact': (len(self.customer_data) - len(frequent_customers)) * self.customer_data['purchase_amount'].mean() * 0.3
        }
        
        # 문제 3: 신규 고객 유입 문제
        new_customers = self.customer_data[self.customer_data['visit_frequency'] == '가끔']
        new_customer_rate = len(new_customers) / len(self.customer_data) * 100
        
        problems['신규고객_유입'] = {
            'current_state': f"{new_customer_rate:.1f}%",
            'target_state': "30% 이상",
            'gap': f"{30 - new_customer_rate:.1f}%",
            'impact': '중간',
            'affected_customers': len(new_customers),
            'revenue_impact': len(new_customers) * self.customer_data['purchase_amount'].mean() * 0.1
        }
        
        # 결과 출력
        print("\n📋 식별된 주요 문제점:")
        for problem, data in problems.items():
            print(f"\n🔸 {problem}:")
            print(f"   - 현재 상태: {data['current_state']}")
            print(f"   - 목표 상태: {data['target_state']}")
            print(f"   - 차이: {data['gap']}")
            print(f"   - 영향도: {data['impact']}")
            print(f"   - 영향받는 고객: {data['affected_customers']}명")
            print(f"   - 매출 영향: {data['revenue_impact']:,.0f}원")
            
        return problems
    
    def generate_insights(self):
        """인사이트 도출"""
        print("\n💡 인사이트 도출...")
        
        insights = {}
        
        # 고객 인사이트
        insights['고객_인사이트'] = {
            '핵심_니즈': {
                '점심시간커피러': '빠른 서비스, 맛있는 커피',
                '스터디이용자': '조용한 공간, 안정적인 와이파이',
                '모임이용자': '대화하기 좋은 공간, 다양한 메뉴',
                '일상커피러': '일관된 품질, 브랜드 경험'
            },
            '구매_결정요인': ['대기시간', '맛', '가격', '서비스', '분위기'],
            '만족도_영향요인': ['대기시간', '서비스 품질', '메뉴 다양성', '가격 대비 품질']
        }
        
        # 시장 인사이트
        insights['시장_인사이트'] = {
            '경쟁사_대비_차별화': '프리미엄 브랜드 이미지, 다양한 메뉴',
            '시장_기회': '점심시간 서비스 개선, 모바일 주문 시스템',
            '위협요인': '경쟁사 가격 경쟁, 신규 브랜드 진입'
        }
        
        # 운영 인사이트
        insights['운영_인사이트'] = {
            '효율성_개선': '점심시간 인력 배치, 주문 프로세스 개선',
            '고객경험_개선': '대기시간 단축, 개인화 서비스',
            '수익성_개선': '재구매율 향상, 평균 구매금액 증가'
        }
        
        self.insights = insights
        
        # 결과 출력
        print("\n📊 도출된 인사이트:")
        for category, data in insights.items():
            print(f"\n🔸 {category}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"   - {key}: {value}")
            else:
                print(f"   {data}")
                
        return insights
    
    def create_strategy(self):
        """전략 수립"""
        print("\n🎯 전략 수립...")
        
        strategies = {}
        
        # 고객 중심 전략
        strategies['고객_중심_전략'] = {
            '점심시간커피러': {
                '전략': '모바일 주문 + 전용 카운터',
                '목표': '대기시간 10분 이하',
                '방안': ['앱 주문 시스템', '전용 카운터 운영', '간편 메뉴 구성']
            },
            '스터디이용자': {
                '전략': '공간 최적화 + 예약 시스템',
                '목표': '장시간 이용 만족도 향상',
                '방안': ['테이블 배치 개선', '충전기 확대', '예약 시스템 도입']
            },
            '모임이용자': {
                '전략': '그룹 공간 + 세트 메뉴',
                '목표': '그룹 고객 만족도 향상',
                '방안': ['4인 이상 테이블 확대', '세트 메뉴 개발', '그룹 할인 혜택']
            }
        }
        
        # 운영 효율성 전략
        strategies['운영_효율성_전략'] = {
            '프로세스_개선': {
                '주문_프로세스': '주문→제조→픽업 3단계 최적화',
                '결제_프로세스': '모바일 결제 확대, 결제 시간 단축',
                '서빙_프로세스': '픽업 시스템 개선, 대기시간 단축'
            },
            '자원_최적화': {
                '인력_배치': '점심시간 전용 직원 배치',
                '공간_활용': '테이블 배치 최적화, 좌석 관리',
                '메뉴_구성': '간편 메뉴 위주, 제조 시간 단축'
            }
        }
        
        # 결과 출력
        print("\n📋 수립된 전략:")
        for category, data in strategies.items():
            print(f"\n🔸 {category}:")
            if isinstance(data, dict):
                for key, value in data.items():
                    print(f"   - {key}: {value}")
            else:
                print(f"   {data}")
                
        return strategies
    
    def create_execution_plan(self):
        """실행 계획 수립"""
        print("\n🚀 실행 계획 수립...")
        
        execution_plan = {
            'Phase_1_즉시실행': {
                '기간': '1-2주',
                '방안': [
                    '점심시간 전용 카운터 운영',
                    '모바일 주문 시스템 도입',
                    '직원 교육 및 프로세스 개선'
                ],
                '예상_효과': '대기시간 30% 단축, 고객 만족도 향상',
                '투자비용': '500만원',
                'ROI': '200%'
            },
            'Phase_2_단기개선': {
                '기간': '3-4주',
                '방안': [
                    '공간 최적화 및 테이블 배치 개선',
                    '충전기 확대 설치',
                    '그룹 공간 확보'
                ],
                '예상_효과': '재구매율 15% 증가, 평균 체류시간 증가',
                '투자비용': '1000만원',
                'ROI': '150%'
            },
            'Phase_3_중장기전략': {
                '기간': '1-2개월',
                '방안': [
                    '예약 시스템 도입',
                    '그룹 메뉴 개발',
                    '고객 생애 가치 향상 프로그램'
                ],
                '예상_효과': '전체 매출 20% 증가, 브랜드 가치 향상',
                '투자비용': '2000만원',
                'ROI': '120%'
            }
        }
        
        # 결과 출력
        print("\n📅 실행 계획:")
        for phase, data in execution_plan.items():
            print(f"\n🔸 {phase}:")
            print(f"   - 기간: {data['기간']}")
            print(f"   - 방안: {', '.join(data['방안'])}")
            print(f"   - 예상 효과: {data['예상_효과']}")
            print(f"   - 투자 비용: {data['투자비용']}")
            print(f"   - ROI: {data['ROI']}")
            
        return execution_plan
    
    def set_kpis(self):
        """KPI 설정"""
        print("\n📊 KPI 설정...")
        
        kpis = {
            'Phase_1_KPI': {
                '대기시간': '15분 → 10분 이하',
                '고객만족도': '3.5점 → 4.0점 이상',
                '점심시간매출': '20% 증가',
                '앱사용률': '30% 이상'
            },
            'Phase_2_KPI': {
                '재구매율': '50% → 65%',
                '평균체류시간': '30분 → 45분',
                '그룹고객만족도': '4.0점 → 4.2점',
                '공간활용도': '80% → 90%'
            },
            'Phase_3_KPI': {
                '전체매출': '15% 증가',
                '고객생애가치': '20% 증가',
                '브랜드만족도': '4.0점 → 4.3점',
                '신규고객유입': '20% → 30%'
            }
        }
        
        # 결과 출력
        print("\n🎯 설정된 KPI:")
        for phase, data in kpis.items():
            print(f"\n🔸 {phase}:")
            for kpi, target in data.items():
                print(f"   - {kpi}: {target}")
                
        return kpis
    
    def generate_report(self):
        """종합 보고서 생성"""
        print("\n📋 종합 보고서 생성...")
        
        report = {
            '프로젝트_개요': {
                '브랜드명': self.brand_name,
                '분석기간': '2024년 1-6월',
                '분석대상': f"고객 {len(self.customer_data)}명, 매출 {len(self.sales_data)}일",
                '주요목표': '고객 중심 비즈니스 문제 해결'
            },
            '고객_세그먼트_분석': self.customer_segments,
            '식별된_문제점': self.identify_problems(),
            '도출된_인사이트': self.insights,
            '수립된_전략': self.create_strategy(),
            '실행계획': self.create_execution_plan(),
            'KPI': self.set_kpis()
        }
        
        # JSON 파일로 저장
        with open(f'{self.brand_name.replace(" ", "_")}_분석보고서.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"\n✅ 종합 보고서가 '{self.brand_name.replace(' ', '_')}_분석보고서.json' 파일로 저장되었습니다!")
        
        return report
    
    def create_visualizations(self):
        """시각화 생성"""
        print("\n📊 시각화 생성...")
        
        # 스타일 설정
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'{self.brand_name} 시장조사 분석 결과', fontsize=16, fontweight='bold')
        
        # 1. 고객 세그먼트 분포
        segment_counts = self.customer_data['segment'].value_counts()
        axes[0, 0].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('고객 세그먼트 분포')
        
        # 2. 세그먼트별 평균 구매금액
        segment_purchase = self.customer_data.groupby('segment')['purchase_amount'].mean()
        axes[0, 1].bar(segment_purchase.index, segment_purchase.values, color='skyblue')
        axes[0, 1].set_title('세그먼트별 평균 구매금액')
        axes[0, 1].set_ylabel('구매금액 (원)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. 세그먼트별 만족도
        segment_satisfaction = self.customer_data.groupby('segment')['satisfaction'].mean()
        axes[1, 0].bar(segment_satisfaction.index, segment_satisfaction.values, color='lightcoral')
        axes[1, 0].set_title('세그먼트별 평균 만족도')
        axes[1, 0].set_ylabel('만족도 (5점 척도)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. 세그먼트별 대기시간
        segment_waiting = self.customer_data.groupby('segment')['waiting_time'].mean()
        axes[1, 1].bar(segment_waiting.index, segment_waiting.values, color='lightgreen')
        axes[1, 1].set_title('세그먼트별 평균 대기시간')
        axes[1, 1].set_ylabel('대기시간 (분)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.brand_name.replace(" ", "_")}_분석결과.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ 시각화가 '{self.brand_name.replace(' ', '_')}_분석결과.png' 파일로 저장되었습니다!")
    
    def run_complete_analysis(self):
        """전체 분석 실행"""
        print(f"🚀 {self.brand_name} 시장조사 기반 문제해결 프로젝트 시작!")
        print("=" * 60)
        
        # 1. 데이터 로드
        self.load_sample_data()
        
        # 2. 고객 세그먼트 분석
        self.analyze_customer_segments()
        
        # 3. 문제점 식별
        self.identify_problems()
        
        # 4. 인사이트 도출
        self.generate_insights()
        
        # 5. 전략 수립
        self.create_strategy()
        
        # 6. 실행 계획 수립
        self.create_execution_plan()
        
        # 7. KPI 설정
        self.set_kpis()
        
        # 8. 종합 보고서 생성
        self.generate_report()
        
        # 9. 시각화 생성
        self.create_visualizations()
        
        print("\n" + "=" * 60)
        print("🎉 시장조사 기반 문제해결 프로젝트 완료!")
        print("📁 생성된 파일:")
        print(f"   - {self.brand_name.replace(' ', '_')}_분석보고서.json")
        print(f"   - {self.brand_name.replace(' ', '_')}_분석결과.png")


def main():
    """메인 실행 함수"""
    # 분석기 생성
    analyzer = MarketResearchAnalyzer("스타벅스 강남점")
    
    # 전체 분석 실행
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
