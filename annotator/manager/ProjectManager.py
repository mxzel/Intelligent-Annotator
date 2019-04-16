import json
from datetime import datetime
from sqlite3 import IntegrityError
from annotator.models import *

"""
Project:
    upload_file(file_name, project_id, file_contents): 上传文件
    get_label_progress(project_id): 获得标注进度
    create_project(project_name, project_tags): 创建项目
    modify_project_name(project_id, new_name): 修改项目名字
    get_projects(): 获得所有项目
    delete_project(project_id): 删除项目
    export_project(project_id): 导出项目
"""


class ProjectManager:

    @staticmethod
    def create_project(project_name: str = '', project_tags: list = None) -> dict:
        """
        新建一个工程

        pipeline:
            1. 点击新建项目
            2. 前端发送新建项目的命令给后台，附带工程的名字
            3. 后台接收到数据，检查数据项目信息表中是否已含有相同名字的项目
            4. 如果有，告知前端项目创建失败，原因是已经含有了相同名字的项目；
            否则在项目信息表中新建条目，告知前端项目创建成功，并返回项目 pid
        """
        if project_tags is None:
            project_tags = []

        try:
            project = Project(project_name=project_name, project_tags='')
            project.store_tags_to_project(project_tags)
            project.save()
            ret_data = {
                "status": True,
                "project_id": project.project_id,
                "code": 200,
                "message": u"Successfully create project!"
            }
            print("项目创建成功")
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("项目创建失败！" + str(e))

        return ret_data

    @staticmethod
    def modify_project_name(project_id: int, new_name: str) -> dict:
        """
        修改项目名字
        """
        try:
            project = Project.objects.get(pk=project_id)
            project.project_name = new_name
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Rename project name successfully!"
            }
            print("项目重命名为 " + new_name)
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("重命名项目失败！")
        return ret_data

    @staticmethod
    def get_projects() -> dict:
        """
        获得项目列表
        """
        try:
            projects = Project.objects.all()
            ret_data = {
                "status": True,
                "code": 200,
                "projects": [(p.project_id, p.project_name) for p in projects],
                "message": u"Successfully fetch projects!"
            }
            print("项目列表获取成功")
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("项目列表获取失败！" + str(e))
        return ret_data

    @staticmethod
    def delete_project(project_id: int) -> dict:
        """
        删除项目
        """
        try:
            Project.objects.get(pk=project_id).delete()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully delete project!"
            }
            print("删除项目成功")
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("删除项目失败！" + str(e))
        return ret_data

    @staticmethod
    def export_project(project_id: int = -1) -> dict:
        """
        将数据库中的标注工程导出

        :param project_id: 项目 id 号

        :return:
            {
                "status": true,
                "data":
                    [
                        "1	\"The system as described above has its greatest application in an arrayed
                            <e1>configuration</e1> of antenna <e2>elements</e2>.\"
                        Component-Whole(e2,e1)
                        AdditionalInfo: Not a collection: there is structure here, organisation.\n\n",

                        "2	\"The <e1>child</e1> was carefully wrapped and bound into the <e2>cradle</e2>
                            by means of a cord.\"
                        Other
                        AdditionalInfo:\n\n",

                        ...
                    ],
                "code": 200,
                "message": "导出工程成功"
            }
        """

        try:
            project = Project.objects.get(pk=project_id)
            labeled_dataset = LabeledData.objects.filter(project_id=project)
            data = []
            for index, labeled_data in enumerate(labeled_dataset):
                line1 = str(index + 1) + '\t' + '"' + labeled_data.labeled_content + '"\n'
                line2 = labeled_data.labeled_relation + '\n'
                line3 = "AdditionalInfo: " + labeled_data.additional_info + '\n'
                line4 = '\n'
                line = line1 + line2 + line3 + line4
                data.append(line)
            ret_dict = {
                "status": True,
                "data": data,
                "code": 200,
                "message": "Project exported successfully."
            }
            print("项目导出成功")
        except IntegrityError as e:
            ret_dict = {
                "status": False,
                "data": None,
                "code": -1,
                "message": "Project export failed."
            }
            print("项目导出失败！" + str(e))

        return ret_dict

    @staticmethod
    def upload_file(project_id: int = -1, file_contents: list = None) -> dict:
        """
        上传文件到数据库

        pipeline:
            1. 点击上传文件按钮
            2. 前端将上传文件的命令发送给后台，附带文件的名字和内容，所属的项目pid
            3. 后台接收到数据，判断项目 pid 下是否已含有同名的文件
            4. 如果有，告知前端文件上传失败，项目中已含有同名文件；
            否则在文件信息表中新建条目，将文件中的内容导入到未标注数据表中

        :param file_contents: 文件内容 ["Today is a good day.", "Today is a good day", ...]


        :return:
            {
                "status": True,
                "file_id": 123,
                "code": 200,
                "message": "上传成功"
            }
        """

        # 检查文件格式
        for sentence in file_contents:
            if len(sentence) > 100:
                ret_data = {
                    "status": False,
                    "code": -1,
                    "message": "文件格式错误！\n每行表示一句话，且不多于100个字符。"
                }
                return ret_data

        # 文件格式正确，尝试写入数据库
        try:
            project = Project.objects.get(pk=project_id)
            file = File(project_id=project)
            file.save()
            for sentence in file_contents:
                unlabeled_data = UnlabeledData(file_id=file, data_content=sentence,
                                               upload_time=datetime.now(), project_id=project)
                unlabeled_data.save()
                project.sentence_unlabeled += 1
            project.save()
            ret_data = {
                "status": True,
                "file_id": file.file_id,
                "code": 200,
                "message": u"Successfully upload file."
            }
            print("上传文件成功")
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("上传文件失败！" + str(e))
        return ret_data

    @staticmethod
    def get_label_progress(project_id: int) -> dict:
        """
        获取标注进度
        """
        try:
            project = Project.objects.get(pk=project_id)
            ret = project.sentence_labeled / (project.sentence_unlabeled + project.sentence_labeled)
            ret_data = {
                "status": True,
                "code": 200,
                "progress": ret,
                "message": u"Successfully fetch labeling process!"
            }
            print("获取标注进度成功！标注进度为: " + "%.2f" % ret)
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
            print("获取标注进度失败！" + str(e))
        return ret_data
