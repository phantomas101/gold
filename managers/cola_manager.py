from managers.database_manager import DatabaseManager

class ColaManager:
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_cola(self, name, responsible):
        """إضافة كولة جديدة"""
        query = "INSERT INTO Colas (Name, Responsible) VALUES (?, ?)"
        return self.db.execute_query(query, (name, responsible))
    
    def update_cola(self, cola_id, name, responsible):
        """تعديل بيانات كولة"""
        query = "UPDATE Colas SET Name=?, Responsible=? WHERE Id=?"
        self.db.execute_query(query, (name, responsible, cola_id))
    
    def delete_cola_permanently(self, cola_id):
        """حذف كولة نهائياً من قاعدة البيانات"""
        # 1. حذف حركات العمال المرتبطة
        query1 = """
            DELETE FROM WorkerTransactions 
            WHERE WorkerId IN (SELECT Id FROM Workers WHERE ColaId=?)
        """
        self.db.execute_query(query1, (cola_id,))
        
        # 2. حذف مشاركات العمال
        query2 = """
            DELETE FROM WorkerShares 
            WHERE WorkerId IN (SELECT Id FROM Workers WHERE ColaId=?)
        """
        self.db.execute_query(query2, (cola_id,))
        
        # 3. حذف العمال
        query3 = "DELETE FROM Workers WHERE ColaId=?"
        self.db.execute_query(query3, (cola_id,))
        
        # 4. حذف الكولة
        query4 = "DELETE FROM Colas WHERE Id=?"
        self.db.execute_query(query4, (cola_id,))
    
    def get_all_colas(self):
        """جلب جميع الكولات"""
        query = "SELECT Id, Name, Responsible, Status, CreatedAt FROM Colas ORDER BY Name"
        return self.db.fetch_all(query)
    
    def get_cola_by_id(self, cola_id):
        """جلب كولة بواسطة المعرف"""
        query = "SELECT Id, Name, Responsible, Status, CreatedAt FROM Colas WHERE Id=?"
        return self.db.fetch_one(query, (cola_id,))
    
    def get_cola_workers_count(self, cola_id):
        """جلب عدد العمال في كولة"""
        query = "SELECT COUNT(*) FROM Workers WHERE ColaId=?"
        result = self.db.fetch_one(query, (cola_id,))
        return result[0] if result else 0
    
    def get_cola_name(self, cola_id):
        """جلب اسم الكولة فقط"""
        query = "SELECT Name FROM Colas WHERE Id=?"
        result = self.db.fetch_one(query, (cola_id,))
        return result[0] if result else None
    
    def get_cola_workers(self, cola_id):
        """جلب جميع عمال الكولة"""
        query = "SELECT Id, Name, Phone FROM Workers WHERE ColaId=?"
        return self.db.fetch_all(query, (cola_id,))