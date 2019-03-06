
import json
from sqlite3 import IntegrityError
from annotator.models import *

"""
Data:
    upload_file(file_name, project_id, file_contents): 上传文件
    get_label_process(project_id): 获得标注进度
    fetch_unlabeled_data(project_id, num): 获取未标注数据
    commit_labeled_data(labeled_data, project_id): 提交已标注数据
"""


class DataManager:
    @staticmethod
    def fetch_unlabeled_data(project_id: int = -1, num: int = -1):
        """
        获取未标注的数据

        pipeline:
            1. 点击下一页
            2. 前端将取未标注数据的命令发送给后台，附带项目的 id 号和要取出数据的数量
            3. 后端接收命令，检查数据库中是否有足够的数据
            4. 如果没有符合条件的数据，告知前端取数据失败；否则将满足条件数量的数据返回给前端

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

        num = int(num)
        try:
            objects = UnLabeledData.objects.filter(project_id=Project.objects.get(pk=project_id))
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
                "message": "Successfully took out " + str(len(unlabeled_data)) + " pieces of data.",
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

    @staticmethod
    def commit_labeled_data(labeled_data: list = None, file_id: int = 0,
                            project_id: int = 0):
        """
        将已标注的数据提交到数据库

        pipeline:
            1. 点击提交按钮
            2. 前端将提交数据命令发送给后台，附带已标注好的数据
            3. 后端接收命令，将标注好的数据插入到数据库中，并将其从未标注数据表中删除
            4. 如果中途出现错误，返回所有数据，并附带错误信息

        :param labeled_data: 已标注的数据

        :return:
            {
                "status": True,
                "code": 200,
                "message": "已标注数据提交成功"
            }
        """
        try:
            project = Project.objects.get(pk=project_id)
            for meta_data in labeled_data:
                content_origin = meta_data["text"].replace("<e1>", "").replace("</e1>", "").replace("<e2>", "").replace(
                    "</e2>", "")
                data = LabeledData(data_content=content_origin, file_id=File.objects.get(pk=file_id),
                                   project_id=Project.objects.get(pk=project_id), labeled_time=datetime.now(),
                                   labeled_content=meta_data["text"],
                                   predicted_relation=meta_data["predicted_relation"],
                                   predicted_e1=meta_data["predicted_e1"], predicted_e2=meta_data["predicted_e2"],
                                   labeled_relation=meta_data["labeled_relation"], labeled_e1=meta_data["labeled_e1"],
                                   labeled_e2=meta_data["labeled_e2"], additional_info=meta_data["additional_info"])
                data.save()
                UnLabeledData.objects.filter(pk=meta_data["unlabeled_id"]).delete()
                project.sentence_labeled += 1
                project.sentence_unlabeled -= 1
            project.save()
            ret_dict = {
                "status": True,
                "code": 200,
                "message": "Labeled data submitted successfully."
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