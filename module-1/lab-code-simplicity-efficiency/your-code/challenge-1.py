"""
This is a dumb calculator that can add and subtract whole numbers from zero to five.
When you run the code, you are prompted to enter two numbers (in the form of English
word instead of number) and the operator sign (also in the form of English word).
The code will perform the calculation and give the result if your input is what it
expects.

The code is very long and messy. Refactor it according to what you have learned about
code simplicity and efficiency.
"""

print('Welcome to this calculator!')
print('It can add and subtract whole numbers from zero to five')
a = input('Please choose your first number (zero to five): ')
b = input('What do you want to do? plus or minus: ')
c = input('Please choose your second number (zero to five): ')

def calculator(a,b,c):
  diccionario = {"zero": 0 ,"one": 1, "two": 2, "three": 3, "four":4, "five": 5}
  a1 = diccionario.get(a)
  c1 = diccionario.get(c) 
  if b == "plus":
    d = a1 + c1
  if b == "minus":
    d = a1 - c1
  print("{} {} {} equals {}".format(a,b,c,d))

calculator("two","plus","one")