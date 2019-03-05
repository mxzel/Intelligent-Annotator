from django.db import models
from django.contrib.postgres.fields import *


class Project(models.Model):
    """创建的项目信息"""
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=20, unique=True)
    project_tags = ArrayField(base_field=models.CharField(max_length=20, unique=True, default=None), default=list)
    sentence_labeled = models.IntegerField(default=0)
    sentence_unlabeled = models.IntegerField(default=0)


class File(models.Model):
    """上传的文件信息"""
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=20, unique=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class BaseTags(models.Model):
    """基础标签？"""
    tag_name = models.CharField(max_length=20, unique=True)


class UnLabeledData(models.Model):
    """未标注数据"""
    unlabeled_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    data_content = models.CharField(max_length=100, unique=False)
    upload_time = models.DateTimeField()


class LabeledData(models.Model):
    """已标注数据"""
    labeled_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    data_content = models.CharField(max_length=100, unique=False)
    labeled_time = models.DateTimeField()
    labeled_content = models.CharField(max_length=120, unique=False)
    predicted_relation = models.CharField(max_length=20, unique=False)
    predicted_e1 = models.CharField(max_length=20, unique=False)
    predicted_e2 = models.CharField(max_length=20, unique=False)
    labeled_relation = models.CharField(max_length=20, unique=False)
    labeled_e1 = models.CharField(max_length=20, unique=False)
    labeled_e2 = models.CharField(max_length=20, unique=False)
    additional_info = models.CharField(max_length=30, unique=False)
