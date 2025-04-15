from django.db import models
import os
from django.conf import settings

# Create your models here.
class PdfFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    html_file = models.FileField(upload_to="html_files/", help_text="Generated HTML file",)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.html_file.name
    
    def delete(self, *args, **kwargs):
        # Delete the associated HTML file from storage
        if self.html_file:
            if os.path.isfile(self.html_file.path):
                os.remove(self.html_file.path)

                filename_with_ext = os.path.basename(self.html_file.name)
                filename = os.path.splitext(filename_with_ext)[0]
                History.objects.create(user=self.user, html_file=filename, status="Deleted")

        super().delete(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.pk is None and self.html_file:
    #         filename_with_ext = os.path.basename(self.html_file.name)
    #         filename = os.path.splitext(filename_with_ext)[0]
    #         History.objects.create(user=self.user, file_fk=self, html_file=filename, status="Uploaded")
    
class History(models.Model):
    # STATUS_CHOICES = [
    #     ("Uploaded", "Uploaded"),
    #     ("Edited", "Edited"),
    #     ("Deleted", "Deleted"),
    # ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_fk = models.ForeignKey(PdfFile, on_delete=models.SET_NULL, null=True, blank=True)
    html_file = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="Uploaded")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.html_file} {self.status}"