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

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    logentry = models.ForeignKey(LogEntry, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'