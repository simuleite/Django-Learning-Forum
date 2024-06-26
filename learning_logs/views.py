from django.shortcuts import render, redirect # 用于渲染，重定向
from django.contrib.auth.decorators import login_required # 用于限制访问
from django.http import Http404 # 用于处理404错误

# Create your views here.
from .models import Topic, Entry # 从当前文件夹的models.py中导入Topic类
from .forms import TopicForm, EntryForm # 导入表单类

def index(request): # urlpattern匹配到对应网址后，来这里调用函数
    """学习笔记主页"""
    return render(request, 'learning_logs/index.html')
    # 两个参数：对象request， 网页模板
    
@login_required # 限制访问，只有登陆用户才能访问topic
def topics(request):
    """显示所有主题"""
    # 从数据库中获取所有主题
    # 全部topic可见
    topics = Topic.objects.order_by('date_added') 
    # 只有topic创建者可见
    # topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics} # 传递给模板的数据
    # 前一个对应models.py中的Topic类，后一个对应topics.html中的{{ topics }}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个topic以及所有entry"""
    # 查询
    topic = Topic.objects.get(id=topic_id) # 获取指定id的topic
    # 确认请求的topic属于当前用户
    # if topic.owner != request.user:
        # raise Http404
    entries = topic.entry_set.order_by('date_added') # 先展示新entry
    context = {'topic': topic, 'entries': entries, 'owner': topic.owner}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST': # GET请求
        # 提交表单使用POST方法，GET方法用于请求数据
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else: # POST请求
        # POST提交的数据，对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid(): # 填写了所有必填字段，则合法
            new_topic = form.save(commit=False) # 不保存到数据库
            new_topic.owner = request.user # 关联当前用户
            form.save()
            return redirect('learning_logs:topics') # 重定向到topics页面
        
    # 显示空表单或者指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """特定topic下添加新entry"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # 不保存到数据库
            new_entry.topic = topic
            new_entry.save() # 保存到数据库，确保与topic关联
            return redirect('learning_logs:topic', topic_id=topic_id)
        
        # 显示空表单或者指出表单数据无效
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑现有entry"""
    # 获取entry与topic
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # if topic.owner != request.user:
        # raise Http404
    
    if request.method != 'POST':
        # 初次请求，使用当前entry填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
