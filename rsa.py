import math as maths
import random

def isPrime(n):
    global primeList
    global start
    if n == 1 or n == 0:
        return False
    if n in primeList:
        return True
    for d in primeList:
        if n % d == 0:
            return False
    if maths.isqrt(d) <= max(primeList):
        return True
    for d in range(start,maths.isqrt(n)+1,6):
        if n % d == 0 or n % (d+2) == 0:
            return False
    return True

def choosePrime(a, b):
    while True:
        p = random.randint(a,b)
        if isPrime(p):
            return p

def factor(num):
    global primeList
    factors = []
    x = 0
    while int(num) != 1:
        if num % primeList[x] == 0:
            factors.append(primeList[x])
            num = num / primeList[x]
            if num % primeList[x] == 0:
                x = -1
        x+=1

    return factors

def lcm(a, b):
    factorsA = factor(a)
    factorsB = factor(b)
    product = 1

    for i in factorsA:
        product = product * i
        if i in factorsB:
            factorsB.remove(i)
    for i in factorsB:
        product = product * i

    return product

def carTotient(a, b):
    return lcm(a-1, b-1)

## the modular multiplicative inverse of a number a mod n is b such that a*b mod n === 1
## this is found by representing the problem as a form of Bezout's identity and using the
## extended Euclidean algorithm to solve it
## this function solves the equation at = 1 mod n
def modInverse(a, n):
    t = 0
    newt = 1
    r = n
    newr = a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t-quotient*newt
        r, newr = newr, r-quotient*newr

    if r > 1:
        return "not invertible"
    if t < 0:
        t = t+n
    return t

## Calculate a^b mod n
## It does this incrementally rather than finding a^b and then taking that mod n to save memory
def modExp(a, b, n):
    c = 1
    for i in range(b):
        c = (a*c)%n
    return c

def encrypt(message, n, e):
    M = [ord(i) for i in message] ## The letters are converted to their ascii value
    c = [modExp(i,e,n) for i in M] ## The cipher text is M^e mod n for each letter
    print(f"ENCRYPTED MESSAGE: {c}")

def decrypt(c, n, d):
    print(f"PLAINTEXT: {''.join([chr(modExp(i,d,n)) for i in c])}")

def genKeys():
    ## Step 1 in wikipedia
    # p and q make up our private keys, as knowing p and q would let you deduce d which is the main component of the private key
    p = choosePrime(10**3, 10**4)
    while True:
        q = choosePrime(10**3, 10**4)
        if q != p:
            break

    ## Step 2
    # n is the first part of the public and private key
    n = p*q

    ## Step 3
    # l is the Carmichael totient of n (the lcm of p-1, q-1)
    l = carTotient(p, q)

    ## Step 4
    # e is the second part of the public key
    while True:
        e = choosePrime(3, l-1)
        if l % e != 0:
            break

    ## d is the second part of the private key
    d = modInverse(e, l)
    print(f"PUBLIC KEY: ({n},{e})")
    print(f"PRIVATE KEY: ({n},{d})")

while True:
    choice = int(input("Type 1 to generate keys, 2 to encrypt a message, 3 to decrypt a message:\n"))
    if choice == 1:
        print("Please wait a bit")
        with open("primeList.txt", "r") as f:
            primeList = [int(i) for i in f.readlines()[:1000]]
        start = primeList[-1]
        genKeys()

    if choice == 2:
        message = input("Enter your message:\n")
        key = [int(i) for i in ''.join(c for c in input("Enter the public key in the form (a,b):\n") if c not in '()[] ').split(',')]
        encrypt(message, key[0], key[1])

    if choice == 3:
        cipher = [int(i) for i in ''.join(c for c in input("Enter your cipher:\n") if c not in '()[] ').split(',')]
        key = [int(i) for i in ''.join(c for c in input("Enter the private key in the form (a,b):\n") if c not in '()[] ').split(',')]
        decrypt(cipher, key[0], key[1])
    print('---')
