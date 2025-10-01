#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Файл для запуска приложения Sweetie
"""

import os
from app import app

if __name__ == '__main__':
    # Устанавливаем переменную окружения для конфигурации
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # Запускаем приложение
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )


