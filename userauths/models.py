from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

from shortuuid.django_fields import ShortUUIDField

GENDER = (
    ('Female', 'Female'),
    ('Male', 'Male'),
)

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (instance.user.id, filename)
    return "user_{0}/{1}".format(instance.user_id, filename)

class User(AbstractUser):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='Male')
    
    otp = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        email_username, full_name = self.email.split("@")
        if self.full_name == "" or self.full_name == None:
            self.full_name == email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User, self).save(*args, **kwargs)
    

class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet='abcdefghijklmnopqrstuvwxyz123')
    image = models.FileField(upload_to=user_directory_path, default='default.jpg', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='Male')
    
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"

    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name == self.user.username
        super(Profile, self).save(*args, **kwargs)

    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
    