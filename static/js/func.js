$(function(){
    $.ajax({
    type:'get',
    url:'get_schedule',
    data:'',
    dataType:'text',
    success:function(msg){
        $("#myDiv").html(msg);
    },
    error:function(){
        $("#myDiv").html("您的浏览器不支持Ajax，本站傲娇了。");
    }
})})

function animedit(aid){
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=function(){
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText == 'ERROR_NOT_LOGIN') {window.location.href = '/login';}
            else if (xmlhttp.responseText == '0') {alert('编辑成功！')}
            else {{alert('编辑失败！')}}
        }}
        xmlhttp.open("GET","/epiedit?epi=" + $("#edit" + aid)[0].value + "&aid=" + aid,true);
        xmlhttp.send();
    }else{
        alert('浏览器版本过低，本站傲娇了。请用IE10以上版本浏览器或者Opera、Chrome等浏览器。')
    }
}

function animeadd(animeid)
{
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=function(){
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText == 'ERROR_NOT_LOGIN') {window.location.href = '/login?aid=' + animeid;}
            else if (xmlhttp.responseText == '0') {alert('添加成功！')}
        }}
        xmlhttp.open("GET","/addanime?aid=" + animeid,true);
        xmlhttp.send();
    }else{
        alert('浏览器版本过低，本站傲娇了。请用IE10以上版本浏览器或者Opera、Chrome等浏览器。')
    }
}

function animedel(animeid)
{
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=function(){
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText == 'ERROR_NOT_LOGIN') {window.location.href = '/login?aid=' + animeid;}
            else if (xmlhttp.responseText == '0') {alert('删除成功！');window.location.reload();}
        }}
        xmlhttp.open("GET","/delanime?aid=" + animeid,false);
        xmlhttp.send();
    }else{
        alert('浏览器版本过低，本站傲娇了。请用IE10以上版本浏览器或者Opera、Chrome等浏览器。')
    }
}

function addhighlight(animeid)
{
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=function(){
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText == 'ERROR_NOT_LOGIN') {window.location.href = '/login';}
            else if (xmlhttp.responseText == '0') {window.top.location.reload();}
            else {alert('傲娇了！添加失败！返回错误：' + xmlhttp.responseText)}
        }}
        xmlhttp.open("GET","/addhighlight?aid=" + animeid,true);
        xmlhttp.send();
    }else{
        alert("浏览器版本过低，本站傲娇了。");
    }
}

function delhighlight(animeid)
{
    var xmlhttp;
    if (window.XMLHttpRequest){
        xmlhttp=new XMLHttpRequest();
        xmlhttp.onreadystatechange=function(){
          if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            if (xmlhttp.responseText == 'ERROR_NOT_LOGIN') {window.location.href = '/login';}
            else if (xmlhttp.responseText == '0') {window.top.location.reload();}
            else {alert('傲娇了！添加失败！返回错误：' + xmlhttp.responseText)}
        }}
        xmlhttp.open("GET","/delhighlight?aid=" + animeid,true);
        xmlhttp.send();
    }else{
        alert("浏览器版本过低，本站傲娇了。");
    }
}