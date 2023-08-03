from django.db import models
class Numbers(models.Model):
    # 双色球数组
    # code
    code = models.CharField(max_length=200)
    # number字符串
    number_str=models.CharField(max_length=200)
    # number_public time
    public_time = models.DateTimeField()


# Create your models here.
