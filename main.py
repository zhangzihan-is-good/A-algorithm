"""
在此处可以修改初始状态（16进制表示），因为16进制表示可以让每个格子都用一个字符表示
比如：
    1  2  3  4
    5  6  7  8
    9 10 11 12
   13 14 0  15
   其中0表示空格，转化为16进制
   1 2 3 4
   5 6 7 8
   9 a b c
   d e f 0
   按行连接在一起，start就为‘123456789abcde0f'
"""
start = '51239674dab80efc'
goal = '123456789abcdef0'
#把16进制数转化成10进制数
def transf(i):
    if type(i) == int:
        return i
    else:
        if i =='a':
            return 10
        if i =='b':
            return 11
        if i =='c':
            return 12
        if i =='d':
            return 13
        if i =='e':
            return 15
        if i =='f':
            return 16
# 计算状态对应的逆序数
def THEnum(node):
    Sum = 0
    for i in range(1, 16):
        num = 0
        for j in range(0, i):
            if node[j] > node[i] and node[i] != '0':
                num = num + 1
        Sum += num
    return Sum
# h(n)函数，用于计算估价函数f(n)，这里的h(n)选择的是与目标相比错位的数目
def Hn(node):
    hn = 0
    for i in range(0, 16):
        if node[i] != goal[i]:
            hn += 1
    return hn
# 拓展node状态对应的子结点
def Expand(node):
    global expand
    tnode = []
    state = node.index("0")
    elist = expand[state]
    j = state
    for i in elist:
        j = state
        i = transf(i)
        j = transf(j)
        if i > j:
            i, j = j, i
        re = node[:i] + node[j] + node[i + 1:j] + node[i] + node[j + 1:]
        tnode.append(re)
    return tnode
# 将最后的结果按格式输出
def PRINT(result):
    for i in range(len(result)):
        print("step--" + str(i + 1))
        print(result[i][:4])
        print(result[i][4:8])
        print(result[i][8:12])
        print(result[i][12:])
# 选择opened表中的最小的估价函数值对应的状态
def MIN(opened):
    ll = {}
    for node in opened:
        k = Fn[node]
        ll[node] = k
    kk = min(ll, key=ll.get)
    return kk
# 主程序开始
opened = []
closed = []
Gn = {}  # 用来存储状态和对应的深度，也就是初始结点到当前结点的路径长度
Fn = {}  # 用来存放状态对应的估价函数值
parent = {}  # 用来存储状态对应的父结点
# expand中存储的是九宫格中每个位置对应的可以移动的情况
# 当定位了0的位置就可以得知可以移动的情况
expand = {0: [1, 4], 1: [0, 2, 5], 2: [1, 3,6],
          3: [2,7], 4: [0,5,8], 5: [1,4,6,9],
          6: [2,5,7,10], 7: [3,6,11], 8: [4,9,12],
          9: [5,8,10,13], 10: [6,9,11,14], 11: [7,10,15],
          12: [8, 13], 13: [9,12,14], 14: [10,13,15],
          15: [11,14]}
idd=0
if start == goal:
    print("初始状态和目标状态一致！")
# 判断从初始状态是否可以达到目标状态
else:
    parent[start] = -1  # 初始结点的父结点存储为-1
    Gn[start] = 0  # 初始结点的g(n)为0
    Fn[start] = Gn[start] + Hn(start)  # 计算初始结点的估价函数值
    #每一个棋盘算作一个节点
    opened.append(start)  # 将初始结点存入opened表
    while opened:
        #如果500步以内无法达到视为不可达
        idd += 1
        if idd > 500:
            print("目标不可达")
            exit()
        current = MIN(opened)  # 选择估价函数值最小的状态
        del Fn[current]
        opened.remove(current)  # 将要遍历的结点取出opened表
        if current == goal:
            break
        if current not in closed:
            closed.append(current)  # 存入closed表
            Tnode = Expand(current)  # 扩展子结点
            for node in Tnode:
                # 如果子结点在opened和closed表中都未出现，则存入opened表
                # 并求出对应的估价函数值
                if node not in opened and node not in closed:
                    Gn[node] = Gn[current] + 1
                    Fn[node] = Gn[node] + Hn(node)
                    parent[node] = current
                    opened.append(node)
                else:
                    # 若子结点已经在opened表中，则判断估价函数值更小的一个路径
                    # 同时改变parent字典和Fn字典中的值
                    if node in opened:
                        fn = Gn[current] + 1 + Hn(node)
                        if fn < Fn[node]:
                            Fn[node] = fn
                            parent[node] = current
    result = []  # 用来存放路径
    result.append(current)
    while parent[current] != -1:  # 根据parent字典中存储的父结点提取路径中的结点
        current = parent[current]
        result.append(current)
    result.reverse()  # 逆序
    PRINT(result)  # 按格式输出结果
