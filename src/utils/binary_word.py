class BinaryWord:
    """
    Represents an n-bit binary word.

    Attributes:
        length (int): The length of the binary word in bits.
        value (int): The integer value of the binary word.

    Methods:
        set_bit(position, bit): Returns a new BinaryWord instance with a bit set at the specified position.
        pop_count(): Returns the population count (i.e. number of bit 1) of the binary word.
        ones(): Returns a new BinaryWord instance with all bits set to 1.
    """

    def __init__(self, length, value=0):
        self.length = length
        self.value = value & ((1 << length) - 1)

    def __repr__(self):
        return f"{self.value:0{self.length}b}"

    def set_bit(self, position, bit):
        if not 0 <= position < self.length:
            raise ValueError("Bit position out of range")
        if bit not in (0, 1):
            raise ValueError("Bit must be 0 or 1")
        newValue = (self.value & ~(1 << position)) | (bit << position)
        return BinaryWord(self.length, newValue)

    def flip_bit(self, position):
        if not 0 <= position < self.length:
            raise ValueError("Bit position out of range")
        return BinaryWord(self.length, self.value ^ (1 << position))

    def get_bit(self, position):
        if not 0 <= position < self.length:
            raise ValueError("Bit position out of range")
        return (self.value >> position) & 1

    def pop_count(self):
        count = 0
        byte = self.value
        while byte:
            count += byte & 1
            byte >>= 1
        return count

    def ones(self):
        return BinaryWord(self.length, 2 ** self.length - 1)

    def zeroes(self):
        return BinaryWord(self.length, 0)

    def __and__(self, other):
        return BinaryWord(self.length, self.value & other.value)

    def __or__(self, other):
        return BinaryWord(self.length, self.value | other.value)

    def __xor__(self, other):
        return BinaryWord(self.length, self.value ^ other.value)

    def __invert__(self):
        return BinaryWord(self.length, ~self.value & ((1 << self.length) - 1))

    def to_int(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __len__(self):
        return self.length

    def __hash__(self):
        return hash((self.value, self.length))
