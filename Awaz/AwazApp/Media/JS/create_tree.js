 $(document).ready(function(){
 					 
              
                $(".lid").on("click",".parent",function(event){   
                    var x= $(this).attr('data-val');
                   
                    $.ajax({
                    		async: false, 
                        url: "/getChildren/"+x+"/",
                        type: "get", 			
                        success: function(response) {
             					 //alert(response);
             					 if (response != "NO")
             					 {
                            var y =jQuery.parseJSON(response) ;
                          //  alert(y[0][0]);
                            if($("#"+x).children(':visible').length == 0)
                            { 
                                var check ;
                                if($("#"+x).children(':visible').length == 0)
                                    check = 0;
                                else check = 1;
                                if(check == 0)  
                                {
                                      
                                    $("#"+x).children().show();
                                     //alert( $("#"+x).children('a').attr('title'));
                                 //   alert($(this).attr("title"));
                                     $(".redd").children('.folder').attr("src","/media/Images/minus.gif");
                                    if($("#"+x).children(':visible').length >0)
                                        check = 1;
                                }
                                for (var i = 0;i < y.length; ++i)
                                {
                                	
                                  //  var a = y[i].fields.ztag_name;
                                    var a = y[i][13];
                                    //console.log(y[i].fields.ztag_name);
                                    console.log(y[i][13]);   
                                    if(check == 0)
                                    {
                                    	 //if(y[i].fields.zcategory_or_template == "D")
                                    	 if(y[i][8] == "D")
                                    	 {
                                    	 	//if(y[i].fields.zis_enabled == 1)
                                    	 	if(y[i][3] == 1)
                                    	 	$("#"+x).append('<li class ="imgs" data-name = "'+y[i][13]+'" data-color = "'+y[i][9]+'" data-imgsrc="'+y[i][12]+'" data-enable="'+y[i][3]+'" data-val = "'+y[i][0]+'"><a style="cursor:pointer"><b>'+a+'</b></a></li>');
                                        	//$("#"+x).append('<li class ="imgs" data-name = "'+y[i].fields.ztag_name+'" data-color = "'+y[i].fields.zcolor+'" data-imgsrc="'+y[i].fields.zpicture+'" data-enable="'+y[i].fields.zis_enabled+'" data-val = "'+y[i].pk+'"><a style="cursor:pointer"><b>'+a+'</b></a></li>');
                                        	else
                                        	$("#"+x).append('<li class ="imgs" data-name = "'+y[i][13]+'" data-color = "'+y[i][9]+'" data-imgsrc="'+y[i][12]+'" data-enable="'+y[i][3]+'" data-val = "'+y[i][0]+'"><a style="cursor:pointer" class = "black"><b>'+a+'</b></a></li>');
                                        	//$("#"+x).append('<li class ="imgs" data-name = "'+y[i].fields.ztag_name+'" data-color = "'+y[i].fields.zcolor+'" data-imgsrc="'+y[i].fields.zpicture+'" data-enable="'+y[i].fields.zis_enabled+'" data-val = "'+y[i].pk+'"><a style="cursor:pointer" class = "black"><b>'+a+'</b></a></li>');
													 }                                        
                                        else
                                        {
                                        	//if(y[i].fields.zis_enabled == 1)
                                        	if(y[i][3] == 1)
                                        	$("#"+x).append('<li class ="imgs" data-name = "'+y[i][13]+'" data-color = "'+y[i][9]+'" data-imgsrc="'+y[i][12]+'" data-enable="'+y[i][3]+'" data-val = "'+y[i][0]+'"><a style="cursor:pointer">'+a+'</a></li>');
                                        	//$("#"+x).append('<li class ="imgs" data-name = "'+y[i].fields.ztag_name+'" data-color = "'+y[i].fields.zcolor+'" data-imgsrc="'+y[i].fields.zpicture+'" data-enable="'+y[i].fields.zis_enabled+'" data-val = "'+y[i].pk+'"><a style="cursor:pointer">'+a+'</a></li>');
													   else
													   $("#"+x).append('<li class ="imgs" data-name = "'+y[i][13]+'" data-color = "'+y[i][9]+'" data-imgsrc="'+y[i][12]+'" data-enable="'+y[i][3]+'" data-val = "'+y[i][0]+'"><a style="cursor:pointer" class = "black">'+a+'</a></li>');
													   //$("#"+x).append('<li class ="imgs" data-name = "'+y[i].fields.ztag_name+'" data-color = "'+y[i].fields.zcolor+'" data-imgsrc="'+y[i].fields.zpicture+'" data-enable="'+y[i].fields.zis_enabled+'" data-val = "'+y[i].pk+'"><a style="cursor:pointer" class = "black">'+a+'</a></li>');
													 }												
												} 
												if(y[i][8] == "D" && check == 0)                                   
                                    //if(y[i].fields.zcategory_or_template == "D" && check == 0)
                                    {
                                       
                                        $("#"+x).append('<a href = "" class="parent" data-val = "'+y[i][0]+'" ><img src="/media/Images/folder.gif"><img src="/media/Images/plus.gif" class = "folder"></a>');	
                                        $("#"+x).append('<ul class="parent" id=  "'+y[i][0]+'"></ul>');	
                                        //$("#folder").attr("src","{{MEDIA_URL}}/Images/minus.gif");
                                    }												
                                }
                                 
                                 
                            }
                            else
                            {
                                
                                $("#"+x).children().hide();
                                $("#content").html("");
                                $(".folder").attr("src","/media/Images/plus.gif");
											$("#contentTop").html("");                               
                                //$("#"+x).css("display","block");
                            } 
                        }
                     }
                    });   	 
                    event.preventDefault();   
                });
                $(".lid").on("click",".imgs",function(event){ 	
                	  $('.redd').each(function() {                	  	
						   $(this).removeClass("redd");
                	  	  });
                	  	  
                	  	  $('.current').each(function() {                	  	
						  	 $(".current").removeClass("current");  
                	  	  });				
                	     
                    var x = $(this).attr('data-imgsrc');
                    var y = $(this).attr('data-val');
                    var l = $(this).attr('data-enable');
                    var m = $(this).attr('data-color');
                    var z = $(this).attr('data-name');
                    $(this).addClass("current");
                    $(this).children('a').addClass("redd");					 				               
                    func(x,y,l,m);
                });
            });
