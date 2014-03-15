import Image
import os
import sys

def flatten(l):
    return [item for sublist in l for item in sublist]

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def encode(img, msg):
    # convert message to bits; padded to 7-bits (8 may be better)
    msg_bits = flatten([list(format(ord(x), 'b').zfill(7)) for x in msg])

    # check that message will fit
    if len(msg_bits) > img.size[0] * img.size[1] * 3 - 1:
        pass

    # load 2d array of pixels
    pix = img.load()
    # we don't want to iterate over all pixels, so use an index generator
    pix_stream = ((x, y) for x in xrange(img.size[0])
                         for y in xrange(img.size[1]))

    # set a pixel's r, g, or b value
    def set_bit(pixel, bit, index):
        pixel = list(pixel)
        pixel[index] = int(''.join(list(bin(pixel[index]))[:-1] + [bit]), 2)
        return tuple(pixel)

    # set the r value of the first pixel to the message length;
    # could be a better way to do this
    len_pix = pix_stream.next()
    pix[len_pix] = (len(msg_bits), pix[len_pix][1], pix[len_pix][2])

    index = 0
    for bit in msg_bits:
        if index == 0:
            x, y = pix_stream.next()
        pix[x, y] = set_bit(pix[x, y], bit, index)
        index = (index + 1) % 3

    return img

def decode(img):
    # load 2d array of image pixels
    pix = img.load()

    # "cycle" through the rgb values of each pixel, lazily
    rgb_cycle = (pix[x, y][i] for x in xrange(img.size[0])
                              for y in xrange(img.size[1])
                              for i in xrange(3))

    # r value of first pixel is message length in bits; could be better
    bitcount = rgb_cycle.next()
    rgb_cycle.next() # throw away rest
    rgb_cycle.next() # of first pixel

    # grab all the message bits from the image
    msg_bits = [rgb_cycle.next() % 2 for i in range(bitcount)]

    # chunkify the bits (using 7-bits, but 8 would cover ascii better)
    msg_chunks = list(chunks(msg_bits, 7))

    # convert the chunks to characters, join, return
    return ''.join([chr(int(''.join(map(str, x)), 2)) for x in msg_chunks])


if __name__ == '__main__':
    img = Image.open("mario.png")
    img2 = encode(img, "I'mma walking here!")
    img2.save("newmario.png")
    print decode(img2)
    test_img = Image.open("newmario.png")
    print decode(test_img)
