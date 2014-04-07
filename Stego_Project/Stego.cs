using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using System.Drawing;

namespace Stegalicious
{
	public class Stego
	{
		// TODO
		// Add compression and encryption layers

		public static void HideMessage(Stream messageStream, Bitmap bitmap)
		{
			ProcessImage(ref messageStream, bitmap, false);
			messageStream = null;
		}

		public static void ExtractMessage(Bitmap bitmap, ref Stream messageStream)
		{
			ProcessImage (ref messageStream, bitmap, true);
		}


		// This table is used to reverse the bits in a byte
		public static byte[] BitReverseTable =
		{
			0x00, 0x80, 0x40, 0xc0, 0x20, 0xa0, 0x60, 0xe0,
			0x10, 0x90, 0x50, 0xd0, 0x30, 0xb0, 0x70, 0xf0,
			0x08, 0x88, 0x48, 0xc8, 0x28, 0xa8, 0x68, 0xe8,
			0x18, 0x98, 0x58, 0xd8, 0x38, 0xb8, 0x78, 0xf8,
			0x04, 0x84, 0x44, 0xc4, 0x24, 0xa4, 0x64, 0xe4,
			0x14, 0x94, 0x54, 0xd4, 0x34, 0xb4, 0x74, 0xf4,
			0x0c, 0x8c, 0x4c, 0xcc, 0x2c, 0xac, 0x6c, 0xec,
			0x1c, 0x9c, 0x5c, 0xdc, 0x3c, 0xbc, 0x7c, 0xfc,
			0x02, 0x82, 0x42, 0xc2, 0x22, 0xa2, 0x62, 0xe2,
			0x12, 0x92, 0x52, 0xd2, 0x32, 0xb2, 0x72, 0xf2,
			0x0a, 0x8a, 0x4a, 0xca, 0x2a, 0xaa, 0x6a, 0xea,
			0x1a, 0x9a, 0x5a, 0xda, 0x3a, 0xba, 0x7a, 0xfa,
			0x06, 0x86, 0x46, 0xc6, 0x26, 0xa6, 0x66, 0xe6,
			0x16, 0x96, 0x56, 0xd6, 0x36, 0xb6, 0x76, 0xf6,
			0x0e, 0x8e, 0x4e, 0xce, 0x2e, 0xae, 0x6e, 0xee,
			0x1e, 0x9e, 0x5e, 0xde, 0x3e, 0xbe, 0x7e, 0xfe,
			0x01, 0x81, 0x41, 0xc1, 0x21, 0xa1, 0x61, 0xe1,
			0x11, 0x91, 0x51, 0xd1, 0x31, 0xb1, 0x71, 0xf1,
			0x09, 0x89, 0x49, 0xc9, 0x29, 0xa9, 0x69, 0xe9,
			0x19, 0x99, 0x59, 0xd9, 0x39, 0xb9, 0x79, 0xf9,
			0x05, 0x85, 0x45, 0xc5, 0x25, 0xa5, 0x65, 0xe5,
			0x15, 0x95, 0x55, 0xd5, 0x35, 0xb5, 0x75, 0xf5,
			0x0d, 0x8d, 0x4d, 0xcd, 0x2d, 0xad, 0x6d, 0xed,
			0x1d, 0x9d, 0x5d, 0xdd, 0x3d, 0xbd, 0x7d, 0xfd,
			0x03, 0x83, 0x43, 0xc3, 0x23, 0xa3, 0x63, 0xe3,
			0x13, 0x93, 0x53, 0xd3, 0x33, 0xb3, 0x73, 0xf3,
			0x0b, 0x8b, 0x4b, 0xcb, 0x2b, 0xab, 0x6b, 0xeb,
			0x1b, 0x9b, 0x5b, 0xdb, 0x3b, 0xbb, 0x7b, 0xfb,
			0x07, 0x87, 0x47, 0xc7, 0x27, 0xa7, 0x67, 0xe7,
			0x17, 0x97, 0x57, 0xd7, 0x37, 0xb7, 0x77, 0xf7,
			0x0f, 0x8f, 0x4f, 0xcf, 0x2f, 0xaf, 0x6f, 0xef,
			0x1f, 0x9f, 0x5f, 0xdf, 0x3f, 0xbf, 0x7f, 0xff
		};

		public static byte ReverseByte(byte toReverse)
		{
			return BitReverseTable[toReverse];
		}

		// This is the workhorse right here. Does all the bit twiddling magic
		private static void ProcessImage(ref Stream messageStream, Bitmap bitmap, bool extract)
		{
			// Maximum X and Y position in picture
			int bitmapWidth = bitmap.Width - 1;

			int bitCount = 0;
			byte curMessageByte = (byte) 0;

			Color pixelColor;
			Int32 messageLength;

			if (extract) {
				// Length of the message is stored in the first pixel
				pixelColor = bitmap.GetPixel (0, 0);
				messageLength = (pixelColor.R << 16) + (pixelColor.G << 8) + pixelColor.B;
				messageStream = new MemoryStream (messageLength);
			} else {
				messageLength = (Int32)messageStream.Length;
				if (messageLength >= 16777215) {
					String tooBig = "Your message is too long, only 16,777,215 bytes are allowed";
					throw new Exception (tooBig);
				}

				// Write the length of the message into the first pixel
				int colorValue = messageLength;

				int redMask = 0xff0000;
				int red = (colorValue & redMask) >> 16;

				int greenMask = 0x00ff00;
				int green = (colorValue & greenMask) >> 8;

				int blueMask = 0x0000ff;
				int blue = colorValue & blueMask;

				pixelColor = Color.FromArgb (red, green, blue);
				bitmap.SetPixel (0, 0, pixelColor);
			}

			// Reset streams

			messageStream.Seek (0, SeekOrigin.Begin);

			// Current position of the host image
			// start with 1 since pixel (0,0) contains the message length
			Point pixelPosition = new Point (1, 0);



			double temp = (messageLength * 8 / 3);
			//int loopCount = (int)Math.Ceiling (temp);
			int loopCount = Convert.ToInt32 (temp);

			if (!extract) {
				curMessageByte = (byte)(messageStream.ReadByte ());
			}

			// Loop over the message and image, hiding each message bit
			for (int messageIndex = 0; messageIndex < loopCount; messageIndex++) {
				// Get the color of a "clean" pixel
				pixelColor = bitmap.GetPixel (pixelPosition.X, pixelPosition.Y);

				if (extract) {
					// Extract the bit from the pixel red component
					curMessageByte = (byte) ( (curMessageByte | (pixelColor.R & 0x0001) ) << 1);
					bitCount++;

					if (bitCount == 7) {
						bitCount = 0;
						messageStream.WriteByte (ReverseByte(curMessageByte));
						curMessageByte = (byte)0;
					}
						
					// Extract the bit from the pixel green component
					curMessageByte = (byte) ((curMessageByte | (pixelColor.G & 0x0001)) << 1);
					bitCount++;

					if (bitCount == 7) {
						bitCount = 0;
						messageStream.WriteByte (ReverseByte(curMessageByte));
						curMessageByte = (byte)0;
					}

					// Extract the bit from the pixel blue component
					curMessageByte = (byte) ((curMessageByte | (pixelColor.B & 0x0001)) << 1);
					bitCount++;

					if (bitCount == 7) {
						bitCount = 0;
						messageStream.WriteByte (ReverseByte(curMessageByte));
						curMessageByte = (byte)0;
					}

				} else {
					int red = 0, green = 0, blue = 0;

					if (bitCount == 7) {
						bitCount = 0;
						curMessageByte = (byte) messageStream.ReadByte();
					}

					// Get the color of the current pixel
					pixelColor = bitmap.GetPixel(pixelPosition.X, pixelPosition.Y);

					// Red component
					if (Convert.ToBoolean(curMessageByte & (0x0001 << bitCount))) { // is current bit is set in the message?
						red = pixelColor.R | 0x0001;
					} else {
						red = pixelColor.R & ~(0x0001);
					}

					bitCount++;

					if (bitCount == 7) {
						bitCount = 0;
						curMessageByte = (byte) messageStream.ReadByte();
					}

					// Green component
					if (Convert.ToBoolean(curMessageByte & (0x0001 << bitCount))) { // is current bit is set in the message?
						green = pixelColor.R | 0x0001;
					} else {
						green = pixelColor.R & ~(0x0001);
					}

					bitCount++;

					if (bitCount == 7) {
						bitCount = 0;
						curMessageByte = (byte) messageStream.ReadByte();
					}

					// Blue component
					if (Convert.ToBoolean(curMessageByte & (0x0001 << bitCount))) { // is current bit is set in the message?
						blue = pixelColor.R | 0x0001;
					} else {
						blue = pixelColor.R & ~(0x0001);
					}

					bitCount++;

					Color dirtyPixel = Color.FromArgb (red, green, blue);
					bitmap.SetPixel (pixelPosition.X, pixelPosition.Y, dirtyPixel);

				}

				// Move X-position
				if (bitmapWidth == pixelPosition.X) {
					pixelPosition.X = 0;
					pixelPosition.Y++;
				} else {
					pixelPosition.X++;
				}
			}

			// extra data gets put in the stream, so just truncate it to the message length
			messageStream.SetLength (messageLength);
			bitmap = null;
		}

	}
}