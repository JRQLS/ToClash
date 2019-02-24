#!/usr/bin/env python
def getNodes(file):  # 得到节点
    with open(file, "r") as f:
        nodes = []
        ProxyGroup = []
        while (1):
            out = f.readline()
            if out == '[Rule]\n':
                break
            if len(out.split(',')) >= 2 and str(
                    out.split(',')[0].split('=')[1]).strip() == 'custom':
                # print(out)
                nodes.append(out)
            elif out.split('=')[0].upper().strip() == 'PROXY' or out.split(
                    '=')[0].upper().strip() == 'AUTO':
                ProxyGroup.append(out)
    return nodes, ProxyGroup


def setNodes(file):  # 设置节点
    nodes = getNodes(file)[0]
    for i, node in enumerate(nodes):
        # newnode = "- { name: ss1,type: ss,server: server,port: 443,cipher: AEAD_CHACHA20_POLY1305,password: password}"
        name = node.split(',')[0].split('=')[0]
        server = node.split(',')[1]
        port = node.split(',')[2]
        cipher = node.split(',')[3]
        password = node.split(',')[4]
        # print(name + server + port + cipher + password)
        newnode = "- { name: " + str(
            name).strip() + " ,type: ss, server: " + str(
                server) + ", port: " + str(port) + ", cipher: " + str(
                    cipher) + ", password: " + str(password) + " }\n"
        nodes[i] = newnode
        # print(newnode)
    nodes.insert(0, '\nProxy:\n')
    return nodes


def setPG(file):
    # 设置策略组，暂只支持auto和proxy两种模式
    Groups = getNodes(file)[1]
    ProxyGroup = []
    for group in Groups:
        if group.split('=')[0].upper().strip() == 'AUTO':
            nodes = group.split('=')[1].split(',')
            for i, node in enumerate(nodes):
                if node.lower().strip() == 'select' or node.lower().strip(
                ) == 'direct' or node.lower().strip(
                ) == 'url-test' or node.lower().strip() == 'url':
                    nodes.remove(node)
                    continue
                nodes[i] = nodes[i].replace("\n", "")
                nodes[i] = nodes[i].strip()
            newgroup = "- { name: " + str(
                group.split('=')[0]
            ) + ", type: url-test, proxies: " + str(
                nodes
            ) + ", url: 'http://www.gstatic.com/generate_204', interval: 300 }\n"

        elif group.split('=')[0].upper().strip() == 'PROXY':
            nodes = group.split('=')[1].split(',')
            for i, node in enumerate(nodes):
                if node.lower().strip() == 'select' or node.lower().strip(
                ) == 'direct':
                    nodes.remove(node)
                    continue
            nodes[i] = nodes[i].replace("\n", "")
            nodes[i] = nodes[i].strip()
            newgroup = "- { name: Proxy, type: select, proxies: " + str(
                nodes) + " }\n"

        ProxyGroup.append(newgroup)
    formGroup(ProxyGroup)
    ProxyGroup.insert(0, '\nProxy Group:\n')
    return ProxyGroup


def formGroup(ProxyGroup):
    # 修改策略组顺序
    for i, pg in enumerate(ProxyGroup):
        if pg.split(',')[0].split(':')[-1].lower().strip() == 'auto':
            ProxyGroup[0], ProxyGroup[i] = ProxyGroup[i], ProxyGroup[0]
            break
        else:
            continue
    return ProxyGroup


def getYml(file):
    # 得到clash配置文件
    with open("./General.yml", "r") as f:
        gener = f.read()
    with open("./clash.yml", "w") as f:
        f.writelines(gener)

    info = setNodes(file) + setPG(file)
    with open("./clash.yml", "a") as f:
        f.writelines(info)

    with open("./rules.yml", "r") as f:
        rules = f.read()
    with open("./clash.yml", "a") as f:
        f.writelines(rules)


if __name__ == "__main__":
    # 本地文件
    file = "./surge.conf"
    getYml(file)
