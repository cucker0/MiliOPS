from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User     # 导入 user类

# Create your models here.

maintain_status_choices = (
    (0, '运行中'),
    (1, '维护中')
)

site_realserver_status_choices = (
    (0, '有源站下线'),
    (1, '全部源站在线'),
    (2, '状态未知')
)

bindip_host_eth_choices = (
    ('00', 'Eth0.0'),
    ('01', 'Eth0.1'),
    ('10', 'Eth1.0'),
    ('11', 'Eth1.1'),
    ('20', 'Eth2.0'),
    ('21', 'Eth2.1'),
    ('30', 'Eth3.0'),
    ('31', 'Eth3.1'),
)

class Site(models.Model):
    """
    站点
    null=True  ==>允许数据库字段为空
    blank=True  ==>允许admin后台字段为空
    """
    site_name = models.CharField('站点名', max_length=64)
    proxy_server_group = models.ForeignKey('ProxyServerGroup',related_name='group_site')
    upstream = models.ForeignKey('Upstream', related_name='upstream_site')
    real_server = models.ManyToManyField('RealServer', related_name='realserver_site', verbose_name='源站服务', null=True, blank=True)
    maintain_status = models.IntegerField('维护状态', default=0, choices=maintain_status_choices, help_text='0:运行中  1:维护中  初始值为0')
    maintain_page_group = models.ForeignKey('MaintainGroup', verbose_name='维护页面组', null=True, blank=True)
    site_realserver_status = models.SmallIntegerField('站点对应的源站聚合状态', choices=site_realserver_status_choices, default=1, help_text='0:有源站下线  1:全部源站在线  2:状态未知')
    def __str__(self):
        return self.site_name


class ProxyServerGroup(models.Model):
    """
    服务器组
    """
    group_name = models.CharField('proxy server组名', max_length=64)
    proxy_server = models.ManyToManyField('ProxyServer', related_name='proxyserver_proxyservergroup', verbose_name='Nginx代理服务实例', null=True, blank=True)
    port = models.BigIntegerField('Dynamic Upstream控制端口',default=17818)
    dir = models.CharField('Dynamic Upstream控制目录', max_length=64,default='du')
    user = models.CharField('Dynamic Upstream登录用户', max_length=64, default='user')
    pwd = models.CharField('Dynamic Upstream登录密码', max_length=64, default='password')
    tag = models.CharField('标签',max_length=20, null=True)

    def __str__(self):
        return self.group_name


class ProxyServer(models.Model):
    """
    服务器列表
    """
    apply_name = models.ForeignKey('ApplyTag', verbose_name='应用名', null=True, blank=True)
    host = models.ForeignKey('Host',verbose_name='主机')
    bindip_host_eth = models.CharField('主机服务绑定IP的网卡', max_length=2, choices=bindip_host_eth_choices, default='00')

    def __str__(self):
        return self.host.name


class Upstream(models.Model):
    """
    upstream集群
    """
    upstream_name = models.CharField('upstream name', max_length=64)
    zone = models.CharField('zone name', max_length=64, help_text='zone值必须与nginx配置文件中相应站点的zone相同', unique=True)

    def __str__(self):
        return self.upstream_name

class RealServer(models.Model):
    """
    WEB源站
    """
    apply_name = models.ForeignKey('ApplyTag', verbose_name='应用名', null=True, blank=True)
    host = models.ForeignKey('Host',verbose_name='主机')
    bindip_host_eth = models.CharField('主机服务绑定IP的网卡', max_length=2, choices=bindip_host_eth_choices, default='00')
    port = models.IntegerField('服务端口', null=True, blank=True)

    def __str__(self):
        return '%s_%s:%s' %(self.apply_name, self.host.eth00_ip, self.port)

class MaintainRealServer(models.Model):
    """
    源站维护广告源站
    """
    apply_name = models.ForeignKey('ApplyTag', verbose_name='应用名', null=True, blank=True)
    host = models.ForeignKey('Host')
    bindip_host_eth = models.CharField('主机服务绑定IP的网卡', max_length=2, choices=bindip_host_eth_choices, default='00')
    port = models.IntegerField('服务端口')

    def __str__(self):
        return '%s_%s:%s' %(self.apply_name, self.host.eth00_ip, self.port)

class MaintainGroup(models.Model):
    """
    维护页面组，一个组里包含一个或多个维护广告页面源站服务器
    """
    group_name = models.CharField('维护广告页面组名', max_length=64)
    real_server = models.ManyToManyField('MaintainRealServer')
    tag = models.CharField('标签', max_length=64)

    def __str__(self):
        return self.group_name

class Host(models.Model):
    """
    主机服务器
    """
    name = models.CharField('主机名', max_length=64, unique=True)
    # ip = models.GenericIPAddressField('主机IP')
    eth00_ip = models.GenericIPAddressField('Eth0 IP 1', null=True, blank=True, unique=True)
    eth01_ip = models.GenericIPAddressField('Eth0 IP 2', null=True, blank=True)
    eth10_ip = models.GenericIPAddressField('Eth1 IP 1', null=True, blank=True)
    eth11_ip = models.GenericIPAddressField('Eth1 IP 2', null=True, blank=True)
    eth20_ip = models.GenericIPAddressField('Eth2 IP 1', null=True, blank=True)
    eth21_ip = models.GenericIPAddressField('Eth2 IP 2', null=True, blank=True)
    eth30_ip = models.GenericIPAddressField('Eth3 IP 1', null=True, blank=True)
    eth31_ip = models.GenericIPAddressField('Eth3 IP 2', null=True, blank=True)

    def __str__(self):
        return self.name

class Config(models.Model):
    """
    系统配置
    """
    upstream_up_realserver_test_choices = (
        (True, '需要测试'),
        (False, '无需测试'),
    )
    upstream_up_realserver_test = models.BooleanField('源站上线前是否需要测试连接源站', choices=upstream_up_realserver_test_choices, default=False)
    upstream_up_realserver_testurl = models.CharField('源站上线测试URL', max_length=64, null=True, blank=True)
    site_paginator = models.IntegerField('站点展示分页数', default=10, help_text='x个记录分一页')

    class Meta:       # 定义表名
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'

class ApplyTag(models.Model):
    tag = models.CharField('应用实例名', max_length=64)
    note = models.CharField('备注', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.tag