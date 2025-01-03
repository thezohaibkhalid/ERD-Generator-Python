import zlib
from typing import List

class ERD_Util:
    # PlantUML encoding table
    PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

    @staticmethod
    def encode_plantuml(text: str) -> str:
        """
        Encodes PlantUML text following the official specification:
        1. UTF-8 encode
        2. Compress using deflate
        3. Encode using PlantUML's modified base64
        """
        # Convert string to bytes using UTF-8
        utf8_bytes = text.encode('utf-8')
        
        # Compress using zlib (deflate) with level 9 for maximum compression
        compressed = zlib.compress(utf8_bytes, level=9)
        
        # Remove zlib header (first 2 bytes) and trailer (last 4 bytes)
        compressed = compressed[2:-4]
        
        # Convert the compressed bytes to 6-bit chunks and map them to the PlantUML alphabet
        result = []
        buf = 0
        bits_in_buf = 0
        
        for b in compressed:
            buf = (buf << 8) | b
            bits_in_buf += 8
            while bits_in_buf >= 6:
                bits_in_buf -= 6
                chunk = (buf >> bits_in_buf) & 0x3F  # 0x3F = 63, mask for 6 bits
                result.append(ERD_Util.PLANTUML_ALPHABET[chunk])
                
        # Handle remaining bits
        if bits_in_buf > 0:
            chunk = (buf << (6 - bits_in_buf)) & 0x3F
            result.append(ERD_Util.PLANTUML_ALPHABET[chunk])
            
        # Join the result and return the encoded string
        return ''.join(result)

    @staticmethod
    def decode_plantuml(encoded: str) -> str:
        """
        Decodes a PlantUML encoded string back to the original text.
        Mainly used for testing the encoder.
        """
        # Create reverse lookup table for decoding
        reverse_lookup = {c: i for i, c in enumerate(ERD_Util.PLANTUML_ALPHABET)}
        
        # Convert the encoded string to binary
        binary = []
        for c in encoded:
            if c not in reverse_lookup:
                raise ValueError(f"Invalid character in encoded string: {c}")
            binary.append(format(reverse_lookup[c], '06b'))
        
        # Join binary strings and pad to make it a multiple of 8 bits
        binary = ''.join(binary)
        padding = (8 - len(binary) % 8) % 8
        binary = binary + '0' * padding
        
        # Convert binary string back to bytes
        bytes_data = bytearray()
        for i in range(0, len(binary), 8):
            bytes_data.append(int(binary[i:i+8], 2))
        
        # Add zlib header and trailer
        compressed = b'\x78\x9c' + bytes(bytes_data) + b'\x00\x00\xff\xff'
        
        # Decompress and return the original text
        try:
            return zlib.decompress(compressed).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decompress data: {str(e)}")
