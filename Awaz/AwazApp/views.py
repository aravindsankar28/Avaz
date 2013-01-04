from django.views.generic.list_detail import object_list
from django.shortcuts import *
from forms import *
from models import *
from django.core.serializers import serialize
from django.core import serializers
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import sha, random,datetime
from ajaxuploader.views import AjaxFileUploader
from django.middleware.csrf import get_token
import string,StringIO
from xlwt import *
from settings import *
import sys,os,simplejson
from struct import pack,unpack
from django.template.loader import render_to_string
import ho.pisa as pisa
import tarfile,urllib2,zipfile,shutil
from django.contrib import auth
from django.core.exceptions import PermissionDenied
import sqlite3 as lite

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
paths = []
dirpaths = []
relativedirpath = []

def setrelative(path):
	global relativedirpath
	relativedirpath = path
	
def getrelative():
	global relativedirpath
	return str(relativedirpath[6:]+'/')
	
def setpaths(path):
	global paths
	paths = path

def getpaths():
	global paths
	print paths
	return paths	
	
def setdirpaths(path):
	global dirpaths
	dirpaths = path

def getdirpaths():
	global dirpaths
	print dirpaths
	return dirpaths
	
	
#Done
'''
This view is for the home page the user goes to, after selecting a dictionary from his list of dictionaries.
Here a connection is established with sq lite database corresponding to that dictionary,and all records    ,
which are the base categories,are retrieved.
'''		
def home(request,foobar):
	if not request.user.is_authenticated() or request.session['logged_in'] == False:
		raise PermissionDenied()
	con = None
	user = request.user
	try:
		ud = UserDictionary.objects.filter(zdictid = foobar)
	except:
		ud = None
	d = Dictionary.objects.get(id = foobar)
	if ud is None:
		raise PermissionDenied()
	path = os.path.join(os.path.dirname(__file__),d.zpath)
	dpath = os.path.join(os.path.dirname(__file__),d.zdir_path)
	con = lite.connect(path)
	setpaths(path)
	setdirpaths(dpath)
	setrelative(d.zdir_path+'custom_images')
	z = getpaths()
	objs = []	
	cur = con.cursor() 
	cur.execute('SELECT * FROM ZPICMODEDICT WHERE ZPARENT_ID = 0 ORDER BY ZSERIAL')
	objss = cur.fetchall()
	objs = []
	for o in objss:
		ol = list(o)
		if ol[12][:3] == "ci_":
			ol[12] = str(getrelative())+ol[12]
		else:
			ol[12] = "png/"+ol[12]
		objs.append(ol)
	con.close()			
	#objectlist = Zpicmodedict.objects.filter(zparent_id = 0).order_by('zserial')
	csrf_token = get_token(request)
	return render_to_response('Home.html', locals(), context_instance = RequestContext(request))


'''
This view gets an ajax call from the home page to get the children of one specific 
template/category.The variable foobar is the pk of that template/category,for which
we need to get the children. It goes through the sqlite database of the dictionary
and returns all elements which have their zparent_id attribute as the zidentifier 
of the item. Then, the records are serialized to json format and returned back to 
the template which did the ajax call.   
'''
#Done
def getChildren(request,foobar):
	if request.is_ajax():
		if foobar == "undefined":
			return HttpResponse("NO")
		#obj = Zpicmodedict.objects.get(z_pk = foobar)
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		cur.execute('SELECT * FROM ZPICMODEDICT WHERE Z_PK = '+foobar+';')
		obj = cur.fetchone()
		x = str(obj[10])
		query = "SELECT * FROM ZPICMODEDICT WHERE ZPARENT_ID = '"+x+"' ORDER BY ZSERIAL"
		#return HttpResponse(query)
		try:
			cur.execute(query)
		except:
			return HttpResponse("NO")
		objss = cur.fetchall()

		objs = []
		for o in objss:
			ol = list(o)
			print o[12]
			if ol[12][:3] == 'ci_':
				ol[12] = str(getrelative())+ str(ol[12])
			else:
				ol[12] = "png/"+ str(ol[12])
			objs.append(ol)
		con.close()		
		#try:
		#	objs = list(Zpicmodedict.objects.filter(zparent_id = obj.zidentifier).order_by('zserial'))
		#except Zpicmodedict.DoesNotExist:
		#	objs = None
		#json = serializers.serialize("json",objs)				
		json1 = simplejson.dumps(objs)    	
    	return HttpResponse(json1)
	try:
		obj = Zpicmodedict.objects.get(z_pk = foobar)
	except Zpicmodedict.DoesNotExist:
		obj = None
	try:
		objs = Zpicmodedict.objects.filter(zparent_id = obj.zidentifier)
	except Zpicmodedict.DoesNotExist:
		objs = None
	return render_to_response('Children.html', locals(), context_instance = RequestContext(request))

'''
This view is a function to clear the image for a particular category/template. It sets the
zpicture attribute of that object to string "NONE" and not python None.It doesnt remove the 
image from the directory, but only modifies the zpicture attribute. The parameter foobar,
which is passed to this url via a get ajax call is the pk of that item. After commiting the
changes to the database,it returns a success message back to the template.
'''

#Done	
def clearImage(request):
	if request.is_ajax():
		foobar = request.GET['zpk']
		paths = getpaths()
		con = lite.connect(paths)
		cur = con.cursor()
		query1 = "SELECT * FROM ZPICMODEDICT WHERE Z_PK = "+str(foobar)
		cur.execute(query1)
		obj = cur.fetchone()
		query2 = "UPDATE ZPICMODEDICT SET ZPICTURE = 'NONE' WHERE Z_PK = "+str(foobar)
		cur.execute(query2)
		con.commit()
		con.close()
		#obj = Zpicmodedict.objects.get(z_pk = str(foobar))
		#obj.zpicture = None;
		#obj.save()
		return HttpResponse("Success")
	return HttpResponseRedirect('/images/'+foobar)

'''
This url is used to return the search results for replacing the image of an item .
It is called by ajax and contains search_val as the input text entered by the user.
It searches through the table ZIMAGE_DATA table by checking the keyword and returns
all the matching records , serialized as json objects to display to the user as a 
carousel.
'''
#Done
def getSearch(request):
	if request.is_ajax():
		search_val = request.GET['search_value']
		paths = getpaths()
		con = lite.connect(paths)
		cur = con.cursor()
		try:
			query = "SELECT * FROM ZIMAGEDATA WHERE ZKEY_WORDS LIKE '%"+search_val+"%'"
			cur.execute(query)
			search = cur.fetchall()
			#search = Zimagedata.objects.filter(zkey_words__icontains = search_val)
			#search_query = Zpicmodedict.objects.filter(Q(ztag_name__icontains = search_val) | Q(zpicture__icontains = search_val)).distinct()
		except:
			search = None
			#search_query = None
		query1 = search
		json = simplejson.dumps(search)
		#json = serializers.serialize("json",query1)
		return HttpResponse(json)


'''
This view is to update the database with the image selected by the user.It gets x as input from the template,
which is the source of the image that is displayed. From that varibale x, the picture name is found out(as 
the search results are from the png directory) and the database is updated accrdingly with the new image. 
'''		
#Done	  
def searchupdate(request):
	if request.is_ajax():
		data = request.GET['x']
		pk = str(request.GET['foobar'])
		#obj = Zpicmodedict.objects.get(z_pk = pk)
		zpicture = data.replace("http://localhost:8000/media/png/","")
		paths = getpaths()
		con = lite.connect(paths)
		cur = con.cursor()
		query = "UPDATE ZPICMODEDICT SET ZPICTURE = '"+zpicture+"' WHERE Z_PK = "+pk
		cur.execute(query)
		con.commit()
		con.close()
		#obj.save()
		if zpicture[:3] == "ci_":
			return HttpResponse(str(getrelative())+zpicture)
		else:
			return HttpResponse("png/"+zpicture)
		         

'''
This view is to edit any template/category and save the changes in the database. It is called by ajax,
and recieves the pk of the item, along the new details entered by the user. It connects with sqlite 
database and updates it, and returns a json object containing the record that was updated.
'''
#Done                        
@csrf_exempt
def editsave(request):
	if request.is_ajax():
		zpk = str(request.POST['zpk'])
		zname = request.POST['zname']
		zcolor = request.POST['zcolor']
		enable = request.POST['enable']
		audio_data = request.POST['audio_data']
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		query1 = "UPDATE ZPICMODEDICT SET ZTAG_NAME='"+zname+"' WHERE Z_PK="+zpk
		query2 = "UPDATE ZPICMODEDICT SET ZCOLOR='"+zcolor+"' WHERE Z_PK="+zpk
		query3 = "UPDATE ZPICMODEDICT SET ZAUDIO_DATA='"+audio_data+"' WHERE Z_PK="+zpk
		query4 = "UPDATE ZPICMODEDICT SET ZIS_ENABLED="+enable+" WHERE Z_PK="+zpk
		#return HttpResponse(query4)		
		cur.execute(query1)
		cur.execute(query2)
		cur.execute(query3)
		cur.execute(query4)
		con.commit()		
		cur.execute("SELECT * FROM ZPICMODEDICT WHERE Z_PK = "+zpk)
		objss = cur.fetchone()
		obj = list(objss)
		if obj[12][:3] == "ci_":
			obj[12] = str(getrelative)+ obj[12]
			print obj[12]
		else:
			obj[12] = "png/"+obj[12]
			print obj[12]		
		con.close()
		'''
		obj = Zpicmodedict.objects.get(z_pk = zpk)
		obj.ztag_name = zname
		obj.zcolor = zcolor
		obj.zis_enabled = enable
		obj.zaudio_data = audio_data
		obj.save()'''
		l = []
		l.append(obj)
		json = simplejson.dumps(obj) 
		#json = serializers.serialize("json",l)		
		return HttpResponse(json)

'''
This view is for creating a new category/template. If a category is selected and create button is clicked,
the new item is created as a child to the selected category.If a template is clicked and create button is 
clicked, the new item is created as a sibling to the selected template. Finally, the newly created object 
and the selected object are returned back to template as json objects.
'''
#Done		
@csrf_exempt		
def create(request):
	if request.is_ajax():
		zparentid = request.POST['parentid']	
		data = request.POST['select']	
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		cur.execute("SELECT * FROM ZPICMODEDICT WHERE Z_PK = "+zparentid)
		parent = cur.fetchone()
		#parent = Zpicmodedict.objects.get(z_pk = zparentid)
		#obj = Zpicmodedict()
		#obj.ztag_name = "untitled"
		#obj.zpicture = "descriptives/how.png"
		zcat = []
		zparent_id = []
		if data == 'category':
			zcat =  "D"   #value d
		else:
			zcat  = "T"
		if parent[8] == "D":
			zparent_id = parent[10]  #value d
		else:
			zparent_id = parent[11]
		salt = sha.new(str(random.random())).hexdigest()[:5]
		zidentifier = sha.new(salt).hexdigest()  #value d
		x = parent[5]  #value
		zserial = x+1
		#last = Zpicmodedict.objects.latest("z_pk")
		#y = last.z_pk
		#return HttpResponse(y)
		#obj.z_pk = y+1
		#obj.zserial = x+1
		#obj.save()
		#return HttpResponse(zparent_id)
		query = "INSERT INTO ZPICMODEDICT(ZIS_ENABLED,ZSERIAL,ZCATEGORY_OR_TEMPLATE,ZIDENTIFIER,ZPARENT_ID,ZPICTURE,ZTAG_NAME) VALUES (1,"+str(zserial)+",'"+str(zcat)+"','"+str(zidentifier)+"','"+str(zparent_id)+"','descriptives/how.png','untitled')"
		#return HttpResponse(query)
		cur.execute(query)
		lid = str(cur.lastrowid)
		cur.execute("SELECT * FROM ZPICMODEDICT WHERE Z_PK = "+lid)
		#obj = cur.fetchone()
		objss = cur.fetchone()
		obj = list(objss)
		if obj[12][:3] == "ci_":
			obj[12] = str(getrelative)+ obj[12]
			print obj[12]
		else:
			obj[12] = "png/"+obj[12]
			print obj[12]	
		con.commit()		
		con.close()
		#return HttpResponse(lid)
		l = []
		l.append(obj)
		l.append(parent)		
		#json = serializers.serialize("json",l)
		json  = simplejson.dumps(l)
		return HttpResponse(json)
	else:		
		zparentid = 5
		parent = Zpicmodedict.objects.get(z_pk = zparentid)
		json = serializers.serialize("json",[parent])
		last = Zpicmodedict.objects.latest('z_pk')		
		return HttpResponse(last.z_pk)
		
def audio(request):
	return render_to_response('Audio.html', locals(), context_instance = RequestContext(request))
	
'''
This view is used to search thru all the objects and return those which have their name 
similar to the text entered by the user.
'''
#Done
def word(request):
	if request.is_ajax():
		search = request.GET['search']
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		try:
			query = "SELECT * FROM ZPICMODEDICT WHERE ZTAG_NAME LIKE '%"+search+"%'"
			cur.execute(query)
			search_query = cur.fetchall()
			#search_query = Zpicmodedict.objects.filter(ztag_name__icontains = search)
		except:
			search_query = None
		#json = serializers.serialize("json",search_query)
		con.close()
		json = simplejson.dumps(search_query)
		return HttpResponse(json)

		
#Done
def getParent(request):
	if request.is_ajax():
		x = request.GET['x']
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		query = "SELECT * FROM ZPICMODEDICT WHERE ZIDENTIFIER = '"+x+"'"
		#return HttpResponse(query)
		cur.execute(query)
		obj = cur.fetchall()
		#obj = Zpicmodedict.objects.filter(zidentifier = x)
		#json = serializers.serialize("json",obj)
		json = simplejson.dumps(obj)
		return HttpResponse(json)
		
def start(request):
    csrf_token = get_token(request)
    return render_to_response('import.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))
        

import_uploader = AjaxFileUploader(UPLOAD_DIR = 'Temp')
import_db = AjaxFileUploader(UPLOAD_DIR = 'Dict_Files')

'''
This view is used to commit the uploaded file to the database.
It gets the file name as an input and updates the zpicture attribute of the 
item for which a file was uploaded. It returns the path to the picture.
'''
#Done
def upload(request):
	if request.is_ajax():
		zpk = request.GET['zpk']
		name = request.GET['file_name']
		src = os.path.join(os.path.dirname(__file__), 'Media/Temp/',name)
		zpicture = "ci_"+name
		dst = str(getdirpaths())+"custom_images/"+zpicture
		shutil.move(src,dst)
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		query = "UPDATE ZPICMODEDICT SET ZPICTURE = '"+zpicture+"'WHERE Z_PK = "+zpk
		cur.execute(query)
		con.commit()
		cur.execute("SELECT * FROM ZPICMODEDICT WHERE Z_PK = "+zpk)
		obj = cur.fetchone()		
		con.close()
		#obj = Zpicmodedict.objects.get(z_pk = zpk)
		#obj.zpicture = 'ci_'+name
		#obj.save()
		#img = Zimagedata()
		#x = ""
		#x = name[:-len(".png")]
     	#img.zfile_name = x
     	#img.zdirectory_path = 'custom_images'
     	#for char in string.punctuation:
      #		x = x.replace(char, ' ')
     	#print x
     	#img.zkey_words = x
     	#img.save()
     	path_rel = str(getrelative())+zpicture
     	return HttpResponse(path_rel)


     	
def xls(request):
	
    requirements=Zpicmodedict.objects.all()
    a=1
    foobar = "1"
    if foobar == "1":
        #print "hello"
        w=Workbook()
        ws = w.add_sheet('Items')
        cols=19
        #ws.write(0,0,'Event Name')
        for colx,heading in enumerate(('Z_PK','Z_ENT','Z_OPT','ZIS_ENABLED','ZIS_SENTENCE_BOX_ENABLED','ZSERIAL','ZVERSION','ZAUDIO_DATA','ZCATEGORY_OR_TEMPLATE','ZCOLOR','ZIDENTIFIER','ZPARENT_ID','ZPICTURE','ZTAG_NAME')*1):
            ws.write(0,colx,heading)
		
        rx=0
        for r in requirements:
            rx+=1
            ws.write(rx,0,r.z_pk)
            ws.write(rx,1,r.z_ent)
            ws.write(rx,2,r.z_opt)
            ws.write(rx,3,r.zis_enabled)
            ws.write(rx,4,r.zis_sentence_box_enabled)         
            ws.write(rx,5,r.zserial)
            ws.write(rx,6,r.zversion)
            ws.write(rx,7,r.zaudio_data)
            ws.write(rx,8,r.zcategory_or_template)
            ws.write(rx,9,r.zcolor)
            ws.write(rx,10,r.zidentifier)
            ws.write(rx,11,r.zparent_id)
            ws.write(rx,12,r.zpicture)
            ws.write(rx,13,r.ztag_name)	        
        fname = 'Avaz.xls'
        response = HttpResponse(mimetype="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        w.save(response)
        return response

def printChildren(obj,htmls):
	#children = Zpicmodedict.objects.filter(zparent_id = obj.zidentifier)
	paths = getpaths()
	con = lite.connect(paths) 
	cur = con.cursor()
	cur.execute("SELECT * FROM ZPICMODEDICT WHERE ZPARENT_ID = '"+obj[10]+"'")
	children = cur.fetchall()
	htmls.write("<ol>")
	for c in children:
		x = str(c[12])
		#x = str(c.zpicture)
		word = x[:3]
		if word == "ci_":
			y = str(getdirpaths()) + "custom_images/"
			#y = os.path.join(os.path.dirname(__file__), 'Media/custom_images/')
		else: 
			y = os.path.join(os.path.dirname(__file__), 'Media/png/')
		z = y+x
		if os.path.exists(z):
			f = open(z,'r')
			try:
				f1 = f.read()
				a = str(getdirpaths())+"Download/Images/"
				#a = os.path.join(os.path.dirname(__file__), 'Media/Download/Images/')
				x = x.replace('/','_')
				print x
				b = a+x 
				w = open(b,"w")
				try:
					w.write(f1)
				finally:
					w.close()
			finally:
				f.close()
		con.close()
		htmls.write("<li>"+c[13]+"<img style = 'width:60px;' src = Images/"+x+"></li>")		
		#htmls.write("<li>"+c.ztag_name+"<img style = 'width:60px;' src = Images/"+x+"></li>")
		printChildren(c,htmls)
	htmls.write("</ol>")

'''
This view is used to export the entire dictionary as a html (with images) directory. 
'''        
def export(request):
	if request.is_ajax() or request.method == "GET":
		#name = os.path.join(os.path.dirname(__file__), 'Media/Download/view.html')
		names = str(getdirpaths()) + "Download"
		name = str(getdirpaths()) + "Download/"+"view.html"
		if not os.path.exists(names):
			os.mkdir(names)
		if not os.path.exists(names+"/Images"):
			os.mkdir(names+"/Images")
		htmls = open(name,"w")
		paths = getpaths()
		con = lite.connect(paths) 
		cur = con.cursor()
		cur.execute("SELECT * FROM ZPICMODEDICT WHERE ZPARENT_ID = 0")
		objs = cur.fetchall()
		#objs = Zpicmodedict.objects.filter(zparent_id = 0)
		htmls.write("<html>")
		htmls.write("<ol>")
		for obj in objs :
			x = str(obj[12])
			#x = str(obj.zpicture)
			word = x[:3]
			if word == "ci_":
				y = str(getdirpaths()) +"custom_images/"
				#y = os.path.join(os.path.dirname(__file__), 'Media/custom_images/')
			else: 
				y = os.path.join(os.path.dirname(__file__), 'Media/png/')
			#y = os.path.join(os.path.dirname(__file__), 'Media/png/')
			z = y+x
			if os.path.exists(z):	
				f = open(z,'r')
				try:
					f1 = f.read()
					a = str(getdirpaths())+"Download/Images/"
					#a = os.path.join(os.path.dirname(__file__), 'Media/Download/Images/')
					x = x.replace('/','_')
					print x
					b = a+x 
					w = open(b,"w")
					try:
						w.write(f1)
					finally:
						w.close()
				finally:
					f.close()
			htmls.write("<li>"+obj[13]+"<img style = 'width:60px;' src = Images/"+x+"></li>")
			#htmls.write("<li>"+obj.ztag_name+"<img style = 'width:60px;' src = Images/"+x+"></li>")
			printChildren(obj,htmls)		
			htmls.write("</ol>")
		htmls.write("</html>")		
		con.close()
		response = HttpResponse(htmls,mimetype="application/html")
		response['Content-Disposition'] = 'attachment; filename=idiot'
		return HttpResponse("Exported succesfully")
	
#Done	
'''
This view is for downloading the dictionary in html format(archived).
'''
def downloadHtml(request):
	x = getdirpaths()
	#return HttpResponse(x)
	dir1 = os.path.join(os.path.dirname(__file__),'Media','Download')
	response = HttpResponse(mimetype='application/x-gzip')
	response['Content-Disposition'] = 'attachment; filename=Html.tar.gz'
	tarred = tarfile.open(fileobj=response, mode='w:gz')
	tarred.add(x+"/Download", arcname="TarName")
	tarred.close()
	shutil.rmtree(x+"/Download")
	return response 

'''
This view is for downloading the dictionary with the sqlite and the custom_images directory
'''	
def downloadDict(request):
	x = getdirpaths()
	#return HttpResponse(x)
	response = HttpResponse(mimetype='application/x-gzip')
	response['Content-Disposition'] = 'attachment; filename=Dict.tar.gz'
	tarred = tarfile.open(fileobj=response, mode='w:gz')
	tarred.add(x, arcname="TarName")
	tarred.close()
	return response    

#Done	
'''
This view is used to upload an image given an internet url for the image .
It takes the url and the pk of the item as input and returns the path to the image.
'''
def img(request):
	if request.is_ajax():
		img_url = request.GET['url']
		zpk = request.GET['zpk']
		con = lite.connect(paths) 
		cur = con.cursor()
		#obj =  Zpicmodedict.objects.get(z_pk = zpk)
		try:
			img = urllib2.urlopen(img_url)
		except:
			return HttpResponse("Invalid url !")
		#a = os.path.join(os.path.dirname(__file__), 'Media/custom_images/')
		name = os.path.basename(img_url)
		fname  = "ci_"+name
		path = str(getdirpaths())+"custom_images/"+fname
		f = open(path,"w")
		f.write(img.read())
		f.close()
		#obj.zpicture  = fname
		#obj.save()
		query = "UPDATE ZPICMODEDICT SET ZPICTURE = '"+fname+"'WHERE Z_PK = "+zpk
		cur.execute(query)
		con.commit()
		cur.execute("SELECT * FROM ZPICMODEDICT WHERE Z_PK = "+zpk)
		obj = cur.fetchone()		
		con.close()
		path_rel = str(getrelative())+fname
		return HttpResponse(path_rel)
		#return HttpResponse(obj.zpicture)
	img_url = "http://i59.photobucket.com/albums/g300/wizzer520/hello.png"
	img = urllib2.urlopen(img_url)
	name = os.path.basename(img_url)
	a = os.path.join(os.path.dirname(__file__), 'Media/custom_images/')
	path  =  a+fname
	f = open(path,"w")
	f.write(img.read())
	f.close()
	return HttpResponse("Done")

def extract(request):
	if request.is_ajax() or request.method == 'GET':
		name = request.GET['file_name']
		fname = os.path.join(os.path.dirname(__file__), 'Media/Files/Data.zip')
		with zipfile.ZipFile(fname, 'r') as z:
			dirname = os.path.join(os.path.dirname(__file__), 'Media/Files')
			z.extractall(dirname)
		src1 = os.path.join(os.path.dirname(__file__), 'Media/','custom_images')	
		dst1 = os.path.join(os.path.dirname(__file__), 'Media/','Backup/','custom_images_'+str(datetime.datetime.now())+'')	
		shutil.move(src1, dst1)
		src2 = os.path.join(os.path.dirname(__file__), 'Media/','Files/','Data.sqlite')	
		dst2 = os.path.join(os.path.dirname(__file__), 'Media/','Backup')	
		shutil.move(src2, dst2)
		src3 = os.path.join(os.path.dirname(__file__), 'Media/','Files/','Data/','Data.sqlite')
		dst3 = os.path.join(os.path.dirname(__file__), 'Media/','Files/')	
		shutil.move(src3, dst3)
		src4 = os.path.join(os.path.dirname(__file__), 'Media/','Files/','Data/','custom_images')
		dst4 = os.path.join(os.path.dirname(__file__), 'Media/','custom_images')
		shutil.move(src4, dst4)
		rm5 = os.path.join(os.path.dirname(__file__), 'Media/','Files/','Data')
		shutil.rmtree(rm5)
		return HttpResponse("Files extracted ")
'''
This is used for opening a new dictionary by file upload, saving it in the correct location and assigning the user to own it.
The zip uploaded by the user should contain the sqlite and teh custom_images directory
'''
def extractCreate(request):
	if request.is_ajax() or request.method == 'GET':
		name = request.GET['file_name']
		d = Dictionary()
		d.save()	
		#name = "Data.zip"	
		names = name[:-len(".zip")]
		src = os.path.join(os.path.dirname(__file__), 'Media/','Dict_Files/',name)
		newname = "Dict"+str(d.id)+".zip"
		dst = os.path.join(os.path.dirname(__file__), 'Media/','Dict_Files/',newname)
		#os.renames(src,dst)
		with zipfile.ZipFile(src,'r') as z:
			x = zipfile.ZipInfo(src)
			dirname = os.path.join(os.path.dirname(__file__), 'Media/Dict_Files/')
			z.extractall(path = dirname)
		os.remove(src)
		src1 = dirname + names 
		dst1 = dirname + newname[:-len(".zip")]
		shutil.move(src1,dst1)
		src2 = dst1 +"/"+ names +".sqlite"
		dst2 = dst1 +"/"+ newname[:-len(".zip")] +".sqlite"	
		zpath = newname[:-len(".zip")]
		shutil.move(src2,dst2)
		d.zname = names
		d.zdir_path = "Media/Dict_Files/"+zpath+"/"
		d.zpath = d.zdir_path + zpath + ".sqlite"
		d.save()
		ud = UserDictionary()
		ud.zuserid = request.user.id 
		ud.zdictid = d.id
		ud.save()
		return HttpResponse("Opened")	
'''
This url is to enable a user to login to the site by entering his username and password.
If the user is authenticated correctly, it redirects the listDict page which lists all 
the dictionaries owned by the user.
'''
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['logged_in'] = True
            return HttpResponseRedirect("/listDict/")
        else:
            return render_to_response('Login.html',locals(),context_instance=RequestContext(request))  
    return render_to_response('Login.html', locals(),context_instance=RequestContext(request))	
'''
This url is to enable the user to logout of the site
'''
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")
'''
This url is to list all the dictionaries owned by a specific user who is logged in. It searches 
through the records of the UserDictionary table and returns all Dictionaries owned by that user.
'''    
def listDict(request):
	if not request.user.is_authenticated():
		raise PermissionDenied()
	u = request.user
	objs = list(UserDictionary.objects.filter(zuserid = u.id))
	dicts = []
	for obj in objs:
		d = Dictionary.objects.get(pk = obj.zdictid)
		dicts.append(d)
	return render_to_response('ListDict.html', locals(),context_instance=RequestContext(request))	
'''
This url is used to display a form to create a new dictionary for a user.The parameter foobar is the userid
of the user currently logged in. It creates a new dictionary and assosciates this user with the newly created
dictionary, by creating a new record in the UserDictionary table.
'''
def createDict(request,foobar):
	if not request.user.is_authenticated() :
		raise PermissionDenied()
	user = request.user
	if str(foobar) != str(user.id):
		raise PermissionDenied()
	if request.method == 'POST':
		name = request.POST['name']
		d = Dictionary()
		d.zname = name
		d.save()
		x = "Dict"+str(d.id)		
		src1 = os.path.join(os.path.dirname(__file__), 'Media/','Dict_Files/',x)
		os.makedirs(src1)
		src3 = os.path.join(os.path.dirname(__file__), 'Media/','Dict_Files/',x)
		src2 = os.path.join(os.path.dirname(__file__), 'Media/','Dict_Files/',x,'custom_images')
		os.makedirs(src2)
		fname = os.path.join(os.path.dirname(__file__), 'Media/','Dict_Files/',x,x+'.sqlite')
		src = os.path.join(os.path.dirname(__file__),'..','User-Data.sqlite')
		shutil.copy(src,fname)		
		#f = open(fname,'w')
		#f.close()
		d.zdir_path = "Media/Dict_Files/"+x+"/"		
		d.zpath = d.zdir_path +x+ '.sqlite'
		d.save()
		us = UserDictionary()
		us.zuserid = user.id
		us.zdictid = d.id
		us.save()
		return HttpResponseRedirect('/listDict/')
	return render_to_response('CreateDict.html', locals(),context_instance=RequestContext(request))		
'''
This view is for sharing a dictionary owned by one user, with another user on entering the username of another user.
It creates a new record in the UserDictionary table which has userid as the new user s id and dictid as the current
dictionary s id . This makes sure that the new user can also access that dictionary.
'''
def share(request):
	if request.is_ajax():
		username = request.GET['newuser']
		did = request.GET['did']
		ud = UserDictionary()
		u = User.objects.get(username = username)
		ud.zdictid = did
		ud.zuserid = u.id
		ud.save()
		return HttpResponse("Success")