var state=new Array();
var tags=['Other', 'Cause-Effect', 'Component-Whole', 'Entity-Destination',
                 'Product-Producer', 'Entity-Origin', 'Member-Collection',
                 'Message-Topic', 'Content-Container', 'Instrument-Agency'];//存储标签tag
var textshow="";
var predicted_data=new Array()
var projectName2id = new Map()
HTMLElement.prototype.__defineGetter__("currentStyle", function () {
return this.ownerDocument.defaultView.getComputedStyle(this, null);
});//获取背景色兼容代码

window.onload=function(){
        var projects_array=new Array()
        xml=createXMLHttpRequest();
        xml.open('POST','get_projects',true);
        xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        xml.send()
        xml.onreadystatechange = function () {     //如果是post,那么里面就设置值
        if (xml.readyState == 4 && xml.status == 200) {
             var projectscontent = xml.responseText
        var projectsJson = eval("(" + projectscontent + ")")
        projects_array=projectsJson.projects
    // projects_array = ["name1","name2"]
        for (var i=0;i<projects_array.length;i++){
            var projects_name = projects_array[i]
            projectName2id.set(projects_name[1],projects_name[0])
            var aText = "<li><a onclick=\"changeproject(this)\">"+projects_name[1]+"</a></li>";
            var Text = document.getElementById("selectproject").innerHTML
            document.getElementById("selectproject").innerHTML=Text+aText;
        }
    }
    }
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
            };
            a1.appendChild(a2);
        }
    }
    }


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
    // tags.splice(index,1);
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
    // tags.splice(index,1);
    a1.removeChild(i);

}

//点击导入
function importClick()
{
    if (clickcount>0)
    $("#files").click();
    else
        alert("请先创建或选择项目")
}

function setTextArea() {
    for (var i=1;i<7;i++) {
        var el = document.getElementById("index"+i);
        var childs
        if (el!=null)
         childs= el.childNodes
        else
            childs=null
        if (childs!=null&&childs.length>0) {
            for (var i = childs.length - 1; i >= 0; i--) {
                el.removeChild(childs[i]);
            }
        }
    }
}

//切换项目
function  changeproject(cp) {
    var vs=cp.innerText
    //var vs = $('#selectproject option:selected').val();
    
    var a=0;
    var submit=0;
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
    a=hasData-submit;
    if(submit<hasData){
        var con=confirm("您还有"+a+"条记录没有标注，确定更换吗？");
        if(con==true){
            setTextArea();
            document.getElementById("dropdown").innerHTML="当前项目："+vs;
            var jsoncontent
        var content
        id=projectName2id.get(vs)
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
                hasData=0
            }else{
                hasData=0
            }

            for(var l=0;l<jsoncontent.data.length;l++){
                var row={id:jsoncontent.data[l].id,text:jsoncontent.data[l].text}
                text_id.push(row)
            }

        var unlabeledDatas = [];
        for (var i=0;i<jsoncontent.data.length;i++) {
            var unlabeledData  = new UnlabeledData(jsoncontent.data[i].id,jsoncontent.data[i].predicted_e1, jsoncontent.data[i].predicted_e1_end,
            jsoncontent.data[i].predicted_e1_start,jsoncontent.data[i].predicted_e2,jsoncontent.data[i].predicted_e2_end,
            jsoncontent.data[i].predicted_e2_start,jsoncontent.data[i].predicted_relation,jsoncontent.data[i].text)
        unlabeledDatas.push(unlabeledData)
            }
        predicted_data = unlabeledDatas

        for (var m = 0; m < jsoncontent.data.length; m++) {
            var a0 = document.getElementById("index" + (m + 1));
            var a1 = document.createElement("div");
            for (var i = 0; i < unlabeledDatas[m].text2String.length;i++) {
                var a2 = document.createElement("span")
                a2.id=m+"text"+i
                a2.onclick = function () {
                        getdetail(this);
                };
                a2.innerText = unlabeledDatas[m].text2String[i]+" ";
                a1.appendChild(a2);
            }
            a0.appendChild(a1);
            hasData++
        }

        for (var i=0;i<hasData;i++) {
            var len=0;
            var buttonNode = document.getElementById("buttons"+i.toString())
            var childNodes = buttonNode.childNodes
            for (var k=0;k<childNodes.length;k++){
                if (childNodes[k].innerText== [i].predicted_relation) {
                    document.getElementById(childNodes[k].id).click()
                }
            }

            if(unlabeledDatas[i].predicted_e1_start==unlabeledDatas[i].predicted_e1_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e1_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e1_start);j<parseInt(unlabeledDatas[i].predicted_e1_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            if(unlabeledDatas[i].predicted_e2_start==unlabeledDatas[i].predicted_e2_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e2_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e2_start);j<parseInt(unlabeledDatas[i].predicted_e2_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
        }
        setButtonState(true)
        }
    }else{
            var jsoncontent
        var content
        document.getElementById("dropdown").innerHTML="当前项目："+vs;
        setTextArea();
            id=projectName2id.get(vs)
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
                hasData=0
            }else{
                hasData=0
            }

            for(var l=0;l<jsoncontent.data.length;l++){
                var row={id:jsoncontent.data[l].id,text:jsoncontent.data[l].text}
                text_id.push(row)
            }

        var unlabeledDatas = [];
        for (var i=0;i<jsoncontent.data.length;i++) {
            var unlabeledData  = new UnlabeledData(jsoncontent.data[i].id,jsoncontent.data[i].predicted_e1, jsoncontent.data[i].predicted_e1_end,
            jsoncontent.data[i].predicted_e1_start,jsoncontent.data[i].predicted_e2,jsoncontent.data[i].predicted_e2_end,
            jsoncontent.data[i].predicted_e2_start,jsoncontent.data[i].predicted_relation,jsoncontent.data[i].text)
        unlabeledDatas.push(unlabeledData)
            }
        predicted_data = unlabeledDatas

        for (var m = 0; m < jsoncontent.data.length; m++) {
            var a0 = document.getElementById("index" + (m + 1));
            var a1 = document.createElement("div");
            for (var i = 0; i < unlabeledDatas[m].text2String.length;i++) {
                var a2 = document.createElement("span")
                a2.id=m+"text"+i
                a2.onclick = function () {
                        getdetail(this);
                };
                a2.innerText = unlabeledDatas[m].text2String[i]+" ";
                a1.appendChild(a2);
            }
            a0.appendChild(a1);
            hasData++
        }

        for (var i=0;i<hasData;i++) {
            var len=0;
            var buttonNode = document.getElementById("buttons"+i.toString())
            var childNodes = buttonNode.childNodes
            for (var k=0;k<childNodes.length;k++){
                if (childNodes[k].innerText==unlabeledDatas[i].predicted_relation) {
                    document.getElementById(childNodes[k].id).click()
                }
            }

            if(unlabeledDatas[i].predicted_e1_start==unlabeledDatas[i].predicted_e1_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e1_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e1_start);j<parseInt(unlabeledDatas[i].predicted_e1_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            if(unlabeledDatas[i].predicted_e2_start==unlabeledDatas[i].predicted_e2_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e2_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e2_start);j<parseInt(unlabeledDatas[i].predicted_e2_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
        }
        setButtonState(true)
    }

}

var clickcount=0//用于判断是否是第一次进入
//新建项目
function newproject() {

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
    a=hasData-submit;
    if(clickcount>0) {
        if (submit < hasData) {
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
    $('#myModal').modal('hide');
    if(temp==true){
        // setButton();
        setButtonState(false);
    }
    // var tags_string = tags.join(",")
     xml=createXMLHttpRequest();
     xml.open('POST','create_project',true);
     xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
     xml.send("projectname="+project_name);
     xml.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if(xml.readyState == 4 && xml.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                console.log("projectname:"+xml.responseText)
                project_info.set(project_name, xml.responseText.substring(31, 33))
                id=xml.responseText.substring(31, 33);

            }
        }
}
//确认标签（更改项目配置
function confirmChangeTags() {
    var a2=document.getElementById("tags1");
    var childs = a2.childNodes;
    for(var i = childs .length - 1; i >= 0; i--) {
        a2.removeChild(childs[i]);
    }
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
        setButtonState(true);
    }
    var projectName = document.getElementById("dropdown").innerHTML
    projectName=projectName.substr(5,projectName.length-1)
    var tags_string = tags.join(",")
    xml_add=createXMLHttpRequest();
     xml_add.open('POST','add_tags_to_project',true);
     xml_add.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
     xml_add.send("project_id="+project_info.get(projectName)+"&tags="+tags_string);
     xml_add.onreadystatechange=function () {//如果是post,那么里面就设置值
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

function cleanTags(self) {
    var change_id = document.getElementById(self.id);
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

//改变点击后标签颜色
function changecolor(self) {
    var mycolor = document.getElementById(self.id);
    var i= self.id.replace(/[^0-9]/ig,"");
    state[i] = !state[i];
        var changecolor_parent = document.getElementById("buttons" + Math.floor(i/tags.length));
        for(var m= (Math.floor(i/tags.length))*10;m<i;m++){
            state[m]=false;
    }
    for(var k=parseInt(i)+1;k<(Math.floor(i/tags.length)+1)*tags.length;k++){
            state[k]=false;
    }
        console.log(Math.floor(i/tags.length))
        var changecolors = changecolor_parent.childNodes;
        console.log(changecolors);
        for (var j=0;j<changecolors.length;j++){
            changecolors[j].style.backgroundColor = "rgb(221,221,221)";

        }
        document.getElementById("choose" + (Math.floor(i / tags.length) + 1)).innerText="选中标签为："

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
var mydata=new Array();
var txtdata
var project2file_id=new Map()
var id
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
            var temp = document.getElementById("dropdown").innerText//获取项目名
            var temp1 = temp.split("：")
            var temp2 = temp1[1]
            console.log(temp)
            id = parseInt(project_info.get(temp2))
            xml = createXMLHttpRequest()
            xml.open('POST', 'upload_file', false);   //这边如果是get请求,可以不填,如果是异步提交也可以不填
            xml.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xml.send("file_name=" + name + "&file_contents=" + txtdata + "&project_id=" + id);                         //这里是请求体,如果是get请求,那么里面设为null.
            //xml.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if (xml.readyState == 4 && xml.status == 200) {     //当xml.readyState == 4的时候,相当于jquery的success页面
                content = xml.responseText
                jsoncontent1 = eval("(" + content + ")");
            }

            var jsoncontent
            var content
            setTextArea();
            xml1 = createXMLHttpRequest()
            xml1.open('POST', 'fetch_unlabeled_data', false);
            xml1.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xml1.send("project_id=" + id + "&num=" + Number(6))
            //xml1.onreadystatechange=function () {     //如果是post,那么里面就设置值
            if (xml1.readyState == 4 && xml1.status == 200) {     //当xml.readyState == 4的时候,相当于jquery的success页面
                console.log("content: " + content)
                content = xml1.responseText
                jsoncontent = eval("(" + content + ")");
                console.log("json: " + jsoncontent.data[0].text)
                hasData=0
            } else {
                hasData = 0
            }

            for (var l = 0; l < jsoncontent.data.length; l++) {
                var row = {id: jsoncontent.data[l].id, text: jsoncontent.data[l].text}
                text_id.push(row)
            }

            var unlabeledDatas = [];
            for (var i = 0; i < jsoncontent.data.length; i++) {
                var unlabeledData = new UnlabeledData(jsoncontent.data[i].id, jsoncontent.data[i].predicted_e1, jsoncontent.data[i].predicted_e1_end,
                    jsoncontent.data[i].predicted_e1_start, jsoncontent.data[i].predicted_e2, jsoncontent.data[i].predicted_e2_end,
                    jsoncontent.data[i].predicted_e2_start, jsoncontent.data[i].predicted_relation, jsoncontent.data[i].text)
                unlabeledDatas.push(unlabeledData)
            }
            predicted_data = unlabeledDatas

            for (var m = 0; m < jsoncontent.data.length; m++) {
                var a0 = document.getElementById("index" + (m + 1));
                var a1 = document.createElement("div");
                for (var i = 0; i < unlabeledDatas[m].text2String.length; i++) {
                    var a2 = document.createElement("span")
                    a2.id = m + "text" + i
                    a2.onclick = function () {
                        getdetail(this);
                    };
                    a2.innerText = unlabeledDatas[m].text2String[i] + " ";
                    a1.appendChild(a2);
                }
                a0.appendChild(a1);
                hasData++
            }

            for (var i = 0; i < hasData; i++) {
                var len=0
                var buttonNode = document.getElementById("buttons" + i.toString())
                var childNodes = buttonNode.childNodes
                for (var k = 0; k < childNodes.length; k++) {
                    if (childNodes[k].innerText == unlabeledDatas[i].predicted_relation) {
                        document.getElementById(childNodes[k].id).click()
                    }
                }

                if(unlabeledDatas[i].predicted_e1_start==unlabeledDatas[i].predicted_e1_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e1_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e1_start);j<parseInt(unlabeledDatas[i].predicted_e1_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            if(unlabeledDatas[i].predicted_e2_start==unlabeledDatas[i].predicted_e2_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e2_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e2_start);j<parseInt(unlabeledDatas[i].predicted_e2_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            }
            setButtonState(true)
        }
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
    if (clickcount>0) {
        xml2 = createXMLHttpRequest()
        xml2.open('POST', 'export_project', false);   //这边如果是get请求,可以不填,如果是异步提交也可以不填
        xml2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xml2.send("project_id=" + id);                         //这里是请求体,如果是get请求,那么里面设为null.
        //xml.onreadystatechange=function () {     //如果是post,那么里面就设置值
        if (xml2.readyState == 4 && xml2.status == 200) {     //当xml.readyState == 4的时候,相当于jquery的success页面
            content = xml2.responseText
            jsoncontent2 = eval("(" + content + ")");
        }
        var tempcon = " ";
        for (var i = 0; i < jsoncontent2.data.length; i++) {
            tempcon = tempcon + "labeled_content:" + jsoncontent2.data[i].labeled_content + ",labeled_relation:" + jsoncontent2.data[i].labeled_relation + "additional_info:" + jsoncontent2.data[i].additional_info + "\r\n"
        }
        print("save")

        var file = new File([tempcon], "data.txt", {type: "text/plain;charset=utf-8"});
        saveAs(file);
    }else
        alert("请先创建或选择项目")
}



var page = 0;
var page1 = 6;
var mydata = new Array();

//初始化按钮状态（颜色 勾选
function setButtonState(checkState) {
    document.getElementById('ok1').checked=checkState;
    document.getElementById('ok2').checked=checkState;
    document.getElementById('ok3').checked=checkState;
    document.getElementById('ok4').checked=checkState;
    document.getElementById('ok5').checked=checkState;
    document.getElementById('ok6').checked=checkState;
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

 function UnlabeledData(pre_id,predicted_e1,predicted_e1_end,predicted_e1_start,predicted_e2,predicted_e2_end,predicted_e2_start,predicted_relation,text){
   var unlabeledData = new Object;
   unlabeledData.pre_id = pre_id;
   unlabeledData.predicted_e1 = predicted_e1;
   unlabeledData.predicted_e1_end = predicted_e1_end;
   unlabeledData.predicted_e1_start = predicted_e1_start;
   unlabeledData.predicted_e2 = predicted_e2;
   unlabeledData.predicted_e2_end = predicted_e2_end;
   unlabeledData.predicted_e2_start = predicted_e2_start;
   unlabeledData.predicted_relation = predicted_relation;
   unlabeledData.text2String = text
   unlabeledData.text = [];
   unlabeledData.text = unlabeledData.text2String.join("").split("")
   return unlabeledData;
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
        setTextArea();
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
                hasData=0
            }

        var unlabeledDatas = [];
        for (var i=0;i<jsoncontent.data.length;i++) {
            var unlabeledData  = new UnlabeledData(jsoncontent.data[i].id,jsoncontent.data[i].predicted_e1, jsoncontent.data[i].predicted_e1_end,
            jsoncontent.data[i].predicted_e1_start,jsoncontent.data[i].predicted_e2,jsoncontent.data[i].predicted_e2_end,
            jsoncontent.data[i].predicted_e2_start,jsoncontent.data[i].predicted_relation,jsoncontent.data[i].text)
        unlabeledDatas.push(unlabeledData)
    }
        predicted_data = unlabeledDatas

        for (var m = 0; m < jsoncontent.data.length; m++) {
            var a0 = document.getElementById("index" + (m + 1));
            var a1 = document.createElement("div");
            for (var i = 0; i < unlabeledDatas[m].text2String.length;i++) {
                var a2 = document.createElement("span")
                a2.id=m+"text"+i
                a2.onclick = function () {
                        getdetail(this);
                };
                a2.innerText = unlabeledDatas[m].text2String[i]+" ";
                a1.appendChild(a2);
            }
            a0.appendChild(a1);
            hasData++
        }

        for (var i=0;i<hasData;i++) {
            var buttonNode = document.getElementById("buttons"+i.toString())
            var childNodes = buttonNode.childNodes
            for (var k=0;k<childNodes.length;k++){
                if (childNodes[k].innerText==unlabeledDatas[i].predicted_relation) {
                    document.getElementById(childNodes[k].id).click()
                }
            }

            if(unlabeledDatas[i].predicted_e1_start==unlabeledDatas[i].predicted_e1_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e1_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e1_start);j<parseInt(unlabeledDatas[i].predicted_e1_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            if(unlabeledDatas[i].predicted_e2_start==unlabeledDatas[i].predicted_e2_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e2_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e2_start);j<parseInt(unlabeledDatas[i].predicted_e2_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            if (unlabeledDatas[i].predicted_e1_start==0){
                    document.getElementById(i+"text"+0).click()
                }
                if (unlabeledDatas[i].predicted_e2_start==0){
                    document.getElementById(i+"text"+0).click()
                }
            var len =unlabeledDatas[i].text2String[0].length
            for (var j=1;j<unlabeledDatas[i].text2String.length;j++) {

                if (len==unlabeledDatas[i].predicted_e1_start){
                    document.getElementById(i+"text"+j).click()
                }
                if (len==unlabeledDatas[i].predicted_e2_start){
                    document.getElementById(i+"text"+j).click()
                }
                 len +=unlabeledDatas[i].text2String[j].length
            }
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

        a = hasData - submit;
        commitDataList = []
        if (submit < hasData) {
            var con = confirm("您还有" + a + "条记录没有标注，确定提交吗？");
            if (con == true) {
                var temp = confirm("你已经提交成功！");

                if (temp == true) {
                    for (var i=0;i<hasData;i++) {
                        var labeled_relation1 = document.getElementById("choose" +(i+1).toString()).innerText.split("：")
                        var labeled_relation = labeled_relation1[1].replace(/\([^\)]*\)/g,"")
                        var labeled_e1,labeled_e2,labeled_e1_start,labeled_e1_end,labeled_e2_start,labeled_e2_end
                        var len=0
                        var pos = 0
                        var isBegin = false
                        var tempcolor = document.getElementById(i+"text0")
                            len += tempcolor.innerText.length
                        if (tempcolor.style.backgroundColor == 'orange') {
                            labeled_e1 = document.getElementById(i+"text0").innerText
                            labeled_e1_start = 0
                            labeled_e1_end =predicted_data[0].predicted_e1_end
                            isBegin = true
                        }
                        for (var j = 1; j < predicted_data[i].text2String.length; j++) {
                            if (isBegin){
                                pos=1
                                break
                            }
                        var color = document.getElementById(i+"text" + j)
                            len += color.innerText.length
                        if (color.style.backgroundColor == 'orange') {
                            labeled_e1 = document.getElementById(i+"text" + j).innerText
                            labeled_e1_start = predicted_data[i].predicted_e1_start
                            labeled_e1_end = predicted_data[i].predicted_e1_end
                            pos = j++
                            break
                        }
                        }
                       for (var j = pos; j < predicted_data[i].text2String.length; j++) {
                        var color = document.getElementById(i+"text" + j)
                            len += color.innerText.length
                        if (color.style.backgroundColor == 'orange') {
                            labeled_e2 = document.getElementById(i+"text" + j).innerText
                            labeled_e2_start = predicted_data[i].predicted_e2_start
                            labeled_e2_end = predicted_data[i].predicted_e2_end
                            break
                        }
                    }
                        var labeled_data=new LabeledData(predicted_data[i].text2String,predicted_data[i].predicted_relation,predicted_data[i].predicted_e1,predicted_data[i].predicted_e2,
                           predicted_data[i].predicted_e1_start,predicted_data[i].predicted_e1_end,predicted_data[i].predicted_e2_start,predicted_data[i].predicted_e2_end,
                           labeled_relation,labeled_e1,labeled_e2,labeled_e1_start,labeled_e1_end,labeled_e2_start,labeled_e2_end,"")
                        commitDataList.push(labeled_data)
                    }
                }
            }
        }else{
           for (var i=0;i<hasData;i++) {
                        var labeled_relation1 = document.getElementById("choose" +(i+1).toString()).innerText.split("：")
                        var labeled_relation = labeled_relation1[1].replace(/\([^\)]*\)/g,"")
                        var labeled_e1,labeled_e2,labeled_e1_start,labeled_e1_end,labeled_e2_start,labeled_e2_end
                        var len=0
                        var pos = 0
                        var isBegin = false
                        var tempcolor = document.getElementById(i+"text0")
                            len += tempcolor.innerText.length
                        if (tempcolor.style.backgroundColor == 'orange') {
                            labeled_e1 = document.getElementById(i+"text0").innerText
                            labeled_e1_start = 0
                            labeled_e1_end =predicted_data[0].predicted_e1_end
                            isBegin = true
                        }
                        for (var j = 1; j < predicted_data[i].text2String.length; j++) {
                            if (isBegin){
                                pos=1
                                break
                            }
                        var color = document.getElementById(i+"text" + j)
                            len += color.innerText.length
                        if (color.style.backgroundColor == 'orange') {
                            labeled_e1 = document.getElementById(i+"text" + j).innerText
                            labeled_e1_start = predicted_data[i].predicted_e1_start
                            labeled_e1_end = predicted_data[i].predicted_e1_end
                            pos = j++
                            break
                        }
                        }
                       for (var j = pos; j < predicted_data[i].text2String.length; j++) {
                        var color = document.getElementById(i+"text" + j)
                            len += color.innerText.length
                        if (color.style.backgroundColor == 'orange') {
                            labeled_e2 = document.getElementById(i+"text" + j).innerText
                            labeled_e2_start = predicted_data[i].predicted_e2_start
                            labeled_e2_end = predicted_data[i].predicted_e2_end
                            break
                        }
                    }
                        var labeled_data=new LabeledData(predicted_data[i].text2String,predicted_data[i].pre_id,predicted_data[i].predicted_relation,predicted_data[i].predicted_e1,predicted_data[i].predicted_e2,
                           predicted_data[i].predicted_e1_start,predicted_data[i].predicted_e1_end,predicted_data[i].predicted_e2_start,predicted_data[i].predicted_e2_end,
                           labeled_relation,labeled_e1,labeled_e2,labeled_e1_start,labeled_e1_end,labeled_e2_start,labeled_e2_end,"")
                        commitDataList.push(labeled_data)
                    }
        }
                    xml2 = createXMLHttpRequest()
                    xml2.open('POST', 'commit_label_data', false);
                    xml2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xml2.send("project_id=" + id +"&text0="+JSON.stringify( commitDataList[0].text )+ "&id0="+commitDataList[0].pre_id+"&predicted_relation0=" + commitDataList[0].predicted_relation+"&predicted0_e1="+commitDataList[0].predicted_e1+"&predicted0_e2="+commitDataList[0].predicted_e2
                    +"&predicted_e1_start0=" + commitDataList[0].predicted_e1_start+"&predicted_e1_end0=" + commitDataList[0].predicted_e1_end+"&predicted_e2_start0=" + commitDataList[0].predicted_e2_start+"&predicted_e2_end0=" + commitDataList[0].predicted_e2_end
                        +"&labeled_relation0=" + commitDataList[0].labeled_relation+"&labeled0_e1="+commitDataList[0].labeled_e1+"&labeled0_e2="+commitDataList[0].labeled_e2
                    +"&labeled_e1_start0=" + commitDataList[0].labeled_e1_start+"&labeled_e1_end0=" + commitDataList[0].labeled_e1_end+"&labeled_e2_start0=" + commitDataList[0].labeled_e2_start+"&labeled_e2_end0=" + commitDataList[0].labeled_e2_end
                    +"&text1="+JSON.stringify( commitDataList[1].text )+ "&id1="+commitDataList[1].pre_id+ "&predicted_relation1=" + commitDataList[1].predicted_relation+"&predicted1_e1="+commitDataList[1].predicted_e1+"&predicted1_e2="+commitDataList[1].predicted_e2
                    +"&predicted_e1_start1=" + commitDataList[1].predicted_e1_start+"&predicted_e1_end1=" + commitDataList[1].predicted_e1_end+"&predicted_e2_start1=" + commitDataList[1].predicted_e2_start+"&predicted_e2_end1=" + commitDataList[1].predicted_e2_end
                    +"&labeled_relation1=" + commitDataList[1].labeled_relation+"&labeled1_e1="+commitDataList[1].labeled_e1+"&labeled1_e2="+commitDataList[1].labeled_e2
                    +"&labeled_e1_start1=" + commitDataList[1].labeled_e1_start+"&labeled_e1_end1=" + commitDataList[1].labeled_e1_end+"&labeled_e2_start1=" + commitDataList[1].labeled_e2_start+"&labeled_e2_end1=" + commitDataList[1].labeled_e2_end
                        +"&text2="+JSON.stringify( commitDataList[2].text )+ "&id2="+commitDataList[2].pre_id+ "&predicted_relation2=" + commitDataList[2].predicted_relation+"&predicted2_e1="+commitDataList[2].predicted_e1+"&predicted2_e2="+commitDataList[2].predicted_e2
                    +"&predicted_e1_start2=" + commitDataList[2].predicted_e1_start+"&predicted_e1_end2=" + commitDataList[2].predicted_e1_end+"&predicted_e2_start2=" + commitDataList[2].predicted_e2_start+"&predicted_e2_end2=" + commitDataList[2].predicted_e2_end
                    +"&labeled_relation2=" + commitDataList[2].labeled_relation+"&labeled2_e1="+commitDataList[2].labeled_e1+"&labeled2_e2="+commitDataList[2].labeled_e2
                    +"&labeled_e1_start2=" + commitDataList[2].labeled_e1_start+"&labeled_e1_end2=" + commitDataList[2].labeled_e1_end+"&labeled_e2_start2=" + commitDataList[2].labeled_e2_start+"&labeled_e2_end2=" + commitDataList[2].labeled_e2_end
                        +"&text3="+JSON.stringify( commitDataList[3].text )+ "&id3="+commitDataList[3].pre_id+ "&predicted_relation3=" + commitDataList[3].predicted_relation+"&predicted3_e1="+commitDataList[3].predicted_e1+"&predicted3_e2="+commitDataList[3].predicted_e2
                    +"&predicted_e1_start3=" + commitDataList[3].predicted_e1_start+"&predicted_e1_end3=" + commitDataList[3].predicted_e1_end+"&predicted_e2_start3=" + commitDataList[3].predicted_e2_start+"&predicted_e2_end3=" + commitDataList[3].predicted_e2_end
                    +"&labeled_relation3=" + commitDataList[3].labeled_relation+"&labeled3_e1="+commitDataList[3].labeled_e1+"&labeled3_e2="+commitDataList[3].labeled_e2
                    +"&labeled_e1_start3=" + commitDataList[3].labeled_e1_start+"&labeled_e1_end3=" + commitDataList[3].labeled_e1_end+"&labeled_e2_start3=" + commitDataList[3].labeled_e2_start+"&labeled_e2_end3=" + commitDataList[3].labeled_e2_end
                        +"&text4="+JSON.stringify( commitDataList[4].text )+ "&id4="+commitDataList[4].pre_id+ "&predicted_relation4=" + commitDataList[4].predicted_relation+"&predicted4_e1="+commitDataList[4].predicted_e1+"&predicted4_e2="+commitDataList[4].predicted_e2
                    +"&predicted_e1_start4=" + commitDataList[4].predicted_e1_start+"&predicted_e1_end4=" + commitDataList[4].predicted_e1_end+"&predicted_e2_start4=" + commitDataList[4].predicted_e2_start+"&predicted_e2_end4=" + commitDataList[4].predicted_e2_end
                    +"&labeled_relation4=" + commitDataList[4].labeled_relation+"&labeled4_e1="+commitDataList[4].labeled_e1+"&labeled4_e2="+commitDataList[4].labeled_e2
                    +"&labeled_e1_start4=" + commitDataList[4].labeled_e1_start+"&labeled_e1_end4=" + commitDataList[4].labeled_e1_end+"&labeled_e2_start4=" + commitDataList[4].labeled_e2_start+"&labeled_e2_end4=" + commitDataList[4].labeled_e2_end
                        +"&text5="+JSON.stringify( commitDataList[5].text )+ "&id5="+commitDataList[5].pre_id+ "&predicted_relation5=" + commitDataList[5].predicted_relation+"&predicted5_e1="+commitDataList[5].predicted_e1+"&predicted5_e2="+commitDataList[5].predicted_e2
                    +"&predicted_e1_start5=" + commitDataList[5].predicted_e1_start+"&predicted_e1_end5=" + commitDataList[5].predicted_e1_end+"&predicted_e2_start5=" + commitDataList[5].predicted_e2_start+"&predicted_e2_end5=" + commitDataList[5].predicted_e2_end
                    +"&labeled_relation5=" + commitDataList[5].labeled_relation+"&labeled5_e1="+commitDataList[5].labeled_e1+"&labeled5_e2="+commitDataList[5].labeled_e2
                    +"&labeled_e1_start5=" + commitDataList[5].labeled_e1_start+"&labeled_e1_end5=" + commitDataList[5].labeled_e1_end+"&labeled_e2_start5=" + commitDataList[5].labeled_e2_start+"&labeled_e2_end5=" + commitDataList[5].labeled_e2_end
                    )
                        if(xml2.readyState == 4 && xml2.status==200){     //当xml.readyState == 4的时候,相当于jquery的success页面
                            console.log("content: "+content)
                         }
                    hasData=0
                    initButton()
                    setButtonState(true);
                    updata_progress();
                    console.log("commit_label_data");
        submit = 0;

        var jsoncontent
        var content
        setTextArea();
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
                hasData=0
            }else{
                hasData=0
            }

            for(var l=0;l<jsoncontent.data.length;l++){
                var row={id:jsoncontent.data[l].id,text:jsoncontent.data[l].text}
                text_id.push(row)
            }

        var unlabeledDatas = [];
        for (var i=0;i<jsoncontent.data.length;i++) {
            var unlabeledData  = new UnlabeledData(jsoncontent.data[i].id,jsoncontent.data[i].predicted_e1, jsoncontent.data[i].predicted_e1_end,
            jsoncontent.data[i].predicted_e1_start,jsoncontent.data[i].predicted_e2,jsoncontent.data[i].predicted_e2_end,
            jsoncontent.data[i].predicted_e2_start,jsoncontent.data[i].predicted_relation,jsoncontent.data[i].text)
        unlabeledDatas.push(unlabeledData)
            }
        predicted_data = unlabeledDatas

        for (var m = 0; m < jsoncontent.data.length; m++) {
            var a0 = document.getElementById("index" + (m + 1));
            var a1 = document.createElement("div");
            for (var i = 0; i < unlabeledDatas[m].text2String.length;i++) {
                var a2 = document.createElement("span")
                a2.id=m+"text"+i
                a2.onclick = function () {
                        getdetail(this);
                };
                a2.innerText = unlabeledDatas[m].text2String[i]+" ";
                a1.appendChild(a2);
            }
            a0.appendChild(a1);
            hasData++
        }

        for (var i=0;i<hasData;i++) {
            var len=0;
            var buttonNode = document.getElementById("buttons"+i.toString())
            var childNodes = buttonNode.childNodes
            for (var k=0;k<childNodes.length;k++){
                if (childNodes[k].innerText==unlabeledDatas[i].predicted_relation) {
                    document.getElementById(childNodes[k].id).click()
                }
            }
            if(unlabeledDatas[i].predicted_e1_start==unlabeledDatas[i].predicted_e1_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e1_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e1_start);j<parseInt(unlabeledDatas[i].predicted_e1_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
            if(unlabeledDatas[i].predicted_e2_start==unlabeledDatas[i].predicted_e2_end)
                document.getElementById(i+"text"+unlabeledDatas[i].predicted_e2_start).click()
            else {
                for (var j=parseInt(unlabeledDatas[i].predicted_e2_start);j<parseInt(unlabeledDatas[i].predicted_e2_end);j++) {
                    document.getElementById(i+"text"+j).click()
                }
            }
        }
        setButtonState(true)

    }

    function LabeledData(text,pre_id,predicted_relation,predicted_e1,predicted_e2,predicted_e1_start,predicted_e1_end,predicted_e2_start,predicted_e2_end,
                         labeled_relation,labeled_e1,labeled_e2,labeled_e1_start,labeled_e1_end,labeled_e2_start,labeled_e2_end,additional_info){
   var labeledData = new Object;
   labeledData.pre_id = pre_id;
   labeledData.predicted_e1 = predicted_e1;
   labeledData.predicted_e1_end = predicted_e1_end;
   labeledData.predicted_e1_start = predicted_e1_start;
   labeledData.predicted_e2 = predicted_e2;
   labeledData.predicted_e2_end = predicted_e2_end;
   labeledData.predicted_e2_start = predicted_e2_start;
   labeledData.predicted_relation = predicted_relation;
   labeledData.text = text;
   labeledData.labeled_relation=labeled_relation;
   labeledData.labeled_e1=labeled_e1;
   labeledData.labeled_e2=labeled_e2;
   labeledData.labeled_e1_start=labeled_e1_start;
   labeledData.labeled_e1_end=labeled_e1_end;
   labeledData.labeled_e2_start=labeled_e2_start;
   labeledData.labeled_e2_end=labeled_e2_end;
   labeledData.additional_info=additional_info;
   return labeledData;
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
