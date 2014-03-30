using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Drawing;
using System.Windows.Forms;
namespace Stego_Project
{
    class Stegonography
    {
        static public int HideMessage(MemoryStream messageStream, Bitmap bitmap, ProgressBar progressBar)
        {
            
            //get bytes
            byte[] bytes = messageStream.ToArray();
            //check if image has enough of pixels
            if (bytes.Length >= 16777215)
            {
                MessageBox.Show("Your file is too long, only 16,777,215 bytes are allowed", 
                    "Warning", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                return 0;
            }
            //Write Length of the file into the first pixel
            int colorValue = bytes.Length;

            int redMask = 0xff0000;
            int red = (colorValue & redMask) >> 16;

            int greenMask = 0x00ff00;
            int green = (colorValue & greenMask) >> 8;

            int blueMask = 0x0000ff;
            int blue = colorValue & blueMask;
                    
            bitmap.SetPixel(0, 0, Color.FromArgb(red, green, blue));
            //x and y coordinates of image
            int x = 1;
            int y = 0;
            //pixel to be used
            Color pixel = bitmap.GetPixel(x, y);
            int val = 0; //0 - R, 1 - G, 2 - B
            byte R = pixel.R;
            byte G = pixel.G;
            byte B = pixel.B;
            
            for (int i = 0; i < bytes.Length; i++)
            {
                byte cur = bytes[i];
                byte mask = (byte)Convert.ToInt32("00000001", 2);
                for (int j = 0; j < 8; j++)
                {
                                                      
                    //get bit to set
                    byte result = (byte)(cur & mask);
                    //shift bit to the LSB position
                    result = (byte)(result >> j);
                    //Set pixel's value in the image
                    switch (val)
                    {
                        case 0: //just set R channel and update val
                            R = (byte)(((pixel.R>>1)<<1) | result);
                            val++;
                            break;
                        case 1: //just set G channel and update val
                            G = (byte)(((pixel.G >> 1) << 1) | result);
                            val++;
                            break;
                        case 2: //set B channel, and write pixel to bitmap
                            B = (byte)(((pixel.B >> 1) << 1) | result);
                            byte mask5 = (byte)Convert.ToInt32("00000001", 2);
                            Color toSet = Color.FromArgb(R, G, B);
                            bitmap.SetPixel(x, y, toSet);
                            byte mask1 = (byte)Convert.ToInt32("00000001", 2);
                            //Update pixel coordinate and reset variables
                            updateXY(ref x, ref y, bitmap);
                            //get pixel
                            pixel = bitmap.GetPixel(x, y);
                            R = pixel.R;
                            G = pixel.G;
                            B = pixel.B;
                            val = 0;
                            break;
                    }
                    //update mask
                    mask =(byte)(mask << 1);
                    
                }
                progressBar.PerformStep(); //update progress bar
            }
            //Check if need to set the last pixel
            if (val != 0)
            {
                Color toSet = Color.FromArgb(R, G, B);
                bitmap.SetPixel(x, y, toSet);
                
            }
            return 1;
        }

        private static void updateXY(ref int x, ref int y, Bitmap bitmap)
        {
            x = (x + 1) % bitmap.Size.Width;
            if (x == 0)
                y++;
        }

        static public int ExtractMessage(Bitmap bitmap, out MemoryStream messageStream, ProgressBar progressBar)
        {
            //Read the length of the file
            Color pixel = bitmap.GetPixel(0, 0);
            int fileLength = (pixel.R << 16) + (pixel.G << 8) + pixel.B;
            if (fileLength >= 16777215)
            {
                MessageBox.Show("You've chosen the wrong image, it does not contain file gidden with this software",
                    "Warning", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                messageStream = new MemoryStream();
                return 0;
            }
            //Set maximum value of progress bar
            progressBar.Maximum = fileLength;
            //Initialize memory stream
            messageStream = new MemoryStream(fileLength);
            //x and y coordinates of pixel
            int x = 1;
            int y = 0;
            int val = 0; //0 - R, 1 - G, 2 - B
            byte message = (byte)0; //bits will be stored in this variable
            byte mask = (byte)Convert.ToInt32("00000001", 2);
            pixel = bitmap.GetPixel(x, y);
            for (int i = 0; i < fileLength; i++)
            {
                for (int j = 0; j < 8; j++)
                {
                    switch (val)
                    {
                        case 0:
                            message = (byte)(message | ((pixel.R & mask) << j));
                            val++;
                            break;
                        case 1:
                            message = (byte)(message | ((pixel.G & mask) << j));
                            val++;
                            break;
                        case 2:
                            message = (byte)(message | ((pixel.B & mask) << j));
                            updateXY(ref x, ref y, bitmap);
                            pixel = bitmap.GetPixel(x, y);
                            val = 0;
                            break;
                    }
                }
                //Write byte to the stream
                messageStream.WriteByte(message);
                //reset byte
                message = (byte)0;
                //update progress bar
                progressBar.PerformStep();
            }
            return 1;   
        }
    }
}
