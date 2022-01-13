# Electron Python

Electron Python 是一个模板程序，来演示如何将 Electron 和 Python 结合，用于开发GUI 程序。

这篇文档涵盖了使用过程中需要知道的基本信息，但不会包括所用技术栈的说明，请参考官方文档进行学习。部分说明摘自或改编自 [`Vue CLI` 文档](https://cli.vuejs.org/zh/guide/css.html#css-modules)。

## 基本架构

采用基本的 Client/Server 架构, 利用 gRPC 在前端和后端之间进行通信。python 程序作为 Server，提供一系列的 API，用来实现所需的逻辑。Electron App 作为 Client，通过调用 API 实现具体的操作，其本身只负责与用户交互的逻辑。

Electron App 是整个程序的入口。在启动阶段，Electron Main Process 会以子进程的方式启动 python 程序。

技术栈：
- Node: 
  - Electron.js
  - Vue.js
  - gRPC
  - Element-UI

- Python: 
  - gRPC

## 开发环境

- System：Windows 10
- Node: 14.17.0-x86
- yarn 1.x (node.js package manager)
- Python: 3.8.10-x86
- Poetry (python package manager)

注意：请严格按照对应的版本和架构(x86)配置你的环境。如果你需要维护多个不同的 Node 版本，推荐使用 nvs (参考 Node 官方连接)。

除了安装对应版本的 node 和 python，还需要安装 yarn 和 poetry 作为包管理器。请参照官方文档。

安装包管理器后，可以通过命令一键初始化 Node.js 和 python 的相关依赖。

如果选择不同的 node/python 版本，请参考：[使用不同的开发环境](#使用不同的开发环境)

## 安装

``` bash
cd your-project-folder
yarn install
```

这个命令会在项目文件夹内创建一个 python 的虚拟环境，并安装依赖。然后会安装 Node.js 的依赖。然后这个项目已经可以运行了。

注意：请确保你安装了上述开发环境，并将 path 环境变量指向对应的 python 和 node 版本。

## 常用命令
``` bash
yarn install            # 安装 python 和 node 的依赖
yarn electron:serve     # 在开发环境下运行项目
yarn electron:build     # 将项目打包成安装文件
```

## 文件结构

Electron 应用的源码存储在 /src 中，background.js 为 MainProcess 的入口，main.js 为 RendererProcess 的入口。App.vue 为 vue 的根组件实例。

其中，与 MainProcess 相关的模块存放在 `/src/bg` 中，RendererProcess 所引用的模块存放在 `/src/plugin` 中。

`/src/views` 是构成视图界面的 vue 组件的存放位置，一般与应用程序的路由结构相对应。而对于某些可复用的基础组件，则存放在 `/src/components/` 文件夹下。

Python 应用的源码存放在 `py-code/src` 中，打包时会自动处理并打包到最终的 exe 文件里。

更多信息可以参考：https://cli.vuejs.org/zh/guide/mode-and-env.html#%E6%A8%A1%E5%BC%8F

## RPC 通信

这个架构的核心就是一套通过 RPC 来进行远程调用的机制。Electron Renderer Process 提供 Client，Python 提供 Server 并暴露一系列的方法。

对于 python server，主要工作是编写 api 接口。这样你就能在 Electron 应用中通过 client 调用它。

### 在 Server 端实现接口

我们通过向 ApiRouter 注册路由来实现接口。我们以 `/py-code/src/apis/main.py` 中的参考代码为例，见下方。我们可以用 `ApiRouter.route()` 装饰器来将一个 `Callable` 对象注册到路由上（和你在 flask 中使用的一样）。同时，也可以利用 `ApiRouter.register()` 或 `ApiRouter.register_from_map()` 方法。对于更为复杂的应用，将路由定义分散在每个函数的前面会让人无法一目了然的看到所有路由列表，在这种情况下，使用这两个方法更有利于清晰地组织代码。

ApiRouter 被设计成单例模式（Singleton），因此你可以在不同文件中实例化 `ApiRouter` 实例，并注册路由，它们最终会指向同一个实例。这样就可以将各个类别的路由清晰地组织在单个文件中，而不用考虑它们之间的依赖关系。

为了避免错误，注册已经存在的路由会抛出异常。你需要用 `ApiRouter.delete()` 方法显示地删除路由。

``` python
# /py-code/src/apis/main.py
from datetime import datetime
from .ApiRouter import ApiRouter

# ApiRouter is singleton so it can be instantiated safely in different modules
router = ApiRouter()

# --- Example 1: register an API with a decorator
@router.route(':get-current-time')
def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

# --- Example 2: register API with register() or register_from_map() method
# In compicated projects, it's a good practice to organise APIs in seperated 
# files and use register_from_map() so there is a summary of all the APIs
ROUTES = {
    ':arithmetic:add': lambda x, y: x+y,
    ':arithmetic:multiply': lambda x, y: x+y,
    ':arithmetic:abs': abs
}

router.register_from_map(ROUTES)
```

### 路由格式

路由使用 `:` 作为分隔符，用来表示逻辑上的层级关系。

路由需要符合以下格式：`(:[a-zA-Z][\w\-]*\w)*`，解释如下：

1. 每一层级路由的名称由字母，数字，下划线，短横线组成。首个字符必须为字母，最后一个字符必须为数字或字母，最小长度为2。
   
  例如：`foo`，`foo-bar`，`foo1-bar2` 都是合法的，`foo-`，`foo-bar_` 是不合法的。

2. 各个层级的路由名称用 `:` 进行连接，且路由前面的冒号不可省略。

  例如：`:foo-bar:child-0:sub-a0`

除此之外，根路由 `:` 被保留，永远返回当前所有 `API` 路由路径的列表。

如果向 `ApiRouter` 注册一个不符合格式的路由，将会抛出异常。

### 在 Client 端调用接口:

由于大多数的 RPC 调用都是在 Vue 组件中完成的，我们将 rpcClient 对象绑定到 Vue 实例上，因此在 Vue 组件中，你可以无需引用，直接使用 rpcClient 对象:

``` javascript
vm.$rpcClient.request(options).then((reply[, id, route]) => {
  // process
}).catch((err) => {
  // manage error
})
```

在成功调用时的回调函数中，除了返回数据 `reply`，还有可选的 `id` 和 `route` 可供使用。但通常你不太会用到它。

在普通的 javascript 文件中，你也可以通过引入 `/src/plugins/rpc-client/client` 的方式来调用。

``` javascript
import rpcClient from `@/plugins/rpc-client/client`
rpcClient.request(options).then().catch()
```

options 为 RPC 调用时的选项，结构如下：

``` javascript
options = {
  route: String,
  args: optional Array,
  kwargs: optional Object,
  timeout: optional Number
}
```

`route` 是路由的路径，请参考 [路由格式](#路由格式)。如果路径不存在，将抛出异常。

`args` 和  `kwargs` 分别作为位置参数和关键字参数传递给路由对应的函数。

`timeout` 用来指定当次请求的超时时间，单位为 ms。缺省为 `RpcClient.timeout`

注意，只有可序列化的对象才能在 RPC 中传递。包括 int, float, string, bytes, 以及由上述元素组成的 list, tuple, map, dict 等。这些对象会在 javascript 中转化为支持的对应类型。

### RPC 端口

RPC 在 localhost 上运行，默认端口为 23300。当端口被占用或不可用时，会自动搜寻后面的端口，直到找到可用端口。因此，你无需担心端口冲突的问题。

### 使用并行 API

API Server 默认是单线程模式，所有任务顺序执行。如果需要并行执行 API，在调用 `start_rpc_server()` 时将 `max_workers` 设为大于 1 的数，即可并行处理多个 API 请求。请参考 `/py-code/src/__main__.py`。需要注意的是，如果采用多线程模式，你需要保证每个 API 都是线程安全的。

### 超时设置

客户端在启动后会等待连接 server，如果 30s 内无法连接，会报超时错误。

API 调用默认使用 RpcClient.timeout: 3000 (ms)。但你也可以在 `RpcClient.request()` 请求的 `options` 中显式地指定超时时间。设置为 `Infinity` 则永不超时。

``` es6
RpcClient.request({
  route: 'foo-bar',
  timeout: 8000 // ms
})
```

## 处理静态资源

静态资源可以通过两种方式进行处理：

- 在 JavaScript 被导入或在 template/CSS 中通过相对路径被引用。这类引用会被 webpack 处理。

- 放置在 public 目录下或通过绝对路径被引用。这类资源将会直接被拷贝，而不会经过 webpack 的处理。

### 从相对路径导入

当你在 JavaScript、CSS 或 *.vue 文件中使用相对路径 (必须以 . 开头) 引用一个静态资源时，该资源将会被包含进入 webpack 的依赖图中。在其编译过程中，所有诸如 `<img src="...">`、`background: url(...)` 和 CSS `@import` 的资源 URL 都会被解析为一个模块依赖。

例如，`url(./image.png)` 会被翻译为 `require('./image.png')`，而：

```html
<img src="./image.png">
```

将会被编译到：

```html
h('img', { attrs: { src: require('./image.png') }})
```

### URL 转换规则

- 如果 URL 是一个绝对路径 (例如 `/images/foo.png`)，它将会被保留不变。

- 如果 URL 以 `.` 开头，它会作为一个相对模块请求被解释且基于你的文件系统中的目录结构进行解析。

- 如果 URL 以 `~` 开头，其后的任何内容都会作为一个模块请求被解析。这意味着你甚至可以引用 Node 模块中的资源：

```html
<img src="~some-npm-package/foo.png">
```

如果 URL 以 `@` 开头，它也会作为一个模块请求被解析。它的用处在于 Vue CLI 默认会设置一个指向 `<projectRoot>/src` 的别名 `@`。(仅作用于模版中)

### public 文件夹

任何放置在 public 文件夹的静态资源都会被简单的复制，而不经过 webpack。你需要通过绝对路径来引用它们。

注意我们推荐将资源作为你的模块依赖图的一部分导入，这样它们会通过 webpack 的处理。这些文件都存放在 `/src/assets/` 文件夹下，并通过其它文件作为依赖导入。

## alias & paths

框架定义了一系列的别名来指向常用路径。

`__static`: 这是一个全局变量，指向 public 文件夹。当项目被打包到生产环境时，public 文件夹中的文件路径会发生改变，使用 `__static` 变量则可保证无论是生产环境还是开发环境都可以正确访问到所需的资源。

`@`: 路径的别名，指向 `/src/`，一般在任何需要使用路径的地方可以使用该别名，只要该文件是被 webpack 处理的。例如:

``` js
import store from '/src/store'
```

## 预置资源

### Vue Plugin

以下将使用 `vm` 来代表一个 Vue 实例。

- alert-error

  使用 `vm.$alertError(error, callback)` 来针对错误信息进行弹框提示。如果制定了 `callback`，将在弹出对话框之后执行。

- event-bus
  
  event-bus 是一个事件总线，用于在非父子组件之间传递消息。它本身是一个 vue 组件。

  ```
  vmA.$bus.$emit('event-name')
  vmB.$bus.$on('event-name', () => {...})
  ```

- lodash

  通过 `vm.$lodash` 来调用 `lodash` 库，无需引入

- vue-electron

  通过 `vm.$electron` 可以调用 `electron` 库，无需引入

- rpc-client

  通过 vm.$rpcClient 来调用 rpcClient 对象。

### 全局 CSS 变量

'@/styles/global-variables.scss' 中的变量，可以在任何 .vue 组件中直接使用，而无需额外导入。你可以将需要全局使用的变量 import 到该文件中。例如，_colors.scss 中的变量已经导入该文件，因而可以在任何 .vue 组件中直接使用。

### element-ui

element-ui 已经全局导入，可以直接使用所有组件。

### font-awesome

集成了 font-awesome 5 的免费图标库。通过在图标分类的类名前加上 el-icon 前缀，即可以与 element-ui 的内置 icon 一样的方式使用。

我们可以在官网图标库中查询图标。例如，对于官网图标中的类：class="fas fa-cog"，可以按照如下方式调用：

<i class="el-icon-fas fa-cog"></i>

## CSS 相关

### 引用静态资源

所有编译后的 CSS 都会通过 css-loader 来解析其中的 url() 引用，并将这些引用作为模块请求来处理。这意味着你可以根据本地的文件结构用相对路径来引用静态资源。另外要注意的是如果你想要引用一个 npm 依赖中的文件，或是想要用 webpack alias，则需要在路径前加上 ~ 的前缀来避免歧义。更多细节请参考处理静态资源。

### 预处理器

项目使用预处理器 (Dart-Sass)，因此你可以使用 sass/scss 格式。

你可以导入相应的文件类型，或在 *.vue 文件中这样来使用：

``` scss
<style lang="scss">
  $color: red;
</style>
```

### CSS Modules

你可以通过 `<style module>` 以开箱即用的方式在 `*.vue` 文件中使用 CSS Modules。

如果想在 JavaScript 中作为 CSS Modules 导入 CSS 或其它预处理文件，该文件应该以 `.module.(css|sass|scss)` 结尾：

``` js
import styles from './foo.module.css'
// 所有支持的预处理器都一样工作
import sassStyles from './foo.module.scss'
```

## 应用程序路径

- `appData`: 每个用户的应用程序数据目录
- `userData`: 储存你应用程序设置文件的文件夹，默认是 appData 文件夹附加应用的名称

应用程序的数据、设置、日志文件都存储在 `userData` 文件夹下。

请参考 Electron 文档：https://www.electronjs.org/docs/api/app#appgetpathname

## Debug & Logging

### 开发环境中的调试:

Electron Main Process: stdio 的输出会显示在 console 中。

Python: stdio 会转发到 Electron Main Process，并显示在 console 中。

Renderer Process: 由于 Renderer Process 是 BrowserWindow 中的渲染进程，因此其调试和普通网页一样，可以通过 Developer Tools 进行。当 Developer Tools 关闭时，可以通过已经定义的快捷键：`Ctrl+Shift+D` 来打开。（为了不影响 UI 的布局，请通过 Developer Tools 中的选项，将 Developer Tools 设置为 "在独立窗口中显示"。）

Vue.js Devtools: 框架集成了 Vue.js Devtools，在 Developer Tools 中显示为 Vue 选项卡。

### 生产环境中的调试：

Electron Main Process 和 Python: 在生产环境中，无法通过 console 来查看信息。因此，生产环境中的调试需要借助以下的 Log 文件来实现。

Renderer Process: 在生产环境中，你依然可以通过快捷键来打开 Developer Tools，调试方法与 [在开发环境下的调试](#在开发环境下调试) 是一样的。

Vue.js Devtools 在开发环境下将不会加载。

### Log 文件：

Log 文件夹的路径为: `<User Data Folder>/Logs`。所有的 Log 文件都存放在这里。

python Server 的 log 文件为 `RPC-Server-LOG`，Server 运行期间的所有异常会记录在该文件中。该文件以天为周期进行滚存，最多保留14天的记录。

Python stdio 中输出的内容将记录在 `Py-Stdio-LOG` 中，记录每次运行时产生的 Log，同时保留上一次运行的 log 为 `Py-Stdio-LOG.old`。更早的运行记录将在运行时删除。这些 log 对于 RPC-Server 无法成功启动时的原因诊断很有帮助。

自定义 logger：在 `py-code/src/logger_config.py` 中，你可以配置其它的 `logger`。所有 `logger` 记录的内容同时也都会冒泡到 `root logger` 并记录在 `RPC-Server-LOG` 文件中。

对于 Electron 进程，你可以使用 `electron-log` 模块进行记录。日志会保存在名为 Main 或 Renderer 的文件内。