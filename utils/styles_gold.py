"""
ملف التنسيقات الذهبية - تصميم فاخر لشركة تنقيب عن الذهب
"""

# ========== الألوان الذهبية ==========
GOLD_COLORS = {
    'gold_dark': '#B8860B',
    'gold_rich': '#D4AF37',
    'gold_light': '#F5D76E',
    'gold_old': '#C5A059',
    'gold_sparkle': '#FFD700',
    'gold_metallic': '#DAA520',
    'black_luxury': '#0D0D0D',
    'black_soft': '#1C1C1C',
    'bronze': '#CD7F32',
    'copper': '#B87333',
    'text_light': '#F5F5DC',
    'text_muted': '#A9A9A9',
    'success': '#2ECC71',
    'danger': '#E74C3C',
    'info': '#3498DB',
}

def apply_gold_style(widget):
    """تطبيق التنسيق الذهبي على الواجهة"""
    style = f"""
    QWidget {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_luxury']},
            stop:1 {GOLD_COLORS['black_soft']});
        font-family: 'Segoe UI';
        font-size: 10pt;
        color: {GOLD_COLORS['text_light']};
    }}
    
    QMainWindow {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_luxury']},
            stop:0.5 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
    }}
    
    QPushButton {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:0.5 {GOLD_COLORS['gold_metallic']},
            stop:1 {GOLD_COLORS['gold_dark']});
        color: {GOLD_COLORS['black_luxury']};
        border: 1px solid {GOLD_COLORS['gold_sparkle']};
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        font-family: 'Segoe UI';
        font-size: 10pt;
        min-width: 80px;
        min-height: 30px;
        white-space: normal;
    }}
    
    QPushButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_sparkle']},
            stop:0.5 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_metallic']});
        border: 1px solid {GOLD_COLORS['gold_sparkle']};
    }}
    
    QPushButton:pressed {{
        background: {GOLD_COLORS['gold_dark']};
        border: 1px solid {GOLD_COLORS['gold_old']};
    }}
    
    QPushButton[secondary="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['bronze']},
            stop:1 {GOLD_COLORS['copper']});
        color: {GOLD_COLORS['black_luxury']};
        border: 1px solid {GOLD_COLORS['bronze']};
    }}
    
    QPushButton[secondary="true"]:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['copper']},
            stop:1 {GOLD_COLORS['bronze']});
        border: 1px solid {GOLD_COLORS['gold_old']};
    }}
    
    QPushButton[success="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2ECC71,
            stop:1 #27AE60);
        color: white;
        border: 1px solid #2ECC71;
    }}
    
    QPushButton[success="true"]:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #58D68D,
            stop:1 #2ECC71);
    }}
    
    QPushButton[danger="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #E74C3C,
            stop:1 #C0392B);
        color: white;
        border: 1px solid #E74C3C;
    }}
    
    QPushButton[danger="true"]:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #F1948A,
            stop:1 #E74C3C);
    }}
    
    QPushButton[small="true"] {{
        padding: 4px 10px;
        font-size: 9pt;
        min-width: 50px;
        min-height: 22px;
    }}
    
    QPushButton[large="true"] {{
        padding: 12px 24px;
        font-size: 12pt;
        min-width: 120px;
        min-height: 40px;
    }}
    
    QLineEdit, QComboBox, QTextEdit, QDateEdit, QSpinBox, QDoubleSpinBox {{
        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {GOLD_COLORS['gold_old']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 8px;
        padding: 8px 14px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
        color: {GOLD_COLORS['text_light']};
        font-family: 'Segoe UI';
        font-size: 10pt;
        min-height: 30px;
    }}
    
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QDateEdit:focus {{
        border: 2px solid {GOLD_COLORS['gold_sparkle']};
        background: {GOLD_COLORS['black_soft']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 4px;
        width: 25px;
    }}
    
    QComboBox QAbstractItemView {{
        background: {GOLD_COLORS['black_soft']};
        border: 1px solid {GOLD_COLORS['gold_old']};
        color: {GOLD_COLORS['text_light']};
        selection-background-color: {GOLD_COLORS['gold_rich']};
        selection-color: {GOLD_COLORS['black_luxury']};
        font-family: 'Segoe UI';
    }}
    
    QTableWidget {{
        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 12px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
        alternate-background-color: {GOLD_COLORS['black_soft']};
        gridline-color: {GOLD_COLORS['gold_old']};
        font-family: 'Segoe UI';
        font-size: 10pt;
    }}
    
    QTableWidget::item {{
        padding: 10px;
        color: {GOLD_COLORS['text_light']};
        font-size: 12pt;
    }}
    
    QTableWidget::item:selected {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        color: {GOLD_COLORS['black_luxury']};
        font-weight: bold;
    }}
    
    QHeaderView::section {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        color: {GOLD_COLORS['black_luxury']};
        padding: 10px;
        border: none;
        font-weight: bold;
        font-family: 'Segoe UI';
        font-size: 11pt;
    }}
    
    QTabWidget::pane {{
        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 12px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
    }}
    
    QTabBar::tab {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
        color: {GOLD_COLORS['gold_old']};
        padding: 10px 20px;
        margin-right: 3px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        font-family: 'Segoe UI';
        font-weight: bold;
        font-size: 10pt;
        min-height: 30px;
    }}
    
    QTabBar::tab:selected {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        color: {GOLD_COLORS['black_luxury']};
        border-bottom: 3px solid {GOLD_COLORS['gold_sparkle']};
    }}
    
    QTabBar::tab:hover {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_light']},
            stop:1 {GOLD_COLORS['gold_old']});
        color: {GOLD_COLORS['black_luxury']};
    }}
    
    QLabel[title="true"] {{
        font-family: 'Times New Roman';
        font-size: 22pt;
        font-weight: bold;
        color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:0.5 {GOLD_COLORS['gold_sparkle']},
            stop:1 {GOLD_COLORS['gold_rich']});
    }}
    
    QLabel[heading="true"] {{
        font-family: 'Segoe UI';
        font-size: 12pt;
        font-weight: bold;
        color: {GOLD_COLORS['gold_light']};
    }}
    
    QLabel[gold="true"] {{
        color: {GOLD_COLORS['gold_rich']};
        font-weight: bold;
        font-family: 'Segoe UI';
    }}
    
    QLabel[success="true"] {{
        color: #2ECC71;
        font-weight: bold;
    }}
    
    QLabel[danger="true"] {{
        color: #E74C3C;
        font-weight: bold;
    }}
    
    QFrame[gold-card="true"] {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 12px;
        padding: 15px;
    }}
    
    QFrame[gold-card="true"]:hover {{
        border: 2px solid {GOLD_COLORS['gold_sparkle']};
    }}
    
    QDialog {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_luxury']},
            stop:1 {GOLD_COLORS['black_soft']});
        border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 15px;
        font-family: 'Segoe UI';
    }}
    
    QMessageBox {{
        background: {GOLD_COLORS['black_luxury']};
        border: 2px solid {GOLD_COLORS['gold_old']};
        border-radius: 15px;
        font-family: 'Segoe UI';
        font-size: 11pt;
    }}
    
    QMessageBox QPushButton {{
        min-width: 80px;
    }}
    
    QListWidget {{
        border: 1px solid {GOLD_COLORS['gold_old']};
        border-radius: 6px;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['black_soft']},
            stop:1 {GOLD_COLORS['black_luxury']});
        color: {GOLD_COLORS['text_light']};
        padding: 5px;
        font-family: 'Segoe UI';
        font-size: 11pt;
    }}
    
    QListWidget::item {{
        padding: 5px;
        font-size: 12pt;
    }}
    
    QListWidget::item:selected {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        color: {GOLD_COLORS['black_luxury']};
        font-weight: bold;
    }}
    
    QScrollBar:vertical {{
        border: none;
        background: {GOLD_COLORS['black_soft']};
        width: 12px;
        margin: 0px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 6px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {GOLD_COLORS['gold_sparkle']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background: {GOLD_COLORS['black_soft']};
        height: 12px;
        margin: 0px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {GOLD_COLORS['gold_rich']},
            stop:1 {GOLD_COLORS['gold_dark']});
        border-radius: 6px;
        min-width: 20px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background: {GOLD_COLORS['gold_sparkle']};
    }}
    """
    widget.setStyleSheet(style)