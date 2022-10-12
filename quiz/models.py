from django.db import models

# Create your models here.\
class Quiz(models.Model):
    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    number_of_questions = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.topic}"
    
    def get_questions(self):
        return self.question_set.all()
    
    class Meta:
        verbose_name_plural = 'Quizzes'