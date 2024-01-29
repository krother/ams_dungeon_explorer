from unittest import result


def count_mines(minelist: list[str])->str:
    print(minelist)
    result = ""

    y = 0
    for i in minelist:
        x = 0
        for a in minelist[y]:
            if minelist [y][x] == "*":
                result += "*"
            else: 
                result += str(0) 
            print(x, y, a)
            x+= 1
        print(y, i)
        y += 1
        result += "\n"
    print (result)
    return result

def test_count_mines():
    input = """
.....*..
.*......
......*.
..**....
..*...*.
.......*""".strip().split("\n")

    result = count_mines(input)
    assert result == """
11101*10
1*100111
023211*1
02**1222
02*311*2
0111012*
""".strip()
