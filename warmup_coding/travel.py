
city = "Berlin"
destination = "Prague"

places = {
    # key      value (a list of strings)
    "Berlin": ["Dresden", "Leipzig", "Hamburg"],
    "Dresden": ["Berlin", "Leipzig", "Prague"],
    "Leipzig": ["Berlin", "Dresden", "Hamburg"],
    "Hamburg": ["Berlin", "Leipzig", "Copenhagen"],
    "Copenhagen": ["Hamburg"],
}

while city != destination:
    print("\nYou are in " + city)
    print("You can go to ", places[city])
    entered = input("Where do you want to go? ")
    if entered in places[city]:
        city = entered
    else:
        print("there is no such place!")

print("Congratulations! You reached your destination.")
