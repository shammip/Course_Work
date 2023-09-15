# class is called MyTrieNode
class MyTrieNode:
    # initialize fields 
    def __init__(self, isRootNode):
        self.isRoot = isRootNode
        self.isWordEnd = False # is this node a word ending node
        self.isRoot = False # is this a root node
        self.count = 0 # frequency count
        self.next = {} # dictionary mapping each character from a-z to 
                       # the child node if any corresponding to that character.

    #add a word to dictionary
    def addWord(self,w):
        # make sure length of word is greater than 0 
        assert(len(w) > 0)
        # let current_node point to the root 
        current_node = self 
        # loop through each letter in the word
        for letter in w: 
            # if the letter is not in the word
            if letter not in current_node.next: 
                # create a new node 
                new_node = MyTrieNode(False)
                # let the next node be equal to the new node 
                current_node.next[letter] = new_node
                # let the current node be the new node 
                current_node = new_node
            # if the letter is in the word    
            else:
                # move to the next letter
                current_node = current_node.next[letter]
        # end of word is reached so it equals true 
        current_node.isWordEnd = True 
        # increase count by 1 
        current_node.count = current_node.count + 1
        return

    #returns a number for the frequency for word and 0 if the word does not occur.
    def lookupWord(self,w):        
        # make sure length of word is greater than 0 
        assert(len(w) > 0)
        # let current_node point to the root 
        current_node = self 
        # loop through each letter in the word
        for letter in w: 
            # if the letter is not in the word, return 0 
            if letter not in current_node.next:
                return 0
            # if the letter is in the word, move to the next letter 
            current_node = current_node.next[letter]
        # end of word is reached so return the frequency of the word 
        return current_node.count

    #autoComplete helper function
    def autoComplete_helper(self, w, current_node, answer):
        # if the current_node is the end of the word, 
        if current_node.isWordEnd == True:
            # add the word and the count to the answer list 
            answer.append((w, current_node.count))
        # loop through each letter that current_node points to 
        for letter in current_node.next:
            # recursively call the autoComplete_helper function 
            self.autoComplete_helper(w + letter, current_node.next[letter], answer)  
    
    #returns list of word and its frequency
    def autoComplete(self,w):
        # make sure length of word is greater than 0 
        assert(len(w) > 0)
        # create an empty list called answer
        answer = []
        # let current_node point to the root 
        current_node = self 
        # loop through each letter in the word
        for letter in w: 
            # if the letter is not in the word, return the empty answer list 
            if letter not in current_node.next:
                return answer
            # if the letter is in the word, move to the next letter 
            current_node = current_node.next[letter]
        # call the autoComplete_helper function using the word, current node, and empty answer list
        self.autoComplete_helper(w, current_node, answer)    
        # return answer list 
        return answer
        

#examples

# create a root trie node
t= MyTrieNode(True) 

#list of words
lst1=['test','testament','testing','ping','pin','pink','pine','pint','testing','pinetree'] 

#add each word from lst1
for w in lst1:
    t.addWord(w)
    
#lookup words
j = t.lookupWord('testy') # should return 0
j2 = t.lookupWord('telltale') # should return 0
j3 = t.lookupWord ('testing') # should return 2
print(j, j2, j3)

#run autocomplete
lst3 = t.autoComplete('pi')
print('Completions for \"pi\" are : ')
print(lst3)

#run autocomplete
lst4 = t.autoComplete('tes')
print('Completions for \"tes\" are : ')
print(lst4)
