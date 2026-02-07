from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, localtime 
import uuid

def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1] # 获取文件拓展名
    filename = f'{uuid.uuid4().hex[:10]}.{ext}' # 生成新的文件名
    return f'user/photos/{instance.user_id}_{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    photo = models.ImageField(default='user/photos/default.png', upload_to=photo_upload_to)
    profile = models.TextField(default="谢谢你的关注", max_length=500) # textfield没有max_length属性，需要再进行截断
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user.username} - {localtime(self.create_time).strftime("%Y-%m-%d %H:%M:%S")}'
