from django.shortcuts import render, get_object_or_404
from api.forms import PostForm
from django.contrib import messages
from django.shortcuts import render, redirect
import json
from api.models import *
from django.forms.models import model_to_dict
from django.http import JsonResponse
import random

from django.db.models import Q
# Create your views here.
def register(request):
    if request.method == 'POST':
        try:
            result_post = json.loads(request.body)
        except:
            result_post = request.POST
        systemDict = {}
        for key in result_post:
            systemDict[key] = result_post.get(key)
        if systemDict['types'] == '0':
            if not UserInfo.objects.filter(username=systemDict['username']):
                UserInfo.objects.create(**systemDict).save()
                return render(request, 'job/login.html', context={'data': 'register success!'})
            else:
                return render(request, 'job/register.html', context={'data': 'account has existing!'})
        elif systemDict['types'] == '1':
            if not EInfo.objects.filter(username=systemDict['username']):
                EInfo.objects.create(**systemDict).save()
                return render(request, 'job/login.html', context={'data': 'register success!'})
            else:
                return render(request, 'job/register.html', context={'data': 'account has existing!'})
        elif systemDict['types'] == '2':
            if not AdminInfo.objects.filter(username=systemDict['username']):
                AdminInfo.objects.create(**systemDict).save()
                return render(request, 'job/login.html', context={'data': 'register success!'})
            else:
                return render(request, 'job/register.html', context={'data': 'account has existing!'})

    else:
        return render(request, 'job/register.html')


def login(request):
    if request.method == 'POST':
        try:
            result_post = json.loads(request.body)
        except:
            result_post = request.POST
        systemDict = {}
        for key in result_post:
            systemDict[key] = result_post.get(key)
        request.session['types'] = systemDict['types']
        if systemDict['types'] == '0':
            if not UserInfo.objects.filter(username=systemDict['username']):
                return render(request, 'job/login.html', context={'data': 'account doesnt existing!'})
            elif UserInfo.objects.filter(username=systemDict['username'], password=systemDict['password']):
                user_id = UserInfo.objects.get(
                    username=systemDict['username']).id
                request.session['user_id'] = user_id
                request.session['username'] = systemDict['username']
                return redirect('/index/')
        elif systemDict['types'] == '1':
            if not EInfo.objects.filter(username=systemDict['username']):
                return render(request, 'job/login.html', context={'data': 'account doesnt existing!'})
            elif EInfo.objects.filter(username=systemDict['username'], password=systemDict['password']):
                user_id = EInfo.objects.get(username=systemDict['username']).id
                request.session['e_id'] = user_id
                request.session['username'] = systemDict['username']
                return redirect('/index/')
        elif systemDict['types'] == '2':
            if not AdminInfo.objects.filter(username=systemDict['username']):
                return render(request, 'job/login.html', context={'data': 'account doesnt existing!'})
            elif AdminInfo.objects.filter(username=systemDict['username'], password=systemDict['password']):
                user_id = AdminInfo.objects.get(
                    username=systemDict['username']).id
                request.session['admin_id'] = user_id
                request.session['username'] = systemDict['username']
                return redirect('/index/')
     # <option value="0">student</option>
      # <option value="1">employers</option>
         # <option value="2">admin</option>
    else:
        return render(request, 'job/login.html')


def index(request):
    list_all = []
    for i in JoinWork.objects.all():
        dict1 = {}
        dict1['job_title'] = i.job_id.job_title
        dict1['job_id'] = i.job_id.id
        dict1['company'] = i.job_id.e_id.company
        dict1['address'] = i.job_id.e_id.address
        dict1['money_max'] = int(i.job_id.work_money_max)
        dict1['money_min'] = int(i.job_id.work_money_min)
        if ',' in i.job_id.job_tags:
            dict1['job_tags'] = i.job_id.job_tags.split(',')
        else:
            dict1['job_tags'] = [i.job_id.job_tags]
        list_all.append(dict1)
    print(list_all)
    # 工作
    jobs_posted = Job.objects.all().count()
    parttime = Job.objects.all().filter(job_type__icontains='Part Time').count()
    fulltime = Job.objects.all().filter(job_type__icontains='Full Time').count()

    print(jobs_posted)
    # 公司
    company = EInfo.objects.all().count()
    # 学生
    stunum = UserInfo.objects.all().count()
    freelancer = UserInfo.objects.filter(tags='freelancer').count()
    Jobs_Filled = 9
    list_all.sort(key=lambda la: la['money_max'], reverse=True)

    return render(request, 'job/index.html', context={'Jobs_Filled': Jobs_Filled,
                                                      'freelancer': freelancer,'parttime':parttime,'fulltime':fulltime,
                                                      'jobs_posted': jobs_posted,
                                                      "stunum":stunum,
                                                      'company': company, 'job_datas': list_all[0:10]})


def personal(request):
    if request.method == 'POST':
        try:
            result_post = json.loads(request.body)
        except:
            result_post = request.POST
        systemDict = {}
        for key in result_post:
            systemDict[key] = result_post.get(key)
        user_id = request.session.get('user_id')
        if not WorkShort.objects.filter(user_id_id=user_id):
            WorkShort.objects.create(user_id_id=user_id, **systemDict)
        else:
            WorkShort.objects.filter(user_id_id=user_id).update(**systemDict)
        systemDict2 = model_to_dict(WorkShort.objects.get(user_id_id=user_id))
        return render(request, 'job/candidate-dashboard.html', context=systemDict2)
    else:
        user_id = request.session.get('user_id')
        if not WorkShort.objects.filter(user_id_id=user_id):
            WorkShort.objects.create(user_id_id=user_id)
        systemDict2 = model_to_dict(WorkShort.objects.get(user_id_id=user_id))
        results = JoinWork.objects.filter(user_id_id=user_id)
        list_pass = []
        list_waiting = []
        for i in results:
            dict1 = {}
            if i.is_pass_status:
                dict1['pass_status'] = 'Pass'
                dict1['job_id'] = i.job_id.id
                dict1['job_title'] = i.job_id.job_title
                dict1['company'] = i.job_id.e_id.company
                dict1['created_at'] = i.created_at
                list_pass.append(dict1)
            else:
                dict1['pass_status'] = 'Waiting'
                dict1['job_id'] = i.job_id.id
                dict1['job_title'] = i.job_id.job_title
                dict1['company'] = i.job_id.e_id.company
                dict1['created_at'] = i.created_at
                list_waiting.append(dict1)
        systemDict2['list_pass'] = list_pass
        systemDict2['list_waiting'] = list_waiting
        print(list_pass)
        return render(request, 'job/candidate-dashboard.html', context=systemDict2)


def find_job(request):
    results = Job.objects.all().order_by('-id')
    list_all = []
    for rs in results:
        dict1 = {}
        dict1['job_id'] = rs.id
        dict1['job_title'] = rs.job_title
        if ',' in rs.job_tags:
            dict1['job_tags'] = rs.job_tags.split(',')
        else:
            dict1['job_tags'] = [rs.job_tags]
        dict1['company'] = rs.e_id.company
        dict1['address'] = rs.e_id.address
        dict1['job_type'] = rs.job_type
        dict1['work_money_min'] = rs.work_money_min
        dict1['work_money_max'] = rs.work_money_max
        dict1['created_at'] = rs.created_at
        list_all.append(dict1)
    print(list_all)
    return render(request, 'job/search-with-sidebar-list-2.html', context={'data': list_all, 'count': len(list_all)})


def test(request):
    return render(request, 'job/base.html', context={})


def job_detail(request):
    job_id = request.GET.get('job_id')
    dict1 = model_to_dict(Job.objects.get(id=job_id))
    company_id = dict1['e_id']
    dict2 = model_to_dict(EInfo.objects.get(id=company_id))
    return render(request, 'job/job-detail.html', context={'dict1': dict1, 'dict2': dict2})


def join_job2(request):
    if request.method == 'GET':
        job_id = request.GET.get('job_id')
    else:
        job_id = request.POST.get('job_id')
    user_id = request.session['user_id']
    if not JoinWork.objects.filter(job_id_id=job_id, user_id_id=user_id):
        JoinWork.objects.create(
            job_id_id=job_id, user_id_id=user_id, msg=request.POST.get('msg')).save()
        dict1 = model_to_dict(Job.objects.get(id=job_id))
        company_id = dict1['e_id']
        dict2 = model_to_dict(EInfo.objects.get(id=company_id))
        return render(request, 'job/job-detail.html',
                      context={'code': 200, 'data': 'apply this job success!', 'dict1': dict1, 'dict2': dict2})
    else:

        dict1 = model_to_dict(Job.objects.get(id=job_id))
        company_id = dict1['e_id']
        dict2 = model_to_dict(EInfo.objects.get(id=company_id))
        return render(request, 'job/job-detail.html',
                      context={'code': 204, 'data': 'You has apply this job!', 'dict1': dict1, 'dict2': dict2})


def join_status_list(request):
    user_id = request.session['user_id']
    results = JoinWork.objects.filter(user_id_id=user_id)
    list_all = []
    for rs in results:
        dict1 = {}
        dict1['job_id'] = rs.job_id.id
        dict1['job_title'] = rs.job_id.job_title
        if ',' in rs.job_id.job_tags:
            dict1['job_tags'] = rs.job_id.job_tags.split(',')
        else:
            dict1['job_tags'] = [rs.job_id.job_tags]
        dict1['company'] = rs.job_id.e_id.company
        dict1['address'] = rs.job_id.e_id.address
        dict1['job_type'] = rs.job_id.job_type
        dict1['work_money_min'] = rs.job_id.work_money_min
        dict1['work_money_max'] = rs.job_id.work_money_max
        dict1['created_at'] = rs.job_id.created_at
        if rs.is_pass_status:
            dict1['pass_status'] = 'Pass'
        else:
            dict1['pass_status'] = 'Waiting'

        list_all.append(dict1)
    return render(request, 'job/job-join-status.html', context={'data': list_all, 'count': len(list_all)})


def e_info(request):
    if request.method == 'POST':
        try:
            result_post = json.loads(request.body)
        except:
            result_post = request.POST
        systemDict = {}
        for key in result_post:
            systemDict[key] = result_post.get(key)
        print(systemDict)
        user_id = request.session.get('e_id')
        EInfo.objects.filter(id=user_id).update(**systemDict)
        return redirect('/e_info/')
    else:
        user_id = request.session.get('e_id')
        systemDict2 = model_to_dict(EInfo.objects.get(id=user_id))
        jobs = [model_to_dict(i, fields=['id', 'job_title'])
                for i in Job.objects.filter(e_id_id=user_id)]
        systemDict2['jobs'] = jobs
        print(jobs)
        results = JoinWork.objects.filter(
            job_id__e_id_id=request.session['e_id'])
        shortlisted = []
        for i in results:
            dict1 = {}
            dict1['user_id'] = i.user_id.id
            dict1['job_title'] = i.job_id.job_title
            dict1['full_name'] = WorkShort.objects.get(
                user_id_id=i.user_id.id).full_name
            if JoinWork.objects.get(user_id_id=i.user_id.id, job_id_id=i.job_id).is_pass_status:
                dict1['pass_status'] = 'Pass'
            else:
                dict1['pass_status'] = 'Waiting'
            dict1['created_at'] = i.created_at
            shortlisted.append(dict1)
        systemDict2['shortlisted'] = shortlisted
        print(shortlisted)
        return render(request, 'job/employer-dashboard.html', context=systemDict2)


def job_delete(request):
    job_id = request.GET.get('job_id')
    Job.objects.filter(id=job_id).delete()
    return redirect('/e_info/')


def job_watting_profile(request):
    user_id = request.GET.get('user_id')
    if not WorkShort.objects.filter(user_id_id=user_id):
        WorkShort.objects.create(user_id_id=user_id)
    systemDict2 = model_to_dict(
        WorkShort.objects.filter(user_id_id=user_id).last())
    systemDict2['msg'] = JoinWork.objects.filter(
        user_id_id=user_id, job_id__e_id_id=request.session['e_id']).last().msg
    return render(request, 'job/view-candidate-profile.html', context=systemDict2)


def check_pass(request):
    user_id = request.GET.get('user_id')
    e_id = request.session['e_id']
    JoinWork.objects.filter(
        user_id_id=user_id, job_id__e_id_id=e_id).update(is_pass_status=True)
    return redirect('/e_info/')


def post_job(request):
    try:
        result_post = json.loads(request.body)
    except:
        result_post = request.POST
    systemDict = {}
    for key in result_post:
        systemDict[key] = result_post.get(key)
    e_id = request.session['e_id']
    Job.objects.create(e_id_id=e_id, **systemDict).save()
    return redirect('/e_info/')


def admin_show_account_stu(request):
    results = WorkShort.objects.all()
    count = results.count()
    list_all = []
    for i in results:
        list_all.append(model_to_dict(
            i, fields=['user_id', 'full_name', 'address', 'experience', 'created_at']))
    return render(request, 'job/candidate-list.html', context={'list_all': list_all, 'count': count})


def admin_show_account_e(request):
    results = EInfo.objects.all()
    count = results.count()
    list_all = []
    for i in results:
        list_all.append(model_to_dict(
            i, fields=['id', 'company', 'address', 'country', 'created_at']))
    return render(request, 'job/candidate-list-e.html', context={'list_all': list_all, 'count': count})


def work_list(request):
    e_id = request.GET.get('e_id')
    list_all = []
    for i in Job.objects.filter(e_id_id=e_id):
        dict1 = model_to_dict(
            i, fields=['id', 'job_title', 'job_tags', 'job_type', 'created_at'])
        list_all.append(dict1)
    return render(request, 'job/candidate-list-job-list.html', context={'list_all': list_all, 'count': len(list_all)})


def find_jobs(request):
    job_title = request.POST.get('job_title', '')
    address = request.POST.get('address', '')
    industry = request.POST.get('industry', '')
    print(industry)
    searchcheck=request.POST.get("searchcheck",'').split(",")
    filter_q = Q()
    if(len(searchcheck)>0):
        for val in searchcheck:
            print(val)
            filter_q |= Q(job_type__icontains=val)
    results = Job.objects.filter(job_title__icontains=job_title).filter(e_id__address__icontains=address).filter(
            industry__icontains=industry).filter(filter_q)
    list_all = []
    for rs in results:
        dict1 = {}
        dict1['job_id'] = rs.id
        dict1['job_title'] = rs.job_title
        if ',' in rs.job_tags:
            dict1['job_tags'] = rs.job_tags.split(',')
        else:
            dict1['job_tags'] = [rs.job_tags]
        dict1['company'] = rs.e_id.company
        dict1['address'] = rs.e_id.address
        dict1['job_type'] = rs.job_type
        dict1['work_money_min'] = rs.work_money_min
        dict1['work_money_max'] = rs.work_money_max
        dict1['created_at'] = rs.created_at
        list_all.append(dict1)

    return render(request, 'job/search-with-sidebar-list-2.html', context={'data': list_all})


def change_password(request):
    if str(request.session['types']) == '0':
        if UserInfo.objects.get(id=request.session['user_id']).password == request.POST.get('password'):
            UserInfo.objects.filter(id=request.session['user_id']).update(
                password=request.POST.get('new_pwd'))
            return redirect('/personal/', {'d': 'password change success'})
        else:
            return redirect('/personal/', {'d': 'password change failed'})
    elif str(request.session['types']) == '1':
        if EInfo.objects.get(id=request.session['e_id']).password == request.POST.get('password'):
            EInfo.objects.filter(id=request.session['user_id']).update(
                password=request.POST.get('new_pwd'))
            return redirect('/e_info/', {'d': 'password change success'})
        else:
            return redirect('/e_info/', {'d': 'password change failed'})


def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = Comment.objects.create(
                post=post,
                user_id=request.session['user_id'],
                text=comment_text
            )
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', post_id=post_id)
        else:
            messages.error(request, 'Comment text cannot be empty!')
            return redirect('post_detail', post_id=post_id)
    else:
        return redirect('post_detail', post_id=post_id)


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            Post.objects.create(
                author_id=request.session['user_id'], title=post.title, content=post.content).save()
            messages.success(request, 'Post added successfully!')
            return redirect('/post_list/')
        else:
            messages.error(request, 'Invalid form submission!')
            return render(request, 'job/posts.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'job/posts.html', {'form': form})

from django.core.paginator import Paginator
def post_list(request):
    page = request.GET.get('page', 1)   # 获取页码,默认第一页
    paginator = Paginator(Post.objects.all(), 1)  # 每页5条记录
    posts = paginator.page(page)
    
    return render(request, 'job/post_list.html', {
        'posts': posts,
        'paginator': paginator
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'job/post_detail.html', {'post': post})
