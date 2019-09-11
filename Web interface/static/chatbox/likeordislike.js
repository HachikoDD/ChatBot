function clicklike(transaction){
  layer.tips('Thank you!','#'+ $(transaction).attr('id'), {
      tips: 3
  });
}

function emailIsValid (email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

function clickdislike(transaction){
  layer.prompt({
    title: 'Please Enter your email for further help.',
    shade: 0,
    anim: 2,
    bnt: ['Confrim', 'Cancel'],
    offset:'400px',
  }, function(val, index){
    var question = $(transaction).attr('value');
    var course = $(transaction).attr('course');
    if(emailIsValid(val)){
      $.ajax({
            url: '/leave_message',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (data) {
              if(data == "1"){
                  generateEmailConfrimation();
                  $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                }else{
                  alert("Error, please try again.")
                }
            },
            data: getJson(question, val, course)
        });
        layer.close(index);
    }else{
      alert("Please Enter correct email.");
    }
  });
}

function getJson(question, email, course){
  var json =
    {
        "question": question
        , "email": email
        , "course": course
    };
    return JSON.stringify(json)
}

function generateEmailConfrimation(){
    rawText = 'Thanks for providing your EMAIL to us, the teacher will respond to your email request in the order in which it was received and within 24 hours.'
    var userHtml = '<div class="Block"><div class="botReply"><div class="botText" id="useruserText">' + rawText + '</div></div></div>';
    $("#chatbox").append(userHtml);
}
