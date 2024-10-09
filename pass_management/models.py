from django.db import models


class Category(models.Model):
    categoryname = models.CharField(max_length=100, null=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.categoryname
    
class Pass(models.Model):
    PassNumber = models.CharField(max_length=200)
    FullName = models.CharField(max_length=200, null=True)
    ContactNumber = models.CharField(max_length=15, null=True)
    Email = models.CharField(max_length=100, null=True)
    IdentityType = models.CharField(max_length=200, null=True)
    IdentityCardno = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Source = models.CharField(max_length=300, null=True)
    Destination = models.CharField(max_length=300, null=True)
    FromDate = models.DateField(null=True)
    ToDate = models.DateField(null=True)
    Cost = models.CharField(max_length=300, null=True)
    PasscreationDate = models.DateTimeField(null=True)

    def __str__(self):
        return self.PassNumber

class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    emailid = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    message = models.CharField(max_length=300, null=True)
    msgdate = models.DateField(null=True)
    isread = models.CharField(max_length=10, null=True)

    def __str__(self):
       return self.emailid
