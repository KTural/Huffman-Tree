# Huffman-Tree

### Content

Building and visualizing the Huffman Tree using Huffman-Coding Algorithm:

1. Encoding original file into binary file which compresses the size of it. 
2. Decoding the binary file into original file which is lossless data decompression. 
3. Visualizing the Huffman tree using graphviz software tool.

### Installation of packages
```sh
# Check whether python installed:
$ python --version

# Check whether pip installed:
$ python -m pip --version

# If above all installed:
$ pip install -r requirements.txt

# Try upgrading pip, if pip is outdated:
$ pip install --upgrade pip
```

### Running the source file

```sh
# Firstly, you need to generate frequency file for determining number of characters in a file, and determining format of input.
# <text> can only be .txt file or any text/sentence you want to write
$ python3 huffman.py -generate <text>
```

```sh
# Then, you can build a tree with -buildtree command and frequency file which is generated from the first command
$ python3 huffman.py -buildtree frequency.txt
# After building a tree, we have tree.dat (characters, frequencies, bitcode values generated from Huffman Coding Algorithm)
# bitcodes.dat (characters and bitcode values that we will use for encoding), visualize.dat(tree nodes that we will use for visualization)
```

```sh
# Now, you can visualize the Tree with bitcodes.dat and visualize.dat that generated from -buildtree command
$ python3 huffman.py -visualize bitcodes.dat visualize.dat
# Ouput will have two files one is .dot file which is the code for Huffman Tree and .pdf file for viewing the visualization
# Note that the leaf nodes are in this format ['<character>', <frequency>]/<bitcode value>, other nodes are just frequencies and sums of frequencies.
```


```sh
# This command will encode text or file and output binary file which will be compressed (You can compare the size of original and binary files)
# You can see <original-text> file in the output of -generate command (This differs because user can either enter file or text into command line)
$ python3 huffman.py -encode <original-text> bitcodes.dat
# Ouput will be binary file <encoded-text.bin>
```

```sh
# If you want to decode binary file into original file
# -decode command takes binary file, so you have to encode file first!
$ python3 huffman.py -decode bitcodes.dat encoded-text.bin
# Ouput will be original file <decoded-text.txt>
```

### Visualization of sample.txt file in Huffman Tree:

![Huffman-Tree](./sample-visualization/huffman-tree.dot.pdf)


### REFERENCES:
Huffman Coding (https://en.wikipedia.org/wiki/Huffman_coding) 

Graphviz Visualization Software (https://graphviz.org/)
