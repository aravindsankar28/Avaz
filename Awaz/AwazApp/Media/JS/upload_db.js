 $(document).ready(function(){            	 
                var file_name = "";
                var uploader = new qq.FileUploader({
                    action: "/ajax-db",
                    element: $('#db-uploader')[0],
                    multiple: true,
                    onComplete: function(id, fileName, responseJSON) {
                        file_name = fileName
                        if(responseJSON.success) {
                        	alert("success");                                          
                        } else {                        
                            alert("upload failed!");
                        }
                    },
                    onAllComplete: function(uploads) {                   
                        // the maps look like this: {file: FileObject, response: JSONServerResponse}                    
                        alert("All complete!");
                                                          
                    },
                    params: {
                        'csrf_token': '{{ csrf_token }}',
                        'csrf_name': 'csrfmiddlewaretoken',
                        'csrf_xname': 'X-CSRFToken',
                    },
                });                                                 
            });