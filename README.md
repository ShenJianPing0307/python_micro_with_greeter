##  一、项目简介

基于Python实现的微服务Demo级别项目（grpc+flask）

### （一）架构说明

- srv层使用的是grpc
- web层使用的是flask

### （二）服务注册与发现

- srv与web层使用consul进行服务注册
- web层使用随机算法实现srv服务发现

### （三）超时重试机制

- 防止服务雪崩
- 通过grpc中的拦截器实现
- 在web层进行实现

## 二、服务组件安装与启动

### （一）consul

...

### （二）nacos

- 作为配置中心使用

> 项目地址：https://github.com/alibaba/nacos
>
> python sdk地址：https://github.com/nacos-group/nacos-sdk-python

- 安装

> 下载指定版本：https://github.com/alibaba/nacos/releases
>
> 比如，windows下载zip包，本地需要先安装好Java

- 启动

> windows系统：下载后的安装包，进入bin目录，然后cmd执行：startup.cmd -m standalone
>
> linux系统：sh startup.sh -m standalone
>
> 默认启动端口：8848

