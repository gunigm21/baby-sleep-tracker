from django.db import models

class SleepSession(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    note = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    def duration(self):
        return self.end_time - self.start_time
    
    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Сон с {self.start_time} до {self.end_time}"
