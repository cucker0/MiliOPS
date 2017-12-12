from django.shortcuts import render, HttpResponse, redirect
import json, os, sys, time
import urllib.request, urllib.error
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# BASIC_DIR = os.path.dirname(os.path.dirname(__file__))
# sys.path.append(BASIC_DIR)
# from MiliOPS import settings

# Create your views here.
from nginx import models

@csrf_exempt
def page_not_found(req):
    """
    404错误页面
    :param req:
    :return:
    """
    return render(req, 'nginx/pages/400.html')

@csrf_exempt
def page_error(req):
    """
    500页面
    :param req:
    :return:
    """
    return render(req, 'nginx/pages/500.html')

def root(req):
    return redirect('/nginx/index/')

@login_required
def index(req):
    """
    首页
    :param req:
    :return:
    """
    sites = models.Site.objects.all()
    proxy_server_groups = models.ProxyServerGroup.objects.all()
    return render(req, 'nginx/index.html',{"sites":sites, "proxy_server_groups":proxy_server_groups})

@login_required
def GetProxyServer(req):
    """
    获取代理服务器列表详情及upstream详情
    :param req:
    :return:
    """
    if req.method == "POST":
        data = req.POST.get("data")
        data = json.loads(data)
        site_id = int(data['site_id'])
        # site = models.Site.objects.get(id=site_id)
        # proxy_server_group = site.proxy_server_group
        # proxy_servers = proxy_server_group.group_server.all()
        # upstream = site.upstream
        # realservers = upstream.upstream_realserver.all()
        # #[{'proxy_server':'192.168.1.46','source_web':[{'id':1 ,'host':'192.168.1.210:20022','url':'http://192.168.1.46:17818/du?upstream=www_tuandai_com_du&verbose='},]},]
        # data_send = []
        # #[{'ip': '192.168.1.59', 'id': 6, 'up_down': 0, 'port': 20026}, {'ip': '192.168.1.146', 'id': 7, 'up_down': 0, 'port': 20026}]
        '''
        for ps in proxy_servers:
            dic = {}
            dic['proxy_server'] = ps.ip
            dic['realserver'] = []

            for s in realservers:
                dic2 = {}
                # http://192.168.1.46:17818/du?upstream=www_tuandai_com_du&verbose=
                # http://192.168.1.46:17818/du?upstream=www_tuandai_com_du&server=192.168.1.41:20022&up=
                # http://192.168.1.46:17818/du?upstream=www_tuandai_com_du&server=192.168.1.41:20022&down=
                url = "http://%s:%s/%s?upstream=%s&server=%s:%s&up=" %(ps.ip, proxy_server_group.port, proxy_server_group.dir, upstream.upstream_name, s.ip, s.port)
                host = "%s:%s" %(s.ip, s.port)
                dic2['id'], dic2['host'], dic2['url'] = s.id, host, url
                dic['realserver'].append(dic2)
            data_send.append(dic)
        '''
        # for i in realservers:
        #     dic = {}
        #     dic['id'] = i.id
        #     dic['ip_port'] = "%s:%s" %(GetHostIp(i), i.port)
        #     data_send.append(dic)
        # upstream_opration_instance = UpstreamOpration(site_id)
        # get_du = upstream_opration_instance.UpsreamVerbose()
        # for i in range(len(data_send)):
        #     total = 0
        #     for j in get_du:
        #         total += j['get_du'][data_send[i]['ip_port']]
        #     average = total/len(get_du)
        #     # 平均数为0表示全部下线成功，1表示需要操作的全部上线成功，>0 且小于 1则表示有些未操作成功。
        #     if average == 0:
        #         data_send[i]['up_down'] = 0
        #     elif average == 1:
        #         data_send[i]['up_down'] = 1
        #     else:
        #         data_send[i]['up_down'] = 2
        # print(data_send)
        # print(get_du)
        # 示例
        # data_send==> [{'ip_port': '192.168.1.41:20022', 'id': 1, 'up_down': 1}, {'ip_port': '192.168.1.140:20022', 'id': 2, 'up_down': 1}, {'ip_port': '192.168.1.165:20022', 'id': 3, 'up_down': 1}, {'ip_port': '192.168.1.168:20022', 'id': 4, 'up_down': 1}, {'ip_port': '192.168.1.210:20022', 'id': 5, 'up_down': 1}]
        # get_du==> [{'proxy_server': 'nginx_21_(1.46)', 'get_du': {'192.168.1.41:20022': 1, '192.168.1.210:20022': 1, '192.168.1.140:20022': 1, '192.168.1.165:20022': 1, '192.168.1.168:20022': 1}}, {'proxy_server': 'nginx_17_(1.142)', 'get_du': {'192.168.1.41:20022': 1, '192.168.1.210:20022': 1, '192.168.1.140:20022': 1, '192.168.1.165:20022': 1, '192.168.1.168:20022': 1}}]

        upstream_opration_instance = UpstreamOpration(site_id)
        data_send, get_du = upstream_opration_instance.GetSiteRealserverStatus(is_get_du=True)
        return HttpResponse(json.dumps({'data':data_send, 'du':get_du, 'site_id':site_id}))
    else:
        return HttpResponse("ok")

def MyPaginator(obj, num, req):
    """
    通用分页
    :param obj: 需要分页对象
    :param num: 每页显示多少个
    :param req: http请求
    :return: obj经过paginator封装的对象, page
    """
    # 每页显示多少行
    paginator = Paginator(obj, num)
    page = None
    if req.method == "POST":
        data = req.POST.get('data')
        data = json.loads(data)
        if 'page' in data.keys():
            page = int(data['page'])  # 从html前端获取用户点击的页编号
    try:
        new_obj = paginator.page(page)
    except PageNotAnInteger:
        new_obj = paginator.page(1)
        page = 1
    except EmptyPage:
        new_obj = paginator.page(paginator.num_pages)

    return new_obj, page

@login_required
def GetProxyServerByGroup(req):
    """
    通过代理组ID获取代理服务器中运行的站点,并生成维护页面组选择元素
    :param req:
    :return:
    """
    if req.method == "POST":
        data = req.POST.get("data")
        data = json.loads(data)
        proxy_server_group_id = int(data['proxy_server_group_id'])
        proxy_server_group = models.ProxyServerGroup.objects.get(id=proxy_server_group_id)
        sites = proxy_server_group.group_site.filter(site_status=1)
        # print(sites)

        html = ShowSiteList(sites, req)
        # if sites:       # 如果 sites存在
        #     # 维护页面select
        #     maintain_group_objs = models.MaintainGroup.objects.all()
        #
        #     maintain_select = '<select name="maintain_group_id" class="col-xs-4 maintain_group_select margin-L10"><option class="mygray-light" selected="selected" value="-1">维护页</option>'
        #     for obj in maintain_group_objs:
        #         ele_maintain_group = '<option value="%s">%s</option>' %(obj.id, obj.tag)
        #         maintain_select += ele_maintain_group
        #     maintain_select += '</select>'
        #
        #     html = '''
        #     <div class="col-xs-9">
        #         %s
        #         <button type="button" action="3" class="btn btn-warning margin-L30" onclick="Maintain(this);">维护</button>
        #         <button type="button" action="4" class="btn btn-success pull-right" onclick="Maintain(this)">恢复</button>
        #     </div>
        #     <table id="table_site" class="table mywidth95">
        #         <thead>
        #             <th><input type="checkbox" name="ckSelectAll" status="0" onclick="SelectAll(this,'#table_site');"></th>
        #             <th>站点</th><th>代理组</th>
        #         </thead>
        #     ''' %(maintain_select)
        #     for site in sites:
        #         ele = '<tr>'
        #         ele += '<td><input type="checkbox" value=%s></td><td onclick="SiteClick(this);">%s%s</td><td>%s</td>' %(site.id, site.site_name, SiteStatus(site), proxy_server_group.tag)
        #         ele += '</tr>'
        #         # html += '<li class="cursor1" site_id="%s" ><span>%s</span></li>' %(site.id, site.site_name)
        #         html += ele
        #     html += '</table>'
        return HttpResponse(json.dumps({'data':html}))
    else:
        return HttpResponse("ok")

def ShowSiteList(sites, req):
    """
    展示站点列表
    :param sites:
    :return:
    """
    config_obj = models.Config.objects.first()
    proxy_server_group = sites.first().proxy_server_group
    sites, page = MyPaginator(sites, config_obj.site_paginator, req)
    html = ' '
    if sites:       # 如果 sites存在
        # 维护页面select
        maintain_group_objs = models.MaintainGroup.objects.all()

        maintain_select = '<select name="maintain_group_id" class="col-xs-4 maintain_group_select margin-L10"><option class="mygray-light" selected="selected" value="-1">维护页</option>'
        for obj in maintain_group_objs:
            ele_maintain_group = '<option value="%s">%s</option>' %(obj.id, obj.tag)
            maintain_select += ele_maintain_group
        maintain_select += '</select>'

        html = '''
        <div class="col-xs-9">
            %s
            <button type="button" action="3" class="btn btn-warning margin-L30" onclick="Maintain(this);">维护</button>
            <button type="button" action="4" class="btn btn-success pull-right" onclick="Maintain(this)">恢复</button>
        </div>
        <table id="table_site" proxy_group_id="%s" class="table mywidth95">
            <thead>
                <th><input type="checkbox" name="ckSelectAll" status="0" onclick="SelectAll(this,'#table_site');"></th>
                <th>站点</th><th>代理组</th>
            </thead>
        ''' %(maintain_select, proxy_server_group.id)
        for site in sites:
            ele = '<tr>'
            ele += '<td><input type="checkbox" value=%s></td><td onclick="SiteClick(this);">%s%s</td><td>%s</td>' %(site.id, site.site_name, SiteStatus(site), site.proxy_server_group.tag)
            ele += '</tr>'
            # html += '<li class="cursor1" site_id="%s" ><span>%s</span></li>' %(site.id, site.site_name)
            html += ele
        html += '</table>'

        ele_paginator_prev, ele_paginator_next, ele_paginator_middle = '', '', ''
        if sites.has_previous():
            ele_paginator_prev = '''
            <li class="pagination pagination-lg">
                <a href="#" page="%s" aria-label="Previous" onclick="GetProxyServerByGroup(this, 2);">
                    <span aria-hidden="true">&lt;</span>
                </a>
            </li>
            ''' %(sites.previous_page_number())

        if sites.has_next():
            ele_paginator_next = '''
            <li class="pagination pagination-lg">
                <a href="#" page="%s" aria-label="Next" onclick="GetProxyServerByGroup(this, 2);">
                    <span aria-hidden="true">&gt;</span>
                </a>
            </li>
            ''' %(sites.next_page_number())
        for page_num in sites.paginator.page_range:
            if page and page == page_num:
                ele_paginator_middle += '<li class="active"><a href="#" page=%s onclick="GetProxyServerByGroup(this, 2);">%s</a></li>' %(page_num, page_num)
            else:
                ele_paginator_middle += '<li><a href="#" page=%s onclick="GetProxyServerByGroup(this, 2);">%s</a></li>' %(page_num, page_num)

        ele_paginator = '''
        <!--分页导航-->
        <div class="col-xs-12">
            <nav>
                <ul class="pagination pagination-sm">
                    %s

                    %s

                    %s
                </ul>
            </nav>
        </div>
        ''' %(ele_paginator_prev, ele_paginator_middle, ele_paginator_next)

        html += ele_paginator
    return html

def SiteStatus(site_obj):
    ele = ''
    if site_obj.maintain_status == 1:       # 维护中
        ele += '<span class="glyphicon glyphicon-exclamation-sign red"></span>'
    elif site_obj.site_realserver_status == 0:      # 有源站下线
        ele += '<span class="glyphicon glyphicon-minus-sign orange"></span>'
    elif site_obj.site_realserver_status == 2:      # 有源站状态未知
        ele += '<span class="glyphicon glyphicon-question-sign"></span>'
    return ele

class UpstreamOpration(object):
    """
    Upsream所有操作
    ngx_dynamic_upstream 用法见：https://github.com/cubicdaiya/ngx_dynamic_upstream
    list：
    curl "http://127.0.0.1:6000/dynamic?upstream=zone_for_backends"
    verbose：
    curl "http://127.0.0.1:6000/dynamic?upstream=zone_for_backends&verbose="
    down：
    curl "http://127.0.0.1:6000/dynamic?upstream=zone_for_backends&server=127.0.0.1:6003&down="
    up：
    curl "http://127.0.0.1:6000/dynamic?upstream=zone_for_backends&server=127.0.0.1:6003&up="
    add：
    curl "http://127.0.0.1:6000/dynamic?upstream=zone_for_backends&add=&server=127.0.0.1:6004"
    remove：
    curl "http://127.0.0.1:6000/dynamic?upstream=zone_for_backends&remove=&server=127.0.0.1:6003"

    """
    def __init__(self, site_id=None, realserver_id=None):
        self.site_id = site_id
        self.realserver_id = realserver_id
        self.opener = self.UrlOpener()
        # self.site
        # self.upstream
        # self.proxy_server_group
        # self.proxy_servers
        # self.realservers

    def UrlOpener(self):
        """
        创建url opener
        :return: url opener
        """
        # 把单个realserver_id转成 列表
        if (self.realserver_id and type(self.realserver_id) != list):
            lis = []
            lis.append(self.realserver_id)
            self.realserver_id = lis
        # if self.realserver_id:
        #     self.site = models.RealServer.objects.get(id=self.realserver_id[0]).realserver_site.first()
        # else:
        #     self.site = models.Site.objects.get(id=self.site_id)
        self.site = models.Site.objects.get(id=self.site_id)
        self.upstream = self.site.upstream
        self.proxy_server_group = self.site.proxy_server_group
        self.proxy_servers = self.proxy_server_group.proxy_server.all()
        if self.realserver_id:
            self.realservers = models.RealServer.objects.filter(id__in=self.realserver_id)

        top_level_url = []
        for ps in self.proxy_servers:
            url1 = "http://%s:%s/%s" %(self.GetHostIp(ps), self.proxy_server_group.port, self.proxy_server_group.dir)
            top_level_url.append(url1)

        # import urllib.request
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        user = self.proxy_server_group.user
        pwd = self.proxy_server_group.pwd
        password_mgr.add_password(None, top_level_url, user, pwd)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        # create "opener" (OpenerDirector instance)
        opener = urllib.request.build_opener(handler)
        return opener

    def ForamtUpsreamVerbose(self, req_ret):
        """
        对获取的upstream详细数据进行格式化
        :param req_ret: upstream详细数
        :return:  以字典类型返回格式化后的数据，如 {'192.168.1.210:20022': 1, 192.168.1.140:20022}
        """
        # 原始数据：['server 192.168.1.210:20022 weight=10 max_fails=2 fail_timeout=10;', 'server 192.168.1.140:20022 weight=20 max_fails=2 fail_timeout=10 down;']
        dic = {}
        for i in req_ret:
            i = i.split(';')[0]
            j = i.split()
            if j[-1] == "down":
                dic[j[1]] = 0
            else:
                dic[j[1]] = 1
        return dic

    def UpsreamVerbose(self):
        """
        获取upsteam 详细信息
        [{'get_du': {'192.168.1.146:20026': 1, '192.168.1.59:20026': 1}, 'proxy_server': 'nginx_11.211'}, {'get_du': {'192.168.1.146:20026': 1, '192.168.1.59:20026': 1}, 'proxy_server': 'nginx_11.213'}]
        :return: 以字典形式返回upsteam 详细信息
        """
        get_upstream_verbose_list = []
        for ps in self.proxy_servers:    # 查询upstream详细信息
            dic = {}
            a_url = "http://%s:%s/%s?upstream=%s&verbose=" %(self.GetHostIp(ps), self.proxy_server_group.port, self.proxy_server_group.dir, self.upstream.zone)
            # print(a_url)
            x = self.opener.open(a_url, timeout=5)
            # 原始数据
            '''
            server 192.168.1.210:20022 weight=10 max_fails=2 fail_timeout=10;
            server 192.168.1.140:20022 weight=20 max_fails=2 fail_timeout=10;

            '''
            ret = x.read().decode('utf8').split('\n')
            ret.pop()
            ret = self.ForamtUpsreamVerbose(ret)
            dic['proxy_server'] = ps.host.name
            dic['get_du'] = ret
            get_upstream_verbose_list.append(dic)
        return get_upstream_verbose_list

    def UpstreamUp(self):
        """
        上线源站服务器
        :return:
        """
        config_obj = models.Config.objects.first()
        if config_obj.upstream_up_realserver_test:  # 源站上线前是否测试
            for rs in self.realservers:
                # http://192.168.1.210:20022/do_not_delete/check.html
                test_url = "http://%s:%s%s" %(self.GetHostIp(rs), rs.port, config_obj.upstream_up_realserver_testurl)
                req = urllib.request.Request(test_url)
                try:
                    response = urllib.request.urlopen(req)
                    response = response.read().decode('utf8')
                except urllib.error.HTTPError as e:
                    print(e.code)
                    continue
        for ps in self.proxy_servers:
            for rs in self.realservers:
                a_url = "http://%s:%s/%s?upstream=%s&server=%s:%s&up=" %(self.GetHostIp(ps), self.proxy_server_group.port, self.proxy_server_group.dir, self.upstream.zone, self.GetHostIp(rs), rs.port)
                x = self.opener.open(a_url)
        self.UpdateSiteRealserverStatusField()

    def UpstreamDown(self):
        """
        下线源站服务器
        :return:
        """
        for ps in self.proxy_servers:
            for rs in self.realservers:
                a_url = "http://%s:%s/%s?upstream=%s&server=%s:%s&down=" %(self.GetHostIp(ps), self.proxy_server_group.port, self.proxy_server_group.dir, self.upstream.zone, self.GetHostIp(rs), rs.port)
                x = self.opener.open(a_url)
        self.UpdateSiteRealserverStatusField()

    def UpstreamMaintain(self, maintain_group_id):
        """
        站点进行维护，挂载维护页
        :return:
        """
        realservers = self.site.real_server.all()
        maintain_group_obj = models.MaintainGroup.objects.get(id=maintain_group_id)
        maintain_realservers = maintain_group_obj.real_server.all()
        ret = {'error':[],'ok':[]}
        for ps in self.proxy_servers:   # 上线维护页源站
            for rs in maintain_realservers:
                try:
                    a_url = "http://%s:%s/%s?upstream=%s&server=%s:%s&add=" %(self.GetHostIp(ps), self.proxy_server_group.port, self.proxy_server_group.dir, self.upstream.zone, self.GetHostIp(rs), rs.port)
                    x = self.opener.open(a_url, timeout=5)
                except Exception as e:
                    ret['error'].append(e)
                    print(e)
                    continue
        time.sleep(0.5)
        ## 下线所有的原来所有的源站
        self.realservers = realservers
        self.UpstreamDown()
        ## -- end -- 下线所有的原来所有的源站
        site_set = models.Site.objects.filter(id=self.site.id)
        site_set.update(maintain_status=1)     # 更新维护状态为维护中
        site_set.update(maintain_page_group=maintain_group_obj)     # 更新关联的维护页面组

        if len(ret['error']) == 0:
            ret['ok'].append("site maintain ok.")
        return(ret)



    def UpstreamBackToNormal(self):
        """
        站点恢复正常运行
        :return:
        """
        realservers = self.site.real_server.all()
        maintain_page_group_obj = self.site.maintain_page_group
        ret = {'error':[],'ok':[]}
        if maintain_page_group_obj:
            maintain_realservers = maintain_page_group_obj.real_server.all()


            ## 上线所有的原来所有的源站
            self.realservers = realservers
            self.UpstreamUp()
            time.sleep(0.5)
            ## -- end -- 上线所有的原来所有的源站
            for ps in self.proxy_servers:   # 下线维护页源站
                for rs in maintain_realservers:
                    try:
                        a_url = "http://%s:%s/%s?upstream=%s&server=%s:%s&remove=" %(self.GetHostIp(ps), self.proxy_server_group.port, self.proxy_server_group.dir, self.upstream.zone, self.GetHostIp(rs), rs.port)
                        x = self.opener.open(a_url, timeout=5)
                    except Exception as e:
                        ret['error'].append(e)
                        print(a_url, "==>", e)
                        continue
            site_set = models.Site.objects.filter(id=self.site.id)
            site_set.update(maintain_status=0)     # 更新维护状态为运行中
            site_set.update(maintain_page_group=None)       # 去掉关联的维护页面组
            if len(ret['error']) == 0:
                ret['ok'].append("site maintain back to normal ok.")
        return(ret)

    def GetHostIp(self,obj):
        """
        通过Reeal Server对象本身获取关联的Host服务的网卡IP
        :param obj:
        :return: Reeal Server关联的Host服务的网卡IP
        """
        ip = '127.0.0.2'
        ## eth00_ip
        eth = "eth%s_ip" %(str(obj.bindip_host_eth) )
        if hasattr(obj.host, eth):
            ip = getattr(obj.host, eth)
        return ip

    def GetSiteRealserverStatus(self, is_get_du=False):
        """
        获取site对应的所有real server综合状态
        :return: site对应的real server综合状态(list类型), UpsreamVerbose详情列表(list类型)
        """
        realservers = self.site.real_server.all()
        SiteRealserverStatus = []
        for i in realservers:
            dic = {}
            dic['id'] = i.id
            dic['ip_port'] = "%s:%s" %(self.GetHostIp(i), i.port)
            SiteRealserverStatus.append(dic)

        get_du = self.UpsreamVerbose()
        for i in range(len(SiteRealserverStatus)):
            total = 0
            for j in get_du:
                total += j['get_du'][SiteRealserverStatus[i]['ip_port']]
            average = total/len(get_du)
            # 平均数为0表示全部下线成功，1表示需要操作的全部上线成功，>0 且小于 1则表示有些未操作成功。
            if average == 0:
                SiteRealserverStatus[i]['up_down'] = 0
            elif average == 1:
                SiteRealserverStatus[i]['up_down'] = 1
            else:
                SiteRealserverStatus[i]['up_down'] = 2
        # print(SiteRealserverStatus)
        # print(get_du)
        # 示例
        # SiteRealserverStatus==> [{'ip_port': '192.168.1.41:20022', 'id': 1, 'up_down': 1}, {'ip_port': '192.168.1.140:20022', 'id': 2, 'up_down': 1}, {'ip_port': '192.168.1.165:20022', 'id': 3, 'up_down': 1}, {'ip_port': '192.168.1.168:20022', 'id': 4, 'up_down': 1}, {'ip_port': '192.168.1.210:20022', 'id': 5, 'up_down': 1}]
        # get_du==> [{'proxy_server': 'nginx_21_(1.46)', 'get_du': {'192.168.1.41:20022': 1, '192.168.1.210:20022': 1, '192.168.1.140:20022': 1, '192.168.1.165:20022': 1, '192.168.1.168:20022': 1}}, {'proxy_server': 'nginx_17_(1.142)', 'get_du': {'192.168.1.41:20022': 1, '192.168.1.210:20022': 1, '192.168.1.140:20022': 1, '192.168.1.165:20022': 1, '192.168.1.168:20022': 1}}]
        if is_get_du:
            return SiteRealserverStatus, get_du
        else:
            return SiteRealserverStatus

    def UpdateSiteRealserverStatusField(self):
        """
        更新site表的site_realserver_status字段
        :return: site对应的real server综合状态(list类型), UpsreamVerbose详情列表(list类型)
        """
        # start -- 判断site realserver 源站聚合状态
        site_realserver_status_list = self.GetSiteRealserverStatus()
        multiply = 1
        for i in site_realserver_status_list:  # 求所有端口状态值的积
            multiply *= i['up_down']
        if multiply == 0:
            tag = 0
        elif multiply == 1:
            tag = 1
        else:
            tag = 2
        if self.site.site_realserver_status != tag:
            site_set = models.Site.objects.filter(id=self.site.id)
            site_set.update(site_realserver_status=tag)

# def GetHostIp(obj):
#     """
#     通过Reeal Server对象本身获取关联的Host服务的网卡IP
#     :param obj:
#     :return: Reeal Server关联的Host服务的网卡IP
#     """
#     ip = '127.0.0.2'
#     ## eth00_ip
#     eth = "eth%s_ip" %(str(obj.bindip_host_eth) )
#     if hasattr(obj.host, eth):
#         ip = getattr(obj.host, eth)
# 
#     # if eth == '00':
#     #     ip = obj.host.eth00_ip
#     # elif eth == '01':
#     #     ip = obj.host.eth01_ip
#     # elif eth == '01':
#     #     ip = obj.host.eth01_ip
#     # elif eth == '10':
#     #     ip = obj.host.eth10_ip
#     # elif eth == '11':
#     #     ip = obj.host.eth11_ip
#     # elif eth == '20':
#     #     ip = obj.host.eth20_ip
#     # elif eth == '21':
#     #     ip = obj.host.eth21_ip
#     # elif eth == '30':
#     #     ip = obj.host.eth30_ip
#     # elif eth == '31':
#     #     ip = obj.host.eth31_ip
#     return ip

@login_required
def UpDownRealserver(req):
    """
    上、下线操作源站
    :param req:
    :return:
    """
    if req.method == "POST":
        data = req.POST.get('data')
        data = json.loads(data)
        action = data['action'].strip()
        realserver_list = data['realserver_list']
        site_id = data['site_id']
        # print(realserver_list, action)
        upsream_opration_instance = UpstreamOpration(site_id,realserver_list)
        if action == '0':
            ret = upsream_opration_instance.UpstreamDown()
        elif action == "1":
            ret = upsream_opration_instance.UpstreamUp()
        else:
            pass
        get_du = upsream_opration_instance.UpsreamVerbose()
        # print(get_du)
        return HttpResponse(json.dumps({'data':get_du}))
    else:
        return HttpResponse("ok")

@login_required
def SearchSite(req):
    """
    搜索站点
    :param req:
    :return:
    """
    if req.method == "POST":
        data = req.POST.get('data')
        data = json.loads(data)
        print(data)
        if data['search_key'].strip():
            sites = models.Site.objects.filter(site_name__contains=data['search_key'].strip())
        html = ShowSiteList(sites, req)
        return HttpResponse(json.dumps({'data':html}))

    return HttpResponse('this method no allowed.')

@login_required
def Maintain(req):
    """
    站点维护，挂载维护页或恢复正常
    :param req:
    :return:
    """
    if req.method == "POST":
        data = req.POST.get('data')
        data = json.loads(data)
        action = data['action'].strip()
        maintain_group_id = data['maintain_group_id']
        site_id_list = data['site_id_list']
        data = {}

        for site_id in site_id_list:
            upstream_optation_instance = UpstreamOpration(site_id)
            if action == '3':
                ret = upstream_optation_instance.UpstreamMaintain(maintain_group_id)
            elif action == '4':
                ret = upstream_optation_instance.UpstreamBackToNormal()
            data[site_id] = ret
            data[site_id] = ret
        return HttpResponse(json.dumps({'data':data}))
    else:
        return HttpResponse("OK")

