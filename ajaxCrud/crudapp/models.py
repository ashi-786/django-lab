from django.db import models

# Create your models here.
class Todo(models.Model):
    # For Radio Buttons
    done = "Done" #as shown in html table
    not_done = "Not Done Yet"
    MY_CHOICES = [(done, 'Done'), (not_done, 'Not Done Yet'),] # Value stored in database

    # for Select Dropdown
    type1 = "Urgent"
    type2 = "Not Urgent"
    type3 = "For Weekend"
    type4 = "Before Week Start"
    MY_CHOICES2 = [
        (type1, 'Urgent'),
        (type2, 'Not Urgent'),
        (type3, 'For Weekend'),
        (type4, 'Before Week Start'),
    ]
    
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=MY_CHOICES, default=not_done)
    type = models.CharField(max_length=255, choices=MY_CHOICES2, null=True, blank=True,)
    todo_img = models.ImageField(upload_to='images/', blank=True, null=True, help_text="Upload an image")
    file = models.FileField(upload_to="documents/", blank=True, null=True, help_text="Upload a document")
    def __str__(self):
        return f"{self.name}, {self.status}, {self.type}, {self.todo_img}, {self.file}"