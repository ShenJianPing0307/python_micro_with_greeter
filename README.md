# python_micro_with_greeter
基于Python实现的微服务Demo级别项目（grpc+flask）

## 架构说明
- srv层使用的是grpc
- web层使用的是flask

## 服务注册与发现
- srv与web层使用consul进行服务注册
- web层使用随机算法实现srv服务发现

