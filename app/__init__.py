import os
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent))

# Импорты теперь будут работать корректно
from app.main import app  # Импорт FastAPI приложения
from app.core.config import settings  # Импорт настроек

__version__ = "1.0.0"
__all__ = ["app", "settings"]  # Что будет доступно при from AnalysisDataFin import *