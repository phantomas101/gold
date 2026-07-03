from managers.database_manager import DatabaseManager
from datetime import datetime

class OperationManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def register_operation(self, cola_id, amount, extra_amount, operation_date, selected_workers, notes=""):
        """
        تسجيل عملية مالية جديدة
        - amount: المبلغ المدفوع
        - extra_amount: الزوادة (تُخصم من المبلغ)
        """
        # 1. خصم الزوادة من المبلغ
        net_amount = amount - extra_amount
        
        # 2. حساب التوزيعات (50% شركة، 50% كولة)
        company_share = net_amount / 2
        cola_share = net_amount / 2
        
        # 3. تقسيم نصيب الكولة على العمال
        total_workers = len(selected_workers)
        if total_workers == 0:
            raise ValueError("يجب اختيار عامل واحد على الأقل")
        
        worker_share = cola_share / total_workers
        
        # 4. تسجيل العملية
        query = """
            INSERT INTO Operations 
            (ColaId, Amount, ExtraAmount, OperationDate, CompanyShare, ColaShare, TotalWorkers, Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        operation_id = self.db.execute_query(query, (
            cola_id, amount, extra_amount, operation_date,
            company_share, cola_share, total_workers, notes
        ))
        
        # 5. تسجيل مشاركات العمال
        for worker_id in selected_workers:
            query = "INSERT INTO WorkerShares (OperationId, WorkerId, ShareAmount) VALUES (?, ?, ?)"
            self.db.execute_query(query, (operation_id, worker_id, worker_share))
            
            # 6. إضافة استحقاق للعامل
            query = """
                INSERT INTO WorkerTransactions 
                (WorkerId, Type, Amount, Description, TransactionDate, ReferenceId)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.db.execute_query(query, (
                worker_id, 'استحقاق', worker_share,
                f"استحقاق من عملية #{operation_id}",
                operation_date, operation_id
            ))
        
        # 7. تسجيل في الخزينة (نصيب الشركة)
        query = """
            INSERT INTO TreasuryTransactions 
            (Type, Amount, Description, ReferenceId, TransactionDate)
            VALUES (?, ?, ?, ?, ?)
        """
        self.db.execute_query(query, (
            'إيراد نصيب شركة', company_share,
            f"نصيب شركة من عملية #{operation_id}",
            operation_id, operation_date
        ))
        
        return operation_id
    
    def get_operations_by_cola(self, cola_id):
        query = """
            SELECT Id, Amount, ExtraAmount, OperationDate, CompanyShare, ColaShare, TotalWorkers, Notes, CreatedAt
            FROM Operations
            WHERE ColaId=?
            ORDER BY OperationDate DESC
        """
        return self.db.fetch_all(query, (cola_id,))
    
    def get_all_operations(self):
        query = """
            SELECT o.Id, c.Name as ColaName, o.Amount, o.ExtraAmount, o.OperationDate, 
                   o.CompanyShare, o.ColaShare, o.TotalWorkers, o.Notes, o.CreatedAt
            FROM Operations o
            JOIN Colas c ON o.ColaId = c.Id
            ORDER BY o.OperationDate DESC
        """
        return self.db.fetch_all(query)
    
    def get_operation_details(self, operation_id):
        query = """
            SELECT o.*, c.Name as ColaName
            FROM Operations o
            JOIN Colas c ON o.ColaId = c.Id
            WHERE o.Id=?
        """
        return self.db.fetch_one(query, (operation_id,))
    
    def get_operation_workers(self, operation_id):
        query = """
            SELECT w.Id, w.Name, ws.ShareAmount
            FROM WorkerShares ws
            JOIN Workers w ON ws.WorkerId = w.Id
            WHERE ws.OperationId=?
        """
        return self.db.fetch_all(query, (operation_id,))