from django.db import models
from django.core.validators import MinLengthValidator

class Item(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Item must be greater than 1 character")]
    )

    def __str__(self):
        return self.name

class LogEntry(models.Model):
    nickname = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Nickname must be greater than 1 character")]
    )
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.nickname