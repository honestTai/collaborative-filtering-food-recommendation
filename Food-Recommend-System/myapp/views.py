import numpy as np
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import models
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from django.utils.timezone import now
from django.template.defaultfilters import date as date_filter
from .models import Users, Foods, Comment, Wishlist, CateAnalysis, CollectAnalysis, CommentAnalysis, WordAnalysis # 确保导入您的用户模型
from FoodRecommend import settings
import json, re
from sklearn.metrics.pairwise import cosine_similarity


# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            # 检查输入
            if not username or not password:
                return JsonResponse({'success': False, 'message': "用户名和密码不能为空！"})
            
            # 获取用户对象
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                return JsonResponse({'success': False, 'message': "用户名不存在！"})
            
            # 验证密码
            if check_password(password, user.password):
                # 登录成功，将用户ID存入session
                request.session["user_id"] = user.id
                return JsonResponse({'success': True, 'message': "登录成功!"})
            else:
                return JsonResponse({'success': False, 'message': "用户名或密码错误！"})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "请求数据格式错误！"})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"登录失败，请稍后重试！{str(e)}"})

def logout(request):
    request.session.flush()
    return redirect('login')
        
def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirmpassword = data.get("confirmpassword")

        try:
            # 检查输入
            if not username or not password or not email or not confirmpassword:
                return JsonResponse({'success': False, 'message': "所有字段都是必需的！"})

            # 检查用户名长度和格式
            if len(username) < 3:
                return JsonResponse({'success': False, 'message': "用户名至少需要 3 个字符！"})
            if not re.match(r'^[\w.@+-]+$', username):
                return JsonResponse({'success': False, 'message': "用户名只能包含字母、数字和一些特殊字符！"})

            # 检查密码强度
            if len(password) < 8:
                return JsonResponse({'success': False, 'message': "密码至少需要 8 个字符！"})
            if password != confirmpassword:
                return JsonResponse({'success': False, 'message': "两次输入的密码不匹配！"})

            # 检查邮箱格式
            if not re.match(r'^[\w.+-]+@[\w-]+\.[\w.-]+$', email):
                return JsonResponse({'success': False, 'message': "无效的邮箱地址！"})

            # 检查用户名和邮箱是否已存在
            if Users.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': "用户名已被占用！"})
            if Users.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': "邮箱已被注册！"})

            # 创建新用户
            user = Users(
                username=username,
                email=email,
                password=make_password(password)  # 使用 make_password 处理密码
            )
            user.save()
            return JsonResponse({'success': True, 'message': "注册成功！"})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': "请求数据格式错误！"})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f"注册失败，请稍后重试！{str(e)}"})
        
def index(request):
    # 获取每种食物类型的第一个食物
    first_foods = Foods.objects.filter(
        id=Subquery(
            Foods.objects.filter(foodtype=OuterRef('foodtype'))
            .order_by('id')
            .values('id')[:1]  # 取第一个食物
        )
    )
    return render(request, 'index.html', {'first_foods': first_foods})

def list(request):
    food_type = request.GET.get('type', None)  # 获取筛选的类型
    food_queryset = Foods.objects.all()  # 默认获取所有菜品

    if food_type:
        food_queryset = food_queryset.filter(foodtype=food_type)  # 按类型筛选

    paginator = Paginator(food_queryset, 16)  # 每页显示16个菜品
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'food-list.html', {'page_obj': page_obj})


def get_user_favorites(user_id):
    # 获取用户收藏的菜品
    wishlist_items = Wishlist.objects.filter(user_id=user_id)
    food_ids = wishlist_items.values_list('food_id', flat=True)
    foods = Foods.objects.filter(id__in=food_ids)
    return foods


def get_all_foods():
    # 获取所有的菜品
    all_foods = Foods.objects.all()
    return all_foods


def construct_matrix(foods):
    # 构建基于价格和分类的矩阵
    data = {
        'food_id': [],
        'price': [],
        'foodtype': []
    }
    for food in foods:
        data['food_id'].append(food.id)
        data['price'].append(food.price)
        data['foodtype'].append(food.foodtype)

    df = pd.DataFrame(data)
    return df


def recommend_foods(user_id, top_n=100):
    # 获取用户收藏的菜品
    favorite_foods = get_user_favorites(user_id)

    # 获取所有菜品
    all_foods = get_all_foods()

    # 构建所有菜品的矩阵
    all_food_matrix = construct_matrix(all_foods)

    # 构建用户收藏的菜品矩阵
    favorite_food_matrix = construct_matrix(favorite_foods)

    # 先处理数值型数据
    price_matrix = pd.pivot_table(all_food_matrix, index='food_id', values='price', aggfunc='mean').fillna(0)

    # 确保价格矩阵是浮动类型数据
    price_matrix = price_matrix.astype(float)

    # 处理非数值型数据
    category_matrix = pd.get_dummies(all_food_matrix.set_index('food_id')['foodtype']).groupby('food_id').mean()

    # 确保分类矩阵是浮动类型数据
    category_matrix = category_matrix.astype(float)

    # 检查两个矩阵的形状
    print("Price matrix shape:", price_matrix.shape)
    print("Category matrix shape:", category_matrix.shape)

    # 合并数值型和非数值型数据
    # 使用 'inner' join 以确保只有共同的 food_id 被保留
    all_food_matrix_combined = pd.concat([price_matrix, category_matrix], axis=1, join='inner')

    # 确保所有值都是数值型
    all_food_matrix_combined = all_food_matrix_combined.apply(pd.to_numeric, errors='coerce').fillna(0)

    # 获取用户收藏的菜品矩阵
    favorite_food_matrix_combined = pd.concat(
        [pd.pivot_table(favorite_food_matrix, index='food_id', values='price', aggfunc='mean').fillna(0),
         pd.get_dummies(favorite_food_matrix.set_index('food_id')['foodtype']).groupby('food_id').mean()], axis=1,
        join='inner')

    favorite_food_matrix_combined = favorite_food_matrix_combined.apply(pd.to_numeric, errors='coerce').fillna(0)

    # 计算所有菜品的相似度矩阵
    food_similarity = cosine_similarity(all_food_matrix_combined)

    # 将相似度矩阵转为 DataFrame 以便处理
    food_similarity_df = pd.DataFrame(food_similarity, index=all_food_matrix_combined.index,
                                      columns=all_food_matrix_combined.index)

    # 获取当前用户收藏菜品的相似度得分
    favorite_food_ids = favorite_food_matrix_combined.index.tolist()
    similar_scores = food_similarity_df.loc[favorite_food_ids].mean(axis=0)

    # 将所有菜品的相似度得分转化为 DataFrame
    scores_df = pd.DataFrame(similar_scores, columns=['score'])

    # 排除用户已经收藏的菜品
    scores_df = scores_df[~scores_df.index.isin(favorite_food_ids)]

    # 获取评分最高的前 N 个菜品的 food_id
    top_food_ids = scores_df.sort_values(by='score', ascending=False).head(top_n).index

    # 使用 food_id 从数据库中获取菜品信息
    recommended_foods = Foods.objects.filter(id__in=top_food_ids)
    # 将相似度分数附加到每个推荐的菜品上
    recommended_foods_with_score = []
    for food in recommended_foods:
        score = scores_df.loc[food.id, 'score'] if food.id in scores_df.index else 0
        recommended_foods_with_score.append({
            'food': food,
            'score': score
        })

    return recommended_foods_with_score



def recommend(request):
    user_id = request.session.get('user_id')
    recommended_foods = None
    if user_id:
        recommended_foods = recommend_foods(user_id)

    if recommended_foods is not None:
        paginator = Paginator(recommended_foods, 16)  # 每页显示16个菜品
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'food-recommend.html', {'page_obj': page_obj})

    return render(request, 'food-recommend.html', {'error': 'No recommendations available.'})

def search_list(request):
    search_query = request.GET.get('search', None)  # 获取前端的搜索关键词

    # 默认获取所有菜品
    food_queryset = Foods.objects.all()

    # 如果搜索关键词存在，则首先根据foodname进行筛选
    if search_query:
        food_queryset = food_queryset.filter(models.Q(foodname__icontains=search_query) | models.Q(recommend__icontains=search_query))
    # 分页处理，每页16个菜品
    paginator = Paginator(food_queryset, 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search-list.html', {'page_obj': page_obj})

def detail(request, foodid):
    foodobj = Foods.objects.get(id=foodid)  # 获取食物对象

    # 获取评论并分页
    commentlist = Comment.objects.filter(fid=foodid).order_by('-ctime')  # 按时间降序排列
    paginator = Paginator(commentlist, 7)  # 每页显示7条评论
    page_number = request.GET.get('page')
    comments_paginated = paginator.get_page(page_number)  # 获取当前页的评论

    is_wishlist = False

    user_id = request.session.get('user_id')
    if user_id:
        is_wishlist = Wishlist.objects.filter(user_id=user_id, food=foodobj).exists()

    context = {
        'foodinfo': foodobj,
        'commentlist': comments_paginated,  # 使用分页后的评论列表
        'is_wishlist': is_wishlist,
    }

    return render(request, 'detail.html', context)

def add_comment(request, foodid):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            realname = request.POST.get('realname', '').strip()  # 获取 realname 并去除空白字符
            if not realname:  # 如果没有输入姓名，则使用“匿名用户”
                realname = '匿名用户'
            content = request.POST.get('comment')
            if content:
                ctime = timezone.now()  # 获取当前时间
                Comment.objects.create(uid=user_id, fid=foodid, realname=realname, content=content, ctime=ctime)

                # 格式化时间
                formatted_time = date_filter(ctime, "Y年n月j日 H时i分")
                
                # 返回新评论信息
                return JsonResponse({
                    'success': True,
                    'message': '评论提交成功！',
                    'comment': {
                        'realname': realname,
                        'content': content,
                        'ctime': formatted_time
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': '评论内容不能为空！'})
        else:
            return JsonResponse({'success': False, 'message': '请先登录！'})
    return JsonResponse({'success': False, 'message': '请求方式不正确！'})

def add_to_wishlist(request, foodid):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '请先登录.'})

    food = Foods.objects.get(id=foodid)
    Wishlist.objects.create(user_id=user_id, food=food)
    return JsonResponse({'success': True, 'message': '成功收藏.'})

def remove_from_wishlist(request, foodid):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': '请先登录.'})

    wishlist_item = Wishlist.objects.filter(user_id=user_id, food_id=foodid).first()
    if wishlist_item:
        wishlist_item.delete()
        return JsonResponse({'success': True, 'message': '已从愿望清单移除.'})

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from myapp.models import Users

def user_view(request):
    user = None  # 初始化 user 变量，以防在 GET 请求时没有被定义
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        if not user_id:
            return JsonResponse({'success': False, 'message': '请先登录.'})

        user = Users.objects.get(id=user_id)

        user.email = request.POST.get('email')  # 确保使用 'email'
        user.phone = request.POST.get('phone')
        user.info = request.POST.get('info')

        avatar = request.FILES.get('avatar')
        if avatar:
            static_path = settings.BASE_DIR / 'static' / 'image' / 'headers'
            static_path.mkdir(parents=True, exist_ok=True)
            filename = static_path / avatar.name
            with open(filename, 'wb+') as destination:
                for chunk in avatar.chunks():
                    destination.write(chunk)
            user.face = 'image/headers/' + avatar.name
        
        user_data = {
            'email': user.email,
            'phone': user.phone,
            'info': user.info,
            'face': user.face
        }

        user.save()
        return JsonResponse({'success': True, 'message': '修改成功!', 'user': user_data})

    if user_id:
        user = Users.objects.get(id=user_id)

    return render(request, 'user-view.html', {'user': user})


def change_password(request):
    user = None  # 初始化 user 变量，以防在 GET 请求时没有被定义
    user_id = request.session.get('user_id')

    if request.method == 'POST':
        if not user_id:
            return JsonResponse({'success': False, 'message': '请先登录.'})
        
        user = Users.objects.get(id=user_id)

        init_password = request.POST.get('init_password')
        current_password = request.POST.get('current_password')
        confirm_password = request.POST.get('confirm_password')
        if not init_password:
            return JsonResponse({'success': False, 'message': '请先输入原先密码.'})
        if check_password(init_password,user.password):
            if current_password and confirm_password:
                if current_password == confirm_password:
                    user.password = make_password(current_password)
                    user.save()
                    return JsonResponse({'success': True, 'message': '密码修改成功！'})
                return JsonResponse({'success': False, 'message': '请保证两次密码输入一致！'})
            return JsonResponse({'success': False, 'message': '新密码不能为空！'})
        return JsonResponse({'success': False, 'message': '原密码输入错误！'})
    
    if user_id:
        user = Users.objects.get(id=user_id)
    return render(request, 'change-password.html')

from django.shortcuts import render
from django.core.serializers import serialize
from .models import CateAnalysis, CommentAnalysis, CollectAnalysis

def analysis(request):
    # 获取数据
    cate_object = CateAnalysis.objects.all()
    comment_object = CommentAnalysis.objects.all()
    collect_object = CollectAnalysis.objects.all()
    wordcloud_object = WordAnalysis.objects.all()

    # 处理数据为可以传递给前端的格式
    cate = [[],[]]
    comment = [[], []]
    collect = [[], []]
    wordcloud = [[],[],[]]

    for cate_object_item in cate_object:
        cate[0].append(cate_object_item.cate_num)
        cate[1].append(cate_object_item.cate_list)

    for comment_object_item in comment_object:
        comment[0].append(comment_object_item.comment_num)
        comment[1].append(comment_object_item.comment_list)
    
    for collect_object_item in collect_object:
        collect[0].append(collect_object_item.collect_num)
        collect[1].append(collect_object_item.collect_list)

    for wordcloud_object_item in wordcloud_object:
        wordcloud[0].append(wordcloud_object_item.name)
        wordcloud[1].append(wordcloud_object_item.value)
        wordcloud[2].append(wordcloud_object_item.foodtype)

    # 将数据传递到模板，使用 serialize 序列化数据为 JSON 格式
    context = {
        "cate": cate,
        "comment": comment,
        "collect": collect,
        "wordcloud": wordcloud
    }

    return render(request, 'analysis.html', context)

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Wishlist, Foods

def favorite(request):
    # 获取当前用户的 user_id
    user_id = request.session.get('user_id')

    if not user_id:
        # 如果用户未登录，重定向到登录页面
        return redirect('login')

    # 获取用户收藏的所有食物
    wishlist_items = Wishlist.objects.filter(user_id=user_id)

    # 获取食物的详细信息
    food_ids = wishlist_items.values_list('food_id', flat=True)
    foods = Foods.objects.filter(id__in=food_ids)

    # 分页处理
    paginator = Paginator(foods, 7)  # 每页显示7个食物
    page_number = request.GET.get('page')
    foods_paginated = paginator.get_page(page_number)  # 获取当前页的食物

    context = {
        'foods': foods_paginated,  # 分页后的食物列表
    }

    return render(request, 'favorite.html', context)



