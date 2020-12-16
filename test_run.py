from lunch_table import LunchTable

lt = LunchTable(5, 5)

STEPS = 10

for i in range(STEPS):
    print(lt)
    lt.update()