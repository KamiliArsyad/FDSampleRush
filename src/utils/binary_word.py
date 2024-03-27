class BinaryWord:
    """
    Represents an n-bit binary word.

    Attributes:
        length (int): The length of the binary word in bits.
        value (int): The integer value of the binary word.

    Methods:
        set_bit(position, bit): Returns a new BinaryWord instance with a bit set at the specified position.
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

    def __len__(self):
        return self.length