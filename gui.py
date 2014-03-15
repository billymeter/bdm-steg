import wx
import wx.lib.filebrowsebutton as filebrowse
import sys
import os
import bdm_steg

def max_fit(src_size, tgt_size):
    src_width, src_height = src_size[0], src_size[1]
    tgt_width, tgt_height = tgt_size[0], tgt_size[1]
    ratio_w = float(tgt_width) / src_width;
    ratio_h = float(tgt_height) / src_height;

    ratio = ratio_w if ratio_w < ratio_h else ratio_h

    return (src_width * ratio, src_height * ratio)

class KeyPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.key_label = wx.StaticText(self, label="Enter key:")
        self.key_box = wx.TextCtrl(self, value="", style=wx.TE_MULTILINE)
        self.load_key = wx.Button(self, label="Load", id=wx.ID_OK)
        self.sizer.AddMany(
            [(self.key_label, wx.ID_ANY, wx.ALIGN_CENTER),
            (self.key_box, wx.ID_ANY, wx.EXPAND),
            (self.load_key, wx.ID_ANY, wx.ALIGN_CENTER)])
        self.SetSizer(self.sizer)

class LeftPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.dirname = ''
        self.SetBackgroundColour(wx.WHITE)
        self.parent = parent
        self.width, self.height = self.GetSize()
        self.load_image = filebrowse.FileBrowseButton(
            self, wx.ID_ANY, labelText="Load Image", buttonText="Choose file...",
            fileMask=("Images (*.bmp,*.gif,*.png,*.jpg)|*.bmp;*.gif;*.png;*.jpg|"
                      "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif|"
                      "PNG files (*.png)|*.png|JPG files (*.jpg)|*.jpg"),
            changeCallback=self.SendImage(parent.right_panel))
        self.load_file = filebrowse.FileBrowseButton(
            self, wx.ID_ANY, labelText="Load Message", buttonText="Choose file...",
            changeCallback=self.SendImage(parent.right_panel))
        self.key_panel = KeyPanel(self, wx.ID_ANY)

        self.load_image.SetBackgroundColour((105,210,231))
        self.load_file.SetBackgroundColour((167,219,216))
        self.key_panel.SetBackgroundColour((224,228,204))

        self.sizer = wx.GridSizer(rows=3)
        self.sizer.Add(self.load_image, wx.ID_ANY, wx.EXPAND)
        self.sizer.Add(self.load_file, wx.ID_ANY, wx.EXPAND)
        self.sizer.Add(self.key_panel, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(self.sizer)

    def SendImage(self, tgt_panel):
        def inner_send(event):
            image = wx.Image(event.GetString())
            tgt_panel.DisplayImage(image)
        return inner_send


class RightPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.SetBackgroundColour(wx.WHITE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.parent = parent
        self.width, self.height = self.GetSize()
        self.image = None
        wx.EVT_PAINT(self, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        if self.image:
            dc.DrawBitmap(self.image.ConvertToBitmap(), 0,0)

    def DisplayImage(self, image):
        """ Load an image """
        display_rect = wx.GetClientDisplayRect()
        if display_rect[2] < image.GetWidth() or display_rect[3] < image.GetHeight():
            self.parent.Maximize()
            image = image.Scale(*max_fit(image.GetSize(),
                                   self.GetSize()),
                                   quality=wx.IMAGE_QUALITY_HIGH)
        else:
            image = image.Scale(*self.GetSize(), quality=wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(image))

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY)
        self.dirname = ''

        self.width, self.height = 512, 480
        self.SetInitialSize((512,480))

        self.right_panel = RightPanel(parent=self, ID=wx.ID_ANY)
        self.left_panel = LeftPanel(parent=self, ID=wx.ID_ANY)
        self.right_panel.SetBackgroundColour((250,105,0))
        self.left_panel.SetBackgroundColour((224,228,204))

        self.SetTitle("bdm-steg")

        #initialize menu bar
        menu_bar = wx.MenuBar()

        #file menu options
        file_menu = wx.Menu()
        m_load = file_menu.Append(wx.ID_OPEN, "&Open Image\tAlt-O", "Load Image")
        m_exit = file_menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit")
        self.Bind(wx.EVT_MENU, self.OnOpen, m_load)
        self.Bind(wx.EVT_MENU, self.Kill, m_exit)
        menu_bar.Append(file_menu, "&File")

        #finalize menu bar
        self.SetMenuBar(menu_bar)

        #status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(1)
        self.statusbar.SetStatusText("Stegalicious", 0)

        #window behavior
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.Kill)

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.sizer = wx.GridSizer(cols=2)
        self.sizer.Add(self.left_panel, wx.ID_ANY, wx.EXPAND)
        self.sizer.Add(self.right_panel, wx.ID_ANY, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Fit()
        self.Layout()

    def Kill(self, event):
        self.Destroy()

    def OnSize(self, event):
        self.Layout()

    def OnOpen(self, event):
        """ Load an image """
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "",
                            wildcard=("Images (*.bmp,*.gif,*.png,*.jpg)|"
                                              "*.bmp;*.gif;*.png;*.jpg|"
                                      "BMP files (*.bmp)|*.bmp|"
                                      "GIF files (*.gif)|*.gif|"
                                      "PNG files (*.png)|*.png|"
                                      "JPG files (*.jpg)|*.jpg"),
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename, self.dirname = dlg.GetFilename(), dlg.GetDirectory()
            bitmap = wx.Image(os.path.join(self.dirname, self.filename))
            self.right_panel.DisplayImage(bitmap)
        dlg.Destroy()

    def Update(self, event):
        pass


class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()
