from turtle import *
a = Turtle()
a.speed(7)
for i in range(2):
    a.fd(300)
    a.lt(90)
    a.fd(300)
    a.lt(90)
A = 290
AA = 290
for i in range(30):  
    a.lt(4)
    a.fd(A)
    a.lt(90)
    a.fd(AA)
    a.lt(90)
    a.fd(45)    
    A -= 10
    AA -= 10
done()