from lunch_table import LunchTable

lt = LunchTable(5, 5)

for i in range(100):
    print(lt)
    lt.update()