var editor = null;

function UpdateStatus(){
      var question_id = document.getElementById("question_id");
      var question_content = document.getElementById("question_content");
       $.ajax({
             url: '/answer',
             type: 'post',
             dataType: 'json',
             contentType: 'application/json',
             beforeSend:function(XMLHttpRequest){
                document.getElementById('loading').innerHTML = '<i class="fa fa-spinner fa-spin"></i>  Loading';
                document.getElementById('loading').setAttribute("disabled", "true");
     	       },
             success: function (data) {
              //  $("#loading").empty();
               if(data == "1"){
                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                 }else{
                   alert("Error, please try again.");
                 }
             },
             data: getJson(question_id.innerHTML, editor.txt.html())
         });

}

function getJson(question_id, question_content){
  var json =
    {
        "question_id": question_id
        , "answer": question_content
    };
    return JSON.stringify(json)
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}
