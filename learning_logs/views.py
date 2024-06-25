from django.shortcuts import render, redirect # 用于渲染，重定向

# Create your views here.
from .models import Topic # 从当前文件夹的models.py中导入Topic类
from .forms import TopicForm

def index(request): # urlpattern匹配到对应网址后，来这里调用函数
    """学习笔记主页"""
    return render(request, 'learning_logs/index.html')
    # 两个参数：对象request， 网页模板
    
def topics(request):
    """显示所有主题"""
    topics = Topic.objects.order_by('date_added') # 从数据库中获取所有主题
    context = {'topics': topics} # 传递给模板的数据
    # 前一个对应models.py中的Topic类，后一个对应topics.html中的{{ topics }}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """显示单个topic以及所有entry"""
    # 查询
    topic = Topic.objects.get(id=topic_id) # 获取指定id的topic
    entries = topic.entry_set.order_by('date_added') # 先展示新entry
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

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
            form.save()
            return redirect('learning_logs:topics') # 重定向到topics页面
        
    # 显示空表单或者指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
