        $(document).ready(function(){
                var file_name = "";
        			 var uploader = new qq.FileUploader({
                action: "/ajax-upload",
                element: $('#file-uploader')[0],
                multiple: true,
                onComplete: function(id, fileName, responseJSON) {
                	  file_name = fileName
                    if(responseJSON.success) {
                        //alert("success!");
                    } else {
                        alert("upload failed!");
                    }
                },
                onAllComplete: function(uploads) {
                    // uploads is an array of maps
                    // the maps look like this: {file: FileObject, response: JSONServerResponse}
                    
                    alert("All complete!");
                    var zpk = getValue();        
                    alert(file_name);  
                     $.ajax({
						   
                        url:'/upload/',
                        type:'get',
                        data:{file_name:file_name,zpk:zpk},                              		
                        success: function(response) { 
                        alert(response);   
                        $(".current").attr('data-imgsrc',response);          
                        $('#contentTop').html("<img id = 'currImg' src ='{{MEDIA_URL}}/png/"+response+"' >");                     
                        }
                        });                    
                },
                params: {
                    'csrf_token': '{{ csrf_token }}',
                    'csrf_name': 'csrfmiddlewaretoken',
                    'csrf_xname': 'X-CSRFToken',
                },
            });                                        
        
        });
