from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from forms import signupform
from django.contrib import messages
from newtodo.models import Signup,Tasks
from datetime import date
count=0
today=date.today()
print "TODAY IS",today
# Create your views here.
def signup(request):
	if request.method == 'GET':
		signup=Signup()
		
		print signup.name
		return render(request,"signup.html",{})
	elif request.method == 'POST':
		signup=Signup()
		value=0
		print "requesmethod",request.method
		name=request.POST.get("name" or None)
		if name is None or '' or len(name)==0:
			print "name"
			value=1
		print "len name",len(name)
		email=request.POST.get("email" or None)
		if email== None or '@' not in email:
			print "email"
			value=2
		passwd=request.POST.get("passwd" or None)
		if passwd== None or len(passwd)<8:
			print "passwd"
			value=3
		print value
		if value==1:
			return render(request,"signup.html",{'noname':True})
		elif value==2:
			return render(request,"signup.html",{'noemail':True})
		elif value==3:
			return render(request,"signup.html",{'nopasswd':True})
		p=Signup(name=name,email=email,passwd=passwd)
		p.save()
		print p.name
		# messages.add_message(request, messages.INFO, 'All items on this page have free shipping.',fail_silently=True)
		return render(request,"signup.html",{})

def login(request):
	login=Signup()
	if request.method=='GET':
		return render(request,"login.html",{})
	elif request.method=='POST' and 'searchform' not in request.POST:
		login=Signup()
		name=request.POST.get("name")
		passwd=request.POST.get("passwd")
		print name,passwd
		try:
			print "here"
			names=Signup.objects.get(name=name)
			print "names is",names
			if names.passwd==passwd:
				request.session['member_id'] = names.id
				print "names passwd",names.passwd,"passwd",passwd,"request",request.session['member_id']
				user=request.session['member_id']
				obj=Signup.objects.get(id=user)
				tasks=Tasks()
				print "obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
				try:
					todaylist=[]
					remain=[]
					todaysize=False
					remainsize=False
					todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
					for tod in todoes:
						if tod.mydate==date.today():
							todaylist.append(tod)
							todaysize=True
							print "todaylist",todaylist
						else:
							remain.append(tod)
							print "reaminlist",remain
							remainsize=True
					# print todoes[0].priority,todoes[0].task
					RANGE=len(todoes)
					print "range is",RANGE
					dic={
					"todaysize":todaysize,
					"remainsize":remainsize,
					"remain":remain,
					"todaylist":todaylist,
					"range":RANGE,
					"name":obj.name
					}
					return render(request,"todo.html",dic)
				except:
					return render(request,"todo.html",{"task":False,"name":obj.name})
			else:
				return render(request,"login.html",{'invalid':True})
		except:
			print "inexceept"
			return render(request,"login.html",{'there':True})
	elif request.method=='POST' and 'searchform' in request.POST:
			print "inseachlogin"
			result=request.POST.get("search")
			print "searchresult",result
			user=request.session['member_id']
			obj=Signup.objects.get(id=user)
			tasks=Tasks()
			print "search::obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
			try:	
				searchlist=[]
				todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
				print "todoes",todoes
				for work in todoes:
					if str(work.task)==str(result) or str(work.priority)==str(result):
						searchlist.append(work)
					print searchlist
				if len(searchlist)>0:
					print len(searchlist)
					dc={
						"found":True,
						"searchlist":searchlist
						}
					print dc
					return render(request,"search.html",dc)
				else:
					return render(request,"search.html",{"notfound":True})
			except:
				print "notthere"
				return render(request,"search.html",{"exception":True})
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request,"logout.html",{})

def add(request):
	try:
		if request.method == 'GET':
			user=request.session['member_id']
			obj=Signup.objects.get(id=user)
			tasks=Tasks()
			print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
			print "TODAY IS",today
			try:
				todaylist=[]
				remain=[]
				todaysize=False
				remainsize=False
				todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
				for t in todoes:
					print t.mydate
					print "TODAY IS",today
					if t.mydate == today:
						print "if"
						todaylist.append(t)
						todaysize=True
						print "todaylist",todaylist
					else:
						print "else"
						remain.append(t)
						print "remainlist",remain
						remainsize=True
				# print todoes[0].priority,todoes[0].task
				RANGE=len(todoes)
				print "range is",RANGE
				dic={
				"todaysize":todaysize,
				"remainsize":remainsize,
				"remain":remain,
				"todaylist":todaylist,
				"range":RANGE,
				"name":obj.name,
				"task":True
				}
				return render(request,"todo.html",dic)
			except Exception as e:
				print "except"
				print '%s (%s)' % (e.message, type(e))
				return render(request,"todo.html",{"task":True,"name":obj.name})
		elif request.method == 'POST' and 'mainform' in request.POST:
			obj=Signup()
			obj=Signup.objects.get(id=request.session['member_id'])
			print "signup.id",obj.id
			tasks=Tasks()
			value=0
			print "requesmethod",request.method
			task=request.POST.get("task" or None)
			if task is None or '' or len(task)==0:
				print "task"
				value=1
			print "len task",len(task)
			priority=request.POST.get("priority" or None)
			print "priority is",priority
			if priority=="" or str(priority)== None or priority==-1:
				print "priority"
				value=2
			date=request.POST.get("date" or None)
			if date== None or len(date)<0:
				print "date"
				value=3
			time=request.POST.get("time" or None)
			if time== None or len(time)<0:
				print "time"
				value=4	
			print value
			if value==1:
				user=request.session['member_id']
				obj=Signup.objects.get(id=user)
				tasks=Tasks()
				print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
				try:
					todaylist=[]
					remain=[]
					todaysize=False
					remainsize=False
					todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
					for tod in todoes:
						if tod.mydate==today:
							todaylist.append(tod)
							todaysize=True
							print "todaylist",todaylist
						else:
							remain.append(tod)
							print "reaminlist",remain
							remainsize=True
					# print todoes[0].priority,todoes[0].task
					RANGE=len(todoes)
					print "range is",RANGE
					dic={
					"todaysize":todaysize,
					"remainsize":remainsize,
					"remain":remain,
					"todaylist":todaylist,
					"range":RANGE,
					"name":obj.name,
					'notask':True,
					'task':True
					}
					return render(request,"todo.html",dic)
				except:
					return render(request,"todo.html",{"task":True,"name":obj.name,'notask':True})
			elif value==2:
				user=request.session['member_id']
				obj=Signup.objects.get(id=user)
				tasks=Tasks()
				print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
				try:
					todaylist=[]
					remain=[]
					todaysize=False
					remainsize=False
					todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
					for tod in todoes:
						if tod.mydate==today:
							todaylist.append(tod)
							todaysize=True
							print "todaylist",todaylist
						else:
							remain.append(tod)
							print "reaminlist",remain
							remainsize=True
					# print todoes[0].priority,todoes[0].task
					RANGE=len(todoes)
					print "range is",RANGE
					dic={
					"todaysize":todaysize,
					"remainsize":remainsize,
					"remain":remain,
					"todaylist":todaylist,
					"range":RANGE,
					"name":obj.name,
					'nopriority':True,
					'task':True
					}
					return render(request,"todo.html",dic)
				except:
					return render(request,"todo.html",{"task":True,"name":obj.name,'nopriority':True})
			elif value==3:
				user=request.session['member_id']
				obj=Signup.objects.get(id=user)
				tasks=Tasks()
				print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
				try:	
					todaylist=[]
					remain=[]
					todaysize=False
					remainsize=False
					todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
					for tod in todoes:
						if tod.mydate==today:
							todaylist.append(tod)
							todaysize=True
							print "todaylist",todaylist
						else:
							remain.append(tod)
							print "reaminlist",remain
							remainsize=True
					# print todoes[0].priority,todoes[0].task
					RANGE=len(todoes)
					print "range is",RANGE
					dic={
					"todaysize":todaysize,
					"remainsize":remainsize,
					"remain":remain,
					"todaylist":todaylist,
					"range":RANGE,
					"name":obj.name,
					'nodate':True,
					'task':True
					}
					return render(request,"todo.html",dic)
				except:
					return render(request,"todo.html",{"task":True,"name":obj.name,'nodate':True})
			elif value==4:
				user=request.session['member_id']
				obj=Signup.objects.get(id=user)
				tasks=Tasks()
				print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
				try:
					todaylist=[]
					remain=[]
					todaysize=False
					remainsize=False
					todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
					for tod in todoes:
						if tod.mydate==today:
							todaylist.append(tod)
							todaysize=True
							print "todaylist",todaylist
						else:
							remain.append(tod)
							print "reaminlist",remain
							remainsize=True
					# print todoes[0].priority,todoes[0].task
					RANGE=len(todoes)
					print "range is",RANGE
					dic={
					"todaysize":todaysize,
					"remainsize":remainsize,
					"remain":remain,
					"todaylist":todaylist,
					"range":RANGE,
					"name":obj.name,
					'notime':True,
					'task':True
						}
					return render(request,"todo.html",dic)
				except:
					return render(request,"todo.html",{"task":True,"name":obj.name,'notime':True})
			p=Tasks(userid=obj,task=task,priority=priority,mydate=date,mytime=time)
			p.save()
			print p.mydate,p.mytime
			user=request.session['member_id']
			obj=Signup.objects.get(id=user)
			tasks=Tasks()
			print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
			try:
				todaylist=[]
				remain=[]
				todaysize=False
				remainsize=False
				todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
				for tod in todoes:
					print tod.mydate
					print today
					if tod.mydate==today:
						todaylist.append(tod)
						todaysize=True
						print "todaylist",todaylist
					else:
						remain.append(tod)
						print "reaminlist",remain
						remainsize=True
				# print todoes[0].priority,todoes[0].task
				RANGE=len(todoes)
				print "range is",RANGE
				dic={
				"todaysize":todaysize,
				"remainsize":remainsize,
				"remain":remain,
				"todaylist":todaylist,
				"range":RANGE,
				"name":obj.name,
				'task':False
				}
				return render(request,"todo.html",dic)
			except Exception as e:
				print "except"
				print '%s (%s)' % (e.message, type(e))
				return render(request,"todo.html",{"name":obj.name})
		elif request.method=='POST' and 'searchform' in request.POST:
			print "inseachlogin"
			result=request.POST.get("search")
			print "searchresult",result
			user=request.session['member_id']
			obj=Signup.objects.get(id=user)
			tasks=Tasks()
			print "search::obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
			try:	
				searchlist=[]
				todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
				print "todoes",todoes
				for work in todoes:
					if str(work.task)==str(result) or str(work.priority)==str(result):
						searchlist.append(work)
					print searchlist
				if len(searchlist)>0:
					print len(searchlist)
					dc={
						"found":True,
						"searchlist":searchlist
						}
					print dc
					return render(request,"search.html",dc)
				else:
					return render(request,"search.html",{"notfound":True})
			except:
				print "notthere"
				return render(request,"search.html",{"exception":True})
	except:
		return HttpResponseRedirect("/login/")


def checkout(request,taskid):
	if request.method=='GET':
		to_delete=taskid
		Tasks.objects.filter(taskid=taskid).delete()
		user=request.session['member_id']
		obj=Signup.objects.get(id=user)
		tasks=Tasks()
		print "ADD:obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
		try:
			todaylist=[]
			remain=[]
			todaysize=False
			remainsize=False
			todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
			for tod in todoes:
				if tod.mydate==date.today():
					todaylist.append(tod)
					todaysize=True
					print "todaylist",todaylist
				else:
					remain.append(tod)
					print "reaminlist",remain
					remainsize=True
			# print todoes[0].priority,todoes[0].task
			RANGE=len(todoes)
			print "range is",RANGE
			dic={
			"todaysize":todaysize,
			"remainsize":remainsize,
			"remain":remain,
			"todaylist":todaylist,
			"range":RANGE,
			"name":obj.name,
			'task':False
			}
			return render(request,"todo.html",dic)
		except:
			return render(request,"todo.html",{"name":obj.name})
	elif request.method=='POST' and 'searchform' in request.POST:
		print "inseachlogin"
		result=request.POST.get("search")
		print "searchresult",result
		user=request.session['member_id']
		obj=Signup.objects.get(id=user)
		tasks=Tasks()
		print "search::obj=",obj,"for id",Signup.objects.get(id=user),"obje name",obj.name
		try:	
			searchlist=[]
			todoes=Tasks.objects.filter(userid=obj).order_by('mydate')
			print "todoes",todoes
			for work in todoes:
				if str(work.task)==str(result) or str(work.priority)==str(result):
					searchlist.append(work)
				print searchlist
			if len(searchlist)>0:
				print len(searchlist)
				dc={
					"found":True,
					"searchlist":searchlist
					}
				print dc
				return render(request,"search.html",dc)
			else:
				return render(request,"search.html",{"notfound":True})
		except:
			print "notthere"
			return render(request,"search.html",{"exception":True})





































































	# def login(request):
# 	login=Signup()
# 	if request.method=='GET':
# 		return render(request,"login.html",{})
# 	else:
# 		login=Signup()
# 		name=request.POST.get("name")
# 		passwd=request.POST.get("passwd")
# 		print name,passwd
# 		try:
# 			print "here"
# 			names=Signup.objects.get(name=name)
# 			print "names is",names
# 			if names.passwd==passwd:
# 				request.session['member_id'] = names.id
# 				print "names passwd",names.passwd,"passwd",passwd,"request.sesionn",request.session['member_id'],"member id",member_id
# 				return render(request,"todo.html",{'name':name})
# 			else:
# 				return render(request,"login.html",{'invalid':True})
# 		except:
# # 			print "inexceept"
# 			return render(request,"login.html",{'there':True})