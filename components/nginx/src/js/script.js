$( document ).ready(function() {
    $("form#new_sentence_form").submit(function(e){
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
	    url : "/sentences",
	    type: "POST",
	    dataType : "json",
	    contentType: "application/json",
	    data : JSON.stringify(data),
	    context : Form,
	    success : function(callback){
	    },
	    error : function(){
		$(this).html("Error!");
	    }
	});
    });

    $("form#get_sentences_form").submit(function(e){
	e.preventDefault();
	var data = {}
	var Form = this;
	$.each(this.elements, function(i, v){
	    var input = $(v);
	    data[input.attr("name")] = input.val();
	    delete data["undefined"];
	});
	var language = data["language"];
	$.ajax({
	    cache: false,
	    url : "/sentences?language=" + language,
	    type: "GET",
	    dataType : "json",
	    context : Form,
	    success : function(sentences){
		$("#sentences").empty();
		for(var i = 0; i < sentences.length; i++) {
		    var text = sentences[i].time + " / " + sentences[i].author + ": " +
			sentences[i].text;
		    $("#sentences").append("<p>" + text + "</p>");
		}
	    },
	    error : function(){
		$(this).html("Error!");
	    }
	});
    });
});
