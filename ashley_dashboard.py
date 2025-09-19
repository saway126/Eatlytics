#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
애슐리 고객검증 통합 대시보드
Ashley Customer Validation Dashboard

주요 기능:
1. 재방문율 실시간 모니터링
2. 재료 소진율 대시보드
3. AI 접시 분석 결과 시각화
4. 종합 KPI 대시보드

Author: AI Assistant
Date: 2024
"""

import dash
from dash import dcc, html, Input, Output, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from ashley_customer_validation_refactored import AshleyCustomerValidation

# Plotly 한글 폰트 설정
import plotly.io as pio
pio.templates.default = "plotly_white"

# 설정에서 한글 폰트 가져오기
from config import Config
KOREAN_FONT = "Malgun Gothic, AppleGothic, Gulim, Dotum, sans-serif"

class AshleyDashboard:
    """애슐리 고객검증 대시보드 클래스"""
    
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        """레이아웃 설정"""
        self.app.layout = html.Div([
            # 헤더
            html.Div([
                html.H1("🍽️ 애슐리 고객검증 시스템", 
                       style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
                html.P("재방문율 · 재료 소진율 · AI 접시 분석 통합 대시보드", 
                      style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 18})
            ]),
            
            # 새로고침 버튼
            html.Div([
                html.Button('🔄 데이터 새로고침', id='refresh-button', n_clicks=0,
                           style={'backgroundColor': '#3498db', 'color': 'white', 
                                 'border': 'none', 'padding': '10px 20px', 
                                 'borderRadius': '5px', 'cursor': 'pointer',
                                 'fontSize': 16, 'margin': '10px'})
            ], style={'textAlign': 'center', 'marginBottom': 30}),
            
            # 로딩 인디케이터
            dcc.Loading(
                id="loading",
                type="default",
                children=html.Div(id="loading-output")
            ),
            
            # KPI 카드들
            html.Div(id="kpi-cards"),
            
            # 탭 메뉴
            dcc.Tabs(id="main-tabs", value="overview", children=[
                dcc.Tab(label="📊 개요", value="overview"),
                dcc.Tab(label="🔄 재방문율", value="revisit"),
                dcc.Tab(label="🥘 재료 관리", value="ingredients"),
                dcc.Tab(label="🤖 AI 접시 분석", value="ai-analysis"),
                dcc.Tab(label="📈 트렌드 분석", value="trends"),
                dcc.Tab(label="💡 권장사항", value="recommendations")
            ], style={'marginTop': 30}),
            
            # 탭 콘텐츠
            html.Div(id="tab-content", style={'marginTop': 20})
        ], style={'padding': '20px', 'backgroundColor': '#f8f9fa'})
    
    def setup_callbacks(self):
        """콜백 함수 설정"""
        
        @self.app.callback(
            [Output("tab-content", "children"), 
             Output("kpi-cards", "children"),
             Output("loading-output", "children")],
            [Input("main-tabs", "value"), 
             Input("refresh-button", "n_clicks")]
        )
        def update_content(active_tab, n_clicks):
            try:
                # 매번 새로운 validator 인스턴스 생성 (스레드 문제 해결)
                validator = AshleyCustomerValidation()
                
                # 데이터 새로고침
                validator.generate_sample_data()
                
                # 각 분석 실행
                revisit_data = validator.calculate_revisit_rate()
                consumption_data = validator.analyze_ingredient_consumption()
                ai_data = validator.analyze_dish_waste_with_ai()
                
                # 연결 종료
                validator.close_connection()
                
                # KPI 카드 생성
                kpi_cards = self.create_kpi_cards(revisit_data, consumption_data, ai_data)
                
                # 탭 콘텐츠 생성
                if active_tab == "overview":
                    content = self.create_overview_tab(revisit_data, consumption_data, ai_data)
                elif active_tab == "revisit":
                    content = self.create_revisit_tab(revisit_data)
                elif active_tab == "ingredients":
                    content = self.create_ingredients_tab(consumption_data)
                elif active_tab == "ai-analysis":
                    content = self.create_ai_analysis_tab(ai_data)
                elif active_tab == "trends":
                    content = self.create_trends_tab(revisit_data, consumption_data, ai_data)
                elif active_tab == "recommendations":
                    content = self.create_recommendations_tab(revisit_data, consumption_data, ai_data)
                else:
                    content = html.Div("탭을 선택해주세요.")
                
                return content, kpi_cards, ""
            except Exception as e:
                error_content = html.Div([
                    html.H3("오류가 발생했습니다", style={'color': 'red'}),
                    html.P(str(e)),
                    html.P("새로고침 버튼을 눌러 다시 시도해주세요.")
                ])
                return error_content, html.Div("오류"), str(e)
    
    def create_kpi_cards(self, revisit_data, consumption_data, ai_data):
        """KPI 카드 생성"""
        cards = html.Div([
            html.Div([
                html.Div([
                    html.H3(f"{revisit_data['revisit_rate']:.1f}%", 
                           style={'color': '#e74c3c', 'margin': 0, 'fontSize': 36}),
                    html.P("재방문율", style={'margin': 0, 'fontSize': 14})
                ], style={'textAlign': 'center', 'padding': '20px', 
                         'backgroundColor': 'white', 'borderRadius': '10px',
                         'margin': '5px', 'flex': '1', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
                
                html.Div([
                    html.H3(f"{consumption_data['average_consumption_rate']:.1f}%", 
                           style={'color': '#f39c12', 'margin': 0, 'fontSize': 36}),
                    html.P("평균 재료 소진율", style={'margin': 0, 'fontSize': 14})
                ], style={'textAlign': 'center', 'padding': '20px', 
                         'backgroundColor': 'white', 'borderRadius': '10px',
                         'margin': '5px', 'flex': '1', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
                
                html.Div([
                    html.H3(f"{ai_data['average_waste_percentage']:.1f}%", 
                           style={'color': '#e67e22', 'margin': 0, 'fontSize': 36}),
                    html.P("평균 접시 폐기율", style={'margin': 0, 'fontSize': 14})
                ], style={'textAlign': 'center', 'padding': '20px', 
                         'backgroundColor': 'white', 'borderRadius': '10px',
                         'margin': '5px', 'flex': '1', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
                
                html.Div([
                    html.H3(f"{ai_data['average_satisfaction']:.1f}/5.0", 
                           style={'color': '#27ae60', 'margin': 0, 'fontSize': 36}),
                    html.P("평균 고객 만족도", style={'margin': 0, 'fontSize': 14})
                ], style={'textAlign': 'center', 'padding': '20px', 
                         'backgroundColor': 'white', 'borderRadius': '10px',
                         'margin': '5px', 'flex': '1', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ], style={'display': 'flex', 'marginBottom': 20})
        ])
        
        return cards
    
    def create_overview_tab(self, revisit_data, consumption_data, ai_data):
        """개요 탭 생성"""
        return html.Div([
            html.H3("📊 전체 현황", style={'marginBottom': 20, 'color': '#2c3e50'}),
            
            # 차트 그리드
            html.Div([
                # 재방문율 차트
                html.Div([
                    dcc.Graph(
                        figure=self.create_revisit_chart(revisit_data),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                # 재료 소진율 차트
                html.Div([
                    dcc.Graph(
                        figure=self.create_consumption_chart(consumption_data),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
            ]),
            
            html.Div([
                # AI 분석 차트
                html.Div([
                    dcc.Graph(
                        figure=self.create_ai_analysis_chart(ai_data),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
                
                # 만족도 vs 폐기율 상관관계
                html.Div([
                    dcc.Graph(
                        figure=self.create_correlation_chart(ai_data),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
            ])
        ])
    
    def create_revisit_tab(self, revisit_data):
        """재방문율 탭 생성"""
        return html.Div([
            html.H3("🔄 재방문율 상세 분석", style={'marginBottom': 20, 'color': '#2c3e50'}),
            
            # 통계 카드
            html.Div([
                html.Div([
                    html.H4(f"{revisit_data['total_customers']}명", 
                           style={'color': '#3498db', 'margin': 0}),
                    html.P("총 고객 수", style={'margin': 0})
                ], style={'textAlign': 'center', 'padding': '15px', 
                         'backgroundColor': '#ecf0f1', 'borderRadius': '8px', 'margin': '5px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{revisit_data['repeat_customers']}명", 
                           style={'color': '#e74c3c', 'margin': 0}),
                    html.P("재방문 고객", style={'margin': 0})
                ], style={'textAlign': 'center', 'padding': '15px', 
                         'backgroundColor': '#ecf0f1', 'borderRadius': '8px', 'margin': '5px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{revisit_data['revisit_rate']:.1f}%", 
                           style={'color': '#27ae60', 'margin': 0}),
                    html.P("재방문율", style={'margin': 0})
                ], style={'textAlign': 'center', 'padding': '15px', 
                         'backgroundColor': '#ecf0f1', 'borderRadius': '8px', 'margin': '5px', 'flex': '1'})
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            # 방문 빈도 차트
            dcc.Graph(
                figure=self.create_revisit_chart(revisit_data),
                style={'height': '500px'}
            )
        ])
    
    def create_ingredients_tab(self, consumption_data):
        """재료 관리 탭 생성"""
        return html.Div([
            html.H3("🥘 재료 소진율 관리", style={'marginBottom': 20, 'color': '#2c3e50'}),
            
            # 경고 카드들
            html.Div([
                html.Div([
                    html.H4("⚠️ 주의 필요", style={'color': '#e74c3c', 'margin': 0}),
                    html.P(f"소진율 낮은 재료: {len(consumption_data['low_consumption_ingredients'])}개", 
                          style={'margin': 0, 'fontSize': 14})
                ], style={'padding': '15px', 'backgroundColor': '#fdf2f2', 
                         'borderRadius': '8px', 'margin': '5px', 'flex': '1', 'border': '1px solid #f5c6cb'}),
                
                html.Div([
                    html.H4("💰 폐기 비용", style={'color': '#f39c12', 'margin': 0}),
                    html.P(f"{consumption_data['total_waste_cost']:,.0f}원", 
                          style={'margin': 0, 'fontSize': 14})
                ], style={'padding': '15px', 'backgroundColor': '#fef9e7', 
                         'borderRadius': '8px', 'margin': '5px', 'flex': '1', 'border': '1px solid #ffeaa7'}),
                
                html.Div([
                    html.H4("📊 평균 소진율", style={'color': '#27ae60', 'margin': 0}),
                    html.P(f"{consumption_data['average_consumption_rate']:.1f}%", 
                          style={'margin': 0, 'fontSize': 14})
                ], style={'padding': '15px', 'backgroundColor': '#f0f9ff', 
                         'borderRadius': '8px', 'margin': '5px', 'flex': '1', 'border': '1px solid #74b9ff'})
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            # 재료별 소진율 차트
            dcc.Graph(
                figure=self.create_consumption_chart(consumption_data),
                style={'height': '500px'}
            ),
            
            # 재료 재고 테이블
            html.H4("📋 재료 재고 현황", style={'marginTop': 30, 'marginBottom': 15}),
            dash_table.DataTable(
                data=consumption_data['consumption_data'],
                columns=[{"name": i.replace('_', ' ').title(), "id": i} for i in 
                        ['ingredient', 'initial_quantity', 'current_quantity', 'consumption_rate', 'unit']],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{consumption_rate} < 30'},
                        'backgroundColor': '#fdf2f2',
                        'color': '#e74c3c',
                    },
                    {
                        'if': {'filter_query': '{consumption_rate} > 80'},
                        'backgroundColor': '#f0f9ff',
                        'color': '#3498db',
                    }
                ],
                page_size=10
            )
        ])
    
    def create_ai_analysis_tab(self, ai_data):
        """AI 접시 분석 탭 생성"""
        return html.Div([
            html.H3("🤖 AI 접시 분석 결과", style={'marginBottom': 20, 'color': '#2c3e50'}),
            
            # 분석 통계
            html.Div([
                html.Div([
                    html.H4(f"{ai_data['total_dishes_analyzed']}개", 
                           style={'color': '#3498db', 'margin': 0}),
                    html.P("분석된 접시", style={'margin': 0})
                ], style={'textAlign': 'center', 'padding': '15px', 
                         'backgroundColor': '#ecf0f1', 'borderRadius': '8px', 'margin': '5px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{ai_data['average_waste_percentage']:.1f}%", 
                           style={'color': '#e74c3c', 'margin': 0}),
                    html.P("평균 폐기율", style={'margin': 0})
                ], style={'textAlign': 'center', 'padding': '15px', 
                         'backgroundColor': '#ecf0f1', 'borderRadius': '8px', 'margin': '5px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{ai_data['average_satisfaction']:.1f}/5.0", 
                           style={'color': '#27ae60', 'margin': 0}),
                    html.P("평균 만족도", style={'margin': 0})
                ], style={'textAlign': 'center', 'padding': '15px', 
                         'backgroundColor': '#ecf0f1', 'borderRadius': '8px', 'margin': '5px', 'flex': '1'})
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            # 메뉴별 분석 차트
            dcc.Graph(
                figure=self.create_ai_analysis_chart(ai_data),
                style={'height': '500px'}
            ),
            
            # 상관관계 분석
            html.H4("📈 폐기율 vs 만족도 상관관계", style={'marginTop': 30, 'marginBottom': 15}),
            dcc.Graph(
                figure=self.create_correlation_chart(ai_data),
                style={'height': '400px'}
            )
        ])
    
    def create_trends_tab(self, revisit_data, consumption_data, ai_data):
        """트렌드 분석 탭 생성"""
        # 시뮬레이션 트렌드 데이터 생성
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        
        # 재방문율 트렌드
        revisit_trend = np.random.normal(45, 5, len(dates))
        revisit_trend = np.clip(revisit_trend, 30, 60)
        
        # 소진율 트렌드
        consumption_trend = np.random.normal(65, 8, len(dates))
        consumption_trend = np.clip(consumption_trend, 40, 90)
        
        # 폐기율 트렌드
        waste_trend = np.random.normal(15, 3, len(dates))
        waste_trend = np.clip(waste_trend, 5, 25)
        
        # 만족도 트렌드
        satisfaction_trend = np.random.normal(4.2, 0.3, len(dates))
        satisfaction_trend = np.clip(satisfaction_trend, 3.5, 5.0)
        
        # 트렌드 차트
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('재방문율 트렌드', '재료 소진율 트렌드', '접시 폐기율 트렌드', '고객 만족도 트렌드'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # 재방문율
        fig.add_trace(
            go.Scatter(x=dates, y=revisit_trend, name='재방문율', line=dict(color='#e74c3c')),
            row=1, col=1
        )
        
        # 소진율
        fig.add_trace(
            go.Scatter(x=dates, y=consumption_trend, name='소진율', line=dict(color='#f39c12')),
            row=1, col=2
        )
        
        # 폐기율
        fig.add_trace(
            go.Scatter(x=dates, y=waste_trend, name='폐기율', line=dict(color='#e67e22')),
            row=2, col=1
        )
        
        # 만족도
        fig.add_trace(
            go.Scatter(x=dates, y=satisfaction_trend, name='만족도', line=dict(color='#27ae60')),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, font=dict(family="Malgun Gothic, Arial, sans-serif"))
        fig.update_xaxes(title_text="날짜")
        fig.update_yaxes(title_text="재방문율 (%)", row=1, col=1)
        fig.update_yaxes(title_text="소진율 (%)", row=1, col=2)
        fig.update_yaxes(title_text="폐기율 (%)", row=2, col=1)
        fig.update_yaxes(title_text="만족도", row=2, col=2)
        
        return html.Div([
            html.H3("📈 트렌드 분석", style={'marginBottom': 20, 'color': '#2c3e50'}),
            
            html.P("시간에 따른 변화 추이를 분석하여 비즈니스 개선점을 도출합니다.", 
                  style={'fontSize': 16, 'color': '#7f8c8d', 'marginBottom': 30}),
            
            dcc.Graph(figure=fig)
        ])
    
    def create_recommendations_tab(self, revisit_data, consumption_data, ai_data):
        """권장사항 탭 생성"""
        recommendations = self.validator.generate_recommendations(revisit_data, consumption_data, ai_data)
        
        return html.Div([
            html.H3("💡 개선 권장사항", style={'marginBottom': 20, 'color': '#2c3e50'}),
            
            html.Div([
                html.Div([
                    html.H4("🎯 우선순위 높음", style={'color': '#e74c3c', 'marginBottom': 15}),
                    html.Ul([
                        html.Li(rec, style={'marginBottom': 10, 'fontSize': 14}) 
                        for rec in recommendations[:3]
                    ])
                ], style={'padding': '20px', 'backgroundColor': '#fdf2f2', 
                         'borderRadius': '10px', 'margin': '10px', 'flex': '1', 
                         'border': '2px solid #e74c3c'}),
                
                html.Div([
                    html.H4("📋 일반 권장사항", style={'color': '#3498db', 'marginBottom': 15}),
                    html.Ul([
                        html.Li(rec, style={'marginBottom': 10, 'fontSize': 14}) 
                        for rec in recommendations[3:]
                    ]) if len(recommendations) > 3 else html.P("추가 권장사항이 없습니다.")
                ], style={'padding': '20px', 'backgroundColor': '#f0f9ff', 
                         'borderRadius': '10px', 'margin': '10px', 'flex': '1',
                         'border': '2px solid #3498db'})
            ], style={'display': 'flex', 'marginBottom': 20}),
            
            # 액션 플랜
            html.H4("📅 액션 플랜", style={'marginTop': 30, 'marginBottom': 15}),
            html.Div([
                html.Div([
                    html.H5("즉시 실행 (1주일)", style={'color': '#e74c3c'}),
                    html.Ul([
                        html.Li("재고 관리 시스템 개선"),
                        html.Li("메뉴 포션 크기 조정"),
                        html.Li("직원 교육 프로그램 실시")
                    ])
                ], style={'padding': '15px', 'backgroundColor': '#fdf2f2', 
                         'borderRadius': '8px', 'margin': '5px', 'flex': '1'}),
                
                html.Div([
                    html.H5("단기 개선 (1개월)", style={'color': '#f39c12'}),
                    html.Ul([
                        html.Li("고객 만족도 향상 프로그램"),
                        html.Li("재방문율 증대 캠페인"),
                        html.Li("재료 공급업체 협상")
                    ])
                ], style={'padding': '15px', 'backgroundColor': '#fef9e7', 
                         'borderRadius': '8px', 'margin': '5px', 'flex': '1'}),
                
                html.Div([
                    html.H5("장기 전략 (3개월)", style={'color': '#27ae60'}),
                    html.Ul([
                        html.Li("메뉴 혁신 및 개발"),
                        html.Li("고객 데이터 분석 시스템 구축"),
                        html.Li("브랜드 이미지 개선")
                    ])
                ], style={'padding': '15px', 'backgroundColor': '#f0f9ff', 
                         'borderRadius': '8px', 'margin': '5px', 'flex': '1'})
            ], style={'display': 'flex'})
        ])
    
    # 차트 생성 메서드들
    def create_revisit_chart(self, revisit_data):
        """재방문율 차트 생성"""
        visit_freq = revisit_data['visit_frequency']
        fig = px.bar(x=list(visit_freq.keys()), y=list(visit_freq.values()),
                    title="방문 빈도별 고객 수",
                    labels={'x': '방문 횟수', 'y': '고객 수'})
        fig.update_traces(marker_color='#3498db')
        fig.update_layout(font=dict(family=KOREAN_FONT))
        return fig
    
    def create_consumption_chart(self, consumption_data):
        """재료 소진율 차트 생성"""
        ingredients = [x['ingredient'] for x in consumption_data['consumption_data']]
        consumption_rates = [x['consumption_rate'] for x in consumption_data['consumption_data']]
        
        fig = px.bar(x=ingredients, y=consumption_rates,
                    title="재료별 소진율",
                    labels={'x': '재료', 'y': '소진율 (%)'})
        
        # 색상 설정 (소진율에 따라)
        colors = ['#e74c3c' if rate < 30 else '#f39c12' if rate < 70 else '#27ae60' 
                 for rate in consumption_rates]
        fig.update_traces(marker_color=colors)
        fig.update_layout(font=dict(family=KOREAN_FONT))
        
        return fig
    
    def create_ai_analysis_chart(self, ai_data):
        """AI 분석 차트 생성"""
        if not ai_data['dish_statistics']:
            return go.Figure()
            
        dishes = list(ai_data['dish_statistics'].keys())
        waste_rates = [ai_data['dish_statistics'][dish]['avg_waste'] for dish in dishes]
        satisfaction_scores = [ai_data['dish_statistics'][dish]['avg_satisfaction'] for dish in dishes]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('메뉴별 평균 폐기율', '메뉴별 평균 만족도'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(
            go.Bar(x=dishes, y=waste_rates, name='폐기율', marker_color='#e67e22'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(x=dishes, y=satisfaction_scores, name='만족도', marker_color='#27ae60'),
            row=1, col=2
        )
        
        fig.update_layout(height=400, showlegend=False, font=dict(family="Malgun Gothic, Arial, sans-serif"))
        fig.update_xaxes(title_text="메뉴")
        fig.update_yaxes(title_text="폐기율 (%)", row=1, col=1)
        fig.update_yaxes(title_text="만족도", row=1, col=2)
        
        return fig
    
    def create_correlation_chart(self, ai_data):
        """상관관계 차트 생성"""
        waste_scores = [x['waste_percentage'] for x in ai_data['analysis_results']]
        satisfaction_scores = [x['satisfaction_score'] for x in ai_data['analysis_results']]
        
        fig = px.scatter(x=waste_scores, y=satisfaction_scores,
                        title="폐기율 vs 고객 만족도 상관관계",
                        labels={'x': '폐기율 (%)', 'y': '만족도 (5점 척도)'},
                        opacity=0.6)
        
        # 상관관계 선 추가
        z = np.polyfit(waste_scores, satisfaction_scores, 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=waste_scores, y=p(waste_scores), 
                               mode='lines', name='트렌드', line=dict(color='red', dash='dash')))
        
        fig.update_layout(font=dict(family=KOREAN_FONT))
        return fig
    
    def run(self, debug=True, port=8051):
        """대시보드 실행"""
        print(f"🚀 애슐리 고객검증 대시보드가 http://localhost:{port} 에서 실행됩니다.")
        self.app.run(debug=debug, port=port)


def main():
    """메인 실행 함수"""
    dashboard = AshleyDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
