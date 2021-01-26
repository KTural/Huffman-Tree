import sys, os, heapq    
from graphviz import Digraph

class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
            return self.freq < other.freq

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, HeapNode):
            return False
        return self.freq == other.freq
        
class BinaryHeap:
    def __init__(self):
        self.a = []
        
    def get(self, i):
        if  i >= len(self.a):
            return
        return self.a[i].freq
    
    # swapping characters and frequencies as swapping nodes
    def swap(self, i, j):
        self.a[i].char, self.a[j].char = self.a[j].char, self.a[i].char
        self.a[i].freq, self.a[j].freq = self.a[j].freq, self.a[i].freq
        
    def add(self, node):
        index_ = self.count()
        self.a.append(node)
        
        while index_ != 0:
            p = self.parent(index_)
            if self.get(p) > self.get(index_):
                self.swap(p, index_)
            index_ = p
            
    def count(self):
        return len(self.a)
    
    def isEmpty(self):
        return len(self.a) == 0
    
    def down_heap(self, i):
        a = self.a 
        while True:
            m = a[i].freq
            if self.left(i) < len(a):
                m = min(m, a[self.left(i)].freq)
            if self.right(i) < len(a):
                m = min(m, a[self.right(i)].freq)
            if m == a[i].freq:
                break 
            if m == a[self.left(i)].freq:
                self.swap(i, self.left(i))
                i = self.left(i)
            else:   
                self.swap(i, self.right(i))            
                i = self.right(i)

    def remove_minimum(self): 
        if len(self.a) == 0:
            return
        elif len(self.a) == 1:
            x = self.a.pop()
            return x
        x = self.a[0]
        self.a[0] = self.a.pop()
        self.down_heap(0)
        return x
    
    def left(self, i):
        return (2 * i + 1)

    def right(self, i):
        return (2 * i + 2)

    def parent(self, i):
        return ((i - 1) // 2)
    
class Huffman:
    
    def __init__(self, frequency_file=None):
        self.frequency_file = frequency_file
        self.heap = BinaryHeap()
        self.bit_codes = {}
        self.char_freq = []
    
    # get frequencies from generated frequency.txt file for building tree    
    def get_dictionary_from_file(self, text_file):
        freq_dict = {}
        
        with open(text_file) as f:
    
            for line in f:
                if line != '\n':
                    a = line.rstrip()
                    freq_dict[a[0]] = a[2:]
                else:
                    # special case for new line character and its frequency
                    a = f.readline()
                    freq_dict[line] = a.strip()
                    
        return freq_dict

    # Build binary min heap with chars and frequency as nodes
    def generate_min_heap(self, frequency):
        for key, val in frequency.items():
            node = HeapNode(key, int(val))
            self.heap.add(node)
    
    # get two smallest nodes in heap and create parent node of them
    # parent's frequency as sum of frequencies of two children nodes
    def make_heap_with_frequency(self):
        while self.heap.count() > 1:
            
            node1 = heapq.heappop(self.heap.a)
            node2 = heapq.heappop(self.heap.a)
            
            node = HeapNode(None, int(node1.freq) + int(node2.freq))
            node.left = node1
            node.right = node2
            
            heapq.heappush(self.heap.a, node)
    
    # generate bit codes for characters recursively
    # left traversal has a value 0, right traversal has a value 1        
    def generate_bit_codes(self, node, bit_val):
        if node == None:
            return
        
        if node.char != None:
            self.bit_codes[node.char] = bit_val
            
        self.generate_bit_codes(node.left, bit_val + "0")
        self.generate_bit_codes(node.right, bit_val + "1")
            
    # call recursive bit-code generator for each character, pass argument as root
    def bit_code_assignment(self, root):
        bit_val = ""
        self.generate_bit_codes(root, bit_val)
    
    # traverse the tree to get characters and frequency values
    def traverse_tree(self, root):
        if root == None:
            return
        
        l = self.traverse_tree(root.left)
        r = self.traverse_tree(root.right)
        
        if root.char != None:
            # add characters and frequency together to the list if character is in leaf node
            self.char_freq.append([root.char, root.freq])
        elif root.char == None:
            # add only frequencies to the list if characters don't exist
            self.char_freq.append([root.freq])
    
    # get whole bit values as replacing each character with its bit value
    def get_encoded_text(self, text):
        with open(text) as text_file:
            bit_vals = ""
            
            for line in text_file:
                for character in line:
                    bit_vals += self.bit_codes[character]
                
        return bit_vals
            
    # add extra bits if the encoded text is not multiple of 8
    def padding_encoded_text(self, encoded_text):
        # subtracting remaining bits from 1 byte value to get extra number of bits
        extra_padding = 8 - len(encoded_text) % 8
        
        for _ in range(extra_padding):
            encoded_text += "0"
        
        # converting extra number of bits to 8 bit value and prepend to our encoded text    
        encoded_text = f"{extra_padding:08b}" + encoded_text
        return encoded_text

    # convert each 8 bits to byte and add it to byte array
    def convert_bits(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print('Padded Encoded text Error !!!')
            sys.exit(0)
        
        byte = bytearray()
        
        for i in range(0, len(padded_encoded_text), 8):
            byte.append(int(padded_encoded_text[i:i+8], 2))
        
        return byte
    
    # decode binary file, remove padded bits and map each bit to its character
    def decode_text(self, bits_string):
        text_string = ""
        
        # remove padded bits and extra number of bits for making bits_string 8 bit multiple
        padded_bits = bits_string[:8]
        extra_bits = int(padded_bits, 2)
        
        bits_string = bits_string[8:len(bits_string)-extra_bits]
        
        # iterate over bits_string to find mapping characters in bit_codes and add it to text_string
        bit = ""
        
        for i in range(len(bits_string)):
            bit += bits_string[i]
            if bit in self.bit_codes:
                text_string += self.bit_codes[bit]
                bit = ""
                
        return text_string
    
    def buildTree(self):
        frequency = self.get_dictionary_from_file(self.frequency_file)
        
        self.generate_min_heap(frequency)
        
        self.make_heap_with_frequency()
        
        root = self.heap.remove_minimum()
        
        self.bit_code_assignment(root)
            
        # write generated bitcode values and tree data with frequency to files
        
        with open('tree.dat', 'w') as treeData, open('bitcodes.dat', 'w') as bitData:
            treeData.write('Character  Frequency  Bit code values\n')
            
            for key, val in self.bit_codes.items():
                treeData.write(f'{key}          {frequency[key]}            {val}\n')
                bitData.write(f'{key} {val}\n')        
               
        # for visiualizing the tree we traverse tree and add char,frequency values to the list
        self.traverse_tree(root) 
        
        # write list of chars and frequency values to visualize.dat for visualizing tree later
        with open("visualize.dat", "w") as visualData:
            for i in range(len(self.char_freq)):
                for j in range(len(self.char_freq[i])):
                    visualData.write(str(self.char_freq[i][j])+' ')
                visualData.write('\n')
        
    def encode(self, original_text, bitcodes):
        self.bit_codes = self.get_dictionary_from_file(bitcodes)
        
        encoded_text = self.get_encoded_text(original_text)
        
        padded_encoded_text = self.padding_encoded_text(encoded_text)
        
        byte_array = self.convert_bits(padded_encoded_text)

        with open('encoded-text.bin', 'wb') as encoded_message:
            encoded_message.write(bytes(byte_array))

    def decode(self, bitcodes, bin_file):
        self.bit_codes = {val:key for key, val in self.get_dictionary_from_file(bitcodes).items()}

        with open(bin_file, 'rb') as binary_file, open('decoded-text.txt', 'w') as output_file:
            bits_string = ""
            
            while True:
                byte = binary_file.read(1)
                if len(byte) <= 0:
                    break
                bits = f'{ord(byte):b}'.rjust(8, "0")
                bits_string += bits
        
            decoded_text = self.decode_text(bits_string)
            
            output_file.write(decoded_text)
            
    def visualize(self, bitcodes, visualData):
        
        self.bit_codes = self.get_dictionary_from_file(bitcodes)

        dot = Digraph(comment='Huffman Tree', edge_attr={'arrowhead':'none'})
        
        # get character,frequency as list of lists if characters exists otherwise only frequencies
        with open(visualData) as visual:
                        
            for line in visual:
                if line != '\n':
                    line = line.rstrip()
                    if len(line.split()) == 2:
                        self.char_freq.append([line[0:line.index(' ')], int(line[line.index(' ')+1:])])
                    else:
                        if line[0] == ' ':
                            self.char_freq.append([line[0], int(line[line.index(' ')+1:])])
                        else:
                            self.char_freq.append([int(line)])
                else:
                    first_line = line
                    second_line = visual.readline().strip()
                    self.char_freq.append([first_line, int(second_line)])

        # index to keep track of nodes
        start = 0
        i = 0
        
        while True:
            # the last node or the root in the list
            if len(self.char_freq) == 1:
                break
            # by iterating list of lists, we find frequencies first since they are parents of leaf nodes and further sum of frequencies
            # only frequencies are just one value and value increases as sum of frequencies of children nodes
            if len(self.char_freq[i]) == 1:
                
                # this creates leaf nodes fist and when iteration is in upper level, this nodes will be in the correct position as a leaf child node
                if len(self.char_freq[i-2]) != 1 and len(self.char_freq[i-1]) != 1:
                    for element in range(start, i-2):
                        dot.node(self.bit_codes[self.char_freq[element][0]], \
                            f'{self.char_freq[element]}/{self.bit_codes[self.char_freq[element][0]]}')
                        
                # parent node's reference
                p = str(self.char_freq[i][0]) + str(self.char_freq[i-1][0][-1])
                # frequency value of parent node
                d = str(self.char_freq[i][0])

                # create a node as d being label, when creating other nodes p will be referenced
                dot.node(p, d)    
                # replace the current node with parent's reference
                self.char_freq[i] = [p]     
                # case for when left child is frequency value and right child is leaf node
                # all leaf nodes are in this format ['character','frequency']/bitcode-value, other nodes are just frequency values
                if len(self.char_freq[i-2]) == 1 and len(self.char_freq[i-1]) != 1:
                    dot.edge(p, str(self.char_freq[i-2][0]))
                    dot.node(self.bit_codes[self.char_freq[i-1][0]], f'{self.char_freq[i-1]}/{self.bit_codes[self.char_freq[i-1][0]]}')
                    dot.edge(p, self.bit_codes[self.char_freq[i-1][0]])
                # case for when left child is leaf node and right child is frequency value
                elif len(self.char_freq[i-2]) != 1 and len(self.char_freq[i-1]) == 1:
                    dot.node(self.bit_codes[self.char_freq[i-2][0]], f'{self.char_freq[i-2]}/{self.bit_codes[self.char_freq[i-2][0]]}')
                    dot.edge(p, self.bit_codes[self.char_freq[i-2][0]])
                    dot.edge(p, str(self.char_freq[i-1][0]))
                # case when left and right children are frequency values
                elif len(self.char_freq[i-2]) == 1 and len(self.char_freq[i-1]) == 1:
                    # creating edges between current node and left, right children which were firstly parent nodes of leaf children
                    dot.edge(p, str(self.char_freq[i-2][0]))
                    dot.edge(p, str(self.char_freq[i-1][0]))
                # case when left and right children are leaf nodes
                else:
                    dot.node(self.bit_codes[self.char_freq[i-2][0]], f'{self.char_freq[i-2]}/{self.bit_codes[self.char_freq[i-2][0]]}')
                    dot.node(self.bit_codes[self.char_freq[i-1][0]], f'{self.char_freq[i-1]}/{self.bit_codes[self.char_freq[i-1][0]]}')
                    dot.edge(p, self.bit_codes[self.char_freq[i-2][0]])
                    dot.edge(p, self.bit_codes[self.char_freq[i-1][0]])
                # remove current leaf nodes    
                self.char_freq = self.char_freq[:i-2] + self.char_freq[i:]   
                start = i - 1
                i -= 2
                
            i += 1
        # render file and output it            
        dot.render('huffman-tree.dot', view=True)  
            
# function to determine input format 
# either accepts file or word/sentence as list of strings
def determine_input_format():
    if sys.argv[2][-4:] == '.txt' and sys.argv[2] == sys.argv[-1]:
        text_file = sys.argv[2]
        input_format = '.txt'
    else:
        text_file = sys.argv[2:]
        input_format = 'other'
            
    return determine_frequency(text_file, input_format)

# function to count frequencies of each character
# in a file or word/sentence 
# and write to frequency.txt
def determine_frequency(text_file, input_format):
    frequency_dict = {}
    
    # find frequencies of chars in file and add it to dictionary
    if input_format == '.txt':
        with open(text_file) as f:
            for line in f:
                for char in line:
                    if char in frequency_dict:
                        frequency_dict[char] += 1
                    else:
                        frequency_dict[char] =  1
                        
    # find frequencies of chars in words/sentence and add it to dictionary
    elif input_format == 'other':
        for i in range(len(text_file)):           
            for j in range(len(text_file[i])):
                if text_file[i][j] in frequency_dict:
                    frequency_dict[text_file[i][j]] += 1
                else:
                    frequency_dict[text_file[i][j]] = 1
            # case handling for space character in text from command line
            if ' ' in frequency_dict:
                frequency_dict[' '] += 1
            else:
                frequency_dict[' '] = 1
        # add new line character to text from command line 
        frequency_dict['\n'] = 1
        
        # write text content that is given from command line to the file
        with open('sample.txt', 'w') as f:
            for i in range(len(text_file)):           
                for j in range(len(text_file[i])):
                    f.write(text_file[i][j])
                f.write(' ')
            f.write('\n')

    # write frequencies with characters to the file
    with open('frequency.txt', 'w') as f:
        for key, val in frequency_dict.items():
            f.write(f'{key}  {val} \n') if key == '\n' else f.write(f'{key} {val}\n')
            
    return input_format            
                
def command_handler():
    # -generate command for determining frequency of characters 
    if sys.argv[1] == '-generate':
        # no text or file given
        if sys.argv[1] == sys.argv[-1]:
            print('Enter a text or file in command line')
            sys.exit(0)
        input_format = determine_input_format()
        # check whether original text is derived from file or command line
        print(f'Original text is in {sys.argv[2]}') if input_format == '.txt' else \
            print('Original text is in sample.txt')
            
        print('Generated character frequencies for Huffman code')
        print('Wrote output to frequency.txt')
        
    # -buildtree command for building tree with characters and frequency
    # also building tree with characters and its bit values determined by huffman coding
    elif sys.argv[1] == '-buildtree':
        text_file = sys.argv[2]
        if os.path.exists(text_file):
            huffman = Huffman(text_file)
            huffman.buildTree()
            print('Wrote output to tree.dat and bitcodes.dat. visualize.dat is also generated for visualizing a tree!')
        else:
            print(f"Can't buld a tree. {text_file} file doesn't exist!")
            
    # -encode command for encoding text or file and returning binary file
    elif sys.argv[1] == '-encode':
        original_file = sys.argv[2]
        # bitcodes.dat generated from -buildtree command
        bitcodes = sys.argv[3]
        if os.path.exists(bitcodes):
            huffman = Huffman()
            huffman.encode(original_file, bitcodes)
            print('Wrote output to encoded-text.bin')
        else:
            print(f"Can't encode a file. {bitcodes} file doesn't exist!")
            
    # -decode command for decoding binary file and returning original text
    elif sys.argv[1] == '-decode':
        bitcodes = sys.argv[2]
        # check whether binary file generated from -encode exists
        bin_file = sys.argv[3]
        if os.path.exists(bin_file):
            huffman = Huffman()
            huffman.decode(bitcodes, bin_file)
            print('Wrote output to decoded-text.txt')
        else:
            print(f"Can't decode a file. {bin_file} file doesn't exist!")
            
    # -visualize command for visualizing huffman tree containing characters and frequency as leaf nodes together with their bit code values
    elif sys.argv[1] == '-visualize':
        bitcodes, visualData = sys.argv[2], sys.argv[3]
        # check whether visualData generated from -buildtree exists
        if os.path.exists(visualData):
            huffman = Huffman()
            huffman.visualize(bitcodes, visualData)
            print('Wrote output to huffman-tree.dot. View visualization in huffman-tree.dot.pdf')
        else:
            print(f"Can't visualize a tree. {visualData} file doesn't exist!")

command_handler()