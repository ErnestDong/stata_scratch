"""
Huffman Coding
usage:
    >>> encodeword("HelloWorld")
    10010110000100001001011001001010100000100000
    >>> decodeword("10010110000100001001011001001010100000100000")
    HelloWorld
"""


class HuffmanNode:
    """
    node of Huffman tree
    """

    def __init__(self, frequency, data=None, left=None, right=None):
        self.data = data
        self.frequency = frequency
        self.left = left
        self.right = right
        self.code = None

    def __lt__(self, node):
        return self.frequency < node.frequency


class HuffmanQueue:
    """
    HuffmanQueue by PriorityQueue by heap
    """

    def __init__(self, elist=[]):
        self.__elems = list(elist)
        if elist != []:
            self.buildheap()

    def is_empty(self):
        """
        if empty
        """
        return self.__elems == []

    def peek(self):
        """
        return the value of the top
        """
        if self.is_empty():
            raise ValueError("PriorityQueue is empty")
        return self.__elems[0]

    def enqueue(self, elem):
        """
        add e into PriorityQueue
        """
        self.__elems.append(None)
        self.siftup(elem, len(self.__elems) - 1)

    def siftup(self, elem, last):
        """
        sort and add
        """
        elems, i, j = self.__elems, last, (last - 1) // 2
        while i > 0 and elem < elems[j]:
            elems[i] = elems[j]
            i, j = j, (j - 1) // 2
        elems[i] = elem

    def dequeue(self):
        """
        pop and return top
        """
        if self.is_empty():
            raise ValueError("PriorityQueue is empty")
        elems = self.__elems
        ans = elems[0]
        temp = elems.pop()
        if len(elems) > 0:
            self.siftdown(temp, 0, len(elems))
        return ans

    def siftdown(self, elem, begin, end):
        """
        sort
        """
        elems, i, j = self.__elems, begin, begin * 2 + 1
        while j < end:
            if j + 1 < end and elems[j + 1] < elems[j]:
                j += 1
            if elem < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, 2 * j + 1
        elems[i] = elem

    def buildheap(self):
        """
        build heap for init method
        """
        end = len(self.__elems)
        for i in range(end // 2, -1, -1):
            self.siftdown(self.__elems[i], i, end)

    def count(self):
        """
        get the number of elements
        """
        return len(self.__elems)

WORD="QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm"
BAIKE = {WORD[i]:i for i in range(len(WORD))}


def gen_huffman_tree():
    """
    generate Huffman tree
    """
    tree = HuffmanQueue()
    for word in BAIKE:
        tree.enqueue(HuffmanNode(frequency=BAIKE[word], data=word))
    while tree.count() > 1:
        first = tree.dequeue()
        second = tree.dequeue()
        tmp = first.frequency + second.frequency
        tree.enqueue(HuffmanNode(frequency=tmp, left=first, right=second))
    return tree.dequeue()


def get_binary(node, dict_bin={}, code=''):
    """get binary code of each letter"""
    if node.left is None:
        dict_bin.update({node.data: code})
        return
    code += '1'
    get_binary(node.left, dict_bin, code)
    code = code[:-1] + '0'
    get_binary(node.right, dict_bin, code)
    return dict_bin


HUFFMAN = gen_huffman_tree()
BINARY_CODE = get_binary(HUFFMAN)
REVERSE_BINARY = {i: BINARY_CODE[i] for i in BINARY_CODE}


def encodeword(word="HelloWorld"):
    """
    encode word to binary code
    """
    word = word
    ans = ''
    for letter in word:
        if letter not in BAIKE:
            raise ValueError("Letters Only")
        ans += BINARY_CODE[letter]
    return ans


def decodeword(code="10010110000100001001011001001010100000100000"):
    """
    decode binary code to word
    """
    word = ""
    while code:
        tmp = HUFFMAN
        while tmp.data is None:
            # print(code[0])
            if code[0] == '0':
                tmp = tmp.right
            else:
                tmp = tmp.left
            code = code[1:]
        word += tmp.data
    return word


def encode(info:dict):
    ans={}
    for i in info:
        ans[encodeword(i)]=encodeword(info[i])
    return ans

def decode(info:dict):
    ans={}
    for i in info:
        ans[decodeword(i)]=decodeword(info[i])
    return ans

if __name__ == "__main__":
    # print(gen_huffman_tree().frequency)
    # print(gen_huffman_tree().right.frequency)
    # print(get_binary(gen_huffman_tree()))
    # print(encode())
    # print(decode("10010110000100001001011001001010100000100000"))
    TEST={"dcy":"3133","DCY":"Suq4"}
    # print(decodeword(encodeword('qwertyuioplkjhgfdsazxcvbnm')))
    # print(encodeword("HelloWorld123"))
    # print(decodeword(encodeword("HelloWorld123")))
    print(encode(TEST))
    print(decode(encode(TEST)))
