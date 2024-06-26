from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model): # Model是Django基本类
    """用户学习主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
    
class Entry(models.Model):
    """学习到的有关某个主题的某个知识"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # 外键实例。指向数据库的另一条记录（把条目关联到主题）
    # CASCADE 级联删除，删除Topic，把所有相关Entries都删掉
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # 注意DateTimeField和DateField的区别，前者包含时间，后者只有日期
    
    class Meta: # 用于管理额外信息
        verbose_name_plural = 'entries' # 表示多个条目，默认会是Entry，不符合英语语法

    def __str__(self):
        """返回表示条目entry的简单字符串（只显示前50词）"""
        return f"{self.text[:50]}..."