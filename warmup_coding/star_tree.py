"""
🎯 Write a program that outputs the following image:

     *
    ***
   *****
  *******
 *********
***********
"""
print(

"     *\n"
"    ***\n"
"   *****\n"
"  *******\n"
" *********\n"
"***********\n")


for i in range(0, 6):
    spaces = 6 - i
    stars = 2*i + 1
    print(" "*spaces, "*"*stars)