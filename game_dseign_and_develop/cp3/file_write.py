file = open("data.txt", "w")
file.write("Sample file writing\n")
file.write("This is line 2\n")

text_lines = ["Chapter 3 \n"
              "Sample file writing\n"
              "This is line 5\n"
              "The six line looks like this\n"
              "Edit the file with any text editor\n"]
file.writelines(text_lines)
file.close()



__author__ = 'added new'
