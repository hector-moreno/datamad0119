def my_function(X):
    print("The longest side possible is " + str(max(max([[x,y,z] for x in range(5,X)for y in range(4,X)for z in range(3,X) if (x*x==y*y+z*z)]))))

X = input("What is the maximal length of the triangle side? Enter a number: ")

my_function(int(X))