from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Faculties'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('faculty', 'name')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.code})'


class AcademicSession(models.Model):
    name = models.CharField(max_length=20, unique=True)
    is_current = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        return cls.objects.filter(is_current=True).first()


class Semester(models.Model):
    FIRST = 'first'
    SECOND = 'second'
    SEMESTER_CHOICES = [
        (FIRST, 'First Semester'),
        (SECOND, 'Second Semester'),
    ]

    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    is_current = models.BooleanField(default=False)
    is_result_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'name')
        ordering = ['session__name', 'name']

    def __str__(self):
        return f'{self.get_name_display()} — {self.session.name}'

    def save(self, *args, **kwargs):
        if self.is_current:
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        return cls.objects.filter(is_current=True).select_related('session').first()


class Level(models.Model):
    LEVEL_CHOICES = [
        (100, '100 Level'),
        (200, '200 Level'),
        (300, '300 Level'),
        (400, '400 Level'),
        (500, '500 Level'),
        (600, '600 Level'),
    ]
    level = models.IntegerField(choices=LEVEL_CHOICES, unique=True)

    class Meta:
        ordering = ['level']

    def __str__(self):
        return f'{self.level} Level'