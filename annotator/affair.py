from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
import annotator.manager as manager

import pdb, os
import annotator.offline as offline
from annotator.manager.DataManager import test

import pudb


from annotator.models import BaseTags
from annotator.utils import random_generate_string



def get_projects(request):
    """获取数据库中所有项目的名字"""
    return JsonResponse(manager.get_projects())


def create_project(request):
    """创建项目"""
    # import pudb
    # pudb.set_trace()

    # offline.evaluate(
    #     dataset='semeval_2010_task8',
    #     masking_mode='unk',
    #     test_file=os.path.join(project_dir, './annotator/offline/datasets/SemEval2010_task8/test.jsonl'),
    #     save_dir=os.path.join(project_dir, './annotator/offline/logs/complete/models'),
    #     model_file='model_epoch-3_dev-macro-f1-0.4716132465835384_dev-loss-16.142220458984376_2019-04-23__08-51__925007.pt',
    #     batch_size=8,
    #     log_dir=os.path.join(project_dir, './annotator/offline/logs/')
    # )

    if request.method == "POST":
        project_name = request.POST.get("projectname", '1')

        # project_tags = request.POST.get("tags", [])

        import pudb
        # pudb.set_trace()
        project_tags = BaseTags.BASE_TAGS
        ret_data = manager.create_project(
            project_name=project_name, project_tags=project_tags)
        if ret_data['status'] is False:
            print('Try to recreate the project...')
            new_name = random_generate_string(len=15)
            ret_data = manager.create_project(
                project_name=new_name, project_tags=project_tags)
            print('Successfully recreate the project, the new name is ' + new_name + '.')
        return JsonResponse(ret_data)

    # test(
    #     file_name='TEST_FILE.TXT',
    #     input_dir='/Users/seapatrol/Desktop',
    #     output_dir='/Users/seapatrol/Desktop'
    # )


def upload_file(request):
    """上传文件"""
    import pudb
    # pudb.set_trace()
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
    pudb.set_trace()
    if request.method == "POST":

        project_id = int(request.POST.get("project_id", -1))
        num = int(request.POST.get("num", -1))


        return JsonResponse(manager.fetch_unlabeled_data(project_id=project_id, num=num))


def commit_labeld_data(request):
    """提交已标注的数据"""

    # pudb.set_trace()
    if request.method == "POST":
        project_id = int(request.POST.get("project_id", -1))
        labeled_data = []

        for i in range(6):
            idx = str(i)
            text = request.POST.get("text" + idx, None)

            predicted_relation = request.POST.get("predicted_relation" + idx, None)
            e1_start = int(request.POST.get("predicted_e1_start" + idx, -1))
            e1_end = int(request.POST.get("predicted_e1_end" + idx, -1))
            e2_start = int(request.POST.get("predicted_e2_start" + idx, -1))
            e2_end = int(request.POST.get("predicted_e2_end" + idx, -1))

            labeled_relation = request.POST.get("labeled_relation" + idx, None)
            labeled_e1 = request.POST.get("labeled" + idx + "_e1", None)
            labeled_e2 = request.POST.get("labeled" + idx + "_e2", None)
            labeled_e1_start = int(request.POST.get("labeled_e1_start" + idx, -1))
            labeled_e1_end = int(request.POST.get("labeled_e1_end" + idx, -1))
            labeled_e2_start = int(request.POST.get("labeled_e2_start" + idx, -1))
            labeled_e2_end = int(request.POST.get("labeled_e2_end" + idx, -1))

            additional_info = request.POST.get("additional_info" + idx, None)

            data = {
                "text": text,

                "predicted_relation": predicted_relation,
                "predicted_e1_start": e1_start,
                "predicted_e1_end": e1_end,
                "predicted_e2_start": e2_start,
                "predicted_e2_end": e2_end,

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



def get_label_progress(request):
    """获取标注进度"""
    project_id = int(request.POST.get("project_id", -1))
    return JsonResponse(manager.get_label_progress(project_id))



def export_project(request):
    """导出项目"""
    # pudb.set_trace()
    project_id = int(request.POST.get("project_id", -1))

    return JsonResponse(manager.export_project(project_id=project_id))
