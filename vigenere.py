from sys import stdin, argv

def vigenere_encode(my_str, key):
    '''
    encode my_str using key
    '''
    encoded_str = ''
    curr_key_val = 0

    for i in range(len(my_str)):
        if my_str[i].isalpha():
            # calculate encoded letter
            letter = let_vals[my_str[i].lower()]
            displacement = let_vals[key[curr_key_val%len(key)]]
            encoded = (letter + displacement) % 26

            # treat differently if upper or lower
            if my_str[i].lower() == my_str[i]:
                encoded_str += chr(97 + encoded)
            else:
                encoded_str += chr(65 + encoded)

            curr_key_val += 1
        # if not alpha then just add to the encoded string without changing
        else:
            encoded_str += my_str[i]

    return encoded_str

def vigenere_decode(my_str, key):
    '''
    decode my_str using key
    '''
    decoded_str = ''
    curr_key_val = 0

    for i in range(len(my_str)):
        if my_str[i].isalpha():
            # calculate decoded letter
            letter = let_vals[my_str[i].lower()]
            displacement = let_vals[key[curr_key_val%len(key)]]
            decoded = (26 + letter - displacement) % 26

            # treat differently if upper or lower
            if my_str[i].lower() == my_str[i]:
                decoded_str += chr(97 + decoded)
            else:
                decoded_str += chr(65 + decoded)

            curr_key_val += 1
        # if not alpha then just add to the decoded string without changing
        else:
            decoded_str += my_str[i]

    return decoded_str

# global key component values
let_vals = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
            'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13,
            'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
            'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

if __name__ == '__main__':
    # Check for correct arguments
    if len(argv) != 3:
        print("Incorrect number of command line args")
        exit(1)
    
    # loooooop and process
    for my_input in stdin:
        if argv[1] == '-e':
        # For this and the other: remove from input all new lines, remove from key all spaces
        # and make key all lowercase
            print(vigenere_encode(my_input.replace('\n', ' '), argv[2].lower().replace(' ','')))
        else:
            print(vigenere_decode(my_input.replace('\n', ' '), argv[2].lower().replace(' ','')))
