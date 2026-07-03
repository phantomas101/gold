from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QGroupBox, QFrame,
    QMessageBox, QTabWidget, QSpinBox, QWidget
)
from PySide6.QtCore import Qt
from utils.styles_gold import GOLD_COLORS, FONT_CONFIG, apply_gold_style, refresh_all_styles
from utils.settings_manager import SettingsManager


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ الإعدادات")
        self.setFixedSize(500, 460)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {GOLD_COLORS['black_luxury']};
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 8px;
            }}
        """)
        
        # تهيئة مدير الإعدادات
        self.settings_manager = SettingsManager()
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # عنوان
        title = QLabel("⚙️ إعدادات البرنامج")
        title.setProperty("title", "true")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16pt;")
        layout.addWidget(title)

        # تبويبات
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #333333;
                border-radius: 4px;
                background-color: #1A1A1A;
                padding: 8px;
            }
            QTabBar::tab {
                background-color: transparent;
                color: #888888;
                padding: 4px 12px;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 9pt;
                min-height: 20px;
            }
            QTabBar::tab:selected {
                color: #D4AF37;
                border-bottom: 2px solid #D4AF37;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                color: #F5F5DC;
            }
        """)

        # ===== تبويب الخطوط =====
        font_tab = QWidget()
        font_layout = QVBoxLayout(font_tab)
        font_layout.setSpacing(10)
        font_layout.setContentsMargins(5, 5, 5, 5)

        # الخط الرئيسي
        main_group = QGroupBox("الخط الرئيسي")
        main_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 4px;
                color: {GOLD_COLORS['text_gold']};
                font-weight: bold;
                font-size: 9pt;
                padding-top: 8px;
                margin-top: 6px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px;
                color: {GOLD_COLORS['text_gold']};
                font-size: 9pt;
            }}
        """)
        main_layout = QVBoxLayout(main_group)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 5, 10, 8)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("الخط:"))
        row1.setSpacing(5)
        self.main_font_combo = QComboBox()
        self.main_font_combo.addItems(['Segoe UI', 'Arial', 'Tahoma', 'Georgia', 'Times New Roman'])
        self.main_font_combo.currentTextChanged.connect(self.update_preview)
        self.main_font_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 3px;
                padding: 3px 8px;
                background-color: {GOLD_COLORS['black_soft']};
                color: {GOLD_COLORS['text_light']};
                font-size: 9pt;
                min-height: 22px;
            }}
        """)
        row1.addWidget(self.main_font_combo)
        row1.addStretch()
        main_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("الحجم:"))
        row2.setSpacing(5)
        self.main_font_size = QSpinBox()
        self.main_font_size.setRange(8, 16)
        self.main_font_size.setValue(10)
        self.main_font_size.valueChanged.connect(self.update_preview)
        self.main_font_size.setStyleSheet(f"""
            QSpinBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 3px;
                padding: 3px 8px;
                background-color: {GOLD_COLORS['black_soft']};
                color: {GOLD_COLORS['text_light']};
                font-size: 9pt;
                min-height: 22px;
                min-width: 60px;
            }}
        """)
        row2.addWidget(self.main_font_size)
        row2.addStretch()
        main_layout.addLayout(row2)

        font_layout.addWidget(main_group)

        # خط الأسماء
        names_group = QGroupBox("خط أسماء العمال والكولات")
        names_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 4px;
                color: {GOLD_COLORS['text_gold']};
                font-weight: bold;
                font-size: 9pt;
                padding-top: 8px;
                margin-top: 6px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px;
                color: {GOLD_COLORS['text_gold']};
                font-size: 9pt;
            }}
        """)
        names_layout = QVBoxLayout(names_group)
        names_layout.setSpacing(5)
        names_layout.setContentsMargins(10, 5, 10, 8)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("الخط:"))
        row3.setSpacing(5)
        self.names_font_combo = QComboBox()
        self.names_font_combo.addItems(['Georgia', 'Segoe UI', 'Arial', 'Tahoma', 'Times New Roman'])
        self.names_font_combo.currentTextChanged.connect(self.update_preview)
        self.names_font_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 3px;
                padding: 3px 8px;
                background-color: {GOLD_COLORS['black_soft']};
                color: {GOLD_COLORS['text_light']};
                font-size: 9pt;
                min-height: 22px;
            }}
        """)
        row3.addWidget(self.names_font_combo)
        row3.addStretch()
        names_layout.addLayout(row3)

        row4 = QHBoxLayout()
        row4.addWidget(QLabel("الحجم:"))
        row4.setSpacing(5)
        self.names_font_size = QSpinBox()
        self.names_font_size.setRange(10, 22)
        self.names_font_size.setValue(14)
        self.names_font_size.valueChanged.connect(self.update_preview)
        self.names_font_size.setStyleSheet(f"""
            QSpinBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 3px;
                padding: 3px 8px;
                background-color: {GOLD_COLORS['black_soft']};
                color: {GOLD_COLORS['text_light']};
                font-size: 9pt;
                min-height: 22px;
                min-width: 60px;
            }}
        """)
        row4.addWidget(self.names_font_size)
        row4.addStretch()
        names_layout.addLayout(row4)

        font_layout.addWidget(names_group)

        # معاينة
        preview_group = QGroupBox("معاينة")
        preview_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 4px;
                color: {GOLD_COLORS['text_gold']};
                font-weight: bold;
                font-size: 9pt;
                padding-top: 8px;
                margin-top: 6px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px;
                color: {GOLD_COLORS['text_gold']};
                font-size: 9pt;
            }}
        """)
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setSpacing(5)
        preview_layout.setContentsMargins(10, 5, 10, 8)

        self.preview_label = QLabel("👷 أحمد محمد (عامل)")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet(f"""
            color: {GOLD_COLORS['text_gold']};
            padding: 10px;
            border: 1px solid {GOLD_COLORS['border_dark']};
            border-radius: 4px;
            background-color: {GOLD_COLORS['black_soft']};
            font-size: 14pt;
            font-weight: bold;
        """)
        preview_layout.addWidget(self.preview_label)

        font_layout.addWidget(preview_group)
        font_layout.addStretch()

        tabs.addTab(font_tab, "📝 الخطوط")

        # ===== تبويب التفعيل =====
        activation_tab = QWidget()
        activation_layout = QVBoxLayout(activation_tab)
        activation_layout.setSpacing(10)
        activation_layout.setContentsMargins(10, 10, 10, 10)

        act_group = QGroupBox("تفعيل البرنامج")
        act_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 4px;
                color: {GOLD_COLORS['text_gold']};
                font-weight: bold;
                font-size: 9pt;
                padding-top: 8px;
                margin-top: 6px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px;
                color: {GOLD_COLORS['text_gold']};
                font-size: 9pt;
            }}
        """)
        act_layout = QVBoxLayout(act_group)
        act_layout.setSpacing(5)
        act_layout.setContentsMargins(10, 5, 10, 8)

        status = QLabel("📌 الحالة: غير مفعل")
        status.setStyleSheet(f"color: {GOLD_COLORS['danger']}; font-weight: bold; font-size: 10pt;")
        act_layout.addWidget(status)

        info = QLabel("سيتم إضافة نظام التفعيل في الإصدارات القادمة")
        info.setStyleSheet(f"color: {GOLD_COLORS['text_muted']}; font-size: 9pt;")
        info.setWordWrap(True)
        act_layout.addWidget(info)

        activation_layout.addWidget(act_group)
        activation_layout.addStretch()

        tabs.addTab(activation_tab, "🔑 التفعيل")

        # ===== تبويب كلمات المرور =====
        pass_tab = QWidget()
        pass_layout = QVBoxLayout(pass_tab)
        pass_layout.setSpacing(10)
        pass_layout.setContentsMargins(10, 10, 10, 10)

        pass_group = QGroupBox("كلمات المرور")
        pass_group.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 4px;
                color: {GOLD_COLORS['text_gold']};
                font-weight: bold;
                font-size: 9pt;
                padding-top: 8px;
                margin-top: 6px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 6px;
                color: {GOLD_COLORS['text_gold']};
                font-size: 9pt;
            }}
        """)
        pass_layout_v = QVBoxLayout(pass_group)
        pass_layout_v.setSpacing(5)
        pass_layout_v.setContentsMargins(10, 5, 10, 8)

        pass_info = QLabel("سيتم إضافة نظام إدارة المستخدمين في الإصدارات القادمة")
        pass_info.setStyleSheet(f"color: {GOLD_COLORS['text_muted']}; font-size: 9pt;")
        pass_info.setWordWrap(True)
        pass_layout_v.addWidget(pass_info)

        pass_layout.addWidget(pass_group)
        pass_layout.addStretch()

        tabs.addTab(pass_tab, "🔒 كلمات المرور")

        layout.addWidget(tabs)

        # أزرار
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        save_btn = QPushButton("💾 حفظ")
        save_btn.setProperty("success", "true")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {GOLD_COLORS['success']};
                border: 1px solid {GOLD_COLORS['success']};
                border-radius: 4px;
                padding: 4px 14px;
                font-weight: bold;
                font-size: 9pt;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background-color: {GOLD_COLORS['success']};
                color: {GOLD_COLORS['black_luxury']};
            }}
        """)
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)

        close_btn = QPushButton("❌ إغلاق")
        close_btn.setProperty("secondary", "true")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {GOLD_COLORS['text_muted']};
                border: 1px solid {GOLD_COLORS['border_dark']};
                border-radius: 4px;
                padding: 4px 14px;
                font-weight: bold;
                font-size: 9pt;
                min-height: 24px;
            }}
            QPushButton:hover {{
                background-color: {GOLD_COLORS['black_hover']};
                color: {GOLD_COLORS['text_light']};
                border: 1px solid {GOLD_COLORS['border_light']};
            }}
        """)
        close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

    def update_preview(self):
        names_font = self.names_font_combo.currentText()
        names_size = self.names_font_size.value()
        
        self.preview_label.setStyleSheet(f"""
            color: {GOLD_COLORS['text_gold']};
            padding: 10px;
            border: 1px solid {GOLD_COLORS['border_dark']};
            border-radius: 4px;
            background-color: {GOLD_COLORS['black_soft']};
            font-family: '{names_font}';
            font-size: {names_size}pt;
            font-weight: bold;
        """)

    def load_settings(self):
        """تحميل الإعدادات من الملف"""
        current_font = FONT_CONFIG.get('family', 'Segoe UI')
        idx = self.main_font_combo.findText(current_font)
        if idx >= 0:
            self.main_font_combo.setCurrentIndex(idx)
        
        self.main_font_size.setValue(FONT_CONFIG.get('size', 10))
        
        names_font = FONT_CONFIG.get('names_font', 'Georgia')
        idx = self.names_font_combo.findText(names_font)
        if idx >= 0:
            self.names_font_combo.setCurrentIndex(idx)
        
        self.names_font_size.setValue(FONT_CONFIG.get('names_size', 14))
        self.update_preview()

    def save_settings(self):
        """حفظ الإعدادات إلى الملف وتطبيقها"""
        # تحديث الإعدادات في الذاكرة
        FONT_CONFIG['family'] = self.main_font_combo.currentText()
        FONT_CONFIG['size'] = self.main_font_size.value()
        FONT_CONFIG['names_font'] = self.names_font_combo.currentText()
        FONT_CONFIG['names_size'] = self.names_font_size.value()
        
        # حفظ الإعدادات إلى الملف
        self.settings_manager.save_settings()
        
        # إعادة تطبيق التنسيق على النافذة الرئيسية
        if self.parent():
            from utils.styles_gold import refresh_all_styles
            refresh_all_styles()
        
        QMessageBox.information(
            self,
            "تم الحفظ",
            "✅ تم حفظ الإعدادات وتطبيقها بنجاح!\n"
            "ستبقى الإعدادات محفوظة حتى بعد إغلاق البرنامج.",
            QMessageBox.Ok
        )
        self.accept()