import json
from datetime import datetime

from django.db import IntegrityError

from annotator.models import *


# data = [{'a': 1, 'b': 2, 'c': 3}]
# json_string = json.dumps(data, ensure_ascii=False)
# json_string = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
# print(json_string)
# text = json.loads(json_string)
# print(text)


class DB_interface:

    def svm(self, content):
        return content

    def create_project(self, json_string: json = '', project_name: str = '', project_tags: list = []):
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
        print('开始调用')

        if project_name == '':
            data = json.loads(json_string)
            project_name = data["project_name"]
        try:
            project = ProjectInfo(project_name=project_name, project_tags=project_tags)
            project.save()
            ret_data = {
                "status": True,
                "project_id": project.project_id,
                "code": 200,
                "message": "创建成功"
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

    def modify_project_name(self, project_id: int, new_name: str):
        """
        修改项目名字
        :param project_id: 项目id号
        :param new_name: 项目的新名字
        :return: json
        """
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            project.project_name = new_name
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"项目名称修改成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    def override_tags(self, project_id: int, tags: list):
        """
        用新的tags覆盖项目原有的tags
        :param project_id: 项目id
        :param tags: 新的tags
        :return:
        """
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            project.project_tags = tags
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"添加成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    def add_tag_to_project(self, project_id: int, tag: str):
        """
        添加一个tag到项目中
        :param project_id: 项目id
        :param tag: 被添加的tag
        :return:
        """
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            project.project_tags.append(tag)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"添加成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    def add_tags_to_project(self, project_id: int, tags: list):
        """
        添加一些tag到项目中
        :param project_id: 项目id
        :param tags: 被添加的tags
        :return:
        """
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            project.project_tags.extend(tags)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"添加成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    def delete_tag_from_project(self, project_id: int, tag: str):
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            project.project_tags.remove(tag)
            project.save()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"删除成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    def delete_project(self, project_id: int):
        """
        删除项目
        :param project_id: 项目id号
        :return: json
        """
        try:
            ProjectInfo.objects.get(pk=project_id).delete()
            ret_data = {
                "status": True,
                "code": 200,
                "message": u"项目删除成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string

    def get_project_tags(self, project_id: int):
        """
        获得项目的标签
        :param project_id: 项目id
        :return:
        """
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            ret_data = {
                "status": True,
                "code": 200,
                "tags": project.project_tags,
                "message": u"标签获取成功"
            }
        except IntegrityError as e:
            ret_data = {
                "status": False,
                "code": -1,
                "message": str(e)
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
        return json_string


    def get_base_tags(self):
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

    def upload_file(self, json_string: json = '', file_name: str = '',
                    project_id: int = -1, file_contents: list = None, ):
        """
        上传文件到数据库

        pipeline:
            1. 点击上传文件按钮
            2. 前端将上传文件的命令发送给后台，附带文件的名字和内容，所属的项目pid
            3. 后台接收到数据，判断项目 pid 下是否已含有同名的文件
            4. 如果有，告知前端文件上传失败，项目中已含有同名文件；
            否则在文件信息表中新建条目，将文件中的内容导入到未标注数据表中

        :param json_string: json =
            {
                "file_name": "name",
                "file_contents": ["Today is a good day.", "Today is a good day", ...],
                "project_id": 3
            }
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
        if file_contents is None and project_id == -1:
            data = json.loads(json_string)
            file_name = data["file_name"]
            file_contents = data["file_contents"]
            project_id = data["project_id"]

        # 检查文件格式
        if len(file_contents[0]) > 200:
            ret_data = {
                "status": False,
                "file_id": -1,
                "code": -1,
                "message": "文件格式错误"
            }
            json_string = json.dumps(ret_data, ensure_ascii=False)
            return json_string

        # 文件格式正确，尝试写入数据库
        try:
            project = ProjectInfo.objects.get(pk=project_id)
            file_info = FileInfo(file_name=file_name, project_id=project)
            file_info.save()
            for sentence in file_contents:
                unlabeled_data = UnLabeledData(file_id=file_info, data_content=sentence,
                                               upload_time=datetime.now(), project_id=project)
                unlabeled_data.save()
            ret_data = {
                "status": True,
                "file_id": file_info.file_id,
                "code": 200,
                "message": u"文件上传成功！"
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

    def fetch_unlabeled_data(self, json_string: json = '', project_id: int = -1, num: int = -1):
        """
        获取未标注的数据

        pipeline:
            1. 点击下一页
            2. 前端将取未标注数据的命令发送给后台，附带项目的 id 号和要取出数据的数量
            3. 后端接收命令，检查数据库中是否有足够的数据
            4. 如果没有符合条件的数据，告知前端取数据失败；否则将满足条件数量的数据返回给前端

        :param json_string:
            {
                "project_id": 1,
                "num": 1
            }
        :param project_id: 项目 id
        :param num: 要取出的数据条目数量

        :return:
            {
                "status": true,
                "data":
                    [
                        {
                            "id": 1,
                            "text": "aaa",
                            "predicted_relation": "friend",
                            "predicted_e1": "马云",
                            "predicted_e2": "马化腾",
                        },
                        {
                            "id": 2,
                            "text": "aaa",
                            "predicted_relation": "friend",
                            "predicted_e1": "奥巴马",
                            "predicted_e2": "特朗普",
                        },
                        ...
                    ]
                "code": 200,
                "message": "成功取出 num 条数据",
            }
        """
        print(project_id)
        if project_id == -1 and num == -1:
            data = json.loads(json_string)
            project_id = int(data["project_id"])
            num = int(data["num"])

        try:
            objects = UnLabeledData.objects.filter(project_id=ProjectInfo.objects.get(pk=project_id))
            objects = objects if num == -1 else objects[:num]
            unlabeled_data = [{"unlabeled_id": o.unlabeled_id, "data_content": o.data_content}
                              for o in objects]
            ret_dict = {
                "status": True,
                "data":
                    [
                        {
                            "id": meta_data["unlabeled_id"],
                            "text": meta_data["data_content"],
                            "predicted_relation": "unlabel",
                            "predicted_e1": "unlabel",
                            "predicted_e2": "unlabel",
                        }
                        for meta_data in unlabeled_data
                    ],
                "code": 200,
                "message": "成功取出" + str(len(unlabeled_data)) + "条数据！",
            }
        except IntegrityError as e:
            ret_dict = {
                "status": False,
                "data": None,
                "code": -1,
                "message": str(e),
            }
        # TODO: 对数据进行预标注，将预标注后的数据包装成 dict
        print(ret_dict)
        return json.dumps(ret_dict, ensure_ascii=False)

    def commit_labeled_data(self, json_string: json = '', labeled_data: list = None, file_id: int = None,
                            project_id: int = None):
        """
        将已标注的数据提交到数据库

        pipeline:
            1. 点击提交按钮
            2. 前端将提交数据命令发送给后台，附带已标注好的数据
            3. 后端接收命令，将标注好的数据插入到数据库中，并将其从未标注数据表中删除
            4. 如果中途出现错误，返回所有数据，并附带错误信息

        :param json_string:
            {
            "data":
                [
                    {
                        "unlabeled_id": "364",
                        "text": "<e1>特朗普</e1>是<e2>奥巴马</e2>的朋友",
                        "project_id": "1",
                        "predicted_relation": "朋友",
                        "predicted_e1": "奥巴马",
                        "predicted_e2": "特朗普",
                        "labeled_relation": "朋友",
                        "labeled_e1": "奥巴马",
                        "labeled_e2": "特朗普",
                        "additional_info": ["朋友", "是"]
                    },
                    ...
                ]
            }
        :param labeled_data: 已标注的数据

        :return:
            {
                "status": True,
                "code": 200,
                "message": "已标注数据提交成功"
            }
        """
        if labeled_data is None:
            labeled_data = json.loads(json_string)
            labeled_data = labeled_data["data"]
        try:
            for meta_data in labeled_data:
                content_origin = meta_data["text"].replace("<e1>", "").replace("</e1>", "").replace("<e2>", "").replace(
                    "</e2>", "")
                data = LabeledData(data_content=content_origin, file_id=FileInfo.objects.get(pk=file_id),
                                   project_id=ProjectInfo.objects.get(pk=project_id), labeled_time=datetime.now(),
                                   labeled_content=meta_data["text"],
                                   predicted_relation=meta_data["predicted_relation"],
                                   predicted_e1=meta_data["predicted_e1"], predicted_e2=meta_data["predicted_e2"],
                                   labeled_relation=meta_data["labeled_relation"], labeled_e1=meta_data["labeled_e1"],
                                   labeled_e2=meta_data["labeled_e2"], additional_info=meta_data["additional_info"])
                data.save()
                UnLabeledData.objects.filter(pk=meta_data["unlabeled_id"]).delete()
            ret_dict = {
                "status": True,
                "code": 200,
                "message": "已标注数据提交成功"
            }
        except IntegrityError as e:
            ret_dict = {
                "status": False,
                "code": -1,
                "message": str(e),
                "data": labeled_data
            }

        print(ret_dict)
        return json.dumps(ret_dict, ensure_ascii=False)

    def export_project(self, json_string: json = '', project_id: int = -1):
        """
        将数据库中的标注工程导出

        :param json_string: 项目 id 号
            {
                "project_id": 123
            }
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
        if project_id == -1:
            project_id = json.loads(json_string)
            project_id = project_id["project_id"]
        # try:
        try:
            labeled_dataset = LabeledData.objects.filter(project_id=ProjectInfo.objects.get(pk=project_id))
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
                "message": "工程导出成功"
            }
        except IntegrityError as e:
            ret_dict = {
                "status": False,
                "data": None,
                "code": -1,
                "message": "工程导出失败"
            }

        print(ret_dict)
        return json.dumps(ret_dict, ensure_ascii=False)


def test_create_project(project_name="test_project"):
    interface = DB_interface()
    ret = interface.create_project(project_name='123')
    ret = interface.create_project(project_name='12345')
    ret = interface.create_project(project_name='test_project')


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
    ProjectInfo.objects.all().delete()
    FileInfo.objects.all().delete()
    BaseTags.objects.all().delete()
    UnLabeledData.objects.all().delete()
    LabeledData.objects.all().delete()

    interface = DB_interface()

    # 添加基本 tags
    relations = ["Cause-Effect", "Instrument-Agency", "Product-Producer", "Content-Container", "Entity-Origin", "Entity-Destination", "Component-Whole", "Member-Collection", "Message-Topic", "Other"]
    for r in relations:
        base_tag = BaseTags(tag_name=r)
        base_tag.save()

    project = ProjectInfo(project_name='test_project', project_tags=['Cause-Effect', 'Message-Topic'])
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

