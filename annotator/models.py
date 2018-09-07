from django.db import models
from django.contrib.postgres.fields import *


class ProjectInfo(models.Model):
    """
    project_id = "project_id"
    project_name = "project_name"
    project_tags = "project_tags"
    """
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=20, unique=True)
    project_tags = ArrayField(base_field=models.CharField(max_length=20, unique=True, default=None), default=[])


class FileInfo(models.Model):
    """
    file_id = "file_id"
    file_name = "file_name"
    project_id = "project_id"
    """
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=20, unique=False)
    project_id = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)


class BaseTags(models.Model):
    tag_name = models.CharField(max_length=20, unique=True)


class UnLabeledData(models.Model):
    """
    unlabeled_id = "unlabeled_id"
    file_id = "file_id"
    data_content = "data_content"
    upload_time = "upload_time"
    """
    unlabeled_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(FileInfo, on_delete=models.CASCADE)
    project_id = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    data_content = models.CharField(max_length=100, unique=False)
    upload_time = models.DateTimeField()


class LabeledData(models.Model):
    """
    labeled_id = "labeled_id"
    file_id = "file_id"
    data_content = "data_content"
    labeled_time = "labeled_time"
    labeled_content = "labeled_content"
    predicted_relation = "predicted_relation"
    predicted_e1 = "predicted_e1"
    predicted_e2 = "predicted_e2"
    labeled_relation = "labeled_relation"
    labeled_e1 = "labeled_e1"
    labeled_e2 = "labeled_e2"
    additional_info = "additional_info"
    """
    labeled_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(FileInfo, on_delete=models.CASCADE)
    project_id = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
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
