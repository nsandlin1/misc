import textwrap
from PIL import Image
from pathlib import Path
import argparse
import sys


def read_file(file_name):
    with open(file_name) as f:
        contents = f.readlines()
    return contents


def get_pixel(image, i, j):
    width, height = image.size
    if i > width or j > height:
      return None

    pixel = image.getpixel((i, j))
    return pixel


def open_image(path):
    image = Image.open(path)
    return image


def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


def binary_to_string(string_bits):
    my_byte_array = textwrap.wrap(string_bits, 8)
    my_message = ''.join([chr(int(x, 2)) for x in my_byte_array])
    return my_message


def string_to_binary(my_string):
    string_bytes = ''.join(format(x, '08b') for x in bytearray(my_string, 'utf-8'))
    return string_bytes


def mod_rgb(bit, rgb_val):
    if bit == 0:
        if rgb_val % 2 != 0:
            rgb_val -= 1
    else:
        if rgb_val % 2 == 0:
            rgb_val += 1

    return rgb_val


def encode(binary_string, image_path):
    image = open_image(image_path)
    split3 = textwrap.wrap(binary_string, 3)
    print(split3)
    print("__________________________________________")
    width, height = image.size

    new_image = create_image(width, height)
    pixels = new_image.load()

    # Must create new picture based on original because you cannot modify tuple RGB in original... How to i note the end of the message and copy the rest of the original picture?

    end_message_key = False
    message_done = False

    for i in range(width):
        for j in range(height):

            # print(f"pixel = ({i}, {j})")

            pixel = get_pixel(image, i, j)

            # print(f"pixel before = {pixel}")
            rp = pixel[0]
            #print(f"rp = {rp}")
            gp = pixel[1]
            #print(f"gp = {gp}")
            bp = pixel[2]
            #print(f"bp = {bp}")

            if not message_done:

                # print(f"split3[0][0] = {split3[0][0]}")
                rp = mod_rgb(int(split3[0][0]), rp)


                try:
                    # print(f"split3[0][1] = {split3[0][1]}")
                    gp = mod_rgb(int(split3[0][1]), gp)
                except: pass

                try:
                    # print(f"split3[0][2] = {split3[0][2]}")
                    bp = mod_rgb(int(split3[0][2]), bp)
                except: pass

                split3.pop(0)

            # print(f"(r, g, b) = ({rp}, {gp}, {bp})")
            pixels[i, j] = (rp, gp, bp)

            # print(f"new_pixel = {pixels[i, j]}")
            # print("_____________________________________________")


            # TODO: need new image done string to appendin case last item of message is a zero, so it will not get cut off
            if len(split3) == 0 and not end_message_key:
                split3 += ['000']*400
                end_message_key = True

            if len(split3) == 0:
                message_done = True

    # new_image = pixels
    # the above presumably done automatically
    new_image.save(f'./test/{Path(image_path).stem}_encoded.png')

# TODO: make where final rgb values are not taken, when only one is encoded
def decode(image_path):
    image = open_image(image_path)
    width, height = image.size
    string_bits = ''

    def end_of_message(bit_string):
        if bit_string[-1200:] == '000'*400:
            return True
        return False

    for i in range(width):
        for j in range(height):

            pixel = get_pixel(image, i, j)
            print(f"pixel = {[i, j]}")

            rp = pixel[0]
            gp = pixel[1]
            bp = pixel[2]

            # print(f"({rp},{gp},{bp})")

            if rp % 2 == 0:
                string_bits += '0'
            else:
                string_bits += '1'

            if gp % 2 == 0:
                string_bits += '0'
            else:
                string_bits += '1'

            if bp % 2 == 0:
                string_bits += '0'
            else:
                string_bits += '1'

            try:
                if end_of_message(string_bits):
                    break
            except: pass

        if end_of_message(string_bits):
            break
    return string_bits[-1599:]


def main(argv=[__name__]):

    parser = argparse.ArgumentParser(description="Encode and decode messages to jpg.")
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-p', '--path', type=str, help="Path for image file.", required=True)
    parser.add_argument('-m', '--message', type=str, help="Message to be encoded.", required=True)
    group.add_argument('-e', '--encode', action='store_true', help="Encode message to image.")
    group.add_argument('-d', '--decode', action='store_true', help="Decode message from image.")
    group.add_argument('-f', '--file', action='store_true', help="A filepath for which to encode contents.")
    args = parser.parse_args()

    bit_string = string_to_binary(args.message)
    print(f"bit_string = {bit_string}")
    encode(bit_string, args.path)
    bits = decode('./test/panda_encoded.png')
    print(binary_to_string(bits))

    # print("happy")


if __name__ == '__main__':
    sys.exit(main(sys.argv))
