from django.db import models
from datetime import datetime

# 用户模型
class Users(models.Model):
    # 用户名字段
    username = models.CharField(max_length=255, verbose_name='用户名')
    
    # 密码字段，通常会存储哈希值，因此 255 是足够的长度
    password = models.CharField(max_length=255, verbose_name='密码')
    
    # 邮箱字段，唯一性约束确保每个邮箱只能注册一次
    email = models.EmailField(unique=True, max_length=100)
    
    # 手机号字段，11 位并设置唯一性
    phone = models.CharField(unique=True, max_length=11)
    
    # 个性简介字段，允许为空
    info = models.TextField(blank=True, null=True)
    
    # 头像字段，存储头像 URL 或文件路径
    face = models.CharField(max_length=255, unique=True, blank=True, null=True)
    
    # 注册时间字段，默认当前时间，并添加索引以加快查询速度
    addtime = models.DateTimeField(default=datetime.now, db_index=True)
    
    class Meta:
        db_table = 'users'  # 指定数据库中的表名

    def __str__(self):
        return self.username  # 定义实例的字符串表示，以便在管理界面中识别

# 菜品模型
class Foods(models.Model):
    # 菜品名称字段
    foodname = models.CharField(max_length=70, verbose_name='菜品名称')
    
    # 菜品类别字段
    foodtype = models.CharField(max_length=20, verbose_name='类别')
    
    # 推荐语字段，允许为空
    recommend = models.CharField(max_length=255, null=True, verbose_name='推荐语')
    
    # 图片 URL 字段
    imgurl = models.CharField(max_length=255, verbose_name='图片 URL')
    
    # 价格字段，定义最大位数和小数位数
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='价格')

    class Meta:
        db_table = 'foods'  # 指定数据库中的表名

    def __str__(self):
        return self.foodname  # 定义实例的字符串表示

# 评论模型
class Comment(models.Model):
    # 用户 ID 字段
    uid = models.IntegerField(verbose_name='用户 ID')
    
    # 菜品 ID 字段
    fid = models.IntegerField(verbose_name='菜品 ID')
    
    # 真实姓名字段
    realname = models.CharField(max_length=11, verbose_name='真实姓名')
    
    # 评论内容字段
    content = models.TextField(verbose_name='评论内容')
    
    # 评论时间字段
    ctime = models.DateTimeField(null=True, verbose_name='评论时间')

    class Meta:
        db_table = 'comments'  # 指定数据库中的表名

    def __str__(self):
        return f"Comment by {self.realname} on Food ID {self.fid}"

# 愿望清单模型
class Wishlist(models.Model):
    # 用户外键
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户')
    
    # 菜品外键
    food = models.ForeignKey(Foods, on_delete=models.CASCADE, verbose_name='菜品')
    
    # 添加时间字段
    added_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'wishlist'  # 指定数据库中的表名
        unique_together = ('user', 'food')  # 唯一性约束

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.food.foodname}"
    
# 数据分析模型
class CateAnalysis(models.Model):
    cate_num = models.IntegerField()
    cate_list = models.CharField(max_length=50)

    class Meta:
        db_table = 'cateanalysis'  # 指定数据库中的表名

class CommentAnalysis(models.Model):
    comment_num = models.IntegerField()
    comment_list = models.CharField(max_length=50)

    class Meta:
        db_table = 'commentanalysis'  # 指定数据库中的表名

class CollectAnalysis(models.Model):
    collect_num = models.IntegerField()
    collect_list = models.CharField(max_length=50)

    class Meta:
        db_table = 'collectanalysis'  # 指定数据库中的表名

class WordAnalysis(models.Model):
    name = models.CharField(max_length=50)
    value = models.IntegerField()
    foodtype = models.CharField(max_length=20)
    class Meta:
        db_table = 'wordanalysis'  # 指定数据库中的表名

