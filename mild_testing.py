import numpy as np

a,b = np.random.choice(["me","you"],size = 2,replace=False)
#print(a,b)

class FirstClass:
    def setdata(self,value):
        self.data = value
a = FirstClass()
b = FirstClass()
a.setdata(2)
b.setdata(1)
def oi(classudo,classo):
    print(classudo.data-classo.data)
