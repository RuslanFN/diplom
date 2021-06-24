function gotopdf(content) {
    var ID = content
    var links = document.getElementsByClassName("URL");
    for(var i = 0; i < links.length; i++){
        var id = $(links[i]).attr('id');
        if(ID == id) {
            var Url = $(links[i]).attr('url');
        }
    }

   $.ajax({
 url: '/pdf',
 type: 'post',
 data: {link:Url},
       success: function(response){
     var res = "/pdfview/" + response;
     document.location.href = res;
 },
 });
}