import numpy as np

def get_boundary():
    down_a = 21012
    up_b = 88088
    return down_a, up_b


def get_potential_possible(cnt, final):
    if cnt == 0:
        return ['1', '6', '8', '9']
    elif cnt == final:
        return ['0', '1', '8']
    else:
        return ['0', '1', '6', '8', '9']


def get_reflection(head):
    reflection = {'0':'0', '1':'1', '6':'9', '8':'8', '9':'6'}
    return reflection[head]


def get_mid(boundary):
    l = len(str(boundary))
    if l%2 == 0:
        return int(l/2 - 1)
    else:
        return l//2


def get_inside():
    pass


def get_solution(down_a, up_b):
    lenx = get_mid(down_a)
    ans = {i:[] for i in range(lenx+1)}
    for item in range(lenx+1):
        a_head = int(str(down_a)[item])
        b_head = int(str(up_b)[item])
        print(f"{item}: a = {a_head}, b = {b_head}")
        for num in get_potential_possible(item, lenx):
            print(f"num = {num}, a = {a_head}, b = {b_head}")
            if int(num) >= a_head and int(num) <= b_head:
                if int(num) > a_head and int(num) < b_head:
                    ans[item].append(num)
                elif int(num) == a_head:
                    tail = get_reflection(num)
                    print(item)
                    if int(tail) >= int(str(a_head)[-min(item, lenx-1)]):
                        ans[item].append(num)

                else: # int(num) == b_head
                    tail = get_reflection(num)
                    if int(tail) <= int(str(b_head)[-min(item, lenx-1)]):
                        ans[item].append(num)

            
    print(ans)


if __name__ == "__main__":
    down_a, up_b = get_boundary()
    get_solution(down_a, up_b)
    
