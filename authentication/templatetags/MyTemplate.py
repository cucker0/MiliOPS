#!/usr/bin/env python
# -*- coding:utf-8 -*-

## 自定义模板

from django import template
from django.utils.html import format_html
import datetime

register = template.Library()

@register.simple_tag
def truncate_url(img_url):
    """
    截断图片URL
    如 uploads/user_image/01.png        ==>  /user_image/01.png
    :param img_url: 图片路径
    :return: 截断处理后的url
    """
    if img_url:
        img_url = str(img_url)
        url = img_url.split('/', maxsplit=1)[-1]
    else:
        url = 'system/head_img_00.jpg'
    return url

@register.simple_tag
def get_year():
    """
    获取当年年份
    :return: 当年年份
    """
    now = datetime.datetime.now()
    YYYY = now.year
    return YYYY