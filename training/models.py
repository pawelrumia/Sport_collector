from django.db import models
from datetime import date

class Exercise(models.Model):
    SPORT_CHOICES = [
        ('running', 'Running'),
        ('swimming', 'Swimming'),
        ('pullups', 'Pull-ups'),
        ('cycling', 'Cycling'),
        ('pushups', 'Push-ups'),
        ('weights', 'Weights'),
    ]

    CALORIE_BURN_RATE = {
        'running': 10,      # calories per minute
        'swimming': 12,     # calories per minute
        'cycling': 8,       # calories per minute
        'pullups': 0.5,     # calories per repetition
        'pushups': 0.5,     # calories per repetition
        'weights': 0.6      # calories per repetition
    }

    date = models.DateField(default=date.today)
    sport = models.CharField(max_length=50, choices=SPORT_CHOICES)
    details = models.JSONField(default=dict)  # Stores exercise-specific attributes
    calories_burned = models.FloatField()

    def calculate_calories(self):
        if self.sport in ['running', 'swimming', 'cycling']:
            return self.details.get('time', 0) * self.CALORIE_BURN_RATE[self.sport]
        elif self.sport in ['pullups', 'pushups', 'weights']:
            total_reps = self.details.get('sets', 0) * self.details.get('reps_per_set', 0)
            return total_reps * self.CALORIE_BURN_RATE[self.sport]
        return 0

    def save(self, *args, **kwargs):
        self.calories_burned = self.calculate_calories()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sport} on {self.date}"
