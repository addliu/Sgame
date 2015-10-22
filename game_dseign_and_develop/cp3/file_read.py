file = open("data.txt", "r")
char = file.read(10)
print(char)
print(file.read())
one_line = file.readline()
all_data = file.readlines()
file.close()

__author__ = 'added new'
