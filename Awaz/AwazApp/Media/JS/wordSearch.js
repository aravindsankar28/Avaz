 var y ;
 var prev = 0;
            var r;
            var n;
            function getParent(x)
            {
                var obj = null;
                $.ajax(
                {					
                    url:'/getParent/',
                    type:'get',
                    data: {x:x},    
                    async: false,                           		
                    success: function(response) {
                        obj = jQuery.parseJSON(response) ;                                          
                
                    }
                								
                }).responseText ;			
                return obj;
            }
            function change_display(i)
            {
                if(i>= n)
                {
                    alert("No more");
                    return 0;
                }
                var z =  $(".lid").find("[data-val='" + y[i].pk+ "']");    
              
                if(z[0] == undefined || $(z[0]).is(':visible') == false)
                {
                    var parents = new Array();
                    var index = 0;
                   // var parent = getParent(y[i].fields.zparent_id);
                    var parent = getParent(y[i][11])
                    parents[index] = parent;
                    index = index + 1;
                    while( $(".lid").find("[data-val='" + parent[0][0]+ "']")[0] == undefined | $($(".lid").find("[data-val='" + parent[0][0]+ "']")[0]).is(':visible') == false )
                    //while( $(".lid").find("[data-val='" + parent[0].pk+ "']")[0] == undefined | $($(".lid").find("[data-val='" + parent[0].pk+ "']")[0]).is(':visible') == false )
                    {
                        //parent = getParent(parent[0].fields.zparent_id);
                        parent = getParent(parent[0][11]);
                        parents[index] = parent;
                        index = index +1;
                    }
                    var N = parents.length;
                    var j = N-1;
                    while(j>=0)
                    {	               	
                        //var a =  $(".lid").find("[data-val='" + parents[j][0].pk+ "']");
                        var a =  $(".lid").find("[data-val='" + parents[j][0][0]+ "']");
                        //console.log(parents[j][0].fields.ztag_name)
                        console.log(parents[j][0][13])
                        if(parents[j][0][11] == 0)
                        //if(parents[j][0].fields.zparent_id == 0)
                            $(a).trigger('click');
                        else           
                            $(a[1]).trigger('click');
                        j = j - 1;		
                    }               
                }      
              //  z =  $(".lid").find("[data-val='" + y[i].pk+ "']"); 
                z =  $(".lid").find("[data-val='" + y[i][0]+ "']"); 
                var x = z[0];         
                // change current class and redd class so as to display                                     
                $('.redd').each(function() {     
                            	  	
                    $(this).removeClass("redd");
                });  
                  
                $('.current').each(function() {                	  	
                    $(this).removeClass("current");
                });                            
                            
                $(x).addClass('current');
                                       
                $(x).trigger('click');
                $(z[1]).trigger('click');  
                var yz = $(x).attr('data-name');
                
                var wxyz = $(x).position().top;
               
                //alert(wxyz);                                 
                $("#leftContentTop").scrollTop(wxyz);
                prev = wxyz; 
                $(x).children('a').addClass('redd');
                if(y[i][11] == 0)
                //if(y[i].fields.zparent_id == 0)
                {
                
                    $(x).prev().addClass('redd');
                    $(x).prev().trigger('click');   
                }
            }
            $(document).ready(function(){
		  		
                $("#word_button").click(function(){				  	   
                    var search = $("#search_word").attr('value');
                    $.ajax(		   
                    {
							   
                        url:'/word/',
                        type:'get',
                        data: {search:search},                              		
                        success: function(response) { 
                            y = jQuery.parseJSON(response) ;
                            n = y.length;
                            var j = 0;     
                            r = response;                               	
                            change_display(j);
                                          
                           
                            //document.getElementById('leftContentTop').scrollTop = wxyz.offsetTop;
                            $("#next").click(function(){
                                j = j+1;
                                change_display(j);
                            });
                            $("#prev").click(function(){
                                j = j-1;
                                change_display(j);
                            });
                        }
                    });		   
                });
		   
            });