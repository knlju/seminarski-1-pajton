lista = list()
str1 = """a\nb\n"""
strl = str1.split("\n")
lista += strl
lista.insert(2, "1")

for i in lista:
    print(i)
