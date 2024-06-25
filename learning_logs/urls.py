"""定义 learning_logs 的 URL 模式"""
from django.urls import path # 用于将URL映射到views
from . import views # 注意当前文件夹是learning log

app_name = 'learning_logs' # 区分同名文件urls.py
urlpatterns = [ # 包含在App learning_logs中请求的网页
    # 主页
    path('', views.index, name='index'), 
    # 第一个参数是route，也就是网址；第二个指定view.py中的index函数；
    # 第三个命名为index代替url，方便后序引用。例如base.html
    path('topics/', views.topics, name='topics'),
    # 特定topic的详细页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    
    # 用于用户添加新主题的网页
    path('new_topic/', views.new_topic, name="new_topic"),
]