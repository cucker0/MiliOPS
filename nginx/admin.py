from django.contrib import admin
from . import models


# Register your models here.

class SiteAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'site_status', 'proxy_server_group', 'upstream', 'maintain_status')
    filter_horizontal = ('real_server',)
    raw_id_fields = ('upstream',)
    search_fields = ('site_name',)
    fk_fields = ('upstream',)


class ProxyServerGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'port', 'dir')
    filter_horizontal = ('proxy_server',)


class ProxyServerAdmin(admin.ModelAdmin):
    list_display = ('host', 'apply_name')


class RealServerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'apply_name', 'host', 'port')
    search_fields = ('apply_name__tag',)        # 以__ 表示关联字段属性
    raw_id_fields = ('host','apply_name',)

class MaintainRealServerAdmin(admin.ModelAdmin):
    list_display = ('host', 'port')
    raw_id_fields = ('host',)


class MaintainGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'tag')
    filter_horizontal = ('real_server',)

class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'eth00_ip')
    search_fields = ('eth00_ip',)

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name')

class ConfigAdmin(admin.ModelAdmin):
    list_display = ('upstream_up_realserver_test', 'upstream_up_realserver_testurl')

class UpstreamAdmin(admin.ModelAdmin):
    list_display = ('upstream_name','zone')
    search_fields = ('upstream_name',)

class ApplyTagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'note',)

admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.ProxyServerGroup, ProxyServerGroupAdmin)
admin.site.register(models.ProxyServer, ProxyServerAdmin)
admin.site.register(models.Upstream, UpstreamAdmin)
admin.site.register(models.RealServer, RealServerAdmin)
admin.site.register(models.MaintainRealServer, MaintainRealServerAdmin)
admin.site.register(models.MaintainGroup, MaintainGroupAdmin)
admin.site.register(models.Host, HostAdmin)
# admin.site.register(models.UserProfile)
admin.site.register(models.Config, ConfigAdmin)
admin.site.register(models.ApplyTag, ApplyTagAdmin)