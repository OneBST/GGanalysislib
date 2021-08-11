import numpy as np

def calc_coupling_p(p_a, p_b):
    # a为高优先级 b为低优先级
    # 保底抽数
    pos_a = len(p_a)  # 91
    pos_b = len(p_b)  # 11
    # 状态数为pos_a*pos_b个
    # 状态a_state*pos_b+b_state 表示a_state抽没出a且b_state没出b的状态
    M = np.zeros(((pos_a-1)*pos_b, (pos_a-1)*pos_b), dtype=float)
    # 高优先级没有抽到
    for i in range(1, pos_a-1):  # 本抽高优先级物品状态 1-89
        # 抽到了低优先级
        now_state = i*pos_b
        for j in range(pos_b-1):  # 上抽低优先级物品状态 0-9
            pre_state = (i-1)*pos_b + j
            trans_p = min(1-p_a[i], p_b[j+1])
            M[now_state][pre_state] = trans_p
        # 处理被挤走情况 上抽为10
        pre_state = (i-1)*pos_b + pos_b-1
        M[now_state][pre_state] =  1-p_a[i]

        # 低优先级也没有抽到
        for j in range(pos_b-1):  # 上抽低优先级物品状态 0-9
            now_state = i*pos_b + (j+1)
            pre_state = (i-1)*pos_b + j
            trans_p = max(1-p_a[i]-p_b[j+1], 0)
            M[now_state][pre_state] = trans_p
    # 高优先级的抽到了
    for i in range(pos_a-1):  # 上抽高优先级物品状态 0-89
        for j in range(1, pos_b):  # 上抽低优先级物品状态 0-10
            now_state = j  # 稳态时i/j不可能同时为0
            pre_state = i*pos_b + (j-1)
            trans_p = p_a[i+1]
            M[now_state][pre_state] = trans_p
    # 一直出高优先级物品的情况
    for i in range(pos_a-1):  # 上抽高优先级物品状态 0-88
        now_state = pos_b-1
        pre_state = i*pos_b + pos_b-1
        trans_p = p_a[i+1]
        M[now_state][pre_state] = trans_p
    
    # print(M.cumsum(axis=0)[989])
    # np.savetxt("check.csv", M, delimiter=',')
    # print(M)
    
    # 减去对角阵
    M = M-np.identity((pos_a-1)*pos_b)
    # 末行设置为1
    M[(pos_a-1)*pos_b-1] = 1

    # 设置向量
    X = np.zeros((pos_a-1)*pos_b, dtype=float)
    X[(pos_a-1)*pos_b-1] = 1

    # 解线性方程求解
    ans = np.linalg.solve(M, X)
    

    # stable_p_a = 0
    stable_p_b = 0
    # for j in range(pos_b):  # 低优先级物品状态 0-10
    #     stable_p_a += ans[j]
    for i in range(1, pos_a-1):  # 高优先级物品状态 1-89
        stable_p_b += ans[i*pos_b]
    return stable_p_b