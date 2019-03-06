
import json
from sqlite3 import IntegrityError
from annotator.models import *

"""
Tag: 
    override_tags(project_id, tags): 用新的标签覆盖所有标签
    add_tag_to_project(project_id, tag): 为项目添加一个标签
    add_tags_to_project(project_id, tags): 为项目添加一些标签
    delete_tag_from_project(project_id, tag): 删除项目中的一个标签
    get_project_tags(project_id): 获得项目标签
    get_base_tags(): 获得基础标签
"""

class TagManager:
    @staticmethod
    def override_tags(project_id: int, tags: list):
        """
        用新的tags覆盖项目原有的tags
        :param project_id: 项目id
        :param tags: 新的tags
        :return:
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.project_tags = tags
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully override tags!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    @staticmethod
    def add_tag_to_project(project_id: int, tag: str):
        """
        添加一个tag到项目中
        :param project_id: 项目id
        :param tag: 被添加的tag
        :return:
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.project_tags.append(tag)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully add tag to project!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    @staticmethod
    def add_tags_to_project(project_id: int, tags: list):
        """
        添加一些tag到项目中
        :param project_id: 项目id
        :param tags: 被添加的tags
        :return:
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.project_tags.extend(tags)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully add tags to project!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    @staticmethod
    def delete_tag_from_project(project_id: int, tag: str):
        try:
            project = Project.objects.get(pk=project_id)
            project.project_tags.remove(tag)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully delete tag from project!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    @staticmethod
    def get_project_tags(project_id: int):
        """
        获得项目的标签
        :param project_id: 项目id
        :return: tags: list
        """
        try:
            project = Project.objects.get(pk=project_id)
            ret_data = {
                "status": True,
                "code": 200,
                "tags": project.project_tags,
                "message": u"Successfully fetch tags of project!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    @staticmethod
    def get_base_tags():
        """
        获得基础标签
        :return:
        """
        try:
            base_tags = list(BaseTags.objects.all())
            ret_data = {
                "status": True,
                "code": 200,
                "base_tags": base_tags,
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string