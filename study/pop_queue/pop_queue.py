# -*- coding: UTF-8 -*-
list = []
def pop_queue(list_in, list_out, list_que):
    """
    (n, m)表示有n个元素还没有入栈，栈内目前有m个元素时，出栈的可能数
    初始条件：(n,0)只能进行入栈操作，因此，(n, 0) = (n-1, 1)
    递归条件：当m>1时，可以入栈：(n, m) = (n-1, m+1)
                       可以出栈：(n, m)= (n, m-1)
    终止条件：当没有元素可以入栈时，(0,m) = F(m)
    :param n:
    :param m:
    :return:
    """

    len_in = len(list_in)
    len_out = len(list_out)
    len_que = len(list_que)

    if len_que == 0:
        # 初始条件，若输出为空，且栈内为空，只能入栈
        item = list_in.pop()
        list_que.append(item)
        pop_queue(list_in, list_out, list_que)

    elif len_in == 0:
        # 终止条件，只能出栈
        que_tmp = list_que[::-1]
        str_res = ",".join(list_out + que_tmp)
        list.append(str_res)


    else:
        # 入栈情况：
        item = list_in.pop()
        list_que.append(item)
        pop_queue(list_in, list_out, list_que)
        # 出栈情况, 需要复原
        list_in.append(item)
        list_que.pop()

        item = list_que.pop()
        list_out.append(item)
        pop_queue(list_in, list_out, list_que)
        list_que.append(item)
        list_out.pop()


if __name__ == '__main__':
    str_in = raw_input("输入原始序列，以逗号分隔：")
    list_in = str_in.split(",")
    pop_queue(list_in,[],[])

    for line in list:
        print line
