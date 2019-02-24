#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import base64


def getBasefile(url):  # 获取订阅链接加密文本
    try:
        html = requests.get(url)
        html.raise_for_status
        html.encoding = html.apparent_encoding
        return str(html.text)
    except:
        return "错误"


def getAllLinks(url):  # 从加密文本解析出所有ss链接
    links = getBasefile(url)
    result = decodeInfo(links)
    alllinks = result.split('\\n')
    if len(alllinks[-1]) < 10:
        alllinks.pop()
    return alllinks


def getAllNodes(url):  # 从ss链接汇总得到所有节点信息
    allnodes = []
    links = getAllLinks(url)
    for ss in links:
        link = ss.split('//')[1].split("'")[0]
        # node = getNode(link) if ss.split(':')[0] == "ss" else getNodeR(link)
        if ss.split(':')[0] == "ss":
            node = getNode(link)
            allnodes.append(node)
        else:
            node = getNodeR(link)
            if checkNode(node):
                node = node[:-2]
                allnodes.append(node)
            else:
                continue
    return allnodes


# def formatLink(link):
#     l1 = link.replace('-', '+')
#     l2 = l1.replace('_', '/')
#     return l2


def getNode(link):  # 从ss链接中得到节点信息
    info = decodeInfo(link)
    method = info.split(':')[0]
    pwd = info.split("@")[0].split(":")[1]
    server = info.split("@")[1].split(":")[0]
    port = info.split(':')[2]
    remark = server
    node = [remark, server, port, method, pwd]
    return node


def getNodeR(link):  # 从ssr链接中得到节点信息
    info = decodeInfo(link)
    pwd = decodeInfo(info.split('/')[0].split(':')[-1]).split("'")[1]
    server = info.split(':')[0].split("'")[1]
    port = info.split(':')[1]
    protocol = info.split(':')[2]
    method = info.split(':')[3]
    obfs = info.split(':')[4]
    remark = getName(info.split('&')[2].split('=')[1])

    # print(server, port, method, pwd, protocol, obfs, remark)
    node = [remark, server, port, method, pwd, protocol, obfs]
    return node


def getName(info):  # 得到节点名称（有待合并）
    lens = len(info)
    # lenx = lens - (lens % 4 if lens % 4 else 4)
    if lens % 4 == 1:
        info = info + "==="
    elif lens % 4 == 2:
        info = info + "=="
    elif lens % 4 == 3:
        info = info + "="
    result = base64.urlsafe_b64decode(info).decode('utf-8', errors='ignore')
    return result


def checkNode(node):  # 检查节点是否是ss节点
    obfs = node[6]
    pro = node[5]
    if checkObfs(obfs) and checkPro(pro):
        return True
    else:
        return False


def checkObfs(str):  # 检查是否为ss混淆
    if str == "plain" or str.split('_')[-1] == "compatible":
        return True
    else:
        return False


def checkPro(str):  # 检查是否为ss协议
    if str == "origin" or str.split('_')[-1] == "compatible":
        return True
    else:
        return False


def decodeInfo(info):  # 解码加密内容
    lens = len(info)
    if lens % 4 == 1:
        info = info + "==="
    elif lens % 4 == 2:
        info = info + "=="
    elif lens % 4 == 3:
        info = info + "="
    result = str(base64.urlsafe_b64decode(info))
    return result


def setNodes(nodes):  # 设置节点
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


def setPG(nodes):  # 设置策略组 auto,Fallback-auto,Proxy
    proxy_names = []
    for node in nodes:
        proxy_names.append(node[0])
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

    gener = getBasefile(
        'https://raw.githubusercontent.com/JRQLS/ToClash/master/General.yml')
    with open("./clash.yml", "w") as f:
        f.writelines(gener)

    info = setNodes(nodes) + setPG(nodes)
    with open("./clash.yml", "a") as f:
        f.writelines(info)

    rules = getBasefile(
        'https://raw.githubusercontent.com/JRQLS/ToClash/master/rules.yml')
    with open("./clash.yml", "a") as f:
        f.writelines(rules)


if __name__ == "__main__":
    url = "https://jumpc.xyz/link/6fhH5kh5O9y"
    nodes = getAllNodes(url)

    getClash(nodes)
