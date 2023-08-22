import logging

from celery import shared_task
from django.db.models import Q

from files.models import FileUpload, FileReport
from files.service import code_review

logger = logging.getLogger(__name__)


@shared_task(name='review_reports')
def review_reports() -> None:
    files = (
        FileUpload.objects
        .exclude(Q(status='verified') | Q(is_deleted=True))
        .order_by('-created_at')
        .all()
    )
    try:
        for file in files:
            result = code_review(file.file.name)
            FileReport.objects.create(
                file=file,
                result=result,
                is_notified=False
            )
        files.update(status='verified')
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')


@shared_task(name='send_notification_user')
def send_notification_user() -> None:
    file_reports = (
        FileReport.objects.filter(is_notified=False)
        .order_by('-created_at')
        .all()
    )
    file_reports.update(is_notified=True)
