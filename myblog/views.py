import markdown
import requests
import datetime
import threading
import random
import json
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from pure_pagination import PageNotAnInteger, Paginator
from haystack.views import SearchView

from blog.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
from myblog.models import Blog, Category, Tag, Comment, Counts, PicTest
from myblog.forms import CommentForm



class IndexView(View):
    """
    首页
    """
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-id')
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        count_nums.save()

        for blog in all_blog:
            blog.content = markdown.markdown(blog.content)
            blog.content = blog.content[0:136]
            blog.content = blog.content + " ..."
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blog, 3, request=request)
        all_blog = p.page(page)
        return render(request, 'index.html', {
            'all_blog': all_blog,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
        })


class ArichiveView(View):
    """
    归档
    """
    def get(self, request):
        all_blog = Blog.objects.all().order_by('-create_time')
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_blog, 10, request=request)
        all_blog = p.page(page)

        return render(request, 'archive.html', {
            'all_blog': all_blog,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,

        })


class TagView(View):
    """
    标签云
    """
    def get(self, request):
        all_tag = Tag.objects.all()
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        return render(request, 'tags.html', {
            'all_tag': all_tag,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,
        })


class TagDetailView(View):
    """
        标签下的所有博客
        """
    def get(self, request, tag_name):
        tag = get_object_or_404(Tag, name=tag_name)
        tag_blogs = tag.blog_set.all()
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(tag_blogs, 10, request=request)
        tag_blogs = p.page(page)
        return render(request, 'tag-detail.html', {
            'tag_blogs': tag_blogs,
            'tag_name': tag_name,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,

        })


class BlogDetailView(View):
    """
    博客详情页
    """
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums
        # 博客点击数+1, 评论数统计
        blog.click_nums += 1
        blog.save()
        #获取评论内容
        all_comment = Comment.objects.filter(blog_id=blog_id)
        comment_nums = all_comment.count()
        # 将博客内容用markdown显示出来
        blog.content = markdown.markdown(blog.content)
        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(blog_id)
        blog_id_max = Blog.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        while not has_prev and id_prev >= 1:
            blog_prev = Blog.objects.filter(id=id_prev - 1).first()
            if not blog_prev:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            blog_next = Blog.objects.filter(id=id_next + 1).first()
            if not blog_next:
                id_next += 1
            else:
                has_next = True;

        return render(request, 'blog-detail.html', {
            'blog': blog,
            'blog_prev': blog_prev,
            'blog_next': blog_next,
            'has_prev': has_prev,
            'has_next': has_next,
            'all_comment': all_comment,
            'comment_nums': comment_nums,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,

        })


class AddCommentView(View):
    """
    评论
    """
    def post(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class CategoryDetaiView(View):
    """
    博客分类
    """
    def get(self, request, category_name):
        category = get_object_or_404(Category, name=category_name)
        cate_blogs = category.blog_set.all()
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)
        blog_nums = count_nums.blog_nums
        cate_nums = count_nums.category_nums
        tag_nums = count_nums.tag_nums

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(cate_blogs, 2, request=request)
        cate_blogs = p.page(page)

        return render(request, 'category-detail.html', {
            'cate_blogs': cate_blogs,
            'category_name': category_name,
            'blog_nums': blog_nums,
            'cate_nums': cate_nums,
            'tag_nums': tag_nums,

        })


class MySearchView(SearchView):
    """
    复用搜索源码，将其余内容添加进来
    """
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        # 博客、标签、分类数目统计
        count_nums = Counts.objects.get(id=1)

        context['cate_nums'] = count_nums.category_nums
        context['tag_nums'] = count_nums.tag_nums
        context['blog_nums'] = count_nums.blog_nums
        return context

    def build_page(self):
        #分页重写
        super(MySearchView, self).extra_context()

        try:
            page_no = int(self.request.GET.get('page', 1))
        except PageNotAnInteger:
            raise HttpResponse("Not a valid number for page.")

        if page_no < 1:
            raise HttpResponse("Pages should be 1 or greater.")


        paginator = Paginator(self.results, HAYSTACK_SEARCH_RESULTS_PER_PAGE, request=self.request)
        page = paginator.page(page_no)

        return (paginator, page)


def pic_show(request, id):

    pic = PicTest.objects.get(pk=id)
    context = {'pic': pic}
    return render(request, 'pic_show.html', context)

def listenMyMusic(request):

    music_name = request.POST.get("music")
    print("搜索的歌名{0}".format(music_name))

    headers = {

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/85.0.4183.102 Safari/537.36",
        "Cookie": "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1600350844; _ga=GA1.2.97377989.1600350844; _"
                  "gid=GA1.2.457605519.1600350844; gtoken=vMWeZ4vagWbM; "
                  "gid=2f544fca-5915-4a8a-be29-fda86e9daf20; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1600353178; "
                  "kw_token=HTBQ3W7JRRP",
        "Referer": "http://www.kuwo.cn/search/list?key=%E5%BD%92%E5%8E%BB%E6%9D%A5%E5%85%AE",
        "csrf": "HTBQ3W7JRRP",
    }
    params = {
        "key": music_name,
        "pn": "1",
        "rn": "10",
        "httpsStatus": "1",
        "reqId": "cc337fa0-e856-11ea-8e2d-ab61b365fb50",
    }
    url = "http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"
    # response = apishop_send_request('get', url=url, params=params, headers=headers)
    response = requests.request('get',url=url,params=params,headers=headers)
    response.encoding = "utf-8"
    text = response.text
    json_list = json.loads(text)
    print(json_list)
    if json_list['code'] == 200:
        music_data = json_list["data"]["list"]
        music_list = []
        for i in music_data:
            music_name = i["name"]

            music_singer = i["artist"]

            rid = i["rid"]

            api_music = "http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_" \
                        "url3&br=128kmp3&from=web&t=1600358748184&httpsStatus=1&" \
                        "reqId=a67e85c0-f8ff-11ea-9aba-3f184fbead08".format(rid)

            api_res = requests.get(url=api_music)

            music_url = json.loads(api_res.text)["url"]

            print("歌名：%s  \t\t 歌手：%s" % (music_name, music_singer))
            music_dict = {}
            music_dict["name"] = music_name
            music_dict["url"] = music_url
            music_dict["singer"] = music_singer
            music_list.append(music_dict)
            print(music_list)
        return render(request, 'music.html', {"music_list": music_list})
    else:
        return render(request, 'music.html')

def MyStep(request):
    """
    刷步数
    :param request:
    :return:
    """
    # 获取现在时间
    now_time = datetime.datetime.now()
    print(now_time)
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天5点时间
    next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 17:00:00",
                                           "%Y-%m-%d %H:%M:%S")
    print(next_time)
    # # 获取昨天时间
    # last_time = now_time + datetime.timedelta(days=-1)

    # 获取距离明天3点时间，单位为秒
    timer_start_time = (next_time - now_time).total_seconds()
    print(timer_start_time)

    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, my_request)
    timer.start()

    return HttpResponseRedirect("music/")

def my_request():

    print("开始了")
    keep_step = random.randint(28000, 35000)
    url = "https://api.rncen.com/API/WX/xm1.php"
    header = {
        "Content-Length": " 46",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    body = {
        "phone": "18890307035",
        "password": "2014abcd",
        "step": keep_step
    }
    response = requests.post(url,data=body)
    print(keep_step)
    print(response.text)

    timer = threading.Timer(86400, my_request)
    timer.start()


#配置404 500错误页面
def page_not_found(request):
    return render(request, '404.html')


def page_errors(request):
    return render(request, '500.html')