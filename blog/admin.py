from django.contrib import admin
from .models import Category, Tag, Post
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只展示当前用户分类 """

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        ids = Category.objects.filter(owner=request.user).values_list('id', 'name')
        print('ids:', ids)
        return ids

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(pk=category_id)
        return queryset


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']
    list_display_links = []  # 控制哪些字段以链接形式显示
    # list_filter = ['category']
    list_filter = [CategoryOwnerFilter]  # 过滤器
    search_fields = ['title', 'category__name']  # 按哪些字段进行搜索

    actions_on_top = True
    actions_on_bottom = False

    # 编辑页面
    save_on_top = True
    filter_horizontal = ('tag',)  # 控制多对多字段展示，水平filter_horizontal;垂直filter_vertical

    # exclude = ('owner',)

    # fields = [
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # ]

    # fieldsets = (
    # ('名称', {内容}),
    # ('名称', {内容}),
    # )
    fieldsets = (
        ('基础设置',
         {'description': '基础配置描述',
          'fields': (
            ('title', 'category'),
            'status',
          ),
          }),
        ('内容', {
            'fields': (
                'desc',
                'content'),
        }),
        ('额外信息', {
            'classes': 'collapse',   # wide
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>', 
            reverse('admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '操作'
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)