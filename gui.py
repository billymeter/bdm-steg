import wx
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

class LeftPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.width, self.height = self.GetSize()
        self.image = None
        self.textbox = wx.TextCtrl(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.textbox, wx.ID_ANY, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetBackgroundColour((0, 0, 0))

class RightPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.width, self.height = self.GetSize()
        self.image = None
        self.SetBackgroundColour((255, 255, 255))


class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY)
        self.dirname = ''

        self.width, self.height = 512, 480
        self.SetInitialSize((512,480))

        self.left_panel = LeftPanel(self, wx.ID_ANY)
        self.right_panel = RightPanel(self, wx.ID_ANY)
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

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.left_panel, wx.ID_ANY, wx.EXPAND)
        self.sizer.Add(self.right_panel, wx.ID_ANY, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Fit()
        self.Layout()

    def Kill(self, event):
        self.Destroy()

    def OnSize(self, event):
        if self.right_panel.image:
            im = wx.ImageFromBitmap(self.right_panel.image)
            im = im.Scale(*self.right_panel.GetSize(), quality=wx.IMAGE_QUALITY_HIGH)
            wx.StaticBitmap(self.right_panel, -1, wx.BitmapFromImage(im))
        self.Layout()

    def OnOpen(self, event):
        """ Load an image """
        formats = ("Images (*.bmp,*.gif,*.png,*.jpg)|*.bmp;*.gif;*.png;*.jpg|"
                   "BMP files (*.bmp)|*.bmp|GIF files (*.gif)|*.gif|"
                   "PNG files (*.png)|*.png|JPG files (*.jpg)|*.jpg")
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", formats, wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename, self.dirname = dlg.GetFilename(), dlg.GetDirectory()
            self.right_panel.image = wx.Bitmap(os.path.join(self.dirname, self.filename))
            im = wx.ImageFromBitmap(self.right_panel.image)
            display_rect = wx.GetClientDisplayRect()
            if display_rect[2] < im.GetWidth() or display_rect[3] < im.GetHeight():
                self.Maximize()
                im = im.Scale(*max_fit(im.GetSize(),
                                       self.right_panel.GetSize()),
                                       quality=wx.IMAGE_QUALITY_HIGH)
            else:
                im = im.Scale(*self.right_panel.GetSize(), quality=wx.IMAGE_QUALITY_HIGH)
            wx.StaticBitmap(self.right_panel, -1, wx.BitmapFromImage(im))
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
