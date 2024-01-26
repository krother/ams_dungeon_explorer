"""Josephus problem (academis.eu/advanced_python/challenges/josephus.html)"""
monks = [
       "Adalbertus", "Bonifacius", "Commodus",
       "Dominicus", "Emarius", "Franziskus",
       "Gustavus", "Henrik", "Iohannes"
       ]
i = 4  # position of the first monk to delete (the 5th)

while len(monks) != 1:
    print(monks[i], "gets assassinated")
    del monks[i]             # same as monks.remove(monks[i])  or monks.pop(i)
    i += 4                   # count forward 5 monks minus 1 that got deleted
    while i >= len(monks):   # wrap around and start counting from the beginning
        i -= len(monks)      # i = i % len(monks) instead of while
    print(monks, i)