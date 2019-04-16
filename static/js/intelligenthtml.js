var state=new Array();
var tags=new Array();//存储标签tag
var textshow="";

HTMLElement.prototype.__defineGetter__("currentStyle", function () {
return this.ownerDocument.defaultView.getComputedStyle(this, null);
});//获取背景色兼容代码

//新建项目模态框添加标签
function addTag() {
    var text=$('#tag').val();
    tags.push(text);
    var a1=document.createElement("button")
    a1.innerText=text;
    a1.className="btn btn-lg btn-warning";
    a1.setAttribute("style","margin-left: 8px;margin-bottom:12px;height: 30px;line-height: 10px;");
    a1.onclick=function(){
        deleteTag(this);
    };
    var a2=document.getElementById("tags");
    a2.appendChild(a1);
    var add1=document.getElementById("tag");
    add1.value="";
    add1.focus();
    for(var i=0;i<(tags.length)*6;i++)
    {
        state[i]==false;
    }


}

//进度条更新 每次提交后更新
function updata_progress() {
    var xml = createXMLHttpRequest()
    xml.open('POST', 'get_label_progress', false);   //这边如果是get请求,可以不填,如果是异步提交也可以不填
    xml.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xml.send("project_id=" + id);                         //这里是请求体,如果是get请求,那么里面设为null.
    xml.onreadystatechange = function () {     //如果是post,那么里面就设置值
        if (xml.readyState == 4 && xml.status == 200) {     //当xml.readyState == 4的时候,相当于jquery的success页面
            var content = xml.responseText
            var progress = eval("(" + content + ")");
            console.log("json" + progress.progress)
            var progressbar = document.getElementById('progress')
            progressbar.style.width = progress.progress

        }
    }

    }

    //新建项目模态框中删除标签
function deleteTag(i) {
    var a1=document.getElementById("tags");
    var text=i.innerText;
    var index=0;
    for (var j=0;j<tags.length;j++) {
        if (text==tags[j])
            index=j;
    }
    tags.splice(index,1);
    a1.removeChild(i);
}

//更改项目配置时重新设置标签
function initags() {
    for (var i=0;i<tags.length;i++){
        var text=tags[i];
        var a1=document.createElement("button")
        a1.innerText=text;
        a1.className="btn btn-lg btn-warning";
        a1.setAttribute("style","margin-left: 8px;margin-bottom:12px;height: 30px;line-height: 10px;");
        a1.onclick=function(){
            deleteTag_change(this);
        };
        var a2=document.getElementById("tags1");
        a2.appendChild(a1);
    }
}

//更改项目配置时添加标签
function addTag_change() {
    var text=$('#tag1').val();
    tags.push(text);

    var a1=document.createElement("button")
    a1.innerText=text;
    a1.className="btn btn-lg btn-warning";
    a1.setAttribute("style","margin-left: 8px;margin-bottom:12px;height: 30px;line-height: 10px;");
    a1.onclick=function(){
        deleteTag_change(this);
    };
    var a2=document.getElementById("tags1");
    a2.appendChild(a1);
    var add1=document.getElementById("tag1");
    add1.value="";
    add1.focus();
    for(var i=0;i<(tags.length)*6;i++)
    {
        state[i]==false;
    }
}


//更改项目配置时删除标签
function deleteTag_change(i) {
    var a1=document.getElementById("tags1");
    var text=i.innerText;
    var index=0;
    for (var j=0;j<tags.length;j++) {
        if (text==tags[j])
            index=j;
    }
    tags.splice(index,1);
    a1.removeChild(i);

}

//点击导入
function importClick()
{
    $("#files").click();

}


//切换项目
function  changeproject(cp) {
    var vs=cp.innerText
    //var vs = $('#selectproject option:selected').val();
    document.getElementById("dropdown").innerHTML="当前项目："+vs;
    var a=0;
    a=6-submit;
    if(submit<6){
        var con=confirm("您还有"+a+"条记录没有标注，确定更换吗？");
        if(con==true){
            var temp=confirm("你已经提交成功！");
            if(temp==true){
                initButton();
            }
        }
    }
}

var clickcount=0//用于判断是否是第一次进入
//新建项目
function newproject() {

    tags.splice(0,tags.length);
    var a=0;
    var submit=0;
    textshow="";
    var bo=document.getElementById('ok1');
    if (bo.checked)
        submit++;

    bo=document.getElementById('ok2');
    if (bo.checked)
        submit=submit+1;
    bo=document.getElementById('ok3');
    if (bo.checked)
        submit=submit+1;
    bo=document.getElementById('ok4');
    if (bo.checked)
        submit=submit+1;
    bo=document.getElementById('ok5');
    if (bo.checked)
        submit=submit+1;
    bo=document.getElementById('ok6');
    if (bo.checked)
        submit=submit+1;
    a=6-submit;
    if(clickcount>0) {
        if (submit < 6) {
            var con = confirm("您还有" + a + "条记录没有标注，确定更换吗？");
            if (con == true) {
            confirm("该页数据已提交")
            $('#myModal').modal('show')
            }else{
            $('#myModal').modal('hide')
            }

        }else{
        $('#myModal').modal('show')
    }

    }else{
        $('#myModal').modal('show')
    }
        clickcount++
//返回后台
}
var project_info= new Map();//存储项目信息（编号

//新建项目确认
function confirmCreateProject() {
    $("#buttons0").empty();
    $("#buttons1").empty();
    $("#buttons2").empty();
    $("#buttons3").empty();
    $("#buttons4").empty();
    $("#buttons5").empty();
    var project_name=$('#newname').val();
    if (project_name!=null && project_name!="")
    {
        document.getElementById("dropdown").innerHTML="当前项目："+project_name;
        var aText = "<li><a onclick=\"changeproject(this)\">"+project_name+"</a></li>";
        var Text = document.getElementById("selectproject").innerHTML
        document.getElementById("selectproject").innerHTML=Text+aText;
    }
    var temp=confirm("你已经提交成功！");
    $("div[name='projectname']").val(project_name);
    $("div[name='tags']").val(tags);
    $('#myModal').modal('hide');
    if(temp==true){
        setButton();
        setButtonState();
    }
    var project_id;
    var tags_string = tags.join(",")
     xml=createXMLHttpRequest();
     xml.open('POST','create_project',true);
     xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
     xml.send("projectname="+project_name);
     xml.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml.readyState == 4 && xml.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                console.log("projectname:"+xml.responseText)
                project_info.set(project_name, xml.responseText.substring(31, 33))
                project_id=xml.responseText.substring(31, 33);
                 xml_add=createXMLHttpRequest();
                 xml_add.open('POST','add_tags_to_project',true);
                 xml_add.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
                 xml_add.send("project_id="+project_id+"&tags="+tags_string);
                 xml_add.onreadystatechange=function () {     //如果是post,那么里面就设置值
                    if(xml_add.readyState == 4 && xml_add.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                        console.log("add_tags_to_project:"+xml_add.responseText)
                    }
                 }
            }
        }
}
//确认标签（更改项目配置
function confirmChangeTags() {
    $("#buttons0").empty();
    $("#buttons1").empty();
    $("#buttons2").empty();
    $("#buttons3").empty();
    $("#buttons4").empty();
    $("#buttons5").empty();
    var temp=confirm("你已经提交成功！");
    $("div[name='tags']").val(tags);
    $('#myModal1').modal('hide');
    if(temp==true){
        setButton();
        setButtonState();
    }
    var projectName = document.getElementById("dropdown").innerHTML
    projectName=projectName.substr(5,projectName.length-1)
    var tags_string = tags.join(",")
    xml_add=createXMLHttpRequest();
     xml_add.open('POST','add_tags_to_project',true);
     xml_add.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
     xml_add.send("project_id="+project_info.get(projectName)+"&tags="+tags_string);
     xml_add.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml_add.readyState == 4 && xml_add.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                console.log("add_tags_to_project:"+xml_add.responseText)
            }
        }

}


function createXMLHttpRequest() {
        var xmlHttp;
        // 适用于大多数浏览器，以及IE7和IE更高版本
        try{
            xmlHttp = new XMLHttpRequest();
        } catch (e) {
            // 适用于IE6
            try {
                xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
            } catch (e) {
                // 适用于IE5.5，以及IE更早版本
                try{
                    xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
                } catch (e){}
            }
        }
        return xmlHttp;
    }

function defaultcheck(i) {
    var j=parseInt(i.toString().charAt(7))+1
    var j1 = j.toString()
        document.getElementById("ok"+j1).checked=false;
}

//初始化标签按钮数量
function setButton(){
    var temp=tags.length;

    for(var j=0;j<6;j++){
        var a1=document.getElementById("buttons"+j);
        for(var i=0;i<temp;i++){
            var a2 = document.createElement("button")
            a2.id="changecolor"+(j*tags.length+i);
            a2.innerText=tags[i];
            a2.className="btn";
            a2.setAttribute("style","margin-left: 8px;margin-bottom:12px;height: 30px;line-height: 10px;");
            a2.onclick=function(){
                changecolor(this);
                defaultcheck(this.parentElement.id);
                console.log(this.parentElement.id)
            };
            a1.appendChild(a2);
        }
    }
}

//改变点击后标签颜色
function changecolor(self) {
    var mycolor = document.getElementById(self.id);
    var i= self.id.replace(/[^0-9]/ig,"");
    state[i] = !state[i];
    if (state[i] == true) {
        mycolor.style.backgroundColor = "orange";
    }
    else {
        mycolor.style.backgroundColor = "rgb(221,221,221)";
    }
    var mycontent1 = document.getElementById("choose" + (Math.floor(i / tags.length) + 1));
    if (state[i] == true) {
        mycontent1.innerText = mycontent1.innerText + "(" + mycolor.innerHTML + ")";
    }
    if (state[i] == false) {
        var change = "(" + mycolor.innerHTML + ")";
        mycontent1.innerText = (mycontent1.innerText).replace(change, "")
    }
}


var text_id=[]
var page=0;
var page1=6;
var mydata=new Array();
var txtdata
var project2file_id=new Map()
var id
var file_id
var hasData=0;
//文件读取
function fileImport() {
    var selectedFile = document.getElementById("files").files[0];//获取读取的File对象
    var name = selectedFile.name;//读取选中文件的文件名
    var size = selectedFile.size;//读取选中文件的大小
    console.log("文件名:" + name + "大小：" + size);
    var reader = new FileReader();
    reader.readAsText(selectedFile);//读取文件的内容
    reader.onload = function () {
        console.log(this.result);//当读取完成之后会回调这个函数，然后此时文件的内容存储到了result中。直接操作即可。
        txtdata = this.result;//传入值为空
        var temp= document.getElementById("dropdown").innerText//获取项目名
        var temp1=temp.split("：")
        var temp2=temp1[1]
        console.log(temp)
        id=parseInt(project_info.get(temp2))
        var arrtest="[\'Today is a good day1.\', \'Today is a good day2\', \'Today is a good day3\', \'Today is a good day4\', \'Today is a good day5.\', \'Today is a good day6.\']"
        //var fileinfo={file_name:name,file_contents:arrtest,project_id}
        xml=createXMLHttpRequest()
        xml.open('POST','upload_file',false);   //这边如果是get请求,可以不填,如果是异步提交也可以不填
        xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xml.send("file_name="+name+"&file_contents="+txtdata+"&project_id="+id);                         //这里是请求体,如果是get请求,那么里面设为null.
        //xml.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml.readyState == 4 && xml.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                content=xml.responseText
                jsoncontent1=eval("("+content+")");
                console.log("json"+jsoncontent1.file_id)
                file_id=jsoncontent1.file_id
            }

        var jsoncontent
        var content
        xml1=createXMLHttpRequest()
        xml1.open('POST','fetch_unlabeled_data',false);
        xml1.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xml1.send("project_id="+id+"&num="+Number(6))
        //xml1.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml1.readyState == 4 && xml1.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                console.log("content: "+content)
                content=xml1.responseText
                jsoncontent=eval("("+content+")");
                console.log("json: "+jsoncontent.data[0].text)
            }else{
                hasData=0
            }

            for(var l=0;l<jsoncontent.data.length;l++){
                var row={id:jsoncontent.data[l].id,text:jsoncontent.data[l].text}
                text_id.push(row)
            }

        var table1 = jsoncontent.data[0].text.join("");
        var table2 = jsoncontent.data[1].text.join("");
        var table3 = jsoncontent.data[2].text.join("");
        var table4 = jsoncontent.data[3].text.join("");
        var table5 = jsoncontent.data[4].text.join("");
        var table6 = jsoncontent.data[5].text.join("");
        var mytable = new Array(table1, table2, table3, table4, table5, table6);

        for (var m = 0; m < 6; m++) {
            var a0 = document.getElementById("index" + (m + 1));
            var a1 = document.createElement("div");
            var length1 = jsoncontent.data[m].text.join("").length;
            for (var i = 0; i < length1; i++) {
                var a2 = document.createElement("span")
                a2.id=m+"text"+i
                a2.onclick = function () {
                        getdetail(this);
                };
                a2.innerText = mytable[m][i];
                a1.appendChild(a2);
            }
            a0.appendChild(a1);
        }

        $("#choose1").val(jsoncontent.data[0].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[0].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[0].predicted_e2)
                table1[i].click;
        }
        $("#choose2").val(jsoncontent.data[1].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[1].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[1].predicted_e2)
                table1[i].click;
        }
        $("#choose3").val(jsoncontent.data[2].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[2].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[2].predicted_e2)
                table1[i].click;
        }
        $("#choose4").val(jsoncontent.data[3].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[3].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[3].predicted_e2)
                table1[i].click;
        }
        $("#choose5").val(jsoncontent.data[4].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[4].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[4].predicted_e2)
                table1[i].click;
        }
        $("#choose6").val(jsoncontent.data[5].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[5].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[5].predicted_e2)
                table1[i].click;
        }

    }
    hasData++
}


//选词点击变色
function getdetail(column){

    if (column.style.background=="orange") {
        column.style.background="rgb(233,236,239)"
    }else
    column.style.background="orange";
}


//文件导出
function fileexport(){

    xml2=createXMLHttpRequest()
        xml2.open('POST','export_project',false);   //这边如果是get请求,可以不填,如果是异步提交也可以不填
        xml2.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xml2.send("project_id="+id);                         //这里是请求体,如果是get请求,那么里面设为null.
        //xml.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml2.readyState == 4 && xml2.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                content=xml2.responseText
                jsoncontent2=eval("("+content+")");
            }
            var tempcon=" ";
            for(var i=0;i<jsoncontent2.data.length;i++){
            tempcon=tempcon+"labeled_content:"+jsoncontent2.data[i].labeled_content+",labeled_relation:"+jsoncontent2.data[i].labeled_relation+"additional_info:"+jsoncontent2.data[i].additional_info+"\r\n"
    }
    print("save")

    var file = new File([tempcon], "data.txt", { type: "text/plain;charset=utf-8" });
    saveAs(file);
    alert("文件已下载")
}



var page = 0;
var page1 = 6;
var mydata = new Array();

//初始化按钮状态（颜色 勾选
function setButtonState() {
    document.getElementById('ok1').checked=false;
    document.getElementById('ok2').checked=false;
    document.getElementById('ok3').checked=false;
    document.getElementById('ok4').checked=false;
    document.getElementById('ok5').checked=false;
    document.getElementById('ok6').checked=false;
    var con = new Array(100);
    for (var m = 0; m < tags.length*6; m++) {
        con[m] = "changecolor" + m ;
    }
    for (var j = 0; j < tags.length*6; j++) {
        var mycolor = document.getElementById(con[j]);
        mycolor.style.color = "white";
    }
    var con1 = new Array(19);
    for (var m = 0; m < 6; m++) {

        con[m] = "ok" + (m + 1);

    }
    for (var j = 0; j < 6; j++) {
        var mycolor = document.getElementById(con[j]);
        mycolor.style.color = "white";
    }
}

//初始化button
function initButton() {
    for (var i = 0; i < tags.length*6; i++) {
        state[i] == false;
    }

    for (var i = 0; i < 6; i++) {
        var mycontent1 = document.getElementById("index1");
        var mycontent2 = document.getElementById("index2");
        var mycontent3 = document.getElementById("index3");
        var mycontent4 = document.getElementById("index4");
        var mycontent5 = document.getElementById("index5");
        var mycontent6 = document.getElementById("index6");
        var mycontent7 = document.getElementById("choose1");
        var mycontent8 = document.getElementById("choose2");
        var mycontent9 = document.getElementById("choose3");
        var mycontent10 = document.getElementById("choose4");
        var mycontent11 = document.getElementById("choose5");
        var mycontent12 = document.getElementById("choose6");

        var con1 = new Array(mycontent1, mycontent2, mycontent3, mycontent4, mycontent5,mycontent6);
        var con2 = new Array(mycontent7, mycontent8, mycontent9, mycontent10,mycontent11,mycontent12);
        mydata[mydata.length] = con1[i].innerText + con2[i].innerText;
        con1[i].innerHTML = "";
        con2[i].innerText = "选中标签为：";
    }
        var jsoncontent
        var content
        xml1=createXMLHttpRequest()
        xml1.open('POST','fetch_unlabeled_data',false);
        xml1.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xml1.send("project_id="+id+"&num="+Number(6))
        //xml1.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml1.readyState == 4 && xml1.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                console.log("content"+content)
                content=xml1.responseText
                jsoncontent=eval("("+content+")");
                console.log("json"+jsoncontent.data[0].text)
            }

        var table1 = jsoncontent.data[0].text.join("");
        var table2 = jsoncontent.data[1].text.join("");
        var table3 = jsoncontent.data[2].text.join("");
        var table4 = jsoncontent.data[3].text.join("");
        var table5 = jsoncontent.data[4].text.join("");
        var table6 = jsoncontent.data[5].text.join("");
        var mytable = new Array(table1, table2, table3, table4, table5, table6);

        for (var m = 0; m < 6; m++) {
            var a0 = document.getElementById("index" + (m + 1));
            var a1 = document.createElement("div");
            var length1 = jsoncontent.data[m].text.join("").length;
            for (var i = 0; i < length1; i++) {
                var a2 = document.createElement("span")
                a2.id=m+"text"+i
                a2.onclick = function () {
                        getdetail(this);
                };
                a2.innerText = mytable[m][i];
                a1.appendChild(a2);
            }
            a0.appendChild(a1);
        }

        $("#choose1").val(jsoncontent.data[0].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[0].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[0].predicted_e2)
                table1[i].click;
        }
        $("#choose2").val(jsoncontent.data[1].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[1].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[1].predicted_e2)
                table1[i].click;
        }
        $("#choose3").val(jsoncontent.data[2].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[2].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[2].predicted_e2)
                table1[i].click;
        }
        $("#choose4").val(jsoncontent.data[3].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[3].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[3].predicted_e2)
                table1[i].click;
        }
        $("#choose5").val(jsoncontent.data[4].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[4].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[4].predicted_e2)
                table1[i].click;
        }
        $("#choose6").val(jsoncontent.data[5].predicted_relation)
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[5].predicted_e1)
                table1[i].click;
        }
        for (var i=0;i<table1.length;i++) {
            if (table1[i]==jsoncontent.data[5].predicted_e2)
                table1[i].click;
        }
        text_id=[]
}
     // 提交一页标注文本
    function confirmLabeledData() {

        var a = 0;
        var submit = 0;
        var bo = document.getElementById('ok1');
        if (bo.checked)
            submit++;

        bo = document.getElementById('ok2');
        if (bo.checked)
            submit = submit + 1;
        bo = document.getElementById('ok3');
        if (bo.checked)
            submit = submit + 1;
        bo = document.getElementById('ok4');
        if (bo.checked)
            submit = submit + 1;
        bo = document.getElementById('ok5');
        if (bo.checked)
            submit = submit + 1;
        bo = document.getElementById('ok6');
        if (bo.checked)
            submit = submit + 1;

        a = 6 - submit;
        if (submit < 6&&hasData!=0) {
            var con = confirm("您还有" + a + "条记录没有标注，确定提交吗？");
            if (con == true) {
                var temp = confirm("你已经提交成功！");

                if (temp == true) {

                    var text1 = text_id[0].text
                    var text2 = text_id[1].text
                    var text3 = text_id[2].text
                    var text4 = text_id[3].text
                    var text5 = text_id[4].text
                    var text6 = text_id[5].text
                    var labeled_relation11 = $("#choose1").text().split("：")
                    var labeled_relation1 = labeled_relation11[1]
                    var labeled_relation21 = $("#choose2").text().split("：")
                    var labeled_relation2 = labeled_relation21[1]
                    var labeled_relation31 = $("#choose3").text().split("：")
                    var labeled_relation3 = labeled_relation31[1]
                    var labeled_relation41 = $("#choose4").text().split("：")
                    var labeled_relation4 = labeled_relation41[1]
                    var labeled_relation51 = $("#choose5").text().split("：")
                    var labeled_relation5 = labeled_relation51[1]
                    var labeled_relation61 = $("#choose6").text().split("：")
                    var labeled_relation6 = labeled_relation61[1]
                    var length2 = $("#index1").text().split(" ")
                    var labeled1_e1
                    var labeled1_e2
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("0text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled1_e1 = $("#0text" + i).text()
                            break
                        }
                    }
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("0text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled1_e2 = $("#0text" + i).text()
                        }
                    }

                    length2 = $("#index2").text().split(" ")
                    var labeled2_e1
                    var labeled2_e2
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("1text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled2_e1 = $("#1text" + i).text()
                            break
                        }
                    }
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("1text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled2_e2 = $("#1text" + i).text()
                        }
                    }

                    length2 = $("#index3").text().split(" ")
                    var labeled3_e1
                    var labeled3_e2
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("2text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled3_e1 = $("#2text" + i).text()
                            break
                        }
                    }
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("2text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled3_e2 = $("#2text" + i).text()
                        }
                    }

                    length2 = $("#index4").text().split(" ")
                    var labeled4_e1
                    var labeled4_e2
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("3text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled4_e1 = $("#3text" + i).text()
                            break
                        }
                    }
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("3text" + i)
                        if (color.style.backgroundColor == 'orange')
                            labeled4_e2 = $("#3text" + i).text()
                    }

                    length2 = $("#index5").text().split(" ")
                    var labeled5_e1
                    var labeled5_e2
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("4text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled5_e1 = $("#4text" + i).text()
                            break
                        }
                    }
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("4text" + i)
                        if (color.style.backgroundColor == 'orange')
                            labeled5_e2 = $("#4text" + i).text()
                    }

                    length2 = $("#index6").text().split(" ")
                    var labeled6_e1
                    var labeled6_e2
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("5text" + i)
                        if (color.style.backgroundColor == 'orange') {
                            labeled6_e1 = $("#5text" + i).text()
                            break
                        }
                    }
                    for (var i = 0; i < length2.length - 1; i++) {
                        var color = document.getElementById("5text" + i)
                        if (color.style.backgroundColor == 'orange')
                            labeled6_e2 = $("#5text" + i).text()
                    }
                    var id1 = text_id[0].id
                    var id2 = text_id[1].id
                    var id3 = text_id[2].id
                    var id4 = text_id[3].id
                    var id5 = text_id[4].id
                    var id6 = text_id[5].id
=

                    xml2 = createXMLHttpRequest()
                    xml2.open('POST', 'commit_label_data', false);
                    xml2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xml2.send("file_id=" + file_id + "&id1=" + id1 + "&text1=" + text1 + "&labeled_relation1=" + labeled_relation1 + "&labeled1_e1=" + labeled1_e1 + "&labeled1_e2=" + labeled1_e2 + "&id2=" + id2 + "&text2=" + text2 + "&labeled_relation2=" + labeled_relation2 + "&labeled2_e1=" + labeled2_e1 + "&labeled2_e2=" + labeled2_e2 + "&id3=" + id3 + "&text3=" + text3 + "&labeled_relation3=" + labeled_relation3 + "&labeled3_e1=" + labeled3_e1 + "&labeled3_e2=" + labeled3_e2 + "&id4=" + id4 + "&text4=" + text4 + "&labeled_relation4=" + labeled_relation4 + "&labeled4_e1=" + labeled4_e1 + "&labeled4_e2=" + labeled4_e2 + "&id5=" + id5 + "&text5=" + text5 + "&labeled_relation5=" + labeled_relation5 + "&labeled5_e1=" + labeled5_e1 + "&labeled5_e2=" + labeled5_e2 + "&id6=" + id6 + "&text6=" + text6 + "&labeled_relation6=" + labeled_relation6 + "&labeled6_e1=" + labeled6_e1 + "&labeled6_e2=" + labeled6_e2)
                    initButton()
                    setButtonState();
                    updata_progress();
                    console.log("commit_label_data");
                }


            }
        }else{
            alert("无数据！")
        }

        submit = 0;


    }



function trim(s){
    return trimRight(trimLeft(s));
}
//去掉左边的空白
function trimLeft(s){
    if(s == null) {
        return "";
    }
    var whitespace = new String(" \t\n\r");
    var str = new String(s);
    if (whitespace.indexOf(str.charAt(0)) != -1) {
        var j=0, i = str.length;
        while (j < i && whitespace.indexOf(str.charAt(j)) != -1){
            j++;
        }
        str = str.substring(j, i);
    }
    return str;
}

//去掉右边的空白 www.2cto.com
function trimRight(s){
    if(s == null) return "";
    var whitespace = new String(" \t\n\r");
    var str = new String(s);
    if (whitespace.indexOf(str.charAt(str.length-1)) != -1){
        var i = str.length - 1;
        while (i >= 0 && whitespace.indexOf(str.charAt(i)) != -1){
            i--;
        }
        str = str.substring(0, i+1);
    }
    return str;
}


// function Map(){
//  var struct=function(key,value,add){
//   this.key=key;
//   this.value=value;
//  };
//  //添加map键值对
//  var set =function(key,value,add){
//   for(var i=0;i<this.arr.length;i++){
//    if(this.arr[i].key===key){
//        if(typeof(add) == "undefined"){
//         add = false;
//     }
//     if(add){//add=true 追加值
//      this.arr[i].value+=","+value;//有相同的key,这value的值往后最加,用逗号(,)隔开而不是替换原先的值
//     }else{
//      this.arr[i].value=value;//替换原先的值
//     }
//      return;
//    }
//   };
//   this.arr[this.arr.length]=new struct(key,value);
//  };
//  //根据key获取value
//  var get=function(key){
//   for(var i=0;i<this.arr.length;i++){
//    if(this.arr[i].key==key){
//     return this.arr[i].value;
//    }
//   }
//   return null;
//  };
//  //根据key删除
//  var remove=function(key){
//   var v;
//   for(var i=0;i<this.arr.length;i++){
//    v=this.arr.pop();
//    if(v.key==key){
//     continue;
//    }
//    this.arr.unshift(v);
//   }
//  };
//  //获取map键值对个数
//  var size=function(){
//   return this.arr.length;
//  };
//  //判断map是否为空
//  var isEmpty=function(){
//   return this.arr.length<=0;
//  };
//  this.arr=new Array();
//  this.get=get;
//  this.set=set;
//  this.remove=remove;
//  this.size=size;
//  this.isEmpty=isEmpty;
// }