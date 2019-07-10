import numpy as np
import random
from math import ceil

class Transposition:
    
    def __init__(self):
        
        self.key = random.randint(2,5)

def encrypt_Message(self,message):
        
        rows = self.key
        columns = int(ceil(len(message) / self.key))
        message_List = list(message)
        
        while len(message_List) != rows*columns:
            
            message_List.append("1")
            
        message = "".join(message_List)
        index_List = [i*columns for i in range(rows+1)]
        soon_To_Be_Matrix = [message[index_List[i]:index_List[i+1]] for i in range(len(index_List)-1)]
        matrix = np.zeros((rows,columns), dtype = str)

        for i in range(rows):
            
            soon_To_Be_Matrix[i] = list(soon_To_Be_Matrix[i])
            matrix[i] = soon_To_Be_Matrix[i]
            
        matrix = np.transpose(matrix)
        encrypted_Message = [c for l in matrix for c in l]
        encrypted_Message = list(filter(lambda x: x != "1", encrypted_Message))
        return "".join(encrypted_Message)
        
    def decrypt_Message(self,message):
        
        rows = int(ceil(len(message) / self.key))
        columns = self.key
        message_List = list(message)
        
        if len(message) != rows*columns:
            
            accurate_List = [((rows - i) * columns - 1) % (rows * columns) for i in range(columns*rows - len(message))]
            accurate_List.reverse()
            
            for i in accurate_List:
                
                message_List.insert(i,"1")
                
            message = "".join(message_List)
        index_List = [i*columns for i in range(rows+1)]
        soon_To_Be_Matrix = [message[index_List[i]:index_List[i+1]] for i in range(len(index_List)-1)]
        matrix = np.zeros((rows,columns), dtype = str)

        for i in range(rows):
            
            soon_To_Be_Matrix[i] = list(soon_To_Be_Matrix[i])
            matrix[i] = soon_To_Be_Matrix[i]
            
        matrix = np.transpose(matrix)
        decrypted_Message = [c for l in matrix for c in l]
        decrypted_Message = list(filter(lambda x: x != "1", decrypted_Message))
        return "".join(decrypted_Message)
