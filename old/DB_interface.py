import json
from datetime import datetime

from django.db import IntegrityError

from annotator.manager import *
from annotator.models import *

"""
Project:
    create_project(project_name, project_tags): 创建项目
    modify_project_name(project_id): 修改项目名字
    get_projects(): 获得所有项目
    delete_project(project_id): 删除项目
    export_project(project_id): 导出项目
    
Tag: 
    override_tags(project_id, tags): 用新的标签覆盖所有标签
    add_tag_to_project(project_id, tag): 为项目添加一个标签
    add_tags_to_project(project_id, tags): 为项目添加一些标签
    delete_tag_from_project(project_id, tag): 删除项目中的一个标签
    get_project_tags(project_id): 获得项目标签
    get_base_tags(): 获得基础标签
    
Data:
    upload_file(file_name, project_id, file_contents): 上传文件
    get_label_process(project_id): 获得标注进度
    fetch_unlabeled_data(project_id, num): 获取未标注数据
    commit_labeled_data(labeled_data, project_id): 提交已标注数据
"""


class DB_interface:

    def svm(self, content):
        return content

    @staticmethod
    def create_project(project_name, project_tags):
        return ProjectManager.create_project(project_name, project_tags)

    @staticmethod
    def modify_project_name(project_id, new_name):
        return ProjectManager.modify_project_name(project_id, new_name)

    @staticmethod
    def get_projects():
        return ProjectManager.get_projects()

    @staticmethod
    def delete_project(project_id):
        return ProjectManager.delete_project(project_id)

    @staticmethod
    def export_project(project_id):
        return ProjectManager.export_project(project_id)

    @staticmethod
    def override_tags(project_id: int, tags: list):
        return TagManager.override_tags(project_id, tags)

    @staticmethod
    def add_tag_to_project(project_id: int, tag: str):
        return TagManager.add_tag_to_project(project_id, tag)

    @staticmethod
    def add_tags_to_project(project_id: int, tags: list):
        return TagManager.add_tags_to_project(project_id, tags)

    @staticmethod
    def delete_tag_from_project(project_id: int, tag: str):
        return TagManager.delete_tag_from_project(project_id, tag)

    @staticmethod
    def get_project_tags(project_id: int):
        return TagManager.get_project_tags(project_id)

    @staticmethod
    def get_base_tags():
        return TagManager.get_base_tags()

    @staticmethod
    def fetch_unlabeled_data(project_id: int = -1, num: int = -1):
        return DataManager.fetch_unlabeled_data(project_id, num)

    @staticmethod
    def commit_labeled_data(labeled_data: list = None, file_id: int = 0,
                            project_id: int = 0):
        return DataManager.commit_labeled_data(labeled_data, file_id, project_id)


def test_create_project(project_name="test_project"):
    ret = DB_interface.create_project(project_name='123')
    ret = DB_interface.create_project(project_name='12345')
    ret = DB_interface.create_project(project_name='test_project')


def test_upload_file(project_id=-1, file_name=''):
    # from annotator.models import *
    # from annotator.DB_interface import *
    # interface = DB_interface()
    # 测试通过
    print('\n上传文件', file_name)
    interface = DB_interface()
    ret = interface.upload_file(file_name='123', project_id=1, file_contents=['奥巴马和特朗普是基友', 'Today is a good day'])
    print(ret)
    file_id = json.loads(ret)["file_id"]
    return file_id


def test_fetch_unlabeled_data(file_id=-1, project_id=-1, num=-1):
    print('\n获取未标注数据')
    interface = DB_interface()
    ret = interface.fetch_unlabeled_data(project_id=1, num=1)
    print("unlabeled_data", ret)
    # print(type(ret))
    data = json.loads(ret)["data"]
    return data


def test_commit_labaled_data(unlabeled_data, file_id=-1):
    print('\n提交已标注数据')
    interface = DB_interface()
    labeled_data = {
        "unlabeled_id": 3,
        "text": "<e1>Today</e1> is a good <e2>day1</e2>",
        "predicted_relation": "is",
        "predicted_e1": "Today",
        "predicted_e2": "day",
        "labeled_relation": "is",
        "labeled_e1": "Today",
        "labeled_e2": "day",
        "additional_info": ["a", "good"]
    }
    ret = interface.commit_labeled_data(labeled_data=[labeled_data, ], file_id=3)
    print("unlabeled_data", ret)


def test_export_project(project_id=-1):
    print('\n导出工程')
    interface = DB_interface()
    ret = interface.export_project(project_id=project_id)
    print("导出工程", ret)
    # print(type(ret))
    data = json.loads(ret)["data"]
    return data


def init():
    """
    用作初始化数据库中的数据
    :return:
    """
    Project.objects.all().delete()
    File.objects.all().delete()
    BaseTags.objects.all().delete()
    UnLabeledData.objects.all().delete()
    LabeledData.objects.all().delete()

    interface = DB_interface()

    # 添加基本 tags
    relations = ["Cause-Effect", "Instrument-Agency", "Product-Producer", "Content-Container", "Entity-Origin",
                 "Entity-Destination", "Component-Whole", "Member-Collection", "Message-Topic", "Other"]
    for r in relations:
        base_tag = BaseTags(tag_name=r)
        base_tag.save()

    project = Project(project_name='test_project', project_tags=['Cause-Effect', 'Message-Topic'])
    project.save()

    interface.modify_project_name(project_id=project.project_id, new_name='test_project_1')
    interface.add_tag_to_project(project_id=project.project_id, tag='test_tag_single')
    interface.add_tags_to_project(project_id=project.project_id, tags=['test_tag_multiple', ])
    interface.delete_tag_from_project(project_id=project.project_id, tag='Cause-Effect')
    interface.override_tags(project_id=project.project_id, tags=['test_tag1', 'test_tag2'])

    file_content = ['The most common audits were about waste and recycling.', 'The company fabricates plastic chairs.']
    # file = FileInfo(file_name='test_file', project_id=project, file_content=file_content)
    # file.save()
    file_json = interface.upload_file(file_name='test_file', project_id=project.project_id, file_contents=file_content)
    file_id = json.loads(file_json)["file_id"]

    unlabeled_data_json = interface.fetch_unlabeled_data(project_id=project.project_id, num=1)
    unlabeled_data = json.loads(unlabeled_data_json)["data"][0]
    # labeled_data =
    labeled_data = [{
        "unlabeled_id": unlabeled_data["id"],
        "text": "<e1>特朗普</e1>是<e2>奥巴马</e2>的朋友",
        "project_id": "1",
        "predicted_relation": "朋友",
        "predicted_e1": "奥巴马",
        "predicted_e2": "特朗普",
        "labeled_relation": "朋友",
        "labeled_e1": "奥巴马",
        "labeled_e2": "特朗普",
        "additional_info": ["朋友", "是"]
    }, ]
    interface.commit_labeled_data(labeled_data=labeled_data, file_id=file_id, project_id=project.project_id)

    interface.export_project(project_id=project.project_id)
