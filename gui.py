import wx
import wx.lib.filebrowsebutton as filebrowse
import sys
import os
import bdm_steg


def max_fit(src_size, tgt_size):
    src_width, src_height = src_size[0], src_size[1]
    tgt_width, tgt_height = tgt_size[0], tgt_size[1]
    ratio_w = float(tgt_width) / src_width
    ratio_h = float(tgt_height) / src_height

    ratio = ratio_w if ratio_w < ratio_h else ratio_h

    return src_width * ratio, src_height * ratio


class LeftPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.parent = parent
        self.width, self.height = self.GetSize()

        self.option1 = wx.CheckBox(self, wx.ID_ANY, label="option1")
        self.option2 = wx.CheckBox(self, wx.ID_ANY, label="option2")
        self.option3 = wx.CheckBox(self, wx.ID_ANY, label="option3")

        # self.SetBackgroundColour((105,210,231))
        self.SetBackgroundColour((167,219,216))
        # self.SetBackgroundColour((224,228,204))

        self.sizer = wx.GridSizer(rows=3)
        self.sizer.Add(self.option1, wx.ID_ANY, wx.ALIGN_CENTER)
        self.sizer.Add(self.option2, wx.ID_ANY, wx.ALIGN_CENTER)
        self.sizer.Add(self.option3, wx.ID_ANY, wx.ALIGN_CENTER)
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
        self.dir_name = ""
        self.image_name = "None"
        self.file_name = "None"
        self.key_str = "None"
        self.steg = bdm_steg.BDMSteg()
        self.width, self.height = 512, 480
        self.SetInitialSize((512,480))

        self.right_panel = RightPanel(parent=self, ID=wx.ID_ANY)
        self.left_panel = LeftPanel(parent=self, ID=wx.ID_ANY)
        self.right_panel.SetBackgroundColour((250,105,0))

        self.SetTitle("bdm-steg")

        #initialize toolbar
        self.toolbar = self.CreateToolBar(wx.TB_TEXT|wx.TB_NOICONS)

        # identifiers
        self.ID_ENCODE = 255
        self.ID_DECODE = 552

        # add tools
        m_image = self.toolbar.AddLabelTool(wx.ID_OPEN, "Load image", wx.NullBitmap, longHelp="Load containing image")
        m_file = self.toolbar.AddLabelTool(wx.ID_FILE, "Load file", wx.NullBitmap, longHelp="Load file to hide")
        m_key = self.toolbar.AddLabelTool(wx.ID_ADD, "Add key", wx.NullBitmap, longHelp="Add encryption key")
        m_encode = self.toolbar.AddLabelTool(self.ID_ENCODE, "Encode", wx.NullBitmap, longHelp="Encode image with file")
        m_decode = self.toolbar.AddLabelTool(self.ID_DECODE, "Decode", wx.NullBitmap, longHelp="Decode image")
        m_help = self.toolbar.AddLabelTool(wx.ID_HELP, "Help", wx.NullBitmap, longHelp="Get instructions")
        m_exit = self.toolbar.AddLabelTool(wx.ID_EXIT, "Exit", wx.NullBitmap, longHelp="Exit program")

        # encode/decode are not yet available
        self.toolbar.EnableTool(self.ID_ENCODE, False)
        self.toolbar.EnableTool(self.ID_DECODE, False)

        # bind tools
        self.Bind(wx.EVT_TOOL, self.LoadImage, m_image)
        self.Bind(wx.EVT_TOOL, self.LoadFile, m_file)
        self.Bind(wx.EVT_TOOL, self.LoadKey, m_key)
        self.Bind(wx.EVT_TOOL, self.Kill, m_encode)
        self.Bind(wx.EVT_TOOL, self.Kill, m_decode)
        self.Bind(wx.EVT_TOOL, self.Kill, m_help)
        self.Bind(wx.EVT_TOOL, self.Kill, m_exit)
        self.toolbar.Realize()

        #status bar
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(3)
        self.status_bar.SetStatusWidths([-1, -1, -1])
        self.status_bar.SetStatusText("Image loaded: %s" % self.image_name, 0)
        self.status_bar.SetStatusText("File loaded: %s" % self.file_name, 1)
        self.status_bar.SetStatusText("Key loaded: %s" % self.key_str, 2)

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

    def LoadImage(self, event):
        """ Load an image """
        dlg = wx.FileDialog(self, "Choose a file", self.dir_name, "",
                            wildcard=("Images (*.bmp,*.gif,*.png,*.jpg)|"
                                      "*.bmp;*.gif;*.png;*.jpg|"
                                      "BMP files (*.bmp)|*.bmp|"
                                      "GIF files (*.gif)|*.gif|"
                                      "PNG files (*.png)|*.png|"
                                      "JPG files (*.jpg)|*.jpg"),
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.image_name, self.dir_name = dlg.GetFilename(), dlg.GetDirectory()
            image = wx.Image(os.path.join(self.dir_name, self.image_name))
            self.right_panel.DisplayImage(image)
            self.steg.set_image(image)

            # better way to update this stuff?
            self.status_bar.SetStatusText("Image loaded: %s" % self.image_name, 0)
            if self.key_str != "None":
                if self.file_name != "None":
                    self.toolbar.EnableTool(self.ID_ENCODE, True)
                self.toolbar.EnableTool(self.ID_DECODE, True)
        dlg.Destroy()

    def LoadFile(self, event):
        """ Load a file """
        dlg = wx.FileDialog(self, "Choose a file", self.dir_name, "",
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name, self.dir_name = dlg.GetFilename(), dlg.GetDirectory()
            bitmap = wx.Image(os.path.join(self.dir_name, self.file_name))
            self.steg.set_file(os.path.join(self.dir_name, self.file_name))

            # better way to update this stuff?
            self.status_bar.SetStatusText("File loaded: %s" % self.file_name, 1)
            if self.key_str != "None" and self.image_name != "None":
                self.toolbar.EnableTool(self.ID_ENCODE, True)
        dlg.Destroy()

    def LoadKey(self, event):
        self.steg.set_key('dummy')
        self.key_str = 'dummy'

        # better way to update this stuff?
        self.status_bar.SetStatusText("Key loaded: %s" % self.key_str, 2)
        if self.image_name != "None":
            if self.file_name != "None":
                self.toolbar.EnableTool(self.ID_ENCODE, True)
            self.toolbar.EnableTool(self.ID_DECODE, True)

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
