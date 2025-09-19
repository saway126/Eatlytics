#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터베이스 관리 클래스
Database Manager for Ashley Customer Validation System
"""

import sqlite3
import logging
from typing import Dict, List, Tuple, Optional, Any
from contextlib import contextmanager
from config import Config
from utils import setup_logging, format_date, format_datetime

class DatabaseManager:
    """데이터베이스 관리 클래스"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.get_database_path()
        self.logger = setup_logging()
        self._setup_database()
    
    def _setup_database(self):
        """데이터베이스 초기화"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 고객 방문 기록 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customer_visits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id TEXT NOT NULL,
                        visit_date DATE NOT NULL,
                        table_number INTEGER,
                        order_items TEXT,
                        total_amount REAL,
                        satisfaction_score REAL,
                        visit_duration INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 재료 재고 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ingredient_inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ingredient_name TEXT NOT NULL,
                        initial_quantity REAL,
                        current_quantity REAL,
                        unit TEXT,
                        expiration_date DATE,
                        cost_per_unit REAL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # 접시 사진 분석 결과 테이블
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS dish_analysis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id TEXT,
                        table_number INTEGER,
                        dish_name TEXT,
                        image_path TEXT,
                        analysis_result TEXT,
                        waste_percentage REAL,
                        satisfaction_score REAL,
                        analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                self.logger.info("✅ 데이터베이스 초기화 완료!")
                
        except Exception as e:
            self.logger.error(f"데이터베이스 초기화 오류: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"데이터베이스 연결 오류: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def insert_customer_visits(self, visits: List[Dict[str, Any]]) -> bool:
        """고객 방문 데이터 삽입"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for visit in visits:
                    cursor.execute('''
                        INSERT INTO customer_visits 
                        (customer_id, visit_date, table_number, order_items, 
                         total_amount, satisfaction_score, visit_duration)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        visit['customer_id'], 
                        visit['visit_date'], 
                        visit['table_number'],
                        visit['order_items'], 
                        visit['total_amount'], 
                        visit['satisfaction_score'], 
                        visit['visit_duration']
                    ))
                
                conn.commit()
                self.logger.info(f"✅ {len(visits)}개의 고객 방문 데이터 삽입 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"고객 방문 데이터 삽입 오류: {e}")
            return False
    
    def insert_ingredient_inventory(self, ingredients: List[Dict[str, Any]]) -> bool:
        """재료 재고 데이터 삽입"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for ingredient in ingredients:
                    cursor.execute('''
                        INSERT INTO ingredient_inventory 
                        (ingredient_name, initial_quantity, current_quantity, 
                         unit, expiration_date, cost_per_unit)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        ingredient['ingredient_name'],
                        ingredient['initial_quantity'],
                        ingredient['current_quantity'],
                        ingredient['unit'],
                        ingredient['expiration_date'],
                        ingredient['cost_per_unit']
                    ))
                
                conn.commit()
                self.logger.info(f"✅ {len(ingredients)}개의 재료 재고 데이터 삽입 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"재료 재고 데이터 삽입 오류: {e}")
            return False
    
    def insert_dish_analysis(self, analyses: List[Dict[str, Any]]) -> bool:
        """접시 분석 데이터 삽입"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                for analysis in analyses:
                    cursor.execute('''
                        INSERT INTO dish_analysis 
                        (customer_id, table_number, dish_name, analysis_result, 
                         waste_percentage, satisfaction_score)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        analysis['customer_id'],
                        analysis['table_number'],
                        analysis['dish_name'],
                        analysis['analysis_result'],
                        analysis['waste_percentage'],
                        analysis['satisfaction_score']
                    ))
                
                conn.commit()
                self.logger.info(f"✅ {len(analyses)}개의 접시 분석 데이터 삽입 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"접시 분석 데이터 삽입 오류: {e}")
            return False
    
    def get_customer_visits(self, period_days: int = None) -> List[Tuple]:
        """고객 방문 데이터 조회"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if period_days:
                    start_date = format_date(
                        datetime.now() - timedelta(days=period_days)
                    )
                    cursor.execute('''
                        SELECT * FROM customer_visits 
                        WHERE visit_date >= ?
                        ORDER BY visit_date DESC
                    ''', (start_date,))
                else:
                    cursor.execute('''
                        SELECT * FROM customer_visits 
                        ORDER BY visit_date DESC
                    ''')
                
                return cursor.fetchall()
                
        except Exception as e:
            self.logger.error(f"고객 방문 데이터 조회 오류: {e}")
            return []
    
    def get_ingredient_inventory(self) -> List[Tuple]:
        """재료 재고 데이터 조회"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM ingredient_inventory')
                return cursor.fetchall()
                
        except Exception as e:
            self.logger.error(f"재료 재고 데이터 조회 오류: {e}")
            return []
    
    def get_dish_analysis(self) -> List[Tuple]:
        """접시 분석 데이터 조회"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM dish_analysis ORDER BY analysis_date DESC')
                return cursor.fetchall()
                
        except Exception as e:
            self.logger.error(f"접시 분석 데이터 조회 오류: {e}")
            return []
    
    def clear_all_data(self) -> bool:
        """모든 데이터 삭제"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('DELETE FROM customer_visits')
                cursor.execute('DELETE FROM ingredient_inventory')
                cursor.execute('DELETE FROM dish_analysis')
                
                conn.commit()
                self.logger.info("✅ 모든 데이터 삭제 완료")
                return True
                
        except Exception as e:
            self.logger.error(f"데이터 삭제 오류: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """데이터베이스 통계 조회"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # 고객 방문 수
                cursor.execute('SELECT COUNT(*) FROM customer_visits')
                stats['customer_visits'] = cursor.fetchone()[0]
                
                # 재료 수
                cursor.execute('SELECT COUNT(*) FROM ingredient_inventory')
                stats['ingredients'] = cursor.fetchone()[0]
                
                # 접시 분석 수
                cursor.execute('SELECT COUNT(*) FROM dish_analysis')
                stats['dish_analyses'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            self.logger.error(f"데이터베이스 통계 조회 오류: {e}")
            return {}
