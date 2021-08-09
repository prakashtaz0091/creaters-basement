from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):  #not used in this project
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=15,null=True)
    email = models.CharField(max_length=200,null = True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class AudioFile(models.Model):
    file = models.FileField(upload_to='')
    actual_price = models.FloatField(default = 0)
    tax_amount = models.FloatField(default = 0)
    service_charge = models.FloatField(default = 0)
    delivery_charge = models.FloatField(default = 0)
    total_price = models.FloatField(default = 0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
   


    def __str__(self):
        return str(self.file)


    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)


class OriginalAudio(models.Model):
    audioFile = models.OneToOneField(AudioFile, on_delete=models.CASCADE,primary_key=True)
    originalFile = models.FileField(upload_to='',default ='')

    def __str__(self):
        return str(self.originalFile.name)


    def delete(self, *args, **kwargs):
        self.originalFile.delete()
        super().delete(*args, **kwargs)



class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    downloadable_file = models.FileField(upload_to='cart',default="")

    def __str__(self):
        return str(self.user.username)



class YoutubeLink(models.Model):
    link_id = models.CharField(max_length=1000)

    def __str__(self):
        return self.link_id



class Description(models.Model):
    label = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.label


class ContactMessage(models.Model):
    name = models.CharField( max_length=100)
    email = models.EmailField( max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.name
    
    
    
    
class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rawFile = models.FileField(upload_to="",default="")
    finalProduct = models.FileField(upload_to="",default="")
    actual_price = models.FloatField(default = 0)
    tax_amount = models.FloatField(default = 0)
    service_charge = models.FloatField(default = 0)
    delivery_charge = models.FloatField(default = 0)
    total_price = models.FloatField(default = 0)


    def __str__(self):
        return str(self.rawFile)


    def deleteRawFile(self, *args, **kwargs):
        self.rawFile.delete()
        super().delete(*args, **kwargs)

    def deleteFinalProduct(self, *args, **kwargs):
        self.finalProduct.delete()
        super().delete(*args, **kwargs)


class RequestForDemo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(default="")

    def __str__(self):
        return self.message[:60]


class PhotoGallery(models.Model):
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.id)
    
    