import sys

# We will use a class called my trie node
class MyTrieNode:
    # Initialize some fields 
  
    def __init__(self, isRootNode):
        #The initialization below is just a suggestion.
        #Change it as you will.
        # But do not change the signature of the constructor.
        self.isRoot = isRootNode
        self.isWordEnd = False # is this node a word ending node
        self.isRoot = False # is this a root node
        self.count = 0 # frequency count
        self.next = {} # Dictionary mapping each character from a-z to 
                       # the child node if any corresponding to that character.

    def addWord(self,w):
        # make sure length of word is greater than 0 
        assert(len(w) > 0)
        # YOUR CODE HERE
        # If you want to create helper/auxiliary functions, please do so.
        
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

    def lookupWord(self,w):
        # Return frequency of occurrence of the word w in the trie
        # returns a number for the frequency and 0 if the word w does not occur.
        # YOUR CODE HERE
        
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

    def autoComplete_helper(self, w, current_node, answer):
        # if the current_node is the end of the word, 
        if current_node.isWordEnd == True:
            # add the word and the count to the answer list 
            answer.append((w, current_node.count))
        # loop through each letter that current_node points to 
        for letter in current_node.next:
            # recursively call the autoComplete_helper function 
            self.autoComplete_helper(w + letter, current_node.next[letter], answer)  
    
    def autoComplete(self,w):
        #Returns possible list of autocompletions of the word w
        #Returns a list of pairs (s,j) denoting that
        #         word s occurs with frequency j
        #YOUR CODE HERE
        
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
        
# The original example: let us see if the code works

t= MyTrieNode(True) # Create a root Trie node
lst1=['test','testament','testing','ping','pin','pink','pine','pint','testing','pinetree']
# Insert the words in lst1
for w in lst1:
    t.addWord(w)
    
# Perform lookups
j = t.lookupWord('testy') # should return 0
j2 = t.lookupWord('telltale') # should return 0
j3 = t.lookupWord ('testing') # should return 2

# Run autocompletes
lst3 = t.autoComplete('pi')
print('Completions for \"pi\" are : ')
print(lst3)

lst4 = t.autoComplete('tes')
print('Completions for \"tes\" are : ')
print(lst4)
