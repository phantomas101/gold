from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QFrame, QGridLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QTextEdit, QComboBox, QDialog, QDialogButtonBox,
    QDateEdit, QCheckBox, QScrollArea, QGroupBox, QSplitter,
    QListWidget, QListWidgetItem, QDoubleSpinBox
)
from PySide6.QtCore import Qt, QDate, QTimer
from datetime import datetime
from utils.styles_gold import apply_gold_style, GOLD_COLORS
from managers.cola_manager import ColaManager
from managers.worker_manager import WorkerManager
from managers.operation_manager import OperationManager
from managers.treasury_manager import TreasuryManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏅 نظام إدارة الحسابات - شركة التنقيب عن الذهب")
        self.setGeometry(100, 100, 1300, 800)
        apply_gold_style(self)
        self.init_ui()

    # ===== تحديث شامل =====
    def refresh_all(self):
        self.load_colas()
        self.load_workers()
        self.load_colas_for_worker_combo()
        self.load_operation_colas()
        self.load_operations()
        self.update_dashboard()
        self.load_colas_for_add_workers()
        self.load_treasury_data()

    # ===== تحديث الوقت والتاريخ =====
    def update_datetime(self):
        now = datetime.now()
        days_ar = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
        months_ar = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 
                     'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
        day_name = days_ar[now.weekday()]
        day = now.day
        month = months_ar[now.month - 1]
        year = now.year
        time_str = now.strftime("%I:%M:%S %p")
        self.datetime_label.setText(
            f"✨ الذهب | 📅 {day_name}، {day} {month} {year} | ⏰ {time_str} | 👤 المحاسب"
        )

    # ===== الواجهة الرئيسية =====
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # ===== شريط العنوان =====
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {GOLD_COLORS['black_luxury']},
                    stop:0.3 {GOLD_COLORS['black_soft']},
                    stop:0.7 {GOLD_COLORS['black_soft']},
                    stop:1 {GOLD_COLORS['black_luxury']});
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                border-radius: 15px;
                padding: 15px;
            }}
        """)
        header_layout = QHBoxLayout(header)

        title = QLabel("🏅 نظام إدارة الحسابات - شركة التنقيب عن الذهب")
        title.setProperty("title", "true")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.datetime_label = QLabel("✨ الذهب | 📅 جاري التحميل... | ⏰ جاري التحميل... | 👤 المحاسب")
        self.datetime_label.setProperty("heading", "true")
        self.datetime_label.setStyleSheet(f"color: {GOLD_COLORS['text_light']};")
        header_layout.addWidget(self.datetime_label)

        self.update_datetime()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)

        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                color: {GOLD_COLORS['black_luxury']};
                border: 2px solid {GOLD_COLORS['gold_sparkle']};
                border-radius: 10px;
                padding: 8px 18px;
                font-weight: bold;
                font-family: 'Georgia';
                font-size: 11pt;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_sparkle']},
                    stop:1 {GOLD_COLORS['gold_rich']});
            }}
        """)
        refresh_btn.clicked.connect(self.refresh_all)
        header_layout.addWidget(refresh_btn)

        about_btn = QPushButton("👑 حول البرنامج")
        about_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                color: {GOLD_COLORS['black_luxury']};
                border: 2px solid {GOLD_COLORS['gold_sparkle']};
                border-radius: 10px;
                padding: 8px 22px;
                font-weight: bold;
                font-family: 'Georgia';
                font-size: 11pt;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_sparkle']},
                    stop:1 {GOLD_COLORS['gold_rich']});
            }}
        """)
        about_btn.clicked.connect(self.show_about)
        header_layout.addWidget(about_btn)

        layout.addWidget(header)

        # ===== علامات التبويب =====
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_dashboard_tab(), "📊 لوحة المعلومات")
        self.tabs.addTab(self.create_cola_tab(), "📋 الكولات")
        self.tabs.addTab(self.create_worker_tab(), "👷 العمال")
        self.tabs.addTab(self.create_operation_tab(), "💰 العمليات المالية")
        self.tabs.addTab(self.create_treasury_tab(), "🏦 الخزينة")
        self.tabs.addTab(self.create_placeholder_tab("📊 التقارير"), "📊 التقارير")

        layout.addWidget(self.tabs)
        self.refresh_all()

    # ===== تحديث لوحة المعلومات =====
    def update_dashboard(self):
        dashboard_tab = self.tabs.widget(0)
        if dashboard_tab:
            new_dashboard = self.create_dashboard_tab()
            self.tabs.removeTab(0)
            self.tabs.insertTab(0, new_dashboard, "📊 لوحة المعلومات")

    # ===== تبويب لوحة المعلومات =====
    def create_dashboard_tab(self):
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.setSpacing(15)

        cola_manager = ColaManager()
        worker_manager = WorkerManager()
        operation_manager = OperationManager()
        treasury_manager = TreasuryManager()
        
        colas = cola_manager.get_all_colas()
        total_workers = len(worker_manager.get_all_workers())
        operations = operation_manager.get_all_operations()
        treasury_balance = treasury_manager.get_balance()

        stats = [
            ("🏅 عدد الكولات", str(len(colas)), GOLD_COLORS['gold_rich']),
            ("👷 عدد العمال", str(total_workers), GOLD_COLORS['gold_light']),
            ("💰 رصيد الخزينة", f"{treasury_balance:,.2f} ج.م", GOLD_COLORS['gold_sparkle']),
            ("📊 عدد العمليات", str(len(operations)), GOLD_COLORS['bronze'])
        ]

        for i, (title, value, color) in enumerate(stats):
            card = QFrame()
            card.setProperty("gold-card", "true")
            card_layout = QVBoxLayout(card)
            title_label = QLabel(title)
            title_label.setProperty("heading", "true")
            title_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']}; font-size: 12px;")
            value_label = QLabel(value)
            value_label.setProperty("title", "true")
            value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-family: 'Times New Roman';")
            card_layout.addWidget(title_label)
            card_layout.addWidget(value_label)
            layout.addWidget(card, 0, i)

        # آخر العمليات
        recent_group = QFrame()
        recent_group.setProperty("gold-card", "true")
        recent_layout = QVBoxLayout(recent_group)
        recent_title = QLabel("🔱 آخر العمليات المسجلة")
        recent_title.setProperty("heading", "true")
        recent_title.setStyleSheet(f"color: {GOLD_COLORS['gold_rich']};")
        recent_layout.addWidget(recent_title)
        
        if operations:
            for op in operations[:5]:
                recent_layout.addWidget(QLabel(
                    f"⚜️ #{op[0]} - {op[1]} - {op[2]:,.2f} ج.م - {op[7]} عمال"
                ))
        else:
            recent_label = QLabel("⚜️ لا توجد عمليات مسجلة حتى الآن")
            recent_label.setStyleSheet(f"padding: 6px; color: {GOLD_COLORS['text_light']};")
            recent_layout.addWidget(recent_label)
        
        layout.addWidget(recent_group, 1, 0, 1, 2)

        # الكولات النشطة
        colas_group = QFrame()
        colas_group.setProperty("gold-card", "true")
        colas_layout = QVBoxLayout(colas_group)
        colas_title = QLabel("🏗️ الكولات المسجلة")
        colas_title.setProperty("heading", "true")
        colas_title.setStyleSheet(f"color: {GOLD_COLORS['gold_rich']};")
        colas_layout.addWidget(colas_title)
        
        if colas:
            for cola in colas:
                workers = cola_manager.get_cola_workers_count(cola[0])
                colas_layout.addWidget(QLabel(f"⚜️ {cola[1]} ({workers} عامل) - المسؤول: {cola[2]}"))
        else:
            colas_layout.addWidget(QLabel("⚜️ لا توجد كولات مسجلة"))
        
        layout.addWidget(colas_group, 1, 2, 1, 2)
        return tab

    # ===== تبويب الكولات =====
    def create_cola_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        add_group = QFrame()
        add_group.setProperty("gold-card", "true")
        add_layout = QVBoxLayout(add_group)

        row1 = QHBoxLayout()
        self.cola_name_input = QLineEdit()
        self.cola_name_input.setPlaceholderText("📝 اسم الكولة")
        row1.addWidget(self.cola_name_input)
        self.cola_responsible_input = QLineEdit()
        self.cola_responsible_input.setPlaceholderText("👤 اسم المسؤول")
        row1.addWidget(self.cola_responsible_input)
        add_layout.addLayout(row1)

        row2 = QHBoxLayout()
        workers_label = QLabel("👷 أسماء العمال (اكتب كل اسم في سطر منفصل)")
        workers_label.setProperty("heading", "true")
        workers_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']}; font-size: 11px;")
        row2.addWidget(workers_label)
        add_layout.addLayout(row2)

        self.workers_input = QTextEdit()
        self.workers_input.setPlaceholderText("مثال:\nأحمد محمد\nسعيد علي\nخالد حسن\nمحمد إبراهيم")
        self.workers_input.setMaximumHeight(100)
        add_layout.addWidget(self.workers_input)

        add_btn = QPushButton("➕ إضافة كولة مع العمال")
        add_btn.clicked.connect(self.add_cola_with_workers)
        add_layout.addWidget(add_btn)

        layout.addWidget(add_group)

        # جدول الكولات
        table_container = QFrame()
        table_container.setProperty("gold-card", "true")
        table_layout = QVBoxLayout(table_container)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.edit_cola_btn = QPushButton("✏️ تعديل الكولة المحددة")
        self.edit_cola_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D4AF37,
                    stop:1 #B8860B);
                color: #0D0D0D;
                border: 1px solid #FFD700;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: 'Georgia';
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFD700,
                    stop:1 #D4AF37);
            }
        """)
        self.edit_cola_btn.clicked.connect(self.edit_selected_cola)
        btn_row.addWidget(self.edit_cola_btn)

        self.delete_cola_btn = QPushButton("🗑️ حذف الكولة المحددة نهائياً")
        self.delete_cola_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #EF4444,
                    stop:1 #B91C1C);
                color: white;
                border: 1px solid #EF4444;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: 'Georgia';
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F87171,
                    stop:1 #EF4444);
            }
        """)
        self.delete_cola_btn.clicked.connect(self.delete_selected_cola)
        btn_row.addWidget(self.delete_cola_btn)
        table_layout.addLayout(btn_row)

        self.cola_table = QTableWidget()
        self.cola_table.setColumnCount(4)
        self.cola_table.setHorizontalHeaderLabels(["المعرف", "اسم الكولة", "المسؤول", "عدد العمال"])
        self.cola_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.cola_table.setAlternatingRowColors(True)
        self.cola_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cola_table.setSelectionMode(QTableWidget.SingleSelection)
        table_layout.addWidget(self.cola_table)
        layout.addWidget(table_container)
        return tab

    def load_colas(self):
        cola_manager = ColaManager()
        colas = cola_manager.get_all_colas()
        self.cola_table.setRowCount(len(colas))
        for i, cola in enumerate(colas):
            self.cola_table.setItem(i, 0, QTableWidgetItem(str(cola[0])))
            self.cola_table.setItem(i, 1, QTableWidgetItem(cola[1]))
            self.cola_table.setItem(i, 2, QTableWidgetItem(cola[2]))
            workers_count = cola_manager.get_cola_workers_count(cola[0])
            self.cola_table.setItem(i, 3, QTableWidgetItem(str(workers_count)))

    def add_cola_with_workers(self):
        name = self.cola_name_input.text().strip()
        responsible = self.cola_responsible_input.text().strip()
        workers_text = self.workers_input.toPlainText().strip()

        if not name or not responsible:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى إدخال اسم الكولة واسم المسؤول")
            return

        try:
            cola_manager = ColaManager()
            worker_manager = WorkerManager()
            cola_id = cola_manager.add_cola(name, responsible)
            workers_added = 0
            if workers_text:
                workers_list = [w.strip() for w in workers_text.split('\n') if w.strip()]
                if workers_list:
                    workers_added = worker_manager.add_multiple_workers(workers_list, cola_id)

            msg = f"✅ تم إضافة الكولة '{name}' بنجاح!"
            if workers_added > 0:
                msg += f"\n👷 تم إضافة {workers_added} عامل/عمال"
            QMessageBox.information(self, "نجاح", msg)
            self.cola_name_input.clear()
            self.cola_responsible_input.clear()
            self.workers_input.clear()
            self.refresh_all()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"❌ حدث خطأ: {str(e)}")

    def edit_selected_cola(self):
        selected = self.cola_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى تحديد كولة أولاً")
            return

        cola_id = int(self.cola_table.item(selected, 0).text())
        current_name = self.cola_table.item(selected, 1).text()
        current_responsible = self.cola_table.item(selected, 2).text()

        dialog = QDialog(self)
        dialog.setWindowTitle("✏️ تعديل بيانات الكولة")
        dialog.setFixedSize(450, 250)
        dialog.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['black_luxury']},
                    stop:1 {GOLD_COLORS['black_soft']});
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                border-radius: 20px;
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("✏️ تعديل بيانات الكولة")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-family: 'Times New Roman';
            font-size: 20px;
            font-weight: bold;
            color: {GOLD_COLORS['gold_rich']};
        """)
        layout.addWidget(title)

        name_input = QLineEdit(current_name)
        name_input.setPlaceholderText("اسم الكولة")
        layout.addWidget(name_input)

        resp_input = QLineEdit(current_responsible)
        resp_input.setPlaceholderText("اسم المسؤول")
        layout.addWidget(resp_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                color: {GOLD_COLORS['black_luxury']};
                border: 1px solid {GOLD_COLORS['gold_sparkle']};
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: 'Georgia';
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_sparkle']},
                    stop:1 {GOLD_COLORS['gold_rich']});
            }}
        """)
        buttons.accepted.connect(lambda: self.save_cola_edit(dialog, cola_id, name_input.text().strip(), resp_input.text().strip()))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec()

    def save_cola_edit(self, dialog, cola_id, new_name, new_responsible):
        if not new_name or not new_responsible:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى إدخال جميع البيانات")
            return
        try:
            cola_manager = ColaManager()
            cola_manager.update_cola(cola_id, new_name, new_responsible)
            QMessageBox.information(self, "نجاح", f"✅ تم تعديل الكولة بنجاح!")
            self.refresh_all()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"❌ حدث خطأ: {str(e)}")

    def delete_selected_cola(self):
        selected = self.cola_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى تحديد كولة أولاً")
            return

        cola_id = int(self.cola_table.item(selected, 0).text())
        cola_name = self.cola_table.item(selected, 1).text()
        workers_count = int(self.cola_table.item(selected, 3).text())

        msg = f"⚠️ هل أنت متأكد من حذف الكولة '{cola_name}' نهائياً؟"
        if workers_count > 0:
            msg += f"\n\n👷 تحتوي الكولة على {workers_count} عامل/عمال."
            msg += "\nسيتم حذف جميع العمال المرتبطين بهذه الكولة نهائياً!"
        msg += "\n\n⛔ هذا الإجراء لا يمكن التراجع عنه!"

        reply = QMessageBox.question(self, "تأكيد الحذف النهائي", msg, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                cola_manager = ColaManager()
                cola_manager.delete_cola_permanently(cola_id)
                QMessageBox.information(self, "نجاح", f"✅ تم حذف الكولة '{cola_name}' نهائياً")
                self.refresh_all()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"❌ حدث خطأ: {str(e)}")

    def load_colas_for_add_workers(self):
        pass

    # ===== تبويب العمال =====
    def create_worker_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        add_group = QFrame()
        add_group.setProperty("gold-card", "true")
        add_layout = QHBoxLayout(add_group)

        self.worker_name_input = QLineEdit()
        self.worker_name_input.setPlaceholderText("👷 اسم العامل")
        add_layout.addWidget(self.worker_name_input)

        self.worker_cola_combo = QComboBox()
        self.worker_cola_combo.setPlaceholderText("اختر الكولة")
        add_layout.addWidget(self.worker_cola_combo)

        self.worker_phone_input = QLineEdit()
        self.worker_phone_input.setPlaceholderText("📞 رقم الهاتف (اختياري)")
        add_layout.addWidget(self.worker_phone_input)

        add_btn = QPushButton("➕ إضافة عامل")
        add_btn.clicked.connect(self.add_worker_standalone)
        add_layout.addWidget(add_btn)
        layout.addWidget(add_group)

        self.load_colas_for_worker_combo()

        self.worker_table = QTableWidget()
        self.worker_table.setColumnCount(5)
        self.worker_table.setHorizontalHeaderLabels(["المعرف", "اسم العامل", "الكولة", "الهاتف", "تاريخ الانضمام"])
        self.worker_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.worker_table.setAlternatingRowColors(True)
        layout.addWidget(self.worker_table)
        return tab

    def load_colas_for_worker_combo(self):
        self.worker_cola_combo.clear()
        cola_manager = ColaManager()
        colas = cola_manager.get_all_colas()
        for cola in colas:
            self.worker_cola_combo.addItem(cola[1], cola[0])

    def add_worker_standalone(self):
        name = self.worker_name_input.text().strip()
        cola_id = self.worker_cola_combo.currentData()
        phone = self.worker_phone_input.text().strip()

        if not name:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى إدخال اسم العامل")
            return
        if not cola_id:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى اختيار الكولة")
            return

        try:
            worker_manager = WorkerManager()
            worker_manager.add_worker(name, cola_id, phone)
            QMessageBox.information(self, "نجاح", f"✅ تم إضافة العامل '{name}' بنجاح!")
            self.worker_name_input.clear()
            self.worker_phone_input.clear()
            self.refresh_all()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"❌ حدث خطأ: {str(e)}")

    def load_workers(self):
        worker_manager = WorkerManager()
        cola_manager = ColaManager()
        workers = worker_manager.get_all_workers()

        self.worker_table.setRowCount(len(workers))
        for i, worker in enumerate(workers):
            self.worker_table.setItem(i, 0, QTableWidgetItem(str(worker[0])))
            self.worker_table.setItem(i, 1, QTableWidgetItem(worker[1]))
            cola_name = cola_manager.get_cola_name(worker[2])
            self.worker_table.setItem(i, 2, QTableWidgetItem(cola_name if cola_name else "غير محدد"))
            self.worker_table.setItem(i, 3, QTableWidgetItem(worker[3] if worker[3] else "-"))
            self.worker_table.setItem(i, 4, QTableWidgetItem(worker[4] if worker[4] else "-"))

    # ===== تبويب العمليات المالية =====
    def create_operation_tab(self):
        from PySide6.QtWidgets import QSplitter
        
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Vertical)
        
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(0, 0, 0, 0)

        form_group = QFrame()
        form_group.setProperty("gold-card", "true")
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(8)

        row1 = QHBoxLayout()
        cola_label = QLabel("🏗️ الكولة:")
        cola_label.setProperty("heading", "true")
        cola_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']};")
        row1.addWidget(cola_label)

        self.operation_cola_combo = QComboBox()
        self.operation_cola_combo.setMinimumWidth(150)
        self.operation_cola_combo.currentIndexChanged.connect(self.load_operation_workers)
        row1.addWidget(self.operation_cola_combo)

        row1.addSpacing(20)

        date_label = QLabel("📅 التاريخ:")
        date_label.setProperty("heading", "true")
        date_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']};")
        row1.addWidget(date_label)

        self.operation_date_edit = QDateEdit()
        self.operation_date_edit.setDate(QDate.currentDate())
        self.operation_date_edit.setCalendarPopup(True)
        self.operation_date_edit.setMinimumWidth(120)
        row1.addWidget(self.operation_date_edit)

        row1.addStretch()
        form_layout.addLayout(row1)

        row2 = QHBoxLayout()
        amount_label = QLabel("💰 المبلغ:")
        amount_label.setProperty("heading", "true")
        amount_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']};")
        row2.addWidget(amount_label)

        self.operation_amount_input = QLineEdit()
        self.operation_amount_input.setPlaceholderText("0.00")
        self.operation_amount_input.setMinimumWidth(120)
        self.operation_amount_input.textChanged.connect(self.calculate_operation_summary)
        row2.addWidget(self.operation_amount_input)

        row2.addSpacing(20)

        extra_label = QLabel("➖ الزوادة:")
        extra_label.setProperty("heading", "true")
        extra_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']};")
        row2.addWidget(extra_label)

        self.operation_extra_input = QLineEdit()
        self.operation_extra_input.setPlaceholderText("0.00")
        self.operation_extra_input.setMinimumWidth(120)
        self.operation_extra_input.textChanged.connect(self.calculate_operation_summary)
        row2.addWidget(self.operation_extra_input)

        row2.addStretch()
        form_layout.addLayout(row2)

        row3 = QHBoxLayout()
        workers_label = QLabel("👷 العمال:")
        workers_label.setProperty("heading", "true")
        workers_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']};")
        row3.addWidget(workers_label)

        scroll_workers = QScrollArea()
        scroll_workers.setWidgetResizable(True)
        scroll_workers.setMaximumHeight(50)
        scroll_workers.setStyleSheet("""
            QScrollArea {
                border: 1px solid #C5A059;
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1C1C1C,
                    stop:1 #0D0D0D);
            }
        """)

        self.workers_container = QWidget()
        self.workers_layout = QHBoxLayout(self.workers_container)
        self.workers_layout.setSpacing(10)
        self.workers_layout.setContentsMargins(10, 5, 10, 5)
        self.workers_checkboxes = []
        scroll_workers.setWidget(self.workers_container)
        row3.addWidget(scroll_workers)

        select_all_btn = QPushButton("☑️ الكل")
        select_all_btn.setMaximumWidth(60)
        select_all_btn.clicked.connect(self.select_all_workers)
        row3.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("☐ إلغاء")
        deselect_all_btn.setMaximumWidth(60)
        deselect_all_btn.clicked.connect(self.deselect_all_workers)
        row3.addWidget(deselect_all_btn)

        form_layout.addLayout(row3)

        row4 = QHBoxLayout()
        notes_label = QLabel("📝 ملاحظات:")
        notes_label.setProperty("heading", "true")
        notes_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']};")
        row4.addWidget(notes_label)

        self.operation_notes_input = QTextEdit()
        self.operation_notes_input.setMaximumHeight(40)
        self.operation_notes_input.setPlaceholderText("اختياري...")
        self.operation_notes_input.setMinimumWidth(200)
        row4.addWidget(self.operation_notes_input)

        row4.addStretch()

        register_btn = QPushButton("💰 تسجيل العملية")
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D4AF37,
                    stop:1 #B8860B);
                color: #0D0D0D;
                border: 2px solid #FFD700;
                border-radius: 8px;
                padding: 8px 25px;
                font-weight: bold;
                font-family: 'Georgia';
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFD700,
                    stop:1 #D4AF37);
            }
        """)
        register_btn.clicked.connect(self.register_operation)
        row4.addWidget(register_btn)

        form_layout.addLayout(row4)

        top_layout.addWidget(form_group)

        summary_frame = QFrame()
        summary_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['black_soft']},
                    stop:1 {GOLD_COLORS['black_luxury']});
                border: 1px solid {GOLD_COLORS['gold_old']};
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setSpacing(15)
        summary_layout.setContentsMargins(10, 5, 10, 5)

        self.summary_total_label = QLabel("💵 الصافي: 0.00")
        self.summary_total_label.setStyleSheet(f"color: {GOLD_COLORS['text_light']}; font-size: 11px; font-weight: bold;")
        summary_layout.addWidget(self.summary_total_label)

        self.summary_company_label = QLabel("🏢 الشركة: 0.00")
        self.summary_company_label.setStyleSheet(f"color: {GOLD_COLORS['gold_rich']}; font-size: 11px; font-weight: bold;")
        summary_layout.addWidget(self.summary_company_label)

        self.summary_cola_label = QLabel("👥 الكولة: 0.00")
        self.summary_cola_label.setStyleSheet(f"color: {GOLD_COLORS['gold_light']}; font-size: 11px; font-weight: bold;")
        summary_layout.addWidget(self.summary_cola_label)

        self.summary_worker_label = QLabel("👷 لكل عامل: 0.00")
        self.summary_worker_label.setStyleSheet(f"color: {GOLD_COLORS['gold_sparkle']}; font-size: 11px; font-weight: bold;")
        summary_layout.addWidget(self.summary_worker_label)

        summary_layout.addStretch()

        top_layout.addWidget(summary_frame)

        splitter.addWidget(top_widget)

        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        table_container = QFrame()
        table_container.setProperty("gold-card", "true")
        table_layout = QVBoxLayout(table_container)

        table_title = QLabel("📋 العمليات المسجلة")
        table_title.setProperty("heading", "true")
        table_title.setStyleSheet(f"color: {GOLD_COLORS['gold_rich']};")
        table_layout.addWidget(table_title)

        self.operations_table = QTableWidget()
        self.operations_table.setColumnCount(6)
        self.operations_table.setHorizontalHeaderLabels([
            "المعرف", "الكولة", "المبلغ", "الزوادة", "نصيب الشركة", "عدد العمال"
        ])
        self.operations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.operations_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.operations_table)

        bottom_layout.addWidget(table_container)
        splitter.addWidget(bottom_widget)

        splitter.setSizes([300, 500])

        main_layout.addWidget(splitter)

        self.load_operation_colas()
        self.load_operations()

        return tab

    def load_operation_colas(self):
        self.operation_cola_combo.clear()
        cola_manager = ColaManager()
        colas = cola_manager.get_all_colas()
        for cola in colas:
            self.operation_cola_combo.addItem(cola[1], cola[0])
        if colas:
            self.load_operation_workers()

    def load_operation_workers(self):
        self.workers_checkboxes.clear()
        for i in reversed(range(self.workers_layout.count())):
            widget = self.workers_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        cola_id = self.operation_cola_combo.currentData()
        if not cola_id:
            return
        worker_manager = WorkerManager()
        workers = worker_manager.get_workers_by_cola(cola_id)
        if not workers:
            label = QLabel("⚠️ لا يوجد عمال")
            label.setStyleSheet(f"color: {GOLD_COLORS['text_muted']};")
            self.workers_layout.addWidget(label)
            return
        for worker in workers:
            checkbox = QCheckBox(f"{worker[1]} ({worker[0]})")
            checkbox.setProperty("worker_id", worker[0])
            checkbox.stateChanged.connect(self.calculate_operation_summary)
            checkbox.setStyleSheet(f"""
                QCheckBox {{
                    color: {GOLD_COLORS['text_light']};
                    font-size: 10px;
                    padding: 2px;
                }}
                QCheckBox::indicator {{
                    width: 14px;
                    height: 14px;
                }}
            """)
            self.workers_checkboxes.append(checkbox)
            self.workers_layout.addWidget(checkbox)
        self.calculate_operation_summary()

    def select_all_workers(self):
        for checkbox in self.workers_checkboxes:
            checkbox.setChecked(True)

    def deselect_all_workers(self):
        for checkbox in self.workers_checkboxes:
            checkbox.setChecked(False)

    def calculate_operation_summary(self):
        try:
            amount = float(self.operation_amount_input.text().strip() or 0)
        except ValueError:
            amount = 0
        try:
            extra = float(self.operation_extra_input.text().strip() or 0)
        except ValueError:
            extra = 0
        net_amount = amount - extra
        if net_amount < 0:
            net_amount = 0
        company_share = net_amount / 2
        cola_share = net_amount / 2
        selected_count = sum(1 for cb in self.workers_checkboxes if cb.isChecked())
        worker_share = cola_share / selected_count if selected_count > 0 else 0
        self.summary_total_label.setText(f"💵 الصافي: {net_amount:,.2f}")
        self.summary_company_label.setText(f"🏢 الشركة: {company_share:,.2f}")
        self.summary_cola_label.setText(f"👥 الكولة: {cola_share:,.2f}")
        if selected_count > 0:
            self.summary_worker_label.setText(f"👷 لكل عامل: {worker_share:,.2f} ({selected_count})")
        else:
            self.summary_worker_label.setText("👷 لكل عامل: 0.00 (0)")

    def register_operation(self):
        cola_id = self.operation_cola_combo.currentData()
        if not cola_id:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى اختيار الكولة")
            return
        try:
            amount = float(self.operation_amount_input.text().strip() or 0)
            if amount <= 0:
                QMessageBox.warning(self, "تنبيه", "⚠️ يرجى إدخال مبلغ صحيح أكبر من صفر")
                return
        except ValueError:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى إدخال مبلغ صحيح")
            return
        try:
            extra = float(self.operation_extra_input.text().strip() or 0)
        except ValueError:
            extra = 0
        if extra > amount:
            QMessageBox.warning(self, "تنبيه", "⚠️ الزوادة لا يمكن أن تزيد عن المبلغ المدفوع")
            return
        selected_workers = []
        for checkbox in self.workers_checkboxes:
            if checkbox.isChecked():
                selected_workers.append(checkbox.property("worker_id"))
        if not selected_workers:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى اختيار عامل واحد على الأقل")
            return
        date = self.operation_date_edit.date().toString("yyyy-MM-dd")
        notes = self.operation_notes_input.toPlainText().strip()
        net_amount = amount - extra
        company_share = net_amount / 2
        cola_share = net_amount / 2
        worker_share = cola_share / len(selected_workers)
        confirm_msg = f"""
        ✅ تأكيد تسجيل العملية:
        
        📋 الكولة: {self.operation_cola_combo.currentText()}
        💰 المبلغ المدفوع: {amount:,.2f} ج.م
        ➖ الزوادة (تُخصم): {extra:,.2f} ج.م
        ──────────────────────────────
        💵 المبلغ بعد الخصم: {net_amount:,.2f} ج.م
        👷 عدد العمال: {len(selected_workers)} عامل
        👷 نصيب كل عامل: {worker_share:,.2f} ج.م
        🏢 نصيب الشركة (50%): {company_share:,.2f} ج.م
        👥 نصيب الكولة (50%): {cola_share:,.2f} ج.م
        
        هل أنت متأكد من تسجيل هذه العملية؟
        """
        reply = QMessageBox.question(self, "تأكيد التسجيل", confirm_msg, QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        try:
            operation_manager = OperationManager()
            operation_id = operation_manager.register_operation(
                cola_id, amount, extra, date, selected_workers, notes
            )
            QMessageBox.information(
                self, "نجاح",
                f"✅ تم تسجيل العملية بنجاح!\n"
                f"📋 معرف العملية: #{operation_id}\n"
                f"💰 نصيب الشركة: {company_share:,.2f} ج.م"
            )
            self.operation_amount_input.clear()
            self.operation_extra_input.clear()
            self.operation_notes_input.clear()
            self.deselect_all_workers()
            self.load_operations()
            self.refresh_all()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"❌ حدث خطأ أثناء تسجيل العملية:\n{str(e)}")

    def load_operations(self):
        operation_manager = OperationManager()
        operations = operation_manager.get_all_operations()
        self.operations_table.setRowCount(len(operations))
        for i, op in enumerate(operations):
            self.operations_table.setItem(i, 0, QTableWidgetItem(str(op[0])))
            self.operations_table.setItem(i, 1, QTableWidgetItem(op[1]))
            self.operations_table.setItem(i, 2, QTableWidgetItem(f"{op[2]:,.2f}"))
            self.operations_table.setItem(i, 3, QTableWidgetItem(f"{op[3]:,.2f}"))
            self.operations_table.setItem(i, 4, QTableWidgetItem(f"{op[5]:,.2f}"))
            self.operations_table.setItem(i, 5, QTableWidgetItem(str(op[7])))

    # ===== تبويب الخزينة =====
    def create_treasury_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        balance_group = QFrame()
        balance_group.setProperty("gold-card", "true")
        balance_layout = QHBoxLayout(balance_group)

        self.treasury_balance_label = QLabel("🏦 رصيد الخزينة: 0.00 ج.م")
        self.treasury_balance_label.setProperty("title", "true")
        self.treasury_balance_label.setStyleSheet(f"""
            font-size: 22pt;
            font-weight: bold;
            color: {GOLD_COLORS['gold_sparkle']};
        """)
        balance_layout.addWidget(self.treasury_balance_label)

        balance_layout.addStretch()

        refresh_balance_btn = QPushButton("🔄 تحديث الرصيد")
        refresh_balance_btn.setMaximumWidth(150)
        refresh_balance_btn.clicked.connect(self.update_treasury_balance)
        balance_layout.addWidget(refresh_balance_btn)

        layout.addWidget(balance_group)

        actions_group = QFrame()
        actions_group.setProperty("gold-card", "true")
        actions_layout = QHBoxLayout(actions_group)

        loan_btn = QPushButton("💰 إضافة سلفة لعامل")
        loan_btn.clicked.connect(self.add_loan_dialog)
        actions_layout.addWidget(loan_btn)

        repay_btn = QPushButton("🔄 استرداد سلفة")
        repay_btn.clicked.connect(self.repay_loan_dialog)
        actions_layout.addWidget(repay_btn)

        pay_btn = QPushButton("💵 صرف مستحقات عامل")
        pay_btn.clicked.connect(self.pay_worker_dialog)
        actions_layout.addWidget(pay_btn)

        actions_layout.addStretch()
        layout.addWidget(actions_group)

        table_container = QFrame()
        table_container.setProperty("gold-card", "true")
        table_layout = QVBoxLayout(table_container)

        table_title = QLabel("📋 حركات الخزينة")
        table_title.setProperty("heading", "true")
        table_title.setStyleSheet(f"color: {GOLD_COLORS['gold_rich']};")
        table_layout.addWidget(table_title)

        self.treasury_table = QTableWidget()
        self.treasury_table.setColumnCount(5)
        self.treasury_table.setHorizontalHeaderLabels([
            "التاريخ", "النوع", "المبلغ", "الوصف", "المرجع"
        ])
        self.treasury_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.treasury_table.setAlternatingRowColors(True)
        table_layout.addWidget(self.treasury_table)

        layout.addWidget(table_container)

        self.load_treasury_data()
        return tab

    def load_treasury_data(self):
        treasury_manager = TreasuryManager()
        balance = treasury_manager.get_balance()
        self.treasury_balance_label.setText(f"🏦 رصيد الخزينة: {balance:,.2f} ج.م")
        transactions = treasury_manager.get_transactions()
        self.treasury_table.setRowCount(len(transactions))
        for i, trans in enumerate(transactions):
            self.treasury_table.setItem(i, 0, QTableWidgetItem(str(trans[5])))
            self.treasury_table.setItem(i, 1, QTableWidgetItem(trans[1]))
            amount_item = QTableWidgetItem(f"{trans[2]:,.2f}")
            if trans[2] < 0:
                amount_item.setForeground(Qt.red)
            else:
                amount_item.setForeground(Qt.green)
            self.treasury_table.setItem(i, 2, amount_item)
            self.treasury_table.setItem(i, 3, QTableWidgetItem(trans[3]))
            self.treasury_table.setItem(i, 4, QTableWidgetItem(str(trans[4]) if trans[4] else "-"))

    def update_treasury_balance(self):
        self.load_treasury_data()

    def get_workers_list(self):
        worker_manager = WorkerManager()
        return worker_manager.get_all_workers()

    def add_loan_dialog(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QDialogButtonBox, QDoubleSpinBox

        dialog = QDialog(self)
        dialog.setWindowTitle("💰 إضافة سلفة لعامل")
        dialog.setFixedSize(450, 250)
        dialog.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['black_luxury']},
                    stop:1 {GOLD_COLORS['black_soft']});
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                border-radius: 20px;
            }}
        """)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("💰 إضافة سلفة لعامل")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-family: 'Times New Roman';
            font-size: 18px;
            font-weight: bold;
            color: {GOLD_COLORS['gold_rich']};
        """)
        layout.addWidget(title)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("👷 العامل:"))
        worker_combo = QComboBox()
        workers = self.get_workers_list()
        for worker in workers:
            worker_combo.addItem(worker[1], worker[0])
        row1.addWidget(worker_combo)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("💰 المبلغ:"))
        amount_input = QDoubleSpinBox()
        amount_input.setRange(1, 1000000)
        amount_input.setPrefix("ج.م ")
        amount_input.setMinimumWidth(150)
        row2.addWidget(amount_input)
        layout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("📝 ملاحظات:"))
        desc_input = QLineEdit()
        desc_input.setPlaceholderText("اختياري...")
        desc_input.setMinimumWidth(200)
        row3.addWidget(desc_input)
        layout.addLayout(row3)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                color: {GOLD_COLORS['black_luxury']};
                border: 1px solid {GOLD_COLORS['gold_sparkle']};
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: 'Georgia';
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_sparkle']},
                    stop:1 {GOLD_COLORS['gold_rich']});
            }}
        """)
        buttons.accepted.connect(lambda: self.save_loan(dialog, worker_combo.currentData(), amount_input.value(), desc_input.text().strip()))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def save_loan(self, dialog, worker_id, amount, description):
        from managers.treasury_manager import TreasuryManager

        if not worker_id:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى اختيار عامل")
            return
        if amount <= 0:
            QMessageBox.warning(self, "تنبيه", "⚠️ يرجى إدخال مبلغ صحيح")
            return
        try:
            treasury_manager = TreasuryManager()
            treasury_manager.add_loan(worker_id, amount, description)
            QMessageBox.information(self, "نجاح", f"✅ تم إضافة السلفة بنجاح!")
            self.load_treasury_data()
            self.refresh_all()
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"❌ حدث خطأ: {str(e)}")

    def repay_loan_dialog(self):
        QMessageBox.information(self, "قريباً", "سيتم إضافة هذه الميزة قريباً")

    def pay_worker_dialog(self):
        QMessageBox.information(self, "قريباً", "سيتم إضافة هذه الميزة قريباً")

    # ===== تبويب مؤقت =====
    def create_placeholder_tab(self, text):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(f"🏅 {text}")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"""
            font-family: 'Georgia';
            font-size: 22px;
            color: {GOLD_COLORS['gold_light']};
            padding: 60px;
        """)
        layout.addWidget(label)
        return widget

    # ===== شاشة حول البرنامج =====
    def show_about(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame

        dialog = QDialog(self)
        dialog.setWindowTitle("👑 حول البرنامج")
        dialog.setFixedSize(550, 480)
        dialog.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['black_luxury']},
                    stop:1 {GOLD_COLORS['black_soft']});
                border: 3px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                border-radius: 20px;
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(12)

        logo = QLabel("🏅")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 56px;")
        layout.addWidget(logo)

        title = QLabel("نظام إدارة الحسابات")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-family: 'Times New Roman';
            font-size: 24px;
            font-weight: bold;
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {GOLD_COLORS['gold_rich']},
                stop:0.5 {GOLD_COLORS['gold_sparkle']},
                stop:1 {GOLD_COLORS['gold_rich']});
        """)
        layout.addWidget(title)

        subtitle = QLabel("✨ شركة التنقيب عن الذهب ✨")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            font-family: 'Georgia';
            font-size: 16px;
            color: {GOLD_COLORS['gold_light']};
        """)
        layout.addWidget(subtitle)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {GOLD_COLORS['gold_dark']},
                stop:0.5 {GOLD_COLORS['gold_rich']},
                stop:1 {GOLD_COLORS['gold_dark']});
            height: 3px;
        """)
        layout.addWidget(line)

        info = [
            ("🖥️ تصميم وبرمجة:", "أحمد علي", "gold_rich"),
            ("🏢 الشركة:", "The Stor", "gold_light"),
            ("📞 رقم الهاتف:", "01281888280", "gold_light"),
            ("📅 الإصدار:", "1.0.0 - الذهبي", "gold_sparkle"),
        ]

        for label_text, value_text, color in info:
            row = QVBoxLayout()
            row.setSpacing(2)
            lbl = QLabel(label_text)
            lbl.setStyleSheet(f"color: {GOLD_COLORS['text_muted']}; font-size: 11px;")
            val = QLabel(value_text)
            val.setStyleSheet(f"""
                color: {GOLD_COLORS[color]};
                font-size: 15px;
                font-weight: bold;
                font-family: 'Georgia';
            """)
            row.addWidget(lbl)
            row.addWidget(val)
            layout.addLayout(row)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {GOLD_COLORS['gold_dark']},
                stop:0.5 {GOLD_COLORS['gold_rich']},
                stop:1 {GOLD_COLORS['gold_dark']});
            height: 3px;
        """)
        layout.addWidget(line2)

        copyright_label = QLabel("© 2026 The Stor - جميع الحقوق محفوظة")
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet(f"""
            color: {GOLD_COLORS['gold_old']};
            font-size: 12px;
            font-family: 'Georgia';
        """)
        layout.addWidget(copyright_label)

        close_btn = QPushButton("✨ إغلاق ✨")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_rich']},
                    stop:0.5 {GOLD_COLORS['gold_metallic']},
                    stop:1 {GOLD_COLORS['gold_dark']});
                color: {GOLD_COLORS['black_luxury']};
                border: 2px solid {GOLD_COLORS['gold_sparkle']};
                border-radius: 12px;
                padding: 14px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Georgia';
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {GOLD_COLORS['gold_sparkle']},
                    stop:0.5 {GOLD_COLORS['gold_rich']},
                    stop:1 {GOLD_COLORS['gold_metallic']});
            }}
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec()