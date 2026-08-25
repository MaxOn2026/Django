from django.conf import settings
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        students = data.get("students", [])
        max_students = getattr(settings, "MAX_STUDENTS_PER_COURSE", 20)
        if len(students) > max_students:
            raise serializers.ValidationError(
                f"Максимальное число студентов на курсе — {max_students}."
            )
        return data
