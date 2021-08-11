from django.contrib import admin
from .models import Customer,AudioFile,Cart,OriginalAudio,YoutubeLink,Description,ContactMessage,UserFile,RequestForDemo,PhotoGallery,VerifyUser
# Register your models here.
admin.site.register(Customer)
admin.site.register(AudioFile)
admin.site.register(Cart)
admin.site.register(OriginalAudio)
admin.site.register(YoutubeLink)
admin.site.register(Description)
admin.site.register(ContactMessage)
admin.site.register(UserFile)
admin.site.register(RequestForDemo) 
admin.site.register(PhotoGallery) 
admin.site.register(VerifyUser)