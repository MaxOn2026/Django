import pytest
from rest_framework import status
from rest_framework.test import APIClient

from students.models import Course, Student


# =============================================================================
# Тест 1: Retrieve — получение одного курса
# =============================================================================


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """
    Проверяем, что API возвращает правильный курс по его ID.

    Шаги:
    1. Создаём курс через фабрику.
    2. Строим URL для retrieve-запроса.
    3. Делаем GET-запрос.
    4. Проверяем код ответа 200 и что вернулся именно созданный курс.
    """
    # 1. Создаём курс через фабрику
    course = course_factory(name="Mathematics")

    # 2. Строим URL
    url = f"/api/v1/courses/{course.id}/"

    # 3. Делаем GET-запрос
    response = api_client.get(url)

    # 4. Проверяем код ответа и данные
    assert response.status_code == status.HTTP_200_OK, (
        f"Ожидался код 200, получен {response.status_code}"
    )
    assert response.data["id"] == course.id
    assert response.data["name"] == "Mathematics"
    assert response.data["students"] == []


# =============================================================================
# Тест 2: List — получение списка курсов
# =============================================================================


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """
    Проверяем, что API возвращает список всех курсов.

    Шаги:
    1. Создаём несколько курсов через фабрику.
    2. Делаем GET-запрос на список.
    3. Проверяем код ответа 200 и что возвращены все курсы.
    """
    # 1. Создаём несколько курсов
    course1 = course_factory(name="Mathematics")
    course2 = course_factory(name="Physics")
    course3 = course_factory(name="Chemistry")

    # 2. Делаем GET-запрос на список
    url = "/api/v1/courses/"
    response = api_client.get(url)

    # 3. Проверяем код ответа и количество
    assert response.status_code == status.HTTP_200_OK, (
        f"Ожидался код 200, получен {response.status_code}"
    )
    assert len(response.data) == 3, (
        f"Ожидалось 3 курса, получено {len(response.data)}"
    )

    # Проверяем, что все созданные курсы есть в ответе
    retrieved_ids = {item["id"] for item in response.data}
    expected_ids = {course1.id, course2.id, course3.id}
    assert retrieved_ids == expected_ids


# =============================================================================
# Тест 3: Фильтрация по id
# =============================================================================


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """
    Проверяем фильтрацию списка курсов по ID.

    Шаги:
    1. Создаём несколько курсов.
    2. Передаём ID одного из курсов как GET-параметр.
    3. Проверяем, что возвращён только нужный курс.
    """
    # 1. Создаём курсы
    course1 = course_factory(name="Mathematics")
    course2 = course_factory(name="Physics")
    course3 = course_factory(name="Chemistry")

    # 2. Делаем запрос с фильтром по ID course2
    url = "/api/v1/courses/"
    response = api_client.get(url, data={"id": [course2.id]})

    # 3. Проверяем результат
    assert response.status_code == status.HTTP_200_OK, (
        f"Ожидался код 200, получен {response.status_code}"
    )
    assert len(response.data) == 1, (
        f"Ожидался 1 курс, получено {len(response.data)}"
    )
    assert response.data[0]["id"] == course2.id
    assert response.data[0]["name"] == "Physics"


# =============================================================================
# Тест 4: Фильтрация по name
# =============================================================================


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """
    Проверяем фильтрацию списка курсов по имени.

    Шаги:
    1. Создаём несколько курсов с разными именами.
    2. Передаём полное имя курса как GET-параметр.
    3. Проверяем, что возвращён только нужный курс.
    """
    # 1. Создаём курсы
    course1 = course_factory(name="Mathematics")
    course2 = course_factory(name="Physics")
    course3 = course_factory(name="Chemistry")

    # 2. Делаем запрос с фильтром по имени
    url = "/api/v1/courses/"
    response = api_client.get(url, data={"name": "Chemistry"})

    # 3. Проверяем результат
    assert response.status_code == status.HTTP_200_OK, (
        f"Ожидался код 200, получен {response.status_code}"
    )
    assert len(response.data) == 1, (
        f"Ожидался 1 курс, получено {len(response.data)}"
    )
    assert response.data[0]["name"] == "Chemistry"


# =============================================================================
# Тест 5: Создание курса (POST)
# =============================================================================


@pytest.mark.django_db
def test_create_course(api_client):
    """
    Проверяем успешное создание курса через POST-запрос.

    Шаги:
    1. Готовим JSON-данные для нового курса.
    2. Делаем POST-запрос.
    3. Проверяем код ответа 201 и что курс создан с правильными данными.
    """
    # 1. Готовим данные
    new_course_data = {
        "name": "Biology",
        "students": [],
    }

    # 2. Делаем POST-запрос
    url = "/api/v1/courses/"
    response = api_client.post(url, data=new_course_data, format="json")

    # 3. Проверяем результат
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Ожидался код 201, получен {response.status_code}"
    )
    assert response.data["name"] == "Biology"
    assert response.data["students"] == []

    # Проверяем, что курс действительно сохранён в БД
    assert Course.objects.filter(name="Biology").exists()


# =============================================================================
# Тест 6: Обновление курса (PUT)
# =============================================================================


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """
    Проверяем успешное обновление курса через PUT-запрос.

    Шаги:
    1. Создаём курс через фабрику.
    2. Готовим новые данные для обновления.
    3. Делаем PUT-запрос.
    4. Проверяем код ответа 200 и что данные обновлены.
    """
    # 1. Создаём курс
    course = course_factory(name="Mathematics")

    # 2. Готовим новые данные
    updated_data = {
        "name": "Advanced Mathematics",
        "students": [],
    }

    # 3. Делаем PUT-запрос
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.put(url, data=updated_data, format="json")

    # 4. Проверяем результат
    assert response.status_code == status.HTTP_200_OK, (
        f"Ожидался код 200, получен {response.status_code}"
    )
    assert response.data["name"] == "Advanced Mathematics"

    # Проверяем, что данные обновлены в БД
    course.refresh_from_db()
    assert course.name == "Advanced Mathematics"


# =============================================================================
# Тест 7: Удаление курса (DELETE)
# =============================================================================


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """
    Проверяем успешное удаление курса через DELETE-запрос.

    Шаги:
    1. Создаём курс через фабрику.
    2. Делаем DELETE-запрос.
    3. Проверяем код ответа 204 и что курс удалён из БД.
    """
    # 1. Создаём курс
    course = course_factory(name="Physics")

    # 2. Делаем DELETE-запрос
    url = f"/api/v1/courses/{course.id}/"
    response = api_client.delete(url)

    # 3. Проверяем результат
    assert response.status_code == status.HTTP_204_NO_CONTENT, (
        f"Ожидался код 204, получен {response.status_code}"
    )

    # Проверяем, что курс действительно удалён из БД
    assert not Course.objects.filter(id=course.id).exists()


# =============================================================================
# Дополнительные задания: Валидация MAX_STUDENTS_PER_COURSE
# =============================================================================


@pytest.mark.django_db
@pytest.mark.parametrize(
    "max_students,expected_status",
    [
        (20, status.HTTP_201_CREATED),   # Успешное создание с 20 студентами
        (21, status.HTTP_400_BAD_REQUEST),  # Превышение лимита
    ],
)
def test_max_students_per_course_validation(
    api_client,
    student_factory,
    max_students,
    expected_status,
    settings,
):
    """
    Проверяем ограничение на максимальное число студентов на курсе.

    Используем parametrize для тестирования двух сценариев:
    - Создание курса с количеством студентов <= лимита (успех).
    - Попытка добавить студентов сверх лимита (ошибка валидации).

    Лимит задаётся через settings.MAX_STUDENTS_PER_COURSE.
    """
    # Устанавливаем лимит через фикстуру settings
    settings.MAX_STUDENTS_PER_COURSE = max_students

    # Создаём студентов (без привязки к курсу)
    students = []
    for i in range(max_students + 1 if expected_status == status.HTTP_400_BAD_REQUEST else max_students):
        student = student_factory(name=f"Student_{i+1}")
        students.append(student.id)

    # Подготавливаем данные курса со списком студентов
    course_data = {
        "name": "Test Course",
        "students": students,
    }

    # Делаем POST-запрос на создание курса
    url = "/api/v1/courses/"
    response = api_client.post(url, data=course_data, format="json")

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        assert Course.objects.filter(name="Test Course").exists()
    elif expected_status == status.HTTP_400_BAD_REQUEST:
        assert not Course.objects.filter(name="Test Course").exists()
