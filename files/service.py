import logging
import subprocess
from pathlib import Path

from core import settings

logger = logging.getLogger(__name__)


def code_review(path_file: str) -> str:
    directory = Path(settings.MEDIA_ROOT)
    file_path = directory / Path(path_file)
    try:
        result = subprocess.run(
            ['flake8', str(file_path.absolute())],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return 'Проверка не выявила проблем. Код оформлен по PEP8'
        else:
            return result.stdout
    except Exception as e:
        msg = f'Произошла ошибка: {str(e)}'
        logger.error(msg)
        return msg
