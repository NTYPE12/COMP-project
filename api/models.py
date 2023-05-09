from django.db import models
from django.utils.timezone import now
from django.urls import reverse

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    types = models.IntegerField(default=0)  # 0stu 1 company 2admin
    school = models.CharField(max_length=255, null=True)
    age = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    tags = models.CharField(max_length=255, null=True)
    realname = models.CharField(max_length=255, null=True)
    hope_work_time_min = models.CharField(max_length=255, null=True)
    hope_work_time_max = models.CharField(max_length=255, null=True)
    hope_work_money_min = models.CharField(max_length=255, null=True)
    hope_work_money_max = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=now)


class EInfo(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    types = models.IntegerField(default=1)  # 0stu 1 company 2admin
    company = models.CharField(max_length=255, null=True)
    info = models.TextField(null=True)
    address = models.CharField(max_length=255, null=True)
    tags = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    company_type = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=now)


class AdminInfo(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    types = models.IntegerField(default=2)  # 0stu 1 company 2admin
    created_at = models.DateTimeField(default=now)


class Job(models.Model):
    e_id = models.ForeignKey(EInfo, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=True)
    job_tags = models.CharField(max_length=255, null=True)
    job_type = models.CharField(max_length=255, null=True)
    work_money_min = models.CharField(max_length=255, null=True)
    work_money_max = models.CharField(max_length=255, null=True)
    job_overview = models.TextField(null=True)
    skills_and_qualifications = models.TextField(null=True)
    education = models.TextField(null=True)
    gender = models.CharField(max_length=255, null=True)
    industry = models.CharField(max_length=255, null=True)
    experience = models.CharField(max_length=255, null=True)
    qualification = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=now)


class JoinWork(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    is_pass_status = models.BooleanField(default=False)
    msg = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=now)


class WorkShort(models.Model):
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True)
    job_title = models.CharField(max_length=255, null=True)
    job_tags = models.CharField(max_length=255, null=True)
    specialisms = models.CharField(max_length=255, null=True)
    min_sallery = models.CharField(max_length=255, null=True)
    overview = models.TextField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    experience = models.CharField(max_length=255, null=True)
    age = models.CharField(max_length=255, null=True)
    current_salary = models.CharField(max_length=255, null=True)
    expected_salary = models.CharField(max_length=255, null=True)
    languages = models.CharField(max_length=255, null=True)
    education = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=now)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])
