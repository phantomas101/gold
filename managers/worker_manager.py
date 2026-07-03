from managers.database_manager import DatabaseManager

class WorkerManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_worker(self, name, cola_id, phone=""):
        query = "INSERT INTO Workers (Name, ColaId, Phone) VALUES (?, ?, ?)"
        return self.db.execute_query(query, (name, cola_id, phone))
    
    def add_multiple_workers(self, names, cola_id):
        added = 0
        for name in names:
            if name.strip():
                self.add_worker(name.strip(), cola_id)
                added += 1
        return added
    
    def add_transaction(self, worker_id, trans_type, amount, description, date):
        """إضافة حركة لعامل (استحقاق، سلفة، صرف)"""
        query = """
            INSERT INTO WorkerTransactions 
            (WorkerId, Type, Amount, Description, TransactionDate)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_query(query, (worker_id, trans_type, amount, description, date))
    
    def get_all_workers(self):
        query = "SELECT Id, Name, ColaId, Phone, JoinedAt FROM Workers ORDER BY Name"
        return self.db.fetch_all(query)
    
    def get_workers_by_cola(self, cola_id):
        query = "SELECT Id, Name, Phone FROM Workers WHERE ColaId=?"
        return self.db.fetch_all(query, (cola_id,))
    
    def get_worker_balance_with_details(self, worker_id):
        """جلب رصيد العامل مع تفاصيل الاستحقاقات والسلف"""
        # إجمالي الاستحقاقات
        query1 = "SELECT SUM(Amount) FROM WorkerTransactions WHERE WorkerId=? AND Type='استحقاق'"
        total_earnings = self.db.fetch_one(query1, (worker_id,))
        total_earnings = total_earnings[0] if total_earnings[0] else 0
        
        # إجمالي السلف
        query2 = "SELECT SUM(Amount) FROM WorkerTransactions WHERE WorkerId=? AND Type='سلفة'"
        total_loans = self.db.fetch_one(query2, (worker_id,))
        total_loans = abs(total_loans[0]) if total_loans[0] else 0
        
        # إجمالي الصرف
        query3 = "SELECT SUM(Amount) FROM WorkerTransactions WHERE WorkerId=? AND Type='صرف'"
        total_payments = self.db.fetch_one(query3, (worker_id,))
        total_payments = abs(total_payments[0]) if total_payments[0] else 0
        
        # الرصيد الحالي
        balance = total_earnings - total_loans - total_payments
        
        return {
            'total_earnings': total_earnings,
            'total_loans': total_loans,
            'total_payments': total_payments,
            'balance': balance
        }