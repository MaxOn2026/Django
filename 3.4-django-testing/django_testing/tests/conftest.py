import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


# =============================================================================
# Фикстуры
# =============================================================================


@pytest.fixture
def api_client():
    """Фикстура для API-клиента DRF."""
    return APIClient()


@pytest.fixture
def course_factory():
    """
    Фикстура-фабрика для создания курсов через model_bakery.

    Возвращает callable, который создаёт и сохраняет экземпляр Course в БД.
    """
    def _create_course(**kwargs):
        return baker.make('students.Course', **kwargs)
    return _create_course


@pytest.fixture
def student_factory():
    """
    Фикстура-фабрика для создания студентов через model_bakery.

    Возвращает callable, который создаёт и сохраняет экземпляр Student в БД.
    """
    def _create_student(**kwargs):
        return baker.make('students.Student', **kwargs)
    return _create_student
