from django.db import models

"""
    数据模式
    单句最大长度为100
"""

SENTENCE_MAX_LENGTH = 500
TAG_MAX_LENGTH = 40
ENTITY_MAX_LENGTH = 50
RELATION_MAX_LENGTH = 40
ADDITIONAL_INFO_MAX_LENGTH = 100


class Project(models.Model):
    """创建的项目信息"""
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=20, unique=True)

    sentence_labeled = models.IntegerField(default=0)
    sentence_unlabeled = models.IntegerField(default=0)

    # 这里应该要用 ArrayField，但是 sqlite 不支持，所以改用 TextField，在文本中添加分隔符来模拟数组
    tag_spliter = ','
    project_tags = models.TextField(unique=False)

    def get_tags_from_project(self) -> list:
        """以 list 的形式获取项目标签"""
        return self.project_tags.strip(self.tag_spliter).split(self.tag_spliter)

    def add_tags_to_project(self, new_tags: list):
        """为项目添加标签"""
        tags = self.get_tags_from_project()
        tags.extend(new_tags)
        self.store_tags_to_project(tags)

    def delete_tag_from_project(self, tag: str):
        """从项目中删除一个标签"""
        tags = self.get_tags_from_project()
        tags.remove(tag)
        self.store_tags_to_project(tags)

    def store_tags_to_project(self, tags: list):
        """将 list 形式的 tags 以 str 的形式保存到项目中"""
        self.project_tags = self.tag_spliter.join(tags)


class File(models.Model):
    """上传的文件信息"""
    file_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class BaseTags(models.Model):
    """基础标签"""
    tag_name = models.CharField(max_length=TAG_MAX_LENGTH, unique=True)


class UnlabeledData(models.Model):
    """未标注数据"""

    unlabeled_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    # 1993年2月15日，李彤出生在吉林某城市。
    data_content = models.TextField(unique=False)
    upload_time = models.DateTimeField()


class LabeledData(models.Model):
    """已标注数据"""
    labeled_id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    labeled_time = models.DateTimeField()
    # 1993年2月15日，<e1>李彤</e1>出生在<e2>吉林</e2>某城市。
    labeled_content = models.TextField(unique=False)

    # 人-出生地
    predicted_relation = models.CharField(max_length=RELATION_MAX_LENGTH, unique=False)
    # 李彤
    predicted_e1 = models.CharField(max_length=ENTITY_MAX_LENGTH, unique=False)
    # 吉林
    predicted_e2 = models.CharField(max_length=ENTITY_MAX_LENGTH, unique=False)
    """
    实体在句中可能多次出现，需要标定实体在<strong>原句</strong>中的起始和终止位置。
    如果是中文语料，将字符串以字符切分为列表；
    如果是英文的，则以空格为分隔符切分为列表。
    两者在年份、时间等表示上有所不同。
    起始和终止位置即为该实体在列表中等起始和终止位置，区间左右闭合。
    """
    # 11
    predicted_e1_start = models.IntegerField(default=0)
    # 12
    predicted_e1_end = models.IntegerField(default=0)
    # 16
    predicted_e2_start = models.IntegerField(default=0)
    # 17
    predicted_e2_end = models.IntegerField(default=0)

    labeled_relation = models.CharField(max_length=RELATION_MAX_LENGTH, unique=False)
    labeled_e1 = models.CharField(max_length=ENTITY_MAX_LENGTH, unique=False)
    labeled_e2 = models.CharField(max_length=ENTITY_MAX_LENGTH, unique=False)
    labeled_e1_start = models.IntegerField(default=0)
    labeled_e1_end = models.IntegerField(default=0)
    labeled_e2_start = models.IntegerField(default=0)
    labeled_e2_end = models.IntegerField(default=0)

    # 附加信息，某些关系及其对应的实体可能是由其他信息启发出来的，附加信息指的就是这里的"其他信息"
    additional_info = models.CharField(max_length=ADDITIONAL_INFO_MAX_LENGTH, unique=False)
