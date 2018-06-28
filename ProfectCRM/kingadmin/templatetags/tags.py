from django import template
from django.utils.safestring import mark_safe
from crm import models
register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(request, obj, admin_class):
    '''    生成主信息表    '''
    row_ele = ""
    for index, column in enumerate(admin_class.list_display):
        fidld_obj = obj._meta.get_field(column)
        if fidld_obj.choices:
            column_data = getattr(obj, "get_%s_display" % column)()
        else:
            column_data = getattr(obj, column)
        if 'DateTimeField' in fidld_obj.__repr__():
            column_data  = getattr(obj, column).strftime('%Y-%m-%d %H:%M:%S')
        if index == 0:
            column_data = "<a href='{request_path}{obj_id}/change'>{data}</a>".format(request_path=request.path, obj_id=obj.id, data=column_data)
        row_ele += "<td>%s</td>" % column_data
    return mark_safe(row_ele)


# @register.simple_tag
# def render_filter_ele(conditon, admin_class, filter_conditons):
#     row_ele = ""
#     sets = admin_class.model.objects.all().distinct().values(conditon)
#     row_ele += '<select name="%s" class="form-control"><option value=''>----</option>' % conditon
#     for i in sets:
#         if i[conditon] == filter_conditons.get(conditon, None):
#             row_ele += "<option value='%s' selected='selected'>%s</option>" % (i[conditon], i[conditon])
#         else:
#             row_ele += "<option value='%s'>%s</option>" % (i[conditon], i[conditon])
#     row_ele += '</select>'
#     return mark_safe(row_ele)

@register.simple_tag
def render_filter_ele(fil):
    '''    生成顶部筛选    '''
    ele = '''<div class = "col-lg-2"><span>%s</span><select name="%s" class="form-control">''' % (fil['verbose_name'], fil['column_name'])
    for i in fil['choices']:
        if str(i[0]) == fil.get('selected', None):
            ele += '''<option value='%s' selected='selected'>%s</option>''' % (i[0], i[1])
        else:
            ele += '''<option value='%s'>%s</option>''' % (i[0], i[1])
    ele += '''</select></div>'''
    return mark_safe(ele)


# @register.simple_tag
# def render_page_ele(loop_counter, query_sets, filter_conditons):
#     fil = ''
#     for k, v in filter_conditons.items():
#         fil += '&%s=%s' % (k, v)
#     if loop_counter == query_sets.number:
#         ele = '''<li class="active"><a href="?page=%s%s">%s</a></li>''' % (
#             loop_counter, fil, loop_counter)
#     else:
#         ele = '''<li><a href="?page=%s%s">%s</a></li>''' % (loop_counter, fil, loop_counter)
#     return mark_safe(ele)


@register.simple_tag
def build_painators(query_sets, filter_conditons, previous_orderby, previous_search):
    '''    生成分页器    '''
    fil = ''
    for k, v in filter_conditons.items():
        fil += '&%s=%s' % (k, v)
    page_btns = []
    added_dot_ele = False
    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages - 2 or abs(query_sets.number-page_num) <= 2:
            ele_class = ''
            if query_sets.number == page_num:
                added_dot_ele = False
                ele_class = 'active'
            page_btns.append('''<li class="%s"><a href="?page=%s%s&o=%s&q=%s">%s</a ></li> ''' %
                             (ele_class, page_num, fil, previous_orderby, previous_search,page_num, ))
        else: 
            if added_dot_ele == False:
                page_btns.append('<li><a>...</a></li>')
                added_dot_ele = True
    page_btns = ''.join(page_btns)
    return mark_safe(page_btns)


@register.simple_tag
def build_table_header_column(column, orderby_key, filter_conditons):
    fil = ''
    for k, v in filter_conditons.items():
        fil += '&%s=%s' % (k, v)
    ele = '''<th><a href="?{fil}&o={orderby_key}">{column}</a>{sort_icon}</th>'''
   
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class='glyphicon glyphicon-menu-up'></span>'''
        else:
            sort_icon = '''<span class='glyphicon glyphicon-menu-down'></span>'''
        if orderby_key.strip('-') == column:
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ''
    else:
        orderby_key = column
        sort_icon = ''
    return mark_safe(ele.format(orderby_key=orderby_key, column=column, sort_icon=sort_icon, fil=fil))

@register.simple_tag
def display_orderby_arrow():
    ele = '''<span class='glyphicon glyphicon-menu-down'></span>'''
    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_m2m_obj_list(admin_class, field, form):
    '''返回M2M待选数据'''
    # 表结构对象的某个字段
    field_obj = getattr(admin_class.model, field.name)
    all_obj_list = field_obj.rel.model.objects.all()
    #已选中的
    if form.instance.id:
        selected_field_list = getattr(form.instance, field.name).all()
    else:
        return all_obj_list
    standby_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_field_list:
            standby_obj_list.append(obj)
    return standby_obj_list

@register.simple_tag
def get_m2m_selected_list(form, field):
    ''' 返回已选择的M2M数据'''
    if form.instance.id:
        field_obj = getattr(form.instance, field.name)
        return field_obj.all()
