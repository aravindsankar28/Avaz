            $(document).ready(function(){                  
            
                $("#editsave").click(function(){
                	  var thisobj;
                    var id = getValue();
                    var zname  = $("#ztag_name").attr('value');
                    var audio_data = $("#audio_data").attr('value');
                    var zcolor = $("#selectColor").attr('value');
                    if($("#imageEnable").attr('checked'))
                    	var enable = $("#imageEnable").attr('value');
                    else
                    	var enable =0; 
                    $.ajax(
                    {
                        url:'/editsave/',
                        type:'post',
                        data: {zname:zname,zpk:id,audio_data:audio_data,zcolor:zcolor,enable:enable},        		
                        success: function(response) {
                        
                         alert("Saved successfully");
                                                      
                         objs = jQuery.parseJSON(response) ; 
                         var obj = objs;
                       //  alert(obj[9]);
                         //$('#contentTop').html("<img id = 'currImg' src ='{{MEDIA_URL}}/png/"+obj.zpicture+"' onError='trys(this)'>");
                         $('#contentTop').html("<img id = 'currImg' src ='/media/"+obj[12]+"' onError='errors(this)'>");
                         //$('#contentTop').css('border-color',obj.fields.zcolor);
                         $('#contentTop').css("border-color",obj[9]);
                         if(obj[3] == 0)
                         {                                                	                                            	
                           $('.current').attr('data-enable',0); 
                     
                           }                       
                         else                                                  	 
                         $('.current').attr('data-enable',1);
                         //$('.current').attr('data-color',obj.fields.zcolor);
                         $('.current').attr('data-color',obj[9]);  
                         thisobj = $('.current');
                         var arr =  $('.current').text();
                         //if(obj.fields.zcategory_or_template == "T")
                         if(obj[8] == "T")
                         { 
                         $('.current').html('<a style = "cursor:pointer">'+zname+'</a>');
                         if(obj[3] == 0)
                         {
                         	$('.current').children('a').addClass('black');
                         	
                         }
                         else
                         	$('.current').children('a').removeClass('black');
                         }          
                         else
                         {
                         	$('.current').html('<a style = "cursor:pointer"><b>'+zname+'</b></a>');   
                           $('.current').children('a').addClass("redd"); 
                           if(obj[3] == 0) 
                           	$('.current').children('a').addClass('black');
                           else
                           	$('.current').children('a').removeClass('black');
                           
                           if(obj[11] == 0)
                            {
                            	$('.current').attr('data-color',obj[9]); 
                            	 if(obj[3] == 0) 
										  $('.current').attr('data-enable',0);
										 else
										   $('.current').attr('data-enable',1);                         	
                            }
                           
                         }
                         $(thisobj).children('a').addClass('redd');  
                         $(thisobj).addClass('current');
                                                                                 
                        }			
                    });
                  
                });
            });            
            
             $(document).ready(function(){
                $(".lid").on("click","a",function(event){                               	 
                    $('.redd').each(function() {     
                            	  	
                        $(this).removeClass("redd");
                    });  
                  
                    $('.current').each(function() {                	  	
                        $(this).removeClass("current");
                    });
                          	 	 	
                    $(this).addClass("redd");                    
                    $(this).addClass('current');
                   
                });  
                 
              
            });
$(document).ready(function(){
	
	$("#clearImage").click(function(){
		var zpk = getValue();
		var abcd = deleteTip();
		if(abcd == true)
		{
		$.ajax({
			url:'/clearImage/',
			data:{zpk:zpk},
			type:'get',
			success: function(response) {
				alert(response);
				 $(".current").attr('data-imgsrc',"NONE");          
             $('#contentTop').html("Image not available");
			}
			});
		}
		});
	
	});