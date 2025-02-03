from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.class_obj.name} - {self.title}"


class Slide(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="slides")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='slides/images/', blank=True, null=True)
    video = models.FileField(upload_to='slides/videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"
