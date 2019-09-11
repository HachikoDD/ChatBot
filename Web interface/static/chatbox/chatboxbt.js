window.onscroll = function() {myFunction()};

function myFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    document.getElementById("bt_chatnow").className = "primary-btn chatnowbt_on text-uppercase";
  } else {
    document.getElementById("bt_chatnow").className = "primary-btn chatnowbt_off text-uppercase";
  }
}

function showInfo(type,code){
        window.location.href = "__URL__/show"+type+"/id/"+code;
    }
function  Trim(strValue)
{
    return   strValue.replace(/^s*|s*$/g,"");
}
function SetCookie(sName,sValue)
{
    document.cookie = sName + "=" + escape(sValue);
}
function GetCookie(sName)
{
    var aCookie = document.cookie.split(";");
    for(var　i=0;　i　< aCookie.length;　i++)
    {
        var aCrumb = aCookie[i].split("=");
        if(sName　== Trim(aCrumb[0]))
        {
            return unescape(aCrumb[1]);
        }
    }
    return null;
}
function scrollback()
{
    if(GetCookie("scroll")!=null){document.body.scrollTop=GetCookie("scroll")}
}


function clickLike() {
    alert('Thank you!')
}
