from django.utils import timezone
from django.db.models import Count, Q
import time


def table_filter(request, admin_class):
    '''   进行条件查询并返回过滤后的数据   '''
    filter_conditions = {}
    keywords = ['page', 'o', 'q']
    for k, v in request.GET.items():
        if k in keywords:      # page 分页关键字 o排序关键字
            continue
        if v:
            filter_conditions[k] = v
    return admin_class.model.objects.filter(**filter_conditions).order_by("-%s" % admin_class.ordering if admin_class.ordering else "-id"), filter_conditions


# def table_sort(request, objs):
#     orderby_key = request.GET.get('o')
#     flag = True
#     if orderby_key:
#         res = objs.order_by(orderby_key)
#         if orderby_key.startswith('-'):
#             flag = True
#         else:
#             flag = False
#         return objs.order_by(orderby_key), flag
#     return objs, flag


def table_sort(request, objs):
    orderby_key = request.GET.get('o', None)
    if orderby_key:
        res = objs.order_by(orderby_key)
        if orderby_key.startswith('-'):
            orderby_key = orderby_key.strip('-')
        else:
            orderby_key = '-%s' % (orderby_key)
    else:   
        res = objs
    return res, orderby_key


def get_list_filter(request, admin_class):
    '''
    获取分类的choices
    '''
    filters = []
    for i in admin_class.list_filters:
        col_obj = admin_class.model._meta.get_field(i)
        data = {
            'verbose_name': col_obj.verbose_name,
            'column_name': i
        }
        if col_obj.deconstruct()[1] not in ('django.db.models.DateField', 'django.db.models.DateTimeField'):
            try:
                choices = col_obj.get_choices()
            except AttributeError as e:
                choices_list = col_obj.model.objects.values(i).annotate(count=Count(i))
                choices = [[obj[i], obj[i]] for obj in choices_list]
                choices.insert(0, ['', '----------'])
        else:
            data['column_name'] = i+'__gte'
            today_obj = timezone.datetime.now()
            choices = [
                ('', '--------'),
                (today_obj.strftime("%Y-%m-%d"), '今天'),
                ((today_obj - timezone.timedelta(days=3)).strftime("%Y-%m-%d"), '过去3天'),
                ((today_obj - timezone.timedelta(days=7)).strftime("%Y-%m-%d"), '过去7天'),
                ((today_obj - timezone.timedelta(days=today_obj.day)).strftime("%Y-%m-%d"), '本月'),
                ((today_obj - timezone.timedelta(days=90)).strftime("%Y-%m-%d"), '过去90天'),
                ((today_obj - timezone.timedelta(days=180)).strftime("%Y-%m-%d"), '过去180天'),
                ((today_obj - timezone.timedelta(days=365)).strftime("%Y-%m-%d"), '过去365天'),
                ((today_obj - timezone.timedelta(seconds=time.time())).strftime("%Y-%m-%d"), '所有'),
            ]
        data['choices'] = choices
        if request.GET.get(i):
            data['selected'] = request.GET.get(i)
        filters.append(data)
    return filters


def table_search(request, admin_class, object_list):
    '''搜索'''
    search_key = request.GET.get('q', '')
    q_obj = Q()
    q_obj.connector = 'OR'
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains" % column, search_key))
    res = object_list.filter(q_obj)
    return res
