# post

## Intro

文章结构设计

## Table of Contents

[toc]

## 库表结构

- 标题, title, str
- 作者, author, str
- 标签, tag, json_dict_str
- 简介, intro, str
- 正文, content, text
- 格式, format, tinyint
- 发表时间, create_time, timestamp
- 修改时间, update_time, timestamp

## 发表/编辑入口

- 发表/编辑页面
- Crawler

## 查看入口

- 文章页面
- 文章接口

## 页面逻辑

- 发表: 分为markdown和富文本两种格式书写，保存时区分格式
- 发表: 暂不支持媒体类的嵌入，后期可加入，打通至自己的服务器或第三方API
- 显示: markdown格式转为html输出至页面，富文本直接输出至页面
- 编辑: 编辑对应的markdown文本或者富文本
