#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
빠른 시작 가이드
Quick Start Guide

Author: AI Assistant
Date: 2024
"""

def quick_start():
    """빠른 시작 가이드"""
    print("🚀 시장조사 분석 프로젝트 빠른 시작 가이드")
    print("=" * 60)
    
    print("\n📋 1단계: 환경 설정")
    print("다음 명령어를 실행하세요:")
    print("pip install -r requirements.txt")
    
    print("\n📊 2단계: 샘플 데이터 생성")
    print("다음 명령어를 실행하세요:")
    print("python run_analysis.py --create-sample")
    
    print("\n🎯 3단계: 분석 실행")
    print("다음 명령어를 실행하세요:")
    print("python run_analysis.py --brand '스타벅스 강남점' --mode analysis")
    
    print("\n📈 4단계: 대시보드 실행")
    print("다음 명령어를 실행하세요:")
    print("python run_analysis.py --brand '스타벅스 강남점' --mode dashboard")
    
    print("\n🔄 5단계: 전체 실행")
    print("다음 명령어를 실행하세요:")
    print("python run_analysis.py --brand '스타벅스 강남점' --mode both")
    
    print("\n📁 생성되는 파일들:")
    print("- 스타벅스_강남점_분석보고서.json")
    print("- 스타벅스_강남점_분석결과.png")
    
    print("\n🌐 대시보드 접속:")
    print("http://localhost:8050")
    
    print("\n" + "=" * 60)
    print("🎉 이제 시작해보세요!")

def show_examples():
    """사용 예시"""
    print("\n📚 사용 예시")
    print("=" * 40)
    
    print("\n🔸 예시 1: 기본 분석")
    print("python run_analysis.py")
    
    print("\n🔸 예시 2: 다른 브랜드 분석")
    print("python run_analysis.py --brand '메가커피 강남점'")
    
    print("\n🔸 예시 3: 실제 데이터 사용")
    print("python run_analysis.py --real-data --customer-file customer.csv --sales-file sales.csv")
    
    print("\n🔸 예시 4: 대시보드만 실행")
    print("python run_analysis.py --mode dashboard --port 8051")
    
    print("\n🔸 예시 5: 샘플 데이터 생성")
    print("python run_analysis.py --create-sample")

def show_troubleshooting():
    """문제 해결"""
    print("\n🆘 문제 해결")
    print("=" * 40)
    
    print("\n❌ 문제 1: 패키지 설치 오류")
    print("해결방법:")
    print("pip install --upgrade pip")
    print("pip install pandas numpy matplotlib seaborn plotly dash")
    
    print("\n❌ 문제 2: 대시보드 실행 오류")
    print("해결방법:")
    print("python dashboard_app.py")
    
    print("\n❌ 문제 3: 데이터 로드 오류")
    print("해결방법:")
    print("1. CSV 파일 인코딩을 UTF-8로 변경")
    print("2. 파일 경로 확인")
    print("3. 샘플 데이터 사용: python run_analysis.py --create-sample")
    
    print("\n❌ 문제 4: 메모리 부족")
    print("해결방법:")
    print("1. 데이터 크기 줄이기")
    print("2. 가상환경 사용")
    print("3. 시스템 메모리 확인")

if __name__ == "__main__":
    quick_start()
    show_examples()
    show_troubleshooting()
