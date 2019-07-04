# -*- coding: UTF-8 -*-

def is_match(string_ob, partten):
    # 首先检查长度是否为0
    str_len = len(string_ob)
    par_len = len(partten)
    sum_num = str_len + par_len
    product_num = str_len * par_len
    if sum_num == 0:
        return 0
    if sum_num > 0 and product_num == 0:
        return -1

    # 遍历parrten
    partten_top = partten[0]
    partten_next = partten[1:]
    str_top = string_ob[0]
    if partten_top == "*":
        for i in range(1, str_len):
            str_next = string_ob[i:]
            if is_match(str_next, partten_next) == 0:
                return 0
        return -1
    elif partten_top == "?":
        str_next = string_ob[1:]
        return is_match(str_next, partten_next)
    elif partten_top == str_top:
        str_next = string_ob[1:]
        return is_match(str_next, partten_next)
    else:
        return -1


if __name__ == '__main__':
    print (is_match("abc", "a?c"))
