#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

# from pprint import pprint


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d


def getallNodes(file):
    # 得到所有节点
    with open(file, 'r') as f:
        nodes = []
        out = json.load(f, object_hook=JSONObject)

        for nd in out.configs:
            node = []
            # pprint(nd.password)
            password = getAttr(nd, 'password')  # 密码
            method = getAttr(nd, 'method')  # 加密方式
            remarks = getAttr(nd, 'remarks')  # 节点名称
            server = getAttr(nd, 'server')  # 节点IP或域名
            obfs = getAttr(nd, 'obfs')  # 协议
            protocol = getAttr(nd, 'protocol')  # 混淆
            group = getAttr(nd, 'group')  # 节点组（机场）
            server_port = getAttr(nd, 'server_port')  # 节点端口

            if checkObfs(obfs) and checkPro(protocol):
                node = [remarks, server, server_port, method, password, group]
                nodes.append(node)
            else:
                continue
        # pprint(nodes)
        return nodes


def getAttr(ob, attr):
    # 得到节点属性
    if hasattr(ob, attr):
        at = getattr(ob, attr)
    else:
        at = None
    return at


def checkObfs(str):
    # 检查是否为ss混淆
    if str == "plain" or str.split('_')[-1] == "compatible":
        return True
    else:
        return False


def checkPro(str):
    # 检查是否为ss协议
    if str == "origin" or str.split('_')[-1] == "compatible":
        return True
    else:
        return False


def getGroupNodes(group, file):
    # 得到某个group（机场）的所有节点
    # nodes = getallNodes(file)
    nodes = []
    nodes_1 = getallNodes(file)
    for node in nodes_1:
        if node[-1] == group:
            nodes.append(node)
    return nodes
    # pass


def setNodes(nodes):
    # 设置节点
    proxies = []
    for node in nodes:
        name = node[0]
        server = node[1]
        port = node[2]
        cipher = node[3]
        pwd = node[4]
        proxy = "- { name: " + str(
            name).strip() + ", type: ss, server: " + str(
                server) + ", port: " + str(port) + ", cipher: " + str(
                    cipher) + ", password: " + str(pwd) + " }\n"
        proxies.append(proxy)
    proxies.insert(0, '\nProxy:\n')
    return proxies


def setPG(nodes):
    # 设置策略组 auto,Fallback-auto,Proxy
    proxy_names = []
    for node in nodes:
        proxy_names.append(node[0])
    # print(str(proxy_names))
    auto = "- { name: 'auto', type: url-test, proxies: " + str(
        proxy_names
    ) + ", url: 'http://www.gstatic.com/generate_204', interval: 300 }\n"

    Fallback = "- { name: 'Fallback-auto', type: fallback, proxies: " + str(
        proxy_names
    ) + ", url: 'http://www.gstatic.com/generate_204', interval: 300 }\n"

    Proxy = "- { name: 'Proxy', type: select, proxies: " + str(
        proxy_names) + " }\n"
    ProxyGroup = ['\nProxy Group:\n', auto, Fallback, Proxy]
    # ProxyGroup.insert(0, 'Proxy Group:\n')
    return ProxyGroup


def getClash(nodes):
    with open("./General.yml", "r") as f:
        gener = f.read()
    with open("./clash.yml", "w") as f:
        f.writelines(gener)

    info = setNodes(nodes) + setPG(nodes)
    with open("./clash.yml", "a") as f:
        f.writelines(info)

    with open("./rules.yml", "r") as f:
        rules = f.read()
    with open("./clash.yml", "a") as f:
        f.writelines(rules)


if __name__ == "__main__":
    # 请设置协议：origin，混淆方式：plain，或自行修改代码
    file = "./export.json"  # ss本地配置文件
    nodes = getallNodes(file)
    # nodes = getGroupNodes("MySSR", file) # 自行修改为所需group即可
    # 两种nodes获取方式。第一种获取json中的所有节点；第二种获取json中指定机场的节点

    getClash(nodes)