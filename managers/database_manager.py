import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="database/gold_database.db"):
        """تهيئة مدير قاعدة البيانات"""
        # التأكد من وجود مجلد database
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        return sqlite3.connect(self.db_path)
    
    def create_tables(self):
        """إنشاء جميع الجداول إذا لم تكن موجودة"""
        queries = [
            # ===== جدول الكولات =====
            """
            CREATE TABLE IF NOT EXISTS Colas (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Responsible TEXT NOT NULL,
                Status TEXT DEFAULT 'نشط',
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # ===== جدول العمال =====
            """
            CREATE TABLE IF NOT EXISTS Workers (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                ColaId INTEGER NOT NULL,
                Phone TEXT,
                Status TEXT DEFAULT 'نشط',
                JoinedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ColaId) REFERENCES Colas(Id)
            )
            """,
            
            # ===== جدول العمليات المالية =====
            """
            CREATE TABLE IF NOT EXISTS Operations (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                ColaId INTEGER NOT NULL,
                Amount REAL NOT NULL,
                ExtraAmount REAL DEFAULT 0,
                OperationDate DATE NOT NULL,
                CompanyShare REAL NOT NULL,
                ColaShare REAL NOT NULL,
                TotalWorkers INTEGER NOT NULL,
                Notes TEXT,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ColaId) REFERENCES Colas(Id)
            )
            """,
            
            # ===== جدول مشاركات العمال =====
            """
            CREATE TABLE IF NOT EXISTS WorkerShares (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                OperationId INTEGER NOT NULL,
                WorkerId INTEGER NOT NULL,
                ShareAmount REAL NOT NULL,
                FOREIGN KEY (OperationId) REFERENCES Operations(Id),
                FOREIGN KEY (WorkerId) REFERENCES Workers(Id)
            )
            """,
            
            # ===== جدول حركات العمال =====
            """
            CREATE TABLE IF NOT EXISTS WorkerTransactions (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                WorkerId INTEGER NOT NULL,
                Type TEXT NOT NULL,
                Amount REAL NOT NULL,
                Description TEXT,
                TransactionDate DATE NOT NULL,
                ReferenceId INTEGER,
                FOREIGN KEY (WorkerId) REFERENCES Workers(Id)
            )
            """,
            
            # ===== جدول حركات الخزينة =====
            """
            CREATE TABLE IF NOT EXISTS TreasuryTransactions (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Type TEXT NOT NULL,
                Amount REAL NOT NULL,
                Description TEXT,
                ReferenceId INTEGER,
                TransactionDate DATE NOT NULL
            )
            """
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
        conn.close()
        print("✅ قاعدة البيانات جاهزة!")
    
    # ===== دوال مساعدة للاستعلامات =====
    def execute_query(self, query, params=None):
        """تنفيذ استعلام (INSERT, UPDATE, DELETE)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    def fetch_all(self, query, params=None):
        """جلب بيانات متعددة من قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def fetch_one(self, query, params=None):
        """جلب سجل واحد من قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        data = cursor.fetchone()
        conn.close()
        return data