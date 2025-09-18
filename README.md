# 🍽️ 애슐리 고객검증 시스템

## 🎯 프로젝트 개요

이 프로젝트는 애슐리 레스토랑을 위한 고객검증 시스템으로, 재방문율, 재료 소진율, AI 접시 분석을 통한 종합적인 비즈니스 인사이트를 제공합니다.

### 🚀 주요 기능
- **🔄 재방문율 추적**: 고객 방문 패턴 분석 및 재방문율 계산
- **🥘 재료 소진율 모니터링**: 실시간 재료 재고 관리 및 폐기 비용 분석
- **🤖 AI 접시 사진 분석**: 접시 사진을 AI로 분석하여 폐기율과 고객 만족도 측정
- **📊 통합 대시보드**: 모든 데이터를 한눈에 볼 수 있는 실시간 대시보드
- **💡 스마트 권장사항**: AI 기반 비즈니스 개선 제안
- **📈 트렌드 분석**: 시간별 변화 추이 및 예측 분석

## 🚀 설치 및 실행

### 1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 애슐리 고객검증 시스템 실행
```bash
python run_ashley_validation.py
```

### 3. 개별 실행 옵션

#### 📊 전체 분석 실행
```bash
python ashley_customer_validation.py
```

#### 🖥️ 대시보드 실행
```bash
python ashley_dashboard.py
```
대시보드는 http://localhost:8051 에서 확인할 수 있습니다.

## 📁 파일 구조

```
├── ashley_customer_validation.py  # 애슐리 고객검증 메인 클래스
├── ashley_dashboard.py            # 통합 대시보드
├── run_ashley_validation.py       # 실행 스크립트
├── market_research_analyzer.py    # 기존 시장조사 분석기
├── dashboard_app.py               # 기존 대시보드
├── requirements.txt               # 필요한 패키지 목록
├── README.md                     # 프로젝트 설명서
└── 생성된 파일들/
    ├── ashley_customer_validation_report.json
    ├── ashley_customer_validation_analysis.png
    └── ashley_customer_validation.db
```

## 🔧 주요 클래스 및 메서드

### AshleyCustomerValidation 클래스

#### 주요 메서드
- `generate_sample_data()`: 애슐리 샘플 데이터 생성
- `calculate_revisit_rate()`: 재방문율 계산 및 분석
- `analyze_ingredient_consumption()`: 재료 소진율 분석
- `analyze_dish_waste_with_ai()`: AI 기반 접시 사진 분석
- `generate_comprehensive_report()`: 종합 보고서 생성
- `create_visualizations()`: 시각화 생성
- `generate_recommendations()`: 개선 권장사항 생성

### AshleyDashboard 클래스

#### 주요 기능
- **📊 개요 탭**: 전체 현황 및 KPI 요약
- **🔄 재방문율 탭**: 고객 재방문 패턴 상세 분석
- **🥘 재료 관리 탭**: 재료 소진율 및 재고 관리
- **🤖 AI 접시 분석 탭**: AI 분석 결과 및 상관관계
- **📈 트렌드 분석 탭**: 시간별 변화 추이
- **💡 권장사항 탭**: 개선 제안 및 액션 플랜

### 기존 시스템 (호환성 유지)
- `MarketResearchAnalyzer`: 기존 시장조사 분석기
- `DashboardApp`: 기존 대시보드 (포트 8050)

## 📊 애슐리 분석 결과 예시

### 🔄 재방문율 분석
- **총 고객 수**: 500명 (최근 30일)
- **재방문 고객**: 275명
- **재방문율**: 55.0%
- **방문 빈도 분포**: 1회(45%), 2회(30%), 3회 이상(25%)

### 🥘 재료 소진율 분석
- **평균 소진율**: 65.2%
- **예상 폐기 비용**: 125,000원
- **소진율 낮은 재료**: 3개 (메뉴 구성 재검토 필요)
- **소진율 높은 재료**: 2개 (재고 보충 필요)

### 🤖 AI 접시 분석
- **분석된 접시 수**: 20개
- **평균 폐기율**: 15.3%
- **평균 고객 만족도**: 4.2/5.0
- **폐기율 vs 만족도**: 음의 상관관계 (-0.65)

### 💡 주요 권장사항
1. **즉시 실행**: 재고 관리 시스템 개선
2. **단기 개선**: 메뉴 포션 크기 조정
3. **장기 전략**: 고객 데이터 분석 시스템 구축

## 🎯 활용 방법

### 1. 애슐리 고객검증 시스템 실행
```python
from ashley_customer_validation import AshleyCustomerValidation

# 검증 시스템 생성
validator = AshleyCustomerValidation()

# 전체 분석 실행
validator.run_complete_analysis()
```

### 2. 개별 분석 실행
```python
# 샘플 데이터 생성
validator.generate_sample_data()

# 재방문율 분석
revisit_data = validator.calculate_revisit_rate()

# 재료 소진율 분석
consumption_data = validator.analyze_ingredient_consumption()

# AI 접시 분석
ai_data = validator.analyze_dish_waste_with_ai()
```

### 3. 대시보드 활용
```python
from ashley_dashboard import AshleyDashboard

# 대시보드 실행
dashboard = AshleyDashboard()
dashboard.run()
```

### 4. 통합 실행
```bash
python run_ashley_validation.py
```
- 메뉴에서 원하는 기능 선택
- 대시보드는 http://localhost:8051 에서 확인

## 📈 기대 효과

### 정량적 성과
- **재방문율 향상**: 55% → 70% 이상
- **재료 폐기 비용 절감**: 30% 이상 감소
- **고객 만족도**: 4.2/5.0 → 4.5/5.0 이상
- **운영 효율성**: 재고 관리 40% 개선

### 정성적 성과
- **데이터 기반 의사결정**: AI 분석을 통한 객관적 의사결정
- **예측적 재고 관리**: 재료 소진 패턴 예측 및 최적화
- **고객 경험 개선**: 접시 분석을 통한 메뉴 품질 향상
- **비용 최적화**: 폐기 비용 절감 및 수익성 향상

## 🔄 커스터마이징

### 다른 레스토랑 브랜드 적용
```python
# 다른 브랜드로 분석 (데이터베이스 이름 변경)
validator = AshleyCustomerValidation("other_restaurant_validation.db")
validator.run_complete_analysis()
```

### 실제 데이터 연동
- `generate_sample_data()` 메서드를 실제 데이터 로드로 수정
- CSV 파일이나 API에서 데이터 가져오기
- 데이터베이스 스키마 확장 가능

### AI 모델 커스터마이징
- `analyze_dish_waste_with_ai()` 메서드에 실제 이미지 분석 모델 연동
- TensorFlow, PyTorch 등 ML 프레임워크 활용
- 커스텀 이미지 분류 모델 훈련

## 🛠️ 기술 스택

### 핵심 기술
- **Python 3.8+**: 메인 개발 언어
- **SQLite**: 데이터베이스
- **Pandas/NumPy**: 데이터 분석 및 처리
- **Matplotlib/Seaborn**: 시각화
- **Plotly**: 인터랙티브 차트
- **Dash**: 웹 대시보드

### AI/ML 기술
- **OpenCV**: 이미지 처리
- **TensorFlow/Keras**: AI 모델 (접시 분석)
- **Pillow**: 이미지 조작
- **Scikit-learn**: 머신러닝

### 웹 기술
- **Flask**: API 서버 (확장 가능)
- **Dash**: 실시간 대시보드
- **HTML/CSS/JavaScript**: 프론트엔드

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

## 🚀 빠른 시작 가이드

1. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **시스템 실행**
   ```bash
   python run_ashley_validation.py
   ```

3. **대시보드 확인**
   - 브라우저에서 http://localhost:8051 접속
   - 실시간 데이터 확인 및 분석

---

**🍽️ 애슐리 고객검증 시스템으로 레스토랑 비즈니스를 혁신해보세요!**
