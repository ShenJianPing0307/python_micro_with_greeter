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

### （四）链路追踪

- 通过jaeger实现
- web层通过grpc调用srv层

### （五）熔断

当访问出现一定错误的次数产生熔断，服务暂时不可用，避免服务雪崩。

可使用如下的库：https://github.com/danielfm/pybreaker

### （六）限流

根据设定的规则，限流是允许一部分请求通过，比如：1min允许10个请求，那么多余10个请求的则根据你设定的规则进行返回，如：

> ```
> 请求过于频繁，请稍后重试！
> ```

可用如下的库：https://github.com/tomasbasham/ratelimit

不过该库在装饰器中抛出不满足限流条件的异常，可根据业务需要进行必要的重写：

```python
from functools import wraps
from ratelimit.decorators import RateLimitDecorator
import time

# Use monotonic time if available, otherwise fall back to the system clock.
now = time.monotonic if hasattr(time, 'monotonic') else time.time

class MyRateLimitDecorator(RateLimitDecorator):
    
    ...
    
    def __call__(self, func):
				...
                if self.num_calls > self.clamped_calls:
                    if self.raise_on_limit:
                        kargs['is_exception'] = True
                    return func(*args, **kargs)  # 自定义实现，为了捕捉装饰器中抛出的异常
				...
            return func(*args, **kargs)

        return wrapper

    def __period_remaining(self):
        '''
        Return the period remaining for the current rate limit window.

        :return: The remaing period.
        :rtype: float
        '''
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed
```

然后在grpc的函数中进行调用：

```python
@hello.route('/index')
@breaker  # 熔断机制
@limits(calls=config.CALLS, period=config.FIFTEEN_MINUTES)  # 限流,900s内调用5次,一旦超过会抛出 ratelimit.RateLimitException 异常
def index(*args, **kwargs):  # 与重写部分进行衔接
    if "is_exception" in kwargs:  # 进行限流
        return "请求过于频繁，请稍后重试！"
    channel = initialize.init_srv_conn()
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    hello_response = stub.SayHello(helloworld_pb2.HelloRequest(name='iveBoy'))
    print(hello_response)
    return hello_response.message
```

## 二、服务组件安装与启动

### （一）consul

- 作为服务注册和发现使用

>项目地址：https://github.com/hashicorp/consul
>
>python sdk地址：https://github.com/poppyred/python-consul2

- 安装

>下载指定版本：https://github.com/hashicorp/consul/releases

- 启动

>windows/linux：consul agent -dev -ui -node=consul-dev -client=0.0.0.0
>
>默认启动端口：8500

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

### （三）RetryInterceptor

超时重试通过拦截器实现，可使用github上现有的开源项目：https://github.com/mlorenzana/py-grpc-retry-interceptor

### （四）jaeger与grpc组合

> 安装Python版本的jaeger操作库：https://github.com/jaegertracing/jaeger-client-python
>
> ```powershell
> pip install jaeger-client
> ```
>
> 上述是普通的追踪，比如http请求，调用函数之类的操作，但是grpc的调用，还需要依赖下面的库：
>
> python-grpc库：https://github.com/opentracing-contrib/python-grpc
>
> ```powershell
> pip install grpcio-opentracing
> ```
>
>默认启动端口：16686

### （五）熔断库的安装

```powershell
 pip install pybreaker
```

详细使用见： https://github.com/danielfm/pybreaker#usage

### （六）限流库的安装

```powershell
 pip install ratelimit
```

详细使用见：https://github.com/tomasbasham/ratelimit#usage