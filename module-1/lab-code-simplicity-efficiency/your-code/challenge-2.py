a = input('Enter minimum string length: ')
b = input('Enter maximum string length: ')
n = input('How many random strings to generate? ')


def StringGenerator(a,b,n):
  import random
  letras=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9']
  lista = []
  while len(lista) < int(n):
    palabra = ""
    while len(palabra) < random.choice(range(int(a),int(b))):
      palabra += random.choice(letras)
    lista.append(palabra)
  return lista

print(StringGenerator(a,b,n))