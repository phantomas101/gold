from managers.database_manager import DatabaseManager
from datetime import datetime

class TreasuryManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def get_balance(self):
        """حساب رصيد الخزينة الحالي"""
        query = "SELECT SUM(Amount) FROM TreasuryTransactions"
        result = self.db.fetch_one(query)
        return result[0] if result[0] else 0
    
    def get_transactions(self, limit=100):
        """جلب آخر حركات الخزينة"""
        query = """
            SELECT Id, Type, Amount, Description, ReferenceId, TransactionDate
            FROM TreasuryTransactions
            ORDER BY TransactionDate DESC
            LIMIT ?
        """
        return self.db.fetch_all(query, (limit,))
    
    def add_loan(self, worker_id, amount, description=""):
        """تسجيل سلفة لعامل (تخرج من الخزينة)"""
        # 1. تسجيل في الخزينة
        query = """
            INSERT INTO TreasuryTransactions 
            (Type, Amount, Description, ReferenceId, TransactionDate)
            VALUES (?, ?, ?, ?, ?)
        """
        treasury_id = self.db.execute_query(query, (
            'سلفة صادرة', -amount,
            f"سلفة للعامل #{worker_id} - {description}",
            worker_id, datetime.now().strftime("%Y-%m-%d")
        ))
        
        # 2. تسجيل في حركات العامل
        from managers.worker_manager import WorkerManager
        worker_manager = WorkerManager()
        worker_manager.add_transaction(
            worker_id, 'سلفة', -amount, 
            f"سلفة - {description}", 
            datetime.now().strftime("%Y-%m-%d")
        )
        
        return treasury_id
    
    def repay_loan(self, worker_id, amount, description=""):
        """استرداد سلفة من عامل (تعود إلى الخزينة)"""
        query = """
            INSERT INTO TreasuryTransactions 
            (Type, Amount, Description, ReferenceId, TransactionDate)
            VALUES (?, ?, ?, ?, ?)
        """
        treasury_id = self.db.execute_query(query, (
            'استرداد سلفة', amount,
            f"استرداد سلفة من العامل #{worker_id} - {description}",
            worker_id, datetime.now().strftime("%Y-%m-%d")
        ))
        return treasury_id
    
    def pay_worker(self, worker_id, amount, description=""):
        """صرف مستحقات عامل (تخرج من الخزينة)"""
        query = """
            INSERT INTO TreasuryTransactions 
            (Type, Amount, Description, ReferenceId, TransactionDate)
            VALUES (?, ?, ?, ?, ?)
        """
        treasury_id = self.db.execute_query(query, (
            'صرف مستحقات', -amount,
            f"صرف مستحقات للعامل #{worker_id} - {description}",
            worker_id, datetime.now().strftime("%Y-%m-%d")
        ))
        
        # تسجيل في حركات العامل
        from managers.worker_manager import WorkerManager
        worker_manager = WorkerManager()
        worker_manager.add_transaction(
            worker_id, 'صرف', -amount,
            f"صرف مستحقات - {description}",
            datetime.now().strftime("%Y-%m-%d")
        )
        
        return treasury_id