import json
from datetime import datetime
# data = [{'a': 1, 'b': 2, 'c': 3}]
# json_string = json.dumps(data, ensure_ascii=False)
# json_string = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
# print(json_string)
# text = json.loads(json_string)
# print(text)

from src.task_center.DB_Manager import Labeled_DB_Manager, \
    Unlabeled_DB_Manager, Project_info_DB_Manager, File_info_DB_Manager


class DB_interface:
    labeled_db = Labeled_DB_Manager()
    unlabeled_db = Unlabeled_DB_Manager()
    project_info_db = Project_info_DB_Manager()
    file_info_db = File_info_DB_Manager()

    def svm(self, content):
        return content

    def create_project(self, json_string: json = '', project_name: str = ''):
        """
        新建一个工程

        pipeline:
            1. 点击新建项目
            2. 前端发送新建项目的命令给后台，附带工程的名字
            3. 后台接收到数据，检查数据项目信息表中是否已含有相同名字的项目
            4. 如果有，告知前端项目创建失败，原因是已经含有了相同名字的项目；
            否则在项目信息表中新建条目，告知前端项目创建成功，并返回项目 pid

        :param json_string: 工程名字
            {
                "project_name": "test_project"
            }
        :param project_name: 工程名字

        :return: pid(json)
            {
                "status": true,
                "project_id": 123456,
                "message": "创建成功"
            }
        """
        if project_name == '':
            data = json.loads(json_string)
            project_name = data["project_name"]
        records = self.project_info_db.select(condition="project_name=\'" + project_name + "\'")

        # 可以创建
        if len(records) == 0:
            try:
                pid = self.project_info_db.insert(project_name=project_name)
                ret_data = {
                    "status": True,
                    "project_id": pid[0],
                    "code": 200,
                    "message": "创建成功"
                }
            except:
                ret_data = {
                    "status": False,
                    "project_id": -1,
                    "code": 200,
                    "message": "创建失败，原因未知！"
                }
        # 数据库中已含有同名项目，不可创建
        else:
            ret_data = {
                "status": False,
                "project_id": -1,
                "code": 200,
                "message": "创建失败，数据库中已含有同名项目！"
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
                "file_id": 1,
                "code": 200,
                "message": "上传成功"
            }
        """
        if file_contents is None and project_id == -1:
            data = json.loads(json_string)
            file_name = data["file_name"]
            file_contents = data["file_contents"]
            project_id = data["project_id"]

        # 判断数据库中相同项目下是否已经有了同名的文件
        records = self.file_info_db.select(
            condition="file_name=\'" + file_name + "\' and project_id=\'" + str(project_id) + "\'")

        # 文件可以上传
        if len(records) == 0:
            # try:
            file_id = self.file_info_db.insert(project_id=project_id, file_name=file_name)
            ret = self.unlabeled_db.insert(
                file_id=file_id, data_content='', upload_time=str(datetime.now()))
            self.labeled_db.insert(
                unlabeled_id=ret[0], data_content='', file_id=file_id, labeled_time=str(datetime.now()),
                labeled_content='', predicted_relation='', predicted_e1='', predicted_e2='', labeled_relation='',
                labeled_e1='', labeled_e2='', additional_info=''
            )
            for sentence in file_contents:
                self.unlabeled_db.insert(
                    file_id=file_id, data_content=sentence, upload_time=str(datetime.now()))
            ret_data = {
                "status": True,
                "file_id": file_id[0],
                "code": 200,
                "message": u"文件上传成功！"
            }
            # except:
            #     ret_data = {
            #         "status": False,
            #         "file_id": -1,
            #         "code": -1,
            #         "message": u"文件上传失败，原因未知！"
            #     }
        # 项目下包含了同名文件，不可上传
        else:
            ret_data = {
                "status": False,
                "file_id": -1,
                "code": -1,
                "message": u"文件上传失败，项目中已包含同名文件！"
            }
        json_string = json.dumps(ret_data, ensure_ascii=False)
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
        if project_id == -1 and num == -1:
            data = json.loads(json_string)
            project_id = data["project_id"]
            num = data["num"]

        # 从数据库中取出项目下的一部分未标注的数据
        try:
            rows = self.unlabeled_db.select(columns="unlabeled_id, data_content",
                                            num=num,
                                            additional_tables='file_info',
                                            condition=self.unlabeled_db.table_name
                                                    + '.file_id=file_info.file_id and file_info.project_id='
                                                    + str(project_id) + 'order by unlabeled_id')
        except:
            ret_dict = {
                "status": False,
                "data": None,
                "code": -1,
                "message": "取出数据失败，未知错误！",
            }
            return json.dumps(ret_dict, ensure_ascii=False)

        # 如果数据已经全部标注完
        if len(rows) == 0:
            ret_dict = {
                "status": False,
                "data": None,
                "code": -1,
                "message": "取出数据失败，该项目已经标注完成！",
            }

        # 数据取出成功
        else:
            unlabeled_data = [{"unlabeled_id": row[0], "data_content": row[1]} for row in rows]
            # print(unlabeled_data)
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

        # TODO: 对数据进行预标注，将预标注后的数据包装成 dict
        return json.dumps(ret_dict, ensure_ascii=False)

    def commit_labeled_data(self, json_string: json = '', labeled_data: list = None, file_id: int = None):
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
                        "id": "364",
                        "text": "<e1>特朗普</e1>是<e2>奥巴马</e2>的朋友",
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
        for meta_data in labeled_data:
            # meta_data["text"].replace("<e1>").replace("</e1>").replace("<e2>").replace("</e2>")
            try:
                if file_id is None:
                    self.unlabeled_db.select(columns='file_id', condition='unlabeled_id=' + meta_data["id"])
                    file_id = self.unlabeled_db.fetchone()
                # "text".replace("<>")
                content_origin = meta_data["text"].replace("<e1>", "").replace("</e1>", "").replace("<e2>", "").replace(
                    "</e2>", "")
                # print(file_id)
                self.labeled_db.insert(unlabeled_id=meta_data["id"], data_content=content_origin, file_id=file_id,
                                       labeled_time=str(datetime.now()), labeled_content=meta_data["text"],
                                       predicted_relation=meta_data["predicted_relation"],
                                       predicted_e1=meta_data["predicted_e1"], predicted_e2=meta_data["predicted_e2"],
                                       labeled_relation=meta_data["labeled_relation"],
                                       labeled_e1=meta_data["labeled_e1"],
                                       labeled_e2=meta_data["labeled_e2"], additional_info=meta_data["additional_info"])
                self.unlabeled_db.delete(condition="unlabeled_id=" + str(meta_data["id"]))
            except:
                ret_dict = {
                    "status": False,
                    "code": -1,
                    "message": "提交失败，未知错误！",
                    "data": labeled_data
                }
                return json.dumps(ret_dict, ensure_ascii=False)

        ret_dict = {
            "status": True,
            "code": 200,
            "message": "已标注数据提交成功"
        }
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
                        {
                            "labeled_content": "<e1>特朗普</e1>是<e2>奥巴马</e2>的基友",
                            "labeled_relation": "基友",
                            "additional_info": ["基友", "是"]
                        },
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
        rows = self.labeled_db.select(
            columns="labeled_content, labeled_relation, additional_info",
            additional_tables='file_info',
            condition="file_info.project_id = " + str(project_id) + " " +
                      "and file_info.file_id = " + self.labeled_db.table_name + ".file_id order by labeled_id")
        # except:
        #     ret_dict = {
        #         "status": False,
        #         "data": None,
        #         "code": -1,
        #         "message": "导出失败，原因未知"
        #     }
        #     return json.dumps(ret_dict, ensure_ascii=False)

        ret_dict = {
            "status": True,
            "data": [{
                "labeled_content": row[0],
                "labeled_relation": row[1],
                "additional_info": row[2]
            } for row in rows
            ],
            "code": 200,
            "message": "工程导出成功"
        }
        return json.dumps(ret_dict, ensure_ascii=False)


def test_create_project(project_name="test_project"):
    # 测试通过
    print('\n创建项目', project_name)
    interface = DB_interface()
    data = {
        "project_name": project_name
    }
    json_string = json.dumps(data, ensure_ascii=False)
    # print(json_string)
    ret_info = interface.create_project(json_string=json_string)
    print(ret_info)
    project_id = json.loads(ret_info)["project_id"]
    return project_id


def test_upload_file(project_id=-1, file_name=''):
    # 测试通过
    print('\n上传文件', file_name)
    interface = DB_interface()

    ret = interface.upload_file(file_name=file_name, project_id=project_id,
                                file_contents=['奥巴马和特朗普是基友', 'Today is a good day'])
    print(ret)
    file_id = json.loads(ret)["file_id"]
    return file_id


def test_fetch_unlabeled_data(file_id=-1, project_id=-1, num=-1):
    print('\n获取未标注数据')
    interface = DB_interface()
    ret = interface.fetch_unlabeled_data(project_id=project_id, num=num)
    print("unlabeled_data", ret)
    # print(type(ret))
    data = json.loads(ret)["data"]
    return data


def test_commit_labaled_data(unlabeled_data, file_id=-1):
    print('\n提交已标注数据')
    interface = DB_interface()
    labeled_data = {
        "id": unlabeled_data["id"],
        "text": "<e1>Today</e1> is a good <e2>day</e2>",
        "predicted_relation": "is",
        "predicted_e1": "Today",
        "predicted_e2": "day",
        "labeled_relation": "is",
        "labeled_e1": "Today",
        "labeled_e2": "day",
        "additional_info": ["a", "good"]
    }
    ret = interface.commit_labeled_data(labeled_data=[labeled_data, ], file_id=file_id)
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
    interface = DB_interface()

    # interface.project_info_db.create()
    # interface.file_info_db.create()
    # interface.unlabeled_db.create()
    # interface.labeled_db.create()

    interface.labeled_db.drop()
    interface.unlabeled_db.drop()
    interface.file_info_db.drop()
    interface.project_info_db.drop()

    interface.project_info_db.create()
    interface.file_info_db.create()
    interface.unlabeled_db.create()
    interface.labeled_db.create()

    # print('创建项目')
    # ret_info = interface.create_project(project_name="__test__")
    # print(ret_info)
    # project_id = json.loads(ret_info)["project_id"]
    #
    # print('\n上传文件')
    # ret_info = interface.upload_file(file_name='__test_file__', project_id=project_id,
    #                                  file_contents=['Today is a good day1', 'Today is a good day1'])
    # file_id = json.loads(ret_info)["file_id"]
    # print(ret_info)
    #
    # print('\n获取未标注数据')
    # ret_info = interface.fetch_unlabeled_data(project_id=project_id, num=-1)
    # print(ret_info)
    # unlabeled_data = json.loads(ret_info)["data"][0]
    # labeled_data = {
    #     "id": unlabeled_data["id"],
    #     "text": "<e1>Today</e1> is a good <e2>day1</e2>",
    #     "predicted_relation": "is",
    #     "predicted_e1": "Today",
    #     "predicted_e2": "day1",
    #     "labeled_relation": "is",
    #     "labeled_e1": "Today",
    #     "labeled_e2": "day1",
    #     "additional_info": ["a", "good"]
    # }
    #
    # print('\n提交已标注数据')
    # ret_info = interface.commit_labeled_data(labeled_data=[labeled_data, ], file_id=file_id)
    # print(ret_info)

    # print(ret)


if __name__ == '__main__':
    init()
    project_id = test_create_project()
    file_id = test_upload_file(project_id=project_id, file_name='test_file')
    unlabeled_data = test_fetch_unlabeled_data(project_id=project_id, num=-1)
    test_commit_labaled_data(unlabeled_data=unlabeled_data[1], file_id=file_id)
    test_export_project(project_id=project_id)
