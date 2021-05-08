from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import JobInfo,JobPostByOutSider,JobSearch,UserNextClick,FeedbackByUser
from operator import and_, or_
from functools import reduce
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from functools import wraps
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)

from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from crm import signals as crm_signals



#login authentication decorator
def authentication_decorator(fun):
    @wraps(fun)
    def new_fun(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseForbidden("Not Authenticated")
    return new_fun

@csrf_exempt
@require_http_methods(["GET"])
def health(request):

    return JsonResponse({"status":"UP"})

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    status = "failed"
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print(username,password)
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        print("Logged in")
        return JsonResponse({"status":"success"})
    else:
        # Return an 'invalid login' error message.
        return HttpResponseBadRequest("Login failed")

    #data = json.loads()


@csrf_exempt
@require_http_methods(["GET"])
def logout_user(request):
    logout(request)
    return JsonResponse({"status":"success"})

"""
{
    City:'',
    Position:''
}
"""
@csrf_exempt
@require_http_methods(["POST"])
#@authentication_decorator
def add_job(request):
    status = "failed"
    if request.method != 'POST':
        message = "Invalid request"
        return JsonResponse({"status":status})

    #data = json.loads()
    data = request.POST.dict()
    username = data.get('username')
    password = data.get('password')
    user = authenticate(request, username=username, password=password)
    #print(user)

    #return JsonResponse(data)
    token = data.get('token',None)
    #print(token)
    if token!="AKKA_3":
        return HttpResponseForbidden("Token has not be provided")
    del data['token']
    del data['username']
    del data['password']


    if user is not None:
        try:
            job = JobInfo.objects.create(**data)
            if len(request.FILES.keys())!=0:
                key = list(request.FILES.keys())[0]
                file_handle = request.FILES[key]
                job.image = file_handle
            job.save()
        except:
            return HttpResponseBadRequest("Failed Check log")


        status = "success"
        return JsonResponse({"status":status})
    else:
        return HttpResponseForbidden("Not Authenticated")

@csrf_exempt
@require_http_methods(["POST"])
def add_job_by_outsider(request):
    status = "failed"
    if request.method != 'POST':
        message = "Invalid request"
        return JsonResponse({"status":status})

    data = json.loads(request.body)
    #return JsonResponse(data)
    token = data.get('token',None)
    if token!="AKKA_2":
        return JsonResponse({"status":"failed","message":"No authentication."})
    del data['token']
    try:
        job = JobPostByOutSider.objects.create(**data)
        job.save()
    except Exception as e:
        #print(str(e))
        return JsonResponse({"status":"failed"})


    status = "success"
    return JsonResponse({"status":status})




@csrf_exempt
@require_http_methods(["GET"])
def get_all_jobs(request):
    #all_jobs = [job.to_dict() for job in JobInfo.objects.all()]
    return JsonResponse({},safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def user_next_page(request):
    data = json.loads(request.body)
    usernamefake = data.get('username','NA')
    from_page = data.get('from_page','')
    next_page = data.get('next_page','')
    next_obj = {"usernamefake":usernamefake,'next_page':next_page,'from_page':from_page}
    obj_ = UserNextClick.objects.create(**next_obj)
    obj_.save()
    return JsonResponse({"status":"success","data":next_obj},safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def get_latest_jobs(request):
    data = json.loads(request.body)

    usernamefake = data.get('username','NA')
    from_page = ''
    next_page = 'teacherPortalLandingPage'
    next_obj = {"usernamefake":usernamefake,'next_page':next_page,'from_page':from_page}
    obj_ = UserNextClick.objects.create(**next_obj)
    obj_.save()

    jobs = JobInfo.objects.all().order_by("-entry_time")[:14]
    all_jobs = [job.to_dict() for job in jobs]
    return JsonResponse({"status":"success","data":all_jobs},safe=False)



@csrf_exempt
@require_http_methods(["POST"])
def get_jobs(request):
    def strip_space(string):
        return ','.join(string.split(' '))
    data = json.loads(request.body)
    positions = data.get('positions','')
    positions = positions.split(',')

    subjects = data.get('subjects','')
    subjects = strip_space(subjects).split(',')

    locations = data.get('location','')
    locations = strip_space(locations).split(',')

    usernamefake = data.get('username','NA')




    pos_q = reduce(or_,[Q(positions__icontains=position) for position in positions])
    sub_q = reduce(or_,[Q(subjects__icontains=subject) for subject in subjects])
    loc_q = reduce(or_,[Q(city__icontains=location) for location in locations])
    final_q = reduce(and_,[pos_q,sub_q,loc_q])
    jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
    all_jobs = [job.to_dict() for job in jobs]

    search_data = {'usernamefake':usernamefake,'city':','.join(locations),'positions':','.join(positions),
        'subjects':','.join(subjects),"result_count":len(all_jobs)}
    search_obj = JobSearch.objects.create(**search_data)
    search_obj.save()


    #using crm signals
    search_data = {'user':request.user,'username':usernamefake,'city':','.join(locations),'positions':','.join(positions),
        'subjects':','.join(subjects),"result_count":len(all_jobs)}
    crm_signals.job_search_signal.send(sender=None, **search_data)
    if len(all_jobs)>0:


        return JsonResponse({"status":"success","data":all_jobs},safe=False)
    else:
        final_q = reduce(and_,[loc_q])
        jobs = JobInfo.objects.filter(final_q).all().order_by("-entry_time")
        all_jobs = [job.to_dict() for job in jobs]
        search_data = {'usernamefake':usernamefake,'city':','.join(locations),"result_count":len(all_jobs)}
        search_obj = JobSearch.objects.create(**search_data)
        search_obj.save()

        return JsonResponse({"status":"success","data":all_jobs},safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def get_job_by_id(request):
    def strip_space(string):
        return ','.join(string.split(' '))
    job_id = request.GET['id']
    try:
        job  = JobInfo.objects.get(pk=job_id)
        return JsonResponse({"status":"success","data":[job.to_dict()]},safe=False)
    except:
        return HttpResponseBadRequest("Job not found")


@csrf_exempt
@require_http_methods(["GET"])
def get_job_by_ids(request):
    def strip_space(string):
        return ','.join(string.split(' '))
    job_ids = request.GET['id'].split(',')
    try:
        jobs  = JobInfo.objects.filter(id__in=job_ids).order_by('-entry_time')
        jobs_data = [job.to_dict() for job in jobs]
        return JsonResponse({"status":"success","data":jobs_data},safe=False)
    except:
        return HttpResponseBadRequest("Job not found")

@csrf_exempt
@require_http_methods(["POST"])
def add_feedback_by_user(request):
    data = json.loads(request.body)
    usernamefake = data.get("username",'NA')
    from_page = data.get("from_page",'')
    feedback = data.get("feedback",'')
    obj_data = {"usernamefake":usernamefake,"from_page":from_page,"feedback":feedback}
    try:
        feedback_ojb = FeedbackByUser.objects.create(**obj_data)
        feedback_ojb.save()
        return JsonResponse({"status":"success"})
    except Exception as e:
        #print(str(e))
        return HttpResponseBadRequest("Could not save feedback")



#visualizations
#get data for visualization
@csrf_exempt
@require_http_methods(["POST"])
def get_data_for_vis(request):
    data = json.loads(request.body)
    secretKey = data.get('secretKey','')
    table_name = data.get("table_name",'')
    if secretKey!='du20fu2':
        return HttpResponseForbidden("No authentication provided")
    if table_name=='':
        return HttpResponseBadRequest("Please provide Table name")
    if table_name=='JobInfo':
        data_to_return = JobInfo.objects.all()
        if len(data_to_return)==0:
            return JsonResponse({"status":"success","data":{}},safe=False)
        data_to_return = serialize("json", data_to_return)
        return JsonResponse({"status":"success","data":data_to_return},safe=False)
    if table_name=='JobPostByOutSider':
        data_to_return = JobPostByOutSider.objects.all()
        if len(data_to_return)==0:
            return JsonResponse({"status":"success","data":{}},safe=False)
        data_to_return = serialize("json", data_to_return)
        return JsonResponse({"status":"success","data":data_to_return},safe=False)
    if table_name=='JobSearch':
        data_to_return = JobSearch.objects.all()
        if len(data_to_return)==0:
            return JsonResponse({"status":"success","data":{}},safe=False)
        data_to_return = serialize("json", data_to_return)
        return JsonResponse({"status":"success","data":data_to_return},safe=False)
    if table_name=='UserNextClick':
        data_to_return = UserNextClick.objects.all()
        if len(data_to_return)==0:
            return JsonResponse({"status":"success","data":{}},safe=False)
        data_to_return = serialize("json", data_to_return)
        return JsonResponse({"status":"success","data":data_to_return},safe=False)
    return HttpResponseBadRequest("No such Table name allowed.")
