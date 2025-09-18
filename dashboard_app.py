#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시장조사 분석 대시보드 앱
Market Research Analysis Dashboard App

Author: AI Assistant
Date: 2024
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from market_research_analyzer import MarketResearchAnalyzer

class DashboardApp:
    """시장조사 분석 대시보드 앱 클래스"""
    
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.analyzer = MarketResearchAnalyzer()
        self.setup_layout()
        self.setup_callbacks()
        
    def setup_layout(self):
        """레이아웃 설정"""
        self.app.layout = html.Div([
            html.H1("📊 시장조사 기반 비즈니스 문제해결 대시보드", 
                   style={'textAlign': 'center', 'marginBottom': 30}),
            
            # 브랜드 선택
            html.Div([
                html.Label("브랜드 선택:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='brand-dropdown',
                    options=[
                        {'label': '스타벅스 강남점', 'value': '스타벅스 강남점'},
                        {'label': '메가커피 강남점', 'value': '메가커피 강남점'},
                        {'label': '투썸플레이스 강남점', 'value': '투썸플레이스 강남점'}
                    ],
                    value='스타벅스 강남점',
                    style={'width': '300px'}
                )
            ], style={'marginBottom': 20}),
            
            # 분석 실행 버튼
            html.Div([
                html.Button('분석 실행', id='analyze-button', n_clicks=0,
                           style={'backgroundColor': '#007bff', 'color': 'white', 
                                 'border': 'none', 'padding': '10px 20px', 
                                 'borderRadius': '5px', 'cursor': 'pointer'})
            ], style={'marginBottom': 30}),
            
            # 로딩 인디케이터
            dcc.Loading(
                id="loading",
                type="default",
                children=html.Div(id="loading-output")
            ),
            
            # 탭 메뉴
            dcc.Tabs(id="main-tabs", value="overview", children=[
                dcc.Tab(label="📊 개요", value="overview"),
                dcc.Tab(label="👥 고객 분석", value="customer"),
                dcc.Tab(label="🚨 문제 분석", value="problems"),
                dcc.Tab(label="💡 인사이트", value="insights"),
                dcc.Tab(label="🎯 전략", value="strategy"),
                dcc.Tab(label="📈 KPI", value="kpi")
            ]),
            
            # 탭 콘텐츠
            html.Div(id="tab-content")
        ])
    
    def setup_callbacks(self):
        """콜백 함수 설정"""
        
        @self.app.callback(
            [Output("tab-content", "children"), Output("loading-output", "children")],
            [Input("main-tabs", "value"), Input("analyze-button", "n_clicks")]
        )
        def update_tab_content(active_tab, n_clicks):
            if n_clicks == 0:
                return html.Div("분석 실행 버튼을 클릭하여 데이터를 로드하세요."), ""
            
            # 데이터 로드
            self.analyzer.load_sample_data()
            self.analyzer.analyze_customer_segments()
            problems = self.analyzer.identify_problems()
            insights = self.analyzer.generate_insights()
            strategies = self.analyzer.create_strategy()
            kpis = self.analyzer.set_kpis()
            
            if active_tab == "overview":
                return self.create_overview_tab(), ""
            elif active_tab == "customer":
                return self.create_customer_tab(), ""
            elif active_tab == "problems":
                return self.create_problems_tab(problems), ""
            elif active_tab == "insights":
                return self.create_insights_tab(insights), ""
            elif active_tab == "strategy":
                return self.create_strategy_tab(strategies), ""
            elif active_tab == "kpi":
                return self.create_kpi_tab(kpis), ""
    
    def create_overview_tab(self):
        """개요 탭 생성"""
        # 기본 통계
        total_customers = len(self.analyzer.customer_data)
        avg_satisfaction = self.analyzer.customer_data['satisfaction'].mean()
        avg_purchase = self.analyzer.customer_data['purchase_amount'].mean()
        avg_waiting = self.analyzer.customer_data['waiting_time'].mean()
        
        return html.Div([
            html.H3("📊 기본 통계", style={'marginBottom': 20}),
            
            # 통계 카드들
            html.Div([
                html.Div([
                    html.H4(f"{total_customers:,}", style={'color': '#007bff', 'margin': 0}),
                    html.P("총 고객 수", style={'margin': 0})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '20px', 
                                               'backgroundColor': '#f8f9fa', 'borderRadius': '10px',
                                               'margin': '10px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{avg_satisfaction:.1f}/5.0", style={'color': '#28a745', 'margin': 0}),
                    html.P("평균 만족도", style={'margin': 0})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '20px', 
                                               'backgroundColor': '#f8f9fa', 'borderRadius': '10px',
                                               'margin': '10px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{avg_purchase:,.0f}원", style={'color': '#ffc107', 'margin': 0}),
                    html.P("평균 구매금액", style={'margin': 0})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '20px', 
                                               'backgroundColor': '#f8f9fa', 'borderRadius': '10px',
                                               'margin': '10px', 'flex': '1'}),
                
                html.Div([
                    html.H4(f"{avg_waiting:.1f}분", style={'color': '#dc3545', 'margin': 0}),
                    html.P("평균 대기시간", style={'margin': 0})
                ], className="stat-card", style={'textAlign': 'center', 'padding': '20px', 
                                               'backgroundColor': '#f8f9fa', 'borderRadius': '10px',
                                               'margin': '10px', 'flex': '1'})
            ], style={'display': 'flex', 'marginBottom': 30}),
            
            # 차트들
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=self.create_segment_distribution_chart(),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(
                        figure=self.create_satisfaction_chart(),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block'})
            ])
        ])
    
    def create_customer_tab(self):
        """고객 분석 탭 생성"""
        return html.Div([
            html.H3("👥 고객 세그먼트 분석", style={'marginBottom': 20}),
            
            # 고객 데이터 테이블
            dash_table.DataTable(
                id='customer-table',
                data=self.analyzer.customer_data.head(20).to_dict('records'),
                columns=[{"name": i, "id": i} for i in self.analyzer.customer_data.columns],
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                page_size=10
            ),
            
            html.Br(),
            
            # 세그먼트별 분석 차트
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=self.create_segment_purchase_chart(),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(
                        figure=self.create_segment_waiting_chart(),
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'display': 'inline-block'})
            ])
        ])
    
    def create_problems_tab(self, problems):
        """문제 분석 탭 생성"""
        problem_cards = []
        for problem_name, problem_data in problems.items():
            card = html.Div([
                html.H4(problem_name.replace('_', ' '), style={'color': '#dc3545'}),
                html.P(f"현재 상태: {problem_data['current_state']}"),
                html.P(f"목표 상태: {problem_data['target_state']}"),
                html.P(f"차이: {problem_data['gap']}"),
                html.P(f"영향도: {problem_data['impact']}"),
                html.P(f"매출 영향: {problem_data['revenue_impact']:,.0f}원")
            ], style={'padding': '20px', 'margin': '10px', 'backgroundColor': '#f8f9fa', 
                     'borderRadius': '10px', 'border': '1px solid #dee2e6'})
            problem_cards.append(card)
        
        return html.Div([
            html.H3("🚨 식별된 주요 문제점", style={'marginBottom': 20}),
            html.Div(problem_cards)
        ])
    
    def create_insights_tab(self, insights):
        """인사이트 탭 생성"""
        insight_sections = []
        for category, data in insights.items():
            section = html.Div([
                html.H4(category.replace('_', ' '), style={'color': '#007bff'}),
                html.Pre(str(data), style={'backgroundColor': '#f8f9fa', 'padding': '15px', 
                                         'borderRadius': '5px', 'whiteSpace': 'pre-wrap'})
            ], style={'marginBottom': '20px'})
            insight_sections.append(section)
        
        return html.Div([
            html.H3("💡 도출된 인사이트", style={'marginBottom': 20}),
            html.Div(insight_sections)
        ])
    
    def create_strategy_tab(self, strategies):
        """전략 탭 생성"""
        strategy_sections = []
        for category, data in strategies.items():
            section = html.Div([
                html.H4(category.replace('_', ' '), style={'color': '#28a745'}),
                html.Pre(str(data), style={'backgroundColor': '#f8f9fa', 'padding': '15px', 
                                         'borderRadius': '5px', 'whiteSpace': 'pre-wrap'})
            ], style={'marginBottom': '20px'})
            strategy_sections.append(section)
        
        return html.Div([
            html.H3("🎯 수립된 전략", style={'marginBottom': 20}),
            html.Div(strategy_sections)
        ])
    
    def create_kpi_tab(self, kpis):
        """KPI 탭 생성"""
        kpi_sections = []
        for phase, data in kpis.items():
            section = html.Div([
                html.H4(phase.replace('_', ' '), style={'color': '#ffc107'}),
                html.Pre(str(data), style={'backgroundColor': '#f8f9fa', 'padding': '15px', 
                                         'borderRadius': '5px', 'whiteSpace': 'pre-wrap'})
            ], style={'marginBottom': '20px'})
            kpi_sections.append(section)
        
        return html.Div([
            html.H3("📈 설정된 KPI", style={'marginBottom': 20}),
            html.Div(kpi_sections)
        ])
    
    def create_segment_distribution_chart(self):
        """세그먼트 분포 차트 생성"""
        segment_counts = self.analyzer.customer_data['segment'].value_counts()
        fig = px.pie(values=segment_counts.values, names=segment_counts.index, 
                    title="고객 세그먼트 분포")
        return fig
    
    def create_satisfaction_chart(self):
        """만족도 차트 생성"""
        fig = px.histogram(self.analyzer.customer_data, x='satisfaction', 
                          title="고객 만족도 분포", nbins=20)
        return fig
    
    def create_segment_purchase_chart(self):
        """세그먼트별 구매금액 차트 생성"""
        segment_purchase = self.analyzer.customer_data.groupby('segment')['purchase_amount'].mean()
        fig = px.bar(x=segment_purchase.index, y=segment_purchase.values,
                    title="세그먼트별 평균 구매금액")
        fig.update_xaxis(title="세그먼트")
        fig.update_yaxis(title="구매금액 (원)")
        return fig
    
    def create_segment_waiting_chart(self):
        """세그먼트별 대기시간 차트 생성"""
        segment_waiting = self.analyzer.customer_data.groupby('segment')['waiting_time'].mean()
        fig = px.bar(x=segment_waiting.index, y=segment_waiting.values,
                    title="세그먼트별 평균 대기시간")
        fig.update_xaxis(title="세그먼트")
        fig.update_yaxis(title="대기시간 (분)")
        return fig
    
    def run(self, debug=True, port=8050):
        """대시보드 실행"""
        print(f"🚀 대시보드가 http://localhost:{port} 에서 실행됩니다.")
        self.app.run_server(debug=debug, port=port)


def main():
    """메인 실행 함수"""
    app = DashboardApp()
    app.run()


if __name__ == "__main__":
    main()
