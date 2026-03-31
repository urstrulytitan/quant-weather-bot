import math

def psi(omega, imb, flicker, w1=0.33, w2=0.34, w3=0.33, beta=0.5):
    z = w1*omega + w2*imb + w3*flicker - beta
    return 1/(1+math.exp(-z))