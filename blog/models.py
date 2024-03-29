from django.db import models
from django.contrib.auth.models import User

import mistune
# Create your models here.


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否是导航')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        nomal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                nomal_categories.append(cate)
        return {
            'navs': nav_categories,
            'categories': nomal_categories,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除')
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 访问量（PageView页面浏览量或点击量）
    pv = models.PositiveIntegerField(default=1, verbose_name='访问量')
    # 独立访问量（Unique Visitor 访问网站的一台电脑客户端为一个访客）
    uv = models.PositiveIntegerField(default=1, verbose_name='独立访问量')

    # 存储content经过markdown处理后的内容, 不可编辑，因为非人为处理
    content_html = models.TextField(blank=True, editable=False, verbose_name='正文html代码')

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']   # 根据id降序排列
        # 引入静态资源
        # css = {'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',)}
        # js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            # 使用select_related解决一对多的N+1查询问题
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner', 'category')
        return post_list, category

    @classmethod
    def lasted_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    # 最热文章
    @classmethod
    def host_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).only('id', 'title').order_by('-pv')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.content_html = mistune.markdown(self.content)
        super(Post, self).save(force_insert=False, force_update=False,
                               using=None, update_fields=None)

