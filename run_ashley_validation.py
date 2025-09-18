#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
애슐리 고객검증 시스템 실행 스크립트
Ashley Customer Validation System Runner

Author: AI Assistant
Date: 2024
"""

import sys
import os
from ashley_customer_validation import AshleyCustomerValidation
from ashley_dashboard import AshleyDashboard

def main():
    """메인 실행 함수"""
    print("🍽️ 애슐리 고객검증 시스템")
    print("=" * 50)
    print("1. 전체 분석 실행")
    print("2. 대시보드 실행")
    print("3. 종료")
    print("=" * 50)
    
    while True:
        try:
            choice = input("선택하세요 (1-3): ").strip()
            
            if choice == "1":
                run_analysis()
            elif choice == "2":
                run_dashboard()
            elif choice == "3":
                print("👋 애슐리 고객검증 시스템을 종료합니다.")
                break
            else:
                print("❌ 잘못된 선택입니다. 1-3 중에서 선택해주세요.")
                
        except KeyboardInterrupt:
            print("\n👋 애슐리 고객검증 시스템을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")

def run_analysis():
    """분석 실행"""
    print("\n📊 애슐리 고객검증 분석을 시작합니다...")
    
    try:
        validator = AshleyCustomerValidation()
        validator.run_complete_analysis()
        print("\n✅ 분석이 완료되었습니다!")
        print("📁 생성된 파일:")
        print("   - ashley_customer_validation_report.json")
        print("   - ashley_customer_validation_analysis.png")
        print("   - ashley_customer_validation.db")
        
    except Exception as e:
        print(f"❌ 분석 중 오류가 발생했습니다: {e}")
    finally:
        try:
            validator.close_connection()
        except:
            pass

def run_dashboard():
    """대시보드 실행"""
    print("\n🚀 애슐리 고객검증 대시보드를 실행합니다...")
    print("🌐 브라우저에서 http://localhost:8051 을 열어주세요.")
    print("⏹️  대시보드를 종료하려면 Ctrl+C를 누르세요.")
    
    try:
        dashboard = AshleyDashboard()
        dashboard.run(debug=False, port=8051)
    except KeyboardInterrupt:
        print("\n👋 대시보드가 종료되었습니다.")
    except Exception as e:
        print(f"❌ 대시보드 실행 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
