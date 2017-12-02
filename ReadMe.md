# MiliOPS 运维系统

## 功能：
* Nginx反向代理源站上下线
* Nginx反向代理源站挂载维护页面


## 环境：
python3
django(1.10.6)


管理员：
用户：admin
密码：miliops.abc

普通用户：
用户：myuser
密码：miliops.abc


## 工作原理
Nginx控制源站上下线、挂载维护页面广告，主要调用了dynamic_upstream提供的API接口，[dynamic_upstream](https://github.com/cubicdaiya/ngx_dynamic_upstream "Title")

## Nginx编译安装

模块依赖
dynamic_upstream

## python Django Nginx+ uWSGI 安装配置
```
基础包安装

yum install -y bind-utils traceroute wget man sudo ntp ntpdate screen patch make gcc gcc-c++ flex bison zip unzip ftp net-tools --skip-broken 

关联动态库 

# vi /etc/ld.so.conf                         添加如下内容

include /etc/ld.so.conf.d/*.conf

/usr/local/lib

/usr/local/lib64

/lib

/lib64

/usr/lib

/usr/lib64

 

编辑完ld.so.conf,执行 

# ldconfig 

使动态库生效

 

安装pcre

下载最新的pcre包

http://pcre.org/

#cd /usr/local/src

tar -zxvf pcre-8.40.tar.gz

cd pcre-8.40

./configure --enable-jit; make; make install

 ldconfig 

 

安装openssl

下载最新的openssl包

https://www.openssl.org/

cd /usr/local/src

tar -zxvf openssl-1.0.2k.tar.gz

cd openssl-1.0.2k

 ./config; make; make install

ldconfig  

 

安装python

yum -y install sqlite-devel

下载XZ compressed source tarball    Python-3.5.3.tar.xz 到 /usr/local/src

cd /usr/local/src; tar -Jxvf Python-3.5.3.tar.xz; cd Python-3.5.3; 

./configure --prefix=/usr/local/python_3.5.3; make; make install

python -c "import ssl; print(ssl.OPENSSL_VERSION)"    #打印python中ssl模块版本

 

添加环境变量

在 /etc/profile添加下面这行

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/usr/local/python_3.5.3/bin

重载环境变量  . /etc/profile

若想让 python3 成为默认的python 

可以先查询 原来的python路径，然后把原来的路径做软链接指向新的python3路径即可，可直接向/bin做python3版本的链接 ln -s /usr/local/python_3.5.3/bin/python3.5

which python

 

安装django

pip3 install django

 

安装uwsgi

pip3 install uwsgi

uwsgi --version  # 可查看到uwsgi版本号

创建运行uwsgi的用户

useradd uwsgi -M -s /sbin/nologin

id  uwsgi 

uid=1005(uwsgi) gid=1005(uwsgi) groups=1005(uwsgi)
 

测试

uwsgi --http :8000 --chdir /var/webRoot/project/ --wsgi-file project/wsgi.py

curl http://127.0.0.1:8000 可以测试浏览页面

 

uwsgi 配置

mkdir /etc/uwsgi 

vi  /etc/uwsgi/uwsgi9090.ini

复制代码
[uwsgi]
socket = 127.0.0.1:9090
chdir = /var/webRoot/p1/ 
wsgi-file = p1/wsgi.py
;指定运行的用户,指定运行的用户与组，root用户不用指定uid与gid
;虚拟环境的路径
;virtualenv = /opt/pyevn27/
uid = 1005
gid = 1005
master=True
vacuum=True
processes=5
max-requests=10000
pidfile = /var/run/uwsgi9090.pid
daemonize = /var/log/uwsgi/uwsgi9090.log
复制代码
 

注意：

/var/webRoot/p1/目录及 /var/webRoot/p1/db.sqlite3  所属者与所属组应与上面的 用户与组对应
可参考https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/uwsgi/

uwsgi启动脚本：

Emperor模式
uWSGI的Epreror模式可以用来管理机器上部署的uwsgi服务，在这种模式下，会有一个特殊的进程对其它部署的服务进行监视。我们将所有配置文件（ini或xml文件）统一放到一个文件夹（如：/etc/uwsgi）中，然后启动Emperor模式：

uwsgi --emperor /etc/uwsgi

用systemd管理uwsgi服务

新建  /etc/systemd/system/uwsgi.service 文件，内容如下

复制代码
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/usr/local/python_3.5.3/bin/uwsgi --emperor /etc/uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
复制代码
systemctl enable uwsgi

systemctl start uwsgi

 

 

安装nginx

yum -y install zlib zlib-devel gd gd-devel

 

添加一个不能登录且没有主目录的用户Nginx

#useradd nginx -M -s /sbin/nologin   

下载nginx 最新稳定版

cd /usr/local/src

tar -zxvf nginx-1.10.3.tar.gz; cd nginx-1.10.3

./configure --prefix=/usr/local/nginx --user=nginx --group=nginx --with-http_stub_status_module --with-http_ssl_module --with-pcre=/usr/local/src/pcre-8.40 --with-http_realip_module --with-http_image_filter_module --with-http_gzip_static_module --with-openssl=/usr/local/src/openssl-1.0.2k --with-openssl-opt="enable-tlsext"

make; make install
```


dynamic upstream接口配置

```
server {
	listen       17818;
	server_name  localhost;
	access_log off;
	allow 127.0.0.1;
	allow 192.168.1.66;
	deny all;


# 密码认证
    auth_basic "Authentication";
    auth_basic_user_file /etc/nginx/auth_basic;
	
## Dynamic Upstream
    location /du {
		dynamic_upstream;
	}
}	

```


