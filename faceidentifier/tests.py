from django.test import TestCase
import numpy as np

# Create your tests here.

x = np.array([[0.11565369, 0.30576237, 0.57858394]])
print(np.amax(x[0]))
result = np.where(x[0] == np.amax(x[0]))
print(result[0])
print(np.argmax(x))