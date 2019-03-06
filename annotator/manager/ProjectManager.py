import json
from sqlite3 import IntegrityError
from annotator.models import *

"""
Project:
    create_project(project_name, project_tags): 创建项目
    modify_project_name(project_id, new_name): 修改项目名字
    get_projects(): 获得所有项目
    delete_project(project_id): 删除项目
    export_project(project_id): 导出项目
"""


class ProjectManager:

    @staticmethod
    def create_project(project_name: str = '', project_tags: list = None):
        """
        新建一个工程

        pipeline:
            1. 点击新建项目
            2. 前端发送新建项目的命令给后台，附带工程的名字
            3. 后台接收到数据，检查数据项目信息表中是否已含有相同名字的项目
            4. 如果有，告知前端项目创建失败，原因是已经含有了相同名字的项目；
            否则在项目信息表中新建条目，告知前端项目创建成功，并返回项目 pid

        :param project_name: 工程名字
        :param project_tags: 项目预设 tags

        :return: pid(json)
            {
                "status": true,
                "project_id": 123456,
                "message": "创建成功"
            }
        """
        if project_tags is None:
            project_tags = []

        try:
            project = Project(project_name=project_name, project_tags=project_tags)
            project.save()
            ret_data = {
                "status": True,
                "project_id": project.project_id,
                "code": 200,
                "message": u"Successfully create project!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "project_id": -1,
                "code": 200,
                "message": str(e)
            }

        json_string = json.dumps(ret_data, ensure_ascii=False)
        print(json_string)

        return json_string

    @staticmethod
    def modify_project_name(project_id: int, new_name: str):
        """
        修改项目名字
        :param project_id: 项目id号
        :param new_name: 项目的新名字
        :return: json
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
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    @staticmethod
    def get_projects():
        """
        获得项目列表
        :return:
        """
        try:
            projects = Project.objects.all()
            ret_data = {
                "status": True,
                "code": 200,
                "projects": [(p.project_id, p.project_name) for p in projects],
                "message": u"Successfully fetch projects!"
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
    def delete_project(project_id: int):
        """
        删除项目
        :param project_id: 项目id号
        :return: json
        """
        try:
            Project.objects.get(pk=project_id).delete()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"Successfully delete project!"
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
    def export_project(project_id: int = -1):
        """
        将数据库中的标注工程导出

        :param project_id: 项目 id 号

        :return:
            {
                "status": true,
                "data":
                    [
                        "1	\"The system as described above has its greatest application in an arrayed <e1>configuration</e1> of antenna <e2>elements</e2>.\"
                        Component-Whole(e2,e1)
                        AdditionalInfo: Not a collection: there is structure here, organisation.

                        ",
                        "2	\"The <e1>child</e1> was carefully wrapped and bound into the <e2>cradle</e2> by means of a cord.\"
                        Other
                        AdditionalInfo:

                        ",
                        ...
                    ],
                "code": 200,
                "message": "导出工程成功"
            }
        """

        try:
            labeled_dataset = LabeledData.objects.filter(project_id=Project.objects.get(pk=project_id))
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
        except IntegrityError as e:
            ret_dict = {
                "status": False,
                "data": None,
                "code": -1,
                "message": "Project export failed."
            }

        print(ret_dict)
        return json.dumps(ret_dict, ensure_ascii=False)

    @staticmethod
    def upload_file(file_name: str = '',
                    project_id: int = -1, file_contents: list = None, ):
        """
        上传文件到数据库

        pipeline:
            1. 点击上传文件按钮
            2. 前端将上传文件的命令发送给后台，附带文件的名字和内容，所属的项目pid
            3. 后台接收到数据，判断项目 pid 下是否已含有同名的文件
            4. 如果有，告知前端文件上传失败，项目中已含有同名文件；
            否则在文件信息表中新建条目，将文件中的内容导入到未标注数据表中

        :param file_name: 文件名字
        :param project_id: 项目 id
        :param file_contents: 文件内容 ["Today is a good day.", "Today is a good day", ...]


        :return:
            {
                "status": true,
                "file_id": 123,
                "code": 200,
                "message": "上传成功"
            }
        """
        print("upload_file1")
        print(file_contents)

        # 检查文件格式
        if len(file_contents[0]) > 200:
            ret_data = {
                "status": False,
                "file_id": -1,
                "code": -1,
                "message": "Error of file format!"
            }
            json_string = json.dumps(ret_data, ensure_ascii=False)
            return json_string

        # 文件格式正确，尝试写入数据库
        try:
            project = Project.objects.get(pk=project_id)
            file_info = File(file_name=file_name, project_id=project)
            file_info.save()
            for sentence in file_contents:
                unlabeled_data = UnLabeledData(file_id=file_info, data_content=sentence,
                                               upload_time=datetime.now(), project_id=project)
                unlabeled_data.save()
                project.sentence_unlabeled += 1
            project.save()
            ret_data = {
                "status": True,
                "file_id": file_info.file_id,
                "code": 200,
                "message": u"Successfully upload file."
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "file_id": -1,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        print("upload_file2" + json_string)
        return json_string

    @staticmethod
    def get_label_progress(project_id: int):
        try:
            project = Project.objects.get(pk=project_id)
            ret = project.sentence_labeled / (project.sentence_unlabeled + project.sentence_labeled)
            ret_data = {
                "status": True,
                "code": 200,
                "progress": ret,
                "message": u"Successfully fetch labeling process!"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string