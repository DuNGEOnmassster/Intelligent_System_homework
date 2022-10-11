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


def check_possible(down_a, up_b, head, cnt):
    head_str = ''
    tail_str = ''
    for i in head:
        head_str += i
        tail_str += get_reflection(i)
    tail_str = tail_str[::-1]

    lenx = get_lenx(down_a, cnt)
    min_num = int(head_str + '0'*lenx + tail_str)
    max_num = int(head_str + '9'*lenx + tail_str)
    # print(f"max = {max_num} min = {min_num}")
    # print(f"down_a = {down_a}, up_b = {up_b}")
    return max_num >= down_a and min_num <= up_b


def get_lenx(down_a, cnt):
    mid = get_mid(down_a)
    # print(f"mid = {mid}")
    if len(str(down_a))%2 == 1:
        len_x = 2*(mid-cnt)-1
    else:
        len_x = 2*(mid-cnt)
    return len_x


def get_extend(down_a, up_b, head, cnt, mid):
    new_head = head.copy()
    ans = []
    possibles = get_potential_possible(cnt, mid)
    for p in possibles:
        new_head.append(p)
        if check_possible(down_a, up_b, head, cnt):
            ans.append(new_head)
        new_head.pop()
    return ans


def get_solution(down_a, up_b):
    cnt = 0
    head = []
    ans = []
    mid = get_mid(down_a)
    while cnt <= mid:
        possibles = get_potential_possible(cnt, mid)
        for p in possibles:
            head.append(p)
            if check_possible(down_a, up_b, head, cnt):
                # for every possible number, keep on 
                ans.append(head.copy())
                print(head)

            head.pop()
        print(ans)
        # after getting all the possible solution, cnt+1
        cnt = cnt + 1

    # print(ans)


def test_struct():
    ans = {i:[] for i in range(3)}
    print(ans)
    for i in range(3):
        ans[i].append(i)
    print(ans)
    a = 54829
    num = '1'
    if 0 < int(str(a)[-1*int(num)]):
        print(1)

if __name__ == "__main__":
    down_a, up_b = get_boundary()
    print(f"check possibles = {check_possible(down_a, up_b, ['6', '8'], 1)}")
    get_solution(down_a, up_b)
    test_struct()