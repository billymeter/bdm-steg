using System;
using System.Drawing;
using System.Collections.Generic;
using System.IO;
using Gtk;

public partial class MainWindow: Gtk.Window
{
	public MainWindow () : base (Gtk.WindowType.Toplevel)
	{
		Build ();
	}

	protected void OnDeleteEvent (object sender, DeleteEventArgs a)
	{
		Application.Quit ();
		a.RetVal = true;
	}
	protected void OnOpenActionActivated (object sender, EventArgs e)
	{
		Gtk.FileChooserDialog fc = new FileChooserDialog (
			                           "Choose image to open", 
			                           this,
									   Gtk.FileChooserAction.Open, "Cancel", ResponseType.Cancel, "Open", ResponseType.Accept);
		fc.Filter = new FileFilter();
		fc.Filter.AddPattern ("*.png");
		fc.Filter.AddPattern ("*.jpg");
		fc.Filter.AddPattern("*.jpeg");
		fc.Filter.AddPattern ("*.gif");
		fc.Filter.AddPattern("*.tiff");

		if (fc.Run() == (int)ResponseType.Accept)
		{
			System.Drawing.Image host = System.Drawing.Image.FromFile (fc.Filename);
			Bitmap hostImage = new Bitmap (host);
			MemoryStream pic = new MemoryStream ();
			hostImage.Save (pic, System.Drawing.Imaging.ImageFormat.Png);

			pic.Seek (0, SeekOrigin.Begin);
			Gdk.Pixbuf pb = new Gdk.Pixbuf (pic);
			originalImage.Pixbuf = pb;
		}
		//Don't forget to call Destroy() or the FileChooserDialog window won't get closed.
		fc.Destroy();

	}
}
