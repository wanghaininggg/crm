from crm import models

enabled_admins = {}
class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []
    list_editable = []
    readonly_fields = []
    actions = ["delete_selected_objects",]
    readonly_table = False
    modelform_exclude_fields = []
    add_form = None

class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'name', 'qq', 'phone', 'source', 'consultant', 'date', 'status']
    list_filters = ['source', 'consultant', 'status','date']
    search_fields = ['qq', 'name', 'consultant__name']
    list_per_page = 5
    ordering = 'id'
    filter_horizontal = ['tags']


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ['customer']

def register(model_class, admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}
    
    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class

register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
