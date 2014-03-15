from PIL import Image
from PIL import PngImagePlugin
import os
import sys

def flatten(l):
    return [item for sublist in l for item in sublist]

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

class BDMSteg:
    def __init__(self, image=None, message=None, key=None):
        self.image = image
        self.message = message
        self.key = key

    def set_image(self, image):
        self.image = image

    def set_message(self, message):
        self.message = msg

    def set_key(self, key):
        self.key = key

    def encode(self):
        # convert message to bits; padded to 8 bits
        msg_bits = flatten(list(format(ord(x), 'b').zfill(8)) for x in self.message)
        msg_len = len(msg_bits) / 8

        # check that message will fit
        if msg_len > self.image.size[0] * self.image.size[1] * 3 - 1:
            raise IndexError

        # load 2d array of pixels
        pix = self.image.load()
        # we don't want to iterate over all pixels, so use an index generator
        pix_stream = ((x, y) for x in xrange(self.image.size[0])
                             for y in xrange(self.image.size[1]))

        # set a pixel's r, g, or b value
        def set_bit(pixel, bit, index):
            pixel = list(pixel)
            pixel[index] = int(''.join(list(bin(pixel[index]))[:-1] + [bit]), 2)
            return tuple(pixel)

        # first pixel is the message length; the format is:
        # msg length in chars = r*100 + g*10 + b
        # this gives a maximum message length of 255*100 + 255*10 + 255
        r_count = msg_len/100
        g_count = (msg_len - r_count*100)/10
        b_count = msg_len - g_count*10 - r_count*100
        pix[pix_stream.next()] = (r_count, g_count, b_count)

        index = 0
        for bit in msg_bits:
            if index == 0:
                x, y = pix_stream.next()
            pix[x, y] = set_bit(pix[x, y], bit, index)
            index = (index + 1) % 3

        return self.image

    def decode(self):
        # load 2d array of image pixels
        pix = self.image.load()

        # "cycle" through the rgb values of each pixel, lazily
        rgb_cycle = (pix[x, y][i] for x in xrange(self.image.size[0])
                                  for y in xrange(self.image.size[1])
                                  for i in xrange(3))

        # deriving bitcount from msg length in first pixel, which has format:
        # msg length in chars = r*100 + g*10 + b
        bitcount = rgb_cycle.next() * 8 * 100
        bitcount += rgb_cycle.next() * 8 * 10
        bitcount += rgb_cycle.next() * 8

        # grab all the message bits from the image
        msg_bits = [rgb_cycle.next() % 2 for i in range(bitcount)]

        # create 8-bit chunks
        msg_chunks = list(chunks(msg_bits, 8))

        # convert the chunks to characters, join, return
        return ''.join([chr(int(''.join(map(str, x)), 2)) for x in msg_chunks])

    def save_png(self, file):
        nochange = ('gamma', 'transparency', 'interlace', 'dpi', 'aspect')

        meta = PngImagePlugin.PngInfo()
        for k, v in self.image.info.iteritems():
            if k in nochange: continue
            meta.add_text(k, v)

        self.image.save(file, "PNG", pnginfo=meta)

def main():
    img = BDMSteg(Image.open("mario.png"), "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    img.encode()
    img.save_png("newmario.png")
    print img.decode()
    test_img = BDMSteg(Image.open("newmario.png"))
    print test_img.decode()


if __name__ == '__main__':
    main()
