# 学习笔记

  1. 服务端和客户端传输文件学习了："How to Transfer Files in the Network using Sockets in Python": https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
  2. 爬取知乎问答，分析json文件的链接地址步骤：
     - 打开网页调试功能
     - 选择Network选项卡，筛选XHR类型
     - clear，reload
     - 滚动到页面底部，让新的回答出现，观察增加了哪些链接
     - 逐个点击链接，查看preview，看哪个里面的json内容像是答案的内容
  3. 可以用一个叫jsonpath-ng的模块，类似xpath，可以解析json文件中的内容。教程参考：
   https://www.cnblogs.com/jpfss/p/10973590.html