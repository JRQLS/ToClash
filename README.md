# ToClash

## SS_clash(from ss Local configuration file)

### 功能：

该文件夹实现将ss本地配置文件转换为clash支持的配置文件

### 使用：

下载该文件夹，然后用本地配置文件（json文件）替换export.json文件，为方便使用，推荐仍命名为export.json。之后命令行cd进入该文件夹执行SS_clash.py脚本即可。运行完成后将在同一文件夹生成clash.yml文件，即可使用

###注意：

这四个文件需在同一文件夹。同时当前脚本仅有auto,Fallback-auto,Proxy三个规则组，有需要自行修改配置文件。

当前仅通过mac版ssr添加的个人节点以及自用机场订阅得到的节点导出的配置文件进行测试无误，不保证其他机场可以使用



## SS_clash(from ss subscription)（暂未完成）

###功能：

支持直接通过ss订阅生成clash配置文件

### 使用：

下载py脚本，替换脚本内的订阅链接，运行即可（因个人使用的机场连接触发短期订阅数量限制，暂未实现该功能）

## Surge_clash(local)

### 功能：

支持将本地surge配置文件转换为clash配置文件，适合那些机场只提供了surge文件而没有提供订阅的用户使用

有订阅的用户可以使用F大提供的转换链接即可（将http://example.com替换为自己的托管地址）：

https://tgbot.lbyczf.com/surge2clash?url=http://example.com

###使用：

和ss_clash本地转换类似，下载该文件夹并放入surge配置文件，然后修改脚本内的倒数第二行的配置文件名称（修改配置文件名称和脚本相同也可以），然后执行py脚本即可得到clash配置文件。

### 注意：

因该脚本完成较早，当时是为了转换老板娘的surge配置文件。其配置文件内策略组有较多问题，因此脚本大量代码用来处理其error，较为混乱。并且本人只使用过老板娘的本地surge文件（他人提供）以及自用的myssr surge配置文件（相对规范），其他机场的配置文件不确定可以正常使用。同时本人未使用过surge，如有什么不足请提出。

## 最后：

###有问题发issue，会定期查看

