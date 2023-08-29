#BASIC TOOL SET 

def Convert_Text(_string):
    #create an empty list to store integers
    integer_list = []
    #loop goes through each character in the string 
    for character in _string: 
        #convert character to integer and add to the integer list
        integer_list.append(ord(character))
    #return the integer list
    return integer_list
    
def Convert_Num(_list):
    #create an empty string
    _string = ''
    #loop goes through each integer in the list 
    for i in _list:
        #convert integer to string and add to _string
        _string += chr(i)
    #return the string we created at the beginning
    return _string   
    
#FIRST TOOL SET    

def FME(b, n, m): 
    #initialize result
    result = 1
    #assign b to square because we will be repeatedly squaring b
    square = b
    #while the power n is greater than 0, this loop will convert n to binary
    while n > 0:
        #create binary digit
        k = n % 2
        #if binary digit is 1
        if k == 1:
            #multiply current value of result by the current square and mod m
            result = (result * square) % m
        #compute the Square and Mod method
        square = (square * square) % m
        #right shift to get to the next bit
        n = n >> 1
    #return result
    return result
    
def Euclidean_Alg(a, b):
    #while a and b are greater than 0
    while (a > 0 and b > 0):
        #a mod b is assigned to remainder
        remainder = a % b
        #a is updated to be b 
        a = b
        #b is updated to be the remainder
        b = remainder
    #if a is greater than 0
    if a > 0:
        #return a as the GCD   
        return a  
        
#SECOND TOOL SET 

def Find_Public_Key_e(p, q):
    #compute n 
    n = p*q
    #use for loop to get e in range of 2 and 100    
    for e in range(2,100):
        #e has to be relatively prime with (p-1)(q-1) and 
        #e can't be p or q
        if Euclidean_Alg(e, (p-1)*(q-1)) == 1 and e != p and e != q:
            #return the values of n and e
            return n, e
          
#compute GCD and Bezout's Coefficients (BC)
def gcd(m,n):
    #m >= n >= 0
    #BC of m 
    (s1,t1) = (1,0)
    #BC of n 
    (s2,t2) = (0,1)
    #continue while n is greater than 0
    while (n > 0):
        #k is assigned to be the remainder of m mod n 
        k = m % n
        #q is assigned to be the integer quotient of m divided by n
        q = m // n
        
        #m is updated to be n 
        m = n
        #n is updated to be k
        n = k
        
        #update the new m's BC to n's BC
        (s_1,t_1) = (s2,t2)
        #update the new n's BC using k
        (s_2,t_2) = (s1-(q*s2),t1-(q*t2))

        #update m's BC to the new m's BC
        (s1,t1) = (s_1,t_1)
        #update n's BC to the new n's BC
        (s2,t2) = (s_2,t_2)
        
    #return s1, which is d
    return s1
    
# PUTTING IT ALL TOGETHER

def Find_Private_Key_d(e, p, q):
    #compute d, which is the s1 of e and (p-1)(q-1)
    d = gcd(e,(p-1)*(q-1))
    #continue loop while d is negative
    while d < 0:
        #add (p-1)(q-1) to d
        d = d + ((p-1)*(q-1))
    #return the new value of d
    return d  
    
def Encode(n, e, message):
    #create a cipher text list 
    cipher_text = []
    #convert a string message into an integer list using Convert_Text function
    integer_list = Convert_Text(message)
    #loop through each number in the integer list
    for number in integer_list:
        #use fast modular exponentiation on each number and add to cipher text list
        cipher_text.append(FME(number,e,n))
    #return cipher text list 
    return cipher_text 
    
def Decode(n, d, cipher_text):
    #create a message string
    message = ''
    #create a decipher text list
    decipher_text = []
    #for each number in cipher text list 
    for number in cipher_text: 
        #use fast modular exponentiation on each number and add to decipher text list 
        decipher_text.append(FME(number,d,n))
    #convert each number into a string using Convert_Num function
    message = Convert_Num(decipher_text)
    #return the string message
    return message

# DEMO

#select two prime numbers, p and q    
p = 107
q = 109

#generate Public Key using the Find_Public_Key_e function  
n,e = Find_Public_Key_e(p,q)
#display Public Key
print("Public Key:","(",n,",",e,")")

#generate Private Key using the Find_Private_Key_d function 
d = Find_Private_Key_d(e, p, q)
#display Private Key
print("Private Key:", "(",n,",",d,")")

#assign message to the string that will be encoded 
message_encode = "This message will be encoded!"
#print the message to be encoded
print("Message to be encoded:", message_encode)

#encode a message into cipher text
encoded_message = Encode(n,e,message_encode)
#print the encoded message
print("Encoded message:",encoded_message)
