import os
import configparser
from utils.styles_gold import FONT_CONFIG

class SettingsManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.ini')
        self.config = configparser.ConfigParser()
        self.load_settings()
    
    def load_settings(self):
        """تحميل الإعدادات من الملف"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
            
            # تحميل إعدادات الخطوط
            if 'Fonts' in self.config:
                if 'family' in self.config['Fonts']:
                    FONT_CONFIG['family'] = self.config['Fonts']['family']
                if 'size' in self.config['Fonts']:
                    FONT_CONFIG['size'] = int(self.config['Fonts']['size'])
                if 'names_font' in self.config['Fonts']:
                    FONT_CONFIG['names_font'] = self.config['Fonts']['names_font']
                if 'names_size' in self.config['Fonts']:
                    FONT_CONFIG['names_size'] = int(self.config['Fonts']['names_size'])
    
    def save_settings(self):
        """حفظ الإعدادات إلى الملف"""
        if 'Fonts' not in self.config:
            self.config['Fonts'] = {}
        
        self.config['Fonts']['family'] = FONT_CONFIG['family']
        self.config['Fonts']['size'] = str(FONT_CONFIG['size'])
        self.config['Fonts']['names_font'] = FONT_CONFIG['names_font']
        self.config['Fonts']['names_size'] = str(FONT_CONFIG['names_size'])
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get_font_config(self):
        """إرجاع إعدادات الخطوط الحالية"""
        return FONT_CONFIG