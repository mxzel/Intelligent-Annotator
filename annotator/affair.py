from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
import annotator.manager as manager
import pdb

from annotator.models import BaseTags


def get_projects(request):
    """获取数据库中所有项目的名字"""
    return JsonResponse(manager.get_projects())


def create_project(request):
    """创建项目"""
    if request.method == "POST":
        project_name = request.POST.get("projectname", '')
        # project_tags = request.POST.get("tags", [])
        project_tags = BaseTags.BASE_TAGS
        ret_dict = manager.create_project(
            project_name=project_name, project_tags=project_tags)
        return JsonResponse(ret_dict)


def upload_file(request):
    """上传文件"""
    if request.method == "POST":
        file_content = request.POST.get("file_contents")
        file_contents = file_content.strip().split('\n')
        file_contents = list(filter(lambda content: len(content) > 10, file_contents))
        project_id = int(request.POST.get("project_id", -1))

        return JsonResponse(manager.upload_file(
            project_id=project_id, file_contents=file_contents))


def override_tags(request):
    """覆盖项目的标签"""
    if request.method == "POST":
        project_id = int(request.POST.get("project_id", -1))
        tags = BaseTags.BASE_TAGS
        # tags = request.POST.get("tags", '').split(',')

        return JsonResponse(manager.override_tags(
            project_id=project_id, tags=tags))


def fetch_unlabeled_data(request):
    """获取未标注数据"""
    if request.method == "POST":
        import pudb
        # pudb.set_trace()
        project_id = int(request.POST.get("project_id", -1))
        num = int(request.POST.get("num", -1))


        return JsonResponse(manager.fetch_unlabeled_data(project_id=project_id, num=num))


def commit_label_data(request):
    """提交已标注的数据"""
    if request.method == "POST":
        project_id = int(request.POST.get("project_id", -1))
        labeled_data = []

        for i in range(6):
            idx = str(i + 1)
            text = request.POST.get("text" + idx, None)

            predicted_relation = request.POST.get("predicted_relation" + idx, None)
            predicted_e1 = request.POST.get("predicted" + idx + "_e1", None)
            predicted_e2 = request.POST.get("predicted" + idx + "_e2", None)
            predicted_e1_start = int(request.POST.get("predicted_e1_start" + idx, -1))
            predicted_e1_end = int(request.POST.get("predicted_e1_end" + idx, -1))
            predicted_e2_start = int(request.POST.get("predicted_e2_start" + idx, -1))
            predicted_e2_end = int(request.POST.get("predicted_e2_end" + idx, -1))

            labeled_relation = request.POST.get("labeled_relation" + idx, None)
            labeled_e1 = request.POST.get("labeled" + idx + "_e1", None)
            labeled_e2 = request.POST.get("labeled" + idx + "_e2", None)
            labeled_e1_start = int(request.POST.get("labeled_e1_start" + idx, -1))
            labeled_e1_end = int(request.POST.get("labeled_e1_end" + idx, -1))
            labeled_e2_start = int(request.POST.get("labeled_e2_start" + idx, -1))
            labeled_e2_end = int(request.POST.get("labeled_e2_end", -1))

            additional_info = request.POST.get("additional_info" + idx, None)

            data = {
                "text": text,

                "predicted_relation": predicted_relation,
                "predicted_e1": predicted_e1,
                "predicted_e2": predicted_e2,
                "predicted_e1_start": predicted_e1_start,
                "predicted_e1_end": predicted_e1_end,
                "predicted_e2_start": predicted_e2_start,
                "predicted_e2_end": predicted_e2_end,

                "labeled_relation": labeled_relation,
                "labeled_e1": labeled_e1,
                "labeled_e2": labeled_e2,
                "labeled_e1_start": labeled_e1_start,
                "labeled_e1_end": labeled_e1_end,
                "labeled_e2_start": labeled_e2_start,
                "labeled_e2_end": labeled_e2_end,

                "additional_info": additional_info,
            }

            labeled_data.append(data)

        return JsonResponse(manager.commit_labeled_data(
            labeled_data=labeled_data, project_id=project_id))

        # models.Labeled_DB_Manager.insert(labeled_id=labeledid,unlabeled_id=unlabeledid,data_content=datacontent,labeled_time=labeledtime,labeled_content=labeledcontent,predicted_relation=predictrelation,predicted_e1=predicte1,predicted_e2=predicte2,labeled_relation=labeledrelation,labeled_e1=labelede1,labeled_e2=labelede2,additional_info=additionalinfo)


def export_project(request):
    """导出项目"""
    if request.method == "POST":
        project_id = int(request.POST.get("project_id", -1))

        return JsonResponse(manager.export_project(project_id=project_id))
