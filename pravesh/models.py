from django.db import models
from django.contrib.auth.models import User
import json


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.user.username


class DocumentSet(models.Model):
    name = models.CharField(max_length=200)
    countries = models.ManyToManyField(Country)
    has_backside = models.BooleanField(default=False)
    ocr_labels = models.JSONField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    GENDERS = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    nationality = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    gender = models.CharField(max_length=10, choices=GENDERS)
    document = models.ForeignKey(DocumentSet, on_delete=models.CASCADE)
    document_number = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('first_name','last_name','document_number')
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class CustomerDocument(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file_front = models.FileField(upload_to="customer_documents/")
    file_back = models.FileField(upload_to="customer_documents/")
    extracted_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return json.dumps(self.extracted_data)
