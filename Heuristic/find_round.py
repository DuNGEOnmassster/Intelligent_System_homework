def get_boundary():
    down_a = 21012
    up_b = 88088
    return down_a, up_b


def get_potential_possible(cnt):
    if cnt == 0:
        return ['1', '6', '8', '9']
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
    print(f"max = {max_num} min = {min_num}")
    print(f"down_a = {down_a}, up_b = {up_b}")
    return max_num >= down_a and min_num <= up_b


def get_lenx(down_a, cnt):
    mid = get_mid(down_a)
    print(f"mid = {mid}")
    if len(str(down_a))%2 == 1:
        len_x = 2*(mid-cnt)-1
    else:
        len_x = 2*(mid-cnt)
    return len_x


def get_solution(down_a, up_b):
    cnt = 0
    while cnt <= get_mid(down_a):
        possibles = get_potential_possible(cnt)
        head = []
        for p in possibles:
            head.append(p)
            if check_possible(down_a, up_b, head, cnt):
                # for every possible number, keep on 
                print(head)

            head.pop()
            
        # after getting all the possible solution, cnt+1
        cnt = cnt + 1

def test_struct():
    head = []
    for i in range(3):
        head.append(i)
        print(f"{i}: head = {head}")
        head.pop()


if __name__ == "__main__":
    down_a, up_b = get_boundary()
    print(f"check possibles = {check_possible(down_a, up_b, ['6'], 0)}")
    test_struct()