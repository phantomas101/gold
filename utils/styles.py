"""
ملف التنسيقات والجماليات
"""
COLORS = {
    'primary': '#4F46E5',
    'primary_light': '#818CF8',
    'primary_dark': '#3730A3',
    'secondary': '#0EA5E9',
    'success': '#10B981',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'background': '#F8FAFC',
    'surface': '#FFFFFF',
    'text': '#1E293B',
    'text_light': '#64748B',
    'border': '#E2E8F0',
}

def apply_style(widget):
    style = f"""
    QWidget {{
        background-color: {COLORS['background']};
        font-family: 'Segoe UI';
        font-size: 10pt;
        color: {COLORS['text']};
    }}
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    QPushButton {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_light']};
    }}
    QLineEdit, QComboBox {{
        border: 1px solid {COLORS['border']};
        border-radius: 6px;
        padding: 8px 12px;
        background-color: {COLORS['surface']};
    }}
    QTableWidget {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background-color: {COLORS['surface']};
        alternate-background-color: #F1F5F9;
    }}
    QHeaderView::section {{
        background-color: {COLORS['primary']};
        color: white;
        padding: 8px;
        border: none;
        font-weight: bold;
    }}
    QTabWidget::pane {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background-color: {COLORS['surface']};
    }}
    QTabBar::tab:selected {{
        background-color: {COLORS['surface']};
        color: {COLORS['primary']};
        border-bottom: 3px solid {COLORS['primary']};
    }}
    """
    widget.setStyleSheet(style)