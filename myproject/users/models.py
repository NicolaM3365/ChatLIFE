from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png',upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # if img.mode in ('RGBA', 'LA'):
        # # Create a new image with a white background
        #     background = Image.new('RGB', img.size, (255, 255, 255))
        # # Paste the image onto the background, using the alpha channel as mask
        #     background.paste(img, (0, 0), img if img.mode == 'RGBA' else None)
        #     img = background

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    

