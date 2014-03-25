using System;
using System.Drawing;
using System.Collections.Generic;
using System.Text;
using System.IO;
using Gtk;

namespace Stegalicious
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			// TODO: GUI
			// test code to make sure the stego stuff works
			// then work on the gui


			// Hide message
			MemoryStream stream = new MemoryStream();
			StreamWriter writer = new StreamWriter(stream);
			writer.Write("This is a test");
			writer.Flush();
			stream.Position = 0;

			System.Drawing.Image host = System.Drawing.Image.FromFile ("test.png");
			Bitmap hostImage = new Bitmap (host);

			Stego.HideMessage (stream, hostImage);
			//System.Drawing.Image newImage = new Bitmap (hostImage);
			hostImage.Save ("out.png", System.Drawing.Imaging.ImageFormat.Png);



			// Extract message
			System.Drawing.Image stegoImage = System.Drawing.Image.FromFile ("out.png");
			Bitmap bmap = new Bitmap (stegoImage);

			Stream messageStream = new MemoryStream();
			Stego.ExtractMessage (bmap, ref messageStream);

			messageStream.Seek (0, SeekOrigin.Begin);

			FileStream fs = new FileStream ("outfile.txt", FileMode.Create);
			byte[] streamContent = new Byte[messageStream.Length];
			messageStream.Read (streamContent, 0, streamContent.Length);
			fs.Write (streamContent, 0, streamContent.Length);
			messageStream.Close ();
			fs.Close ();


			// The GUI
			//Application.Init ();
			//MainWindow win = new MainWindow ();
			//win.Show ();
			//Application.Run ();

		}
	}
}
