import json
from django.db import IntegrityError
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
    def override_tags(project_id: int, new_tags: list) -> dict:
        """
        用new_tags覆盖项目原有的tags
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.store_tags_to_project(new_tags)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully override tags!"
            }
            print("Successfully override tags! " + str(new_tags))
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("Failed to override tags! " + str(e))
        return ret_data

    @staticmethod
    def add_tag_to_project(project_id: int, tag: str) -> dict:
        """
        添加一个tag到项目中
        :param tag: 要添加的tag
        """
        return TagManager.add_tags_to_project(project_id, [tag,])

    @staticmethod
    def add_tags_to_project(project_id: int, tags: list) -> dict:
        """
        添加一些tag到项目中
        :param tags: 被添加的tags
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.add_tags_to_project(tags)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully add tags to project!"
            }
            print("成功添加标签到项目！添加的标签为: " + ' '.join(tags))
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("添加标签到项目失败！" + str(e))
        return ret_data

    @staticmethod
    def delete_tag_from_project(project_id: int, tag: str) -> dict:
        try:
            project = Project.objects.get(pk=project_id)
            project.delete_tag_from_project(tag)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully delete tag from project!"
            }
            print("从项目中删除标签成功！被删除的标签为: " + tag)
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("从项目中删除标签失败！" + str(e))
        return ret_data

    @staticmethod
    def get_project_tags(project_id: int) -> dict:
        """
        获得项目的标签
        """
        try:
            project = Project.objects.get(pk=project_id)
            tags = project.get_tags_from_project()
            ret_data = {
                "status": True,
                "code": 200,
                "tags": tags,
                "message": u"Successfully fetch tags of project!"
            }
            print("从项目中获取标签成功！获取到的标签为: " + tags)
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("从项目中获取标签失败！" + str(e))
        return ret_data

    @staticmethod
    @DeprecationWarning
    def get_base_tags() -> dict:
        """
        获得基础标签
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
        return ret_data
