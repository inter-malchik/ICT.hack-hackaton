check_name = lambda x: x.isalpha()
check_num = lambda x: x.isdigit() and len(x) < 10


def clear_argument(s: str):
    forbidden = set(" !@#№%$^&*()><,.?/|\n\t")
    answer = ''
    for i in s:
        if i in forbidden:
            continue
        else:
            answer += i
    return answer
