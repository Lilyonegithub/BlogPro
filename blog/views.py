from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar

from django.views.generic import ListView, DetailView

from django.shortcuts import get_object_or_404

from django.db.models import Q


# Create your views here.
#
#
# def post_list(request, category_id=None, tag_id=None):
#     # content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
#     #     category_id=category_id,
#     #     tag_id=tag_id
#     # )
#     # return HttpResponse(content)
#     tag = None
#     category = None
#
#     # if tag_id:
#         # try:
#         #     tag = Tag.objects.get(id=tag_id)
#         # except Tag.DoesNotExist:
#         #     post_list = {}
#         # else:
#         #     post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#     # else:
#     #     post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#     #     if category_id:
#     #         try:
#     #             category = Category.objects.get(pk=category_id)
#     #         except Category.DoesNotExist:
#     #             category = None
#     #         else:
#     #             post_list = post_list.filter(category_id=category_id)
#
#     # 完善之后
#     if tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.lasted_posts()
#
#     context = {
#         'tag': tag,
#         'category': category,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, post_id=None):
#     # return HttpResponse('detail')
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)
#
#
# class PostDetail(DetailView):
#     model = Post
#     template_name = 'blog/detail1.html'
#
#
# class PostList(ListView):
#     template_name = 'blog/list.html'
#     context_object_name = 'post_list'
#     paginate_by = 2
#     queryset = Post.lasted_posts()


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


# 注意这里继承的顺序，因为二者均有get_context_data方法，如果顺序反了，
# 就不会调用CommonViewMixin的get_context_data方法，应该涉及到广度优先搜索
class IndexView(CommonViewMixin, ListView):
    queryset = Post.lasted_posts()
    paginate_by = 2
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


# 根据文章标题或文章内容筛选文章
class SearchView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        keywords = self.request.GET.get('keywords')
        if keywords:
            queryset = queryset.filter(Q(title__contains=keywords) | Q(desc__contains=keywords))
        return queryset

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keywords': self.request.GET.get('keywords', '')
        })
        return context


# 根据作者筛选文章
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        if author_id:
            queryset = queryset.filter(owner_id=author_id)
        return queryset


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.kwargs 是从url中获取来的，为字典格式，比如{'category_id': 1}
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        category = queryset.filter(category_id=category_id)
        return category


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        tag = queryset.filter(tag__id=tag_id)
        return tag


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.lasted_posts()
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'
