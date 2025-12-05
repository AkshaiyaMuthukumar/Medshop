from django.db import models

CATEGORY_CHOICES = [
    ('pain', 'Pain Relief'),
    ('cold', 'Cold & Flu'),
    ('vitamins', 'Vitamins & Supplements'),
    ('diabetes', 'Diabetes'),
    ('cardio', 'Cardiology'),
    ('skin', 'Skin Care'),
    ('antibiotics', 'Antibiotics'),
]

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    components = models.TextField()
    side_effects = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='medicine_images/', blank=True, null=True)  # <-- updated folder

    def __str__(self):
        return self.name
