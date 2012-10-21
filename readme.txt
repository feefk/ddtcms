##############################################################
#    Name         : DDTCMS
#    Author       : 糊糊, huyoo353@126.com
#    License      : GPL v3
#    
#    Version      : v0.3.0.0.20111104
#    Release Date : 2011-11-16
#    
#    Django Needs : Django 1.3.1 or higher
#    Develop on   : Windows, but can be Deployed on linux
#    Web   Server : Nginx is Recommend
##############################################################

安装指南
========
1 下载DDTCMS v0.3.0.0.20111104的压缩包之后,解压到 非中文 文件夹中.
2 双击dos.cmd, 输入db回车, 自动在根目录下创建data.db的sqlite3数据库.
3 然后在cmd中创建超级管理员,名字你自己随意取,最后会安装一点初始化的数据,不喜欢的话可以到后台删除
  (这一步可直接双击db,一样的效果)
4 双击run.cmd, 使之在127.0.0.1:8000端口运行,run80.cmd是运行在127.0.0.1:80端口的.
5 打开浏览器输入 http://127.0.0.1:8000/ 后回车浏览即可.后面的任务就是进入后台添加数据和自行修改模板了.


初始化安装的内容是:
===================
news : 主要是些新闻分类
theme: 2套主题的名称和路径示例
navbar: 本站菜单条上的初始化.
link:   1条友情链接记录
photologue: 本站模板中使用的图片尺寸设置和水印示例
flatpages:  几个简单页面的使用示例,结合的是default theme主题.

这个是使用 backup_initial.cmd 备份的一点数据.

theme主题只提供1套default, 另外一套在v0.2.5版中没调试好,就去除了.

增加了grapplli, 美化了admin后台, 不喜欢的人可以删除grapplli相关的东西.


