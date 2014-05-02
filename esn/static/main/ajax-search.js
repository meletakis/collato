var pathname = window.location.origin+"/ajax_search/xhr_search"; var request;

$(document).ready(function(){
if((!($("#searchdropdown:hover").length)) && (!($("#ajaxsearch:hover").length))){
 $("#searchdropdown").html('');
  $("#searchdropdown").hide();
 }
/*$("#searchdropdown").blur(function() {
  $("#searchdropdown").html('');
  $("#searchdropdown").hide();

});*/


$("#searchdropdown").hover(function() {
      $("#searchdropdown").stop().show();
  }, function(){
      $("#searchdropdown").html('');
  $("#searchdropdown").stop().hide();
  });
});
        



/*
$(document).ready(function() {
    var $submit = $("#ajaxsearch"),
        $inputs = $('#searchbuttonmain');

    function checkEmpty() {

        // filter over the empty inputs

        return $inputs.filter(function() {
            return !$.trim(this.value);
        }).length === 0;
    }

    $inputs.on('blur', function() {
        $submit.prop("disabled", !checkEmpty());
    }).blur(); // trigger an initial blur
});*/







function ajaxsearch(){
$.post(pathname, { 
    query: $("#ajaxsearch").val()
},
    function(data) {
        $("#searchdropdown").html(data.name);
    }
);
}



$(document).ready(function(){
$("#ajaxsearch").focus(function() {
$(this).data("hasfocus", true);
  
  if ($("#ajaxsearch").val()){
  $("#searchdropdown").show();
 if (request){
request.abort();}
  
  request=  $.post(pathname, { 
    query: $("#ajaxsearch").val() 
},
    function(data) {
        $("#searchdropdown").html(data.name);
    }
);}
});

$("#ajaxsearch").mouseover(function() {
  if ($("#ajaxsearch").val()){
  $("#searchdropdown").show();
 if (request){
request.abort();}
  request=  $.post(pathname, { 
    query: $("#ajaxsearch").val()
},
    function(data) {
        $("#searchdropdown").html(data.name);
    }
);}
});

$("#ajaxsearch").blur(function() {
$(this).data("hasfocus", false);
if (!($("#searchdropdown:hover").length)){
  $("#searchdropdown").html('');
  $("#searchdropdown").hide();
 }
});
});


$(document).ready(function(){
// run every 3s
$("#ajaxsearch").keyup(function() {

 if (request){
request.abort();}
if ($("#ajaxsearch").val()){
  request= $.post(pathname, { 
    query: $("#ajaxsearch").val() 
},
    function(data) {
                $("#searchdropdown").show();
        $("#searchdropdown").html(data.name);
    }
);}
});
});
