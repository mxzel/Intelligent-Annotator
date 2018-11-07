from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
# Create your views here.
from annotator import models
from annotator import DB_interface


def index(request):
    # return HttpResponse("hello world!")
    return render(request, "index.html")


def test_connect(request):
    """
    test if connect is OK
    :param request:
    :return:
    """
    return JsonResponse(data={"training_process": 50, "code": 200, "message": "annotate success"})
#新建项目
def creat_project(request):
    if request.method == 'POST':
        projectname = request.POST.get("projectname", None)
        #tags=request.POST.get("tags",None)
        # projectid=request.POST.get("projectid",None)
        print(projectname)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.create_project(project_name=projectname))

#上传文件
def upload_file(request):
    if request.method == "POST":
        file_content = request.POST.get("file_contents", None)
        file_contents = file_content.strip(',').split('\n')
        # file_contents = ['奥巴马和特朗普是基友', 'Today is a good day']
        file_name = request.POST.get("file_name", None)
        project_id = request.POST.get("project_id", None)
        interface = DB_interface.DB_interface()
        print("views")
        print(file_contents)

        return HttpResponse(
            interface.upload_file(file_name=file_name, project_id=project_id, file_contents=file_contents))


#获取未标注数据
def fetch_unlabeled_data(request):
    if request.method == "POST":
        projectid = request.POST.get("project_id", None)
        num = request.POST.get("num", None)
        interface = DB_interface.DB_interface()
        print("views")
        print(projectid)
        print(num)

        return HttpResponse(interface.fetch_unlabeled_data(project_id=projectid, num=num))

        # datacontent=models.Unlabeled_DB_Manager.data_content

        # return JsonResponse(data=[{"id":id,"text":text,"predicted_relation":relation,"predicted_e1":e1,"predicted-e2":e2},{}])

#提交未标注数据
def commit_label_data(request):
    if request.method == "POST":
        file_id = request.POST.get("file_id", None)
        project_id = request.POST.get("project_id", None)

        id1 = request.POST.get("id1", None)
        text1 = request.POST.get("text1", None)
        predicted_relation1 = request.POST.get("predicted_relation1", None)
        predicted1_e1 = request.POST.get("predicted1_e1", None)
        predicted1_e2 = request.POST.get("predicted1_e2", None)
        labeled_relation1 = request.POST.get("labeled_relation1", None)
        labeled1_e1 = request.POST.get("labeled1_e1", None)
        labeled1_e2 = request.POST.get("labeled1_e2", None)
        additional_info1 = request.POST.get("additional_info1", None)

        id2 = request.POST.get("id2", None)
        text2 = request.POST.get("text2", None)
        predicted_relation2 = request.POST.get("predicted_relation2", None)
        predicted2_e1 = request.POST.get("predicted2_e1", None)
        predicted2_e2 = request.POST.get("predicted2_e2", None)
        labeled_relation2 = request.POST.get("labeled_relation2", None)
        labeled2_e1 = request.POST.get("labeled2_e1", None)
        labeled2_e2 = request.POST.get("labeled2_e2", None)
        additional_info2 = request.POST.get("additional_info2", None)

        id3 = request.POST.get("id3", None)
        text3 = request.POST.get("text3", None)
        predicted_relation3 = request.POST.get("predict_relation3", None)
        predicted3_e1 = request.POST.get("predicted3_e1", None)
        predicted3_e2 = request.POST.get("predicted3_e2", None)
        labeled_relation3 = request.POST.get("labeled_relation3", None)
        labeled3_e1 = request.POST.get("labeled3_e1", None)
        labeled3_e2 = request.POST.get("labeled3_e2", None)
        additional_info3 = request.POST.get("additional_info3", None)

        id4 = request.POST.get("id4", None)
        text4 = request.POST.get("text4", None)
        predicted_relation4 = request.POST.get("predicted_relation4", None)
        predicted4_e1 = request.POST.get("predicted4_e1", None)
        predicted4_e2 = request.POST.get("predicted4_e2", None)
        labeled_relation4 = request.POST.get("labeled_relation4", None)
        labeled4_e1 = request.POST.get("labeled4_e1", None)
        labeled4_e2 = request.POST.get("labeled4_e2", None)
        additional_info4 = request.POST.get("additional_info4", None)

        id5 = request.POST.get("id5", None)
        text5 = request.POST.get("text5", None)
        predicted_relation5 = request.POST.get("predict_relation5", None)
        predicted5_e1 = request.POST.get("predicted5_e1", None)
        predicted5_e2 = request.POST.get("predicted5_e2", None)
        labeled_relation5 = request.POST.get("labeled_relation5", None)
        labeled5_e1 = request.POST.get("labeled5_e1", None)
        labeled5_e2 = request.POST.get("labeled5_e2", None)
        additional_info5 = request.POST.get("additional_info5", None)

        id6 = request.POST.get("id6", None)
        text6 = request.POST.get("text6", None)
        predicted_relation6 = request.POST.get("predict_relation6", None)
        predicted6_e1 = request.POST.get("predicted6_e1", None)
        predicted6_e2 = request.POST.get("predicted6_e2", None)
        labeled_relation6 = request.POST.get("labeled_relation6", None)
        labeled6_e1 = request.POST.get("labeled6_e1", None)
        labeled6_e2 = request.POST.get("labeled6_e2", None)
        additional_info6 = request.POST.get("additional_info6", None)
        interface = DB_interface.DB_interface()
        labeled_data1 = {
            "unlabeled_id": id1,
            "text": text1,
            "project_id": project_id,
            "predicted_relation": predicted_relation1,
            "predicted_e1": predicted1_e1,
            "predicted_e2": predicted1_e2,
            "labeled_relation": labeled_relation1,
            "labeled_e1": labeled1_e1,
            "labeled_e2": labeled1_e2,
            "additional_info": additional_info1
        }
        labeled_data2 = {
            "unlabeled_id": id2,
            "text": text2,
            "project_id": project_id,
            "predicted_relation": predicted_relation2,
            "predicted_e1": predicted2_e1,
            "predicted_e2": predicted2_e2,
            "labeled_relation": labeled_relation2,
            "labeled_e1": labeled2_e1,
            "labeled_e2": labeled2_e2,
            "additional_info": additional_info2
        }
        labeled_data3 = {
            "unlabeled_id": id3,
            "text": text3,
            "project_id": project_id,
            "predicted_relation": predicted_relation3,
            "predicted_e1": predicted3_e1,
            "predicted_e2": predicted3_e2,
            "labeled_relation": labeled_relation3,
            "labeled_e1": labeled3_e1,
            "labeled_e2": labeled3_e2,
            "additional_info": additional_info3
        }
        labeled_data4 = {
            "unlabeled_id": id4,
            "text": text4,
            "project_id": project_id,
            "predicted_relation": predicted_relation1,
            "predicted_e1": predicted4_e1,
            "predicted_e2": predicted4_e2,
            "labeled_relation": labeled_relation4,
            "labeled_e1": labeled4_e1,
            "labeled_e2": labeled4_e2,
            "additional_info": additional_info4
        }
        labeled_data5 = {
            "unlabeled_id": id5,
            "text": text5,
            "project_id": project_id,
            "predicted_relation": predicted_relation5,
            "predicted_e1": predicted5_e1,
            "predicted_e2": predicted5_e2,
            "labeled_relation": labeled_relation5,
            "labeled_e1": labeled5_e1,
            "labeled_e2": labeled5_e2,
            "additional_info": additional_info5
        }
        labeled_data6 = {
            "unlabeled_id": id6,
            "text": text6,
            "project_id": project_id,
            "predicted_relation": predicted_relation6,
            "predicted_e1": predicted6_e1,
            "predicted_e2": predicted6_e2,
            "labeled_relation": labeled_relation6,
            "labeled_e1": labeled6_e1,
            "labeled_e2": labeled6_e2,
            "additional_info": additional_info6
        }

        return HttpResponse(interface.commit_labeled_data(
            labeled_data=[labeled_data1, labeled_data2, labeled_data3, labeled_data4, labeled_data5, labeled_data6],
            file_id=file_id))

        # models.Labeled_DB_Manager.insert(labeled_id=labeledid,unlabeled_id=unlabeledid,file_id=fileid,data_content=datacontent,labeled_time=labeledtime,labeled_content=labeledcontent,predicted_relation=predictrelation,predicted_e1=predicte1,predicted_e2=predicte2,labeled_relation=labeledrelation,labeled_e1=labelede1,labeled_e2=labelede2,additional_info=additionalinfo)

#导出项目
def export_project(request):
    if request.method == "POST":
        projectid = request.POST.get("project_id", None)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.export_project(project_id=projectid))

#更改项目名称
def modify_project_name(request):
    if request.method == "POST":
        projectid = request.POST.get("project_id", None)
        new_name = request.POST.get("new_name",None)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.modify_project_name(project_id=projectid,new_name=new_name))

#更改预设标注标签
def override_tags(request):
    if request.method == "POST":
        project_id=request.POST.get("project_id",None)
        tags=request.POST.get("tags",None)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.override_tags(project_id=project_id,tags=tags))


#删除项目
def delete_project(request):
    if request.method == "POST":
        projectid = request.POST.get("project_id", None)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.delete_project(project_id=projectid))

#获取项目预设标签
def get_project_tags(request):
    if request.method == "POST":
        projectid = request.POST.get("project_id", None)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.get_project_tags(project_id=projectid))


#获取进度条进度
def get_label_progress(request):
    if request.method == "POST":
        projectid = request.POST.get("project_id", None)
        interface = DB_interface.DB_interface()

        return HttpResponse(interface.get_label_progress(project_id=projectid))