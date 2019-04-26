from annotator.manager.ProjectManager import ProjectManager
from annotator.manager.TagManager import TagManager
from annotator.manager.DataManager import DataManager


def create_project(project_name, project_tags=None):
    """创建项目"""
    return ProjectManager.create_project(project_name, project_tags)


def upload_file(project_id: int = -1, file_contents: list = None):
    """上传文件"""
    return ProjectManager.upload_file(project_id, file_contents)


def modify_project_name(project_id, new_name):
    """修改项目名字"""
    return ProjectManager.modify_project_name(project_id, new_name)


def get_projects():
    """获取项目列表"""
    return ProjectManager.get_projects()


def delete_project(project_id):
    """删除项目"""
    return ProjectManager.delete_project(project_id)


def export_project(project_id):
    """导出项目"""
    return ProjectManager.export_project(project_id)


def override_tags(project_id: int, tags: list):
    return TagManager.override_tags(project_id, tags)


def add_tag_to_project(project_id: int, tag: str):
    return TagManager.add_tag_to_project(project_id, tag)


def add_tags_to_project(project_id: int, tags: list):
    return TagManager.add_tags_to_project(project_id, tags)


def delete_tag_from_project(project_id: int, tag: str):
    return TagManager.delete_tag_from_project(project_id, tag)


def get_project_tags(project_id: int):
    return TagManager.get_project_tags(project_id)


def get_base_tags():
    return TagManager.get_base_tags()


def fetch_unlabeled_data(project_id: int, num: int = -1):
    return DataManager.fetch_unlabeled_data(project_id, num)


def commit_labeled_data(labeled_data: list, project_id: int):
    return DataManager.commit_labeled_data(labeled_data, project_id)
