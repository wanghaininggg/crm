from django.shortcuts import render, redirect
from kingadmin import kingadmin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .table import table_filter, get_list_filter, table_sort, table_search
from .forms import create_model_form
# Create your views here.
def index(request):
    return render(request, 'kingadmin\index.html', {'display_list': kingadmin.enabled_admins})


def display_tables(request, app_name, tables_name):
    
    admin_class = kingadmin.enabled_admins[app_name][tables_name]
    filters = get_list_filter(request, admin_class)
    object_list, filter_condtions = table_filter(request, admin_class)
    object_list = table_search(request, admin_class, object_list)
    object_list, orderby_key = table_sort(request, object_list)
    paginator = Paginator(object_list, admin_class.list_per_page)
    page = request.GET.get('page', 1)
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        query_sets = paginator.page(1)
    except EmptyPage:
        query_sets = paginator.page(paginator.num_pages)
    return render(request, 'kingadmin/table_obj.html', {'admin_class': admin_class, 
                                                        'query_sets': query_sets, 
                                                        'filter_contions': filter_condtions, 
                                                        'filters': filters, 
                                                        'orderby_key': orderby_key,
                                                        'previous_orderby': request.GET.get("o", ''),
                                                        'previous_search': request.GET.get("q", '')})


def table_obj_change(request, app_name, tables_name, obj_id):

    admin_class = kingadmin.enabled_admins[app_name][tables_name]
    model_form = create_model_form(request, admin_class)
    obj = admin_class.model.objects.get(id=obj_id)  
    if request.method == 'POST':
        form = model_form(request.POST, instance=obj)    # 更新
        if form.is_valid():
            form.save()      
    else:
        form = model_form(instance=obj)  # 渲染已有数据到修改网页
    return render(request, "kingadmin/table_obj_change.html", {'form': form, 'admin_class': admin_class})


def table_obj_add(request, app_name, tables_name):
    '''    增加字段    '''
    admin_class = kingadmin.enabled_admins[app_name][tables_name]
    model_form = create_model_form(request, admin_class)
    
    if request.method == 'POST':
        form = model_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.path.replace("/add", "/"))
        else:
            return render(request, "kingadmin/table_obj_change.html", {'form': form, 'admin_class': admin_class})
    else:
        form = model_form()
    return render(request, "kingadmin/table_obj_add.html", {'form': form, 'admin_class': admin_class})
