"""
Checkerboard: Write a program that prints this:

#_#_#_#_
_#_#_#_#
#_#_#_#_
_#_#_#_#
#_#_#_#_
_#_#_#_#
#_#_#_#_
_#_#_#_#
"""
print(
"""
#_#_#_#_
_#_#_#_#
#_#_#_#_
_#_#_#_#
#_#_#_#_
_#_#_#_#
#_#_#_#_
_#_#_#_#
"""
)

'''for i in range(4):
    print("""#_#_#_#_
_#_#_#_#""")'''

    
line = "#_#_#_#_"
line2 = "_#_#_#_#"
for i in range(8):
    if (i % 2 == 0):
        print(line)
    else:
        print(line2)

print()
for i in range(8):
    print(line)
    line, line2 = line2, line
