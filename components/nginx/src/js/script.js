$("form#post_message_form").submit(function(e){
  e.preventDefault();
  var data = {}
  var Form = this;
  $.each(this.elements, function(i, v){
    var input = $(v);
    data[input.attr("name")] = input.val();
    delete data["undefined"];
  });
  $.ajax({
    cache: false,
    url : "/post_message",
    type: "POST",
    dataType : "json",
    data : JSON.stringify(data),
    context : Form,
    success : function(callback){
      console.log(JSON.parse(callback));
      $(this).html("Success!");
    },
    error : function(){
      $(this).html("Error!");
    }
  });
