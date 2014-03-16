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


class StatusPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.sizer = wx.GridSizer(rows=2, cols=3)
        self.image_status = wx.StaticText(self, wx.ID_ANY, label="Image loaded:")
        self.file_status = wx.StaticText(self, wx.ID_ANY, label="File loaded:")
        self.key_status = wx.StaticText(self, wx.ID_ANY, label="Key loaded:")
        self.sizer.AddMany(
            [(self.image_status, wx.ID_ANY, wx.ALIGN_CENTER),
             (self.file_status, wx.ID_ANY, wx.ALIGN_CENTER),
             (self.key_status, wx.ID_ANY, wx.ALIGN_CENTER)])
        self.SetSizer(self.sizer)


class ExecutePanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.sizer = wx.GridSizer(cols=2)
        self.encode_btn = wx.Button(self, label="Encode", id=wx.ID_ANY)
        self.decode_btn = wx.Button(self, label="Decode", id=wx.ID_ANY)
        self.sizer.AddMany(
            [(self.encode_btn, wx.ID_ANY, wx.ALIGN_CENTER),
            (self.decode_btn, wx.ID_ANY, wx.ALIGN_CENTER)])
        self.SetSizer(self.sizer)


class OptionsPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.option = wx.CheckBox(self, wx.ID_ANY, label="An option!")
        self.sizer.Add(self.option, wx.ID_ANY, wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)


class LeftPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.dirname = parent.dirname
        self.filename = parent.filename
        self.parent = parent
        self.width, self.height = self.GetSize()

        self.code_panel = ExecutePanel(self, wx.ID_ANY)
        self.options_panel = OptionsPanel(self, wx.ID_ANY)
        self.status_panel = StatusPanel(self, wx.ID_ANY)

        self.code_panel.SetBackgroundColour((105,210,231))
        self.options_panel.SetBackgroundColour((167,219,216))
        self.status_panel.SetBackgroundColour((224,228,204))

        self.sizer = wx.GridSizer(rows=3)
        self.sizer.Add(self.code_panel, wx.ID_ANY, wx.EXPAND)
        self.sizer.Add(self.options_panel, wx.ID_ANY, wx.EXPAND)
        self.sizer.Add(self.status_panel, wx.ID_ANY, wx.EXPAND)
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
        self.dirname = ''
        self.filename = None
        self.steg = bdm_steg.BDMSteg()
        self.width, self.height = 512, 480
        self.SetInitialSize((512,480))

        self.right_panel = RightPanel(parent=self, ID=wx.ID_ANY)
        self.left_panel = LeftPanel(parent=self, ID=wx.ID_ANY)
        self.right_panel.SetBackgroundColour((250,105,0))
        self.left_panel.SetBackgroundColour((224,228,204))

        self.SetTitle("bdm-steg")

        #initialize toolbar
        toolbar = self.CreateToolBar(wx.TB_TEXT|wx.TB_NOICONS)

        m_image = toolbar.AddLabelTool(wx.ID_OPEN, "Load image", wx.NullBitmap, longHelp="Load containing image")
        m_file = toolbar.AddLabelTool(wx.ID_FILE, "Load file", wx.NullBitmap, longHelp="Load file to hide")
        m_key = toolbar.AddLabelTool(wx.ID_ADD, "Add key", wx.NullBitmap, longHelp="Add encryption key")
        m_help = toolbar.AddLabelTool(wx.ID_HELP, "Help", wx.NullBitmap, longHelp="Get instructions")
        m_exit = toolbar.AddLabelTool(wx.ID_EXIT, "Exit", wx.NullBitmap, longHelp="Exit program")
        self.Bind(wx.EVT_TOOL, self.LoadImage, m_image)
        self.Bind(wx.EVT_TOOL, self.LoadFile, m_file)
        self.Bind(wx.EVT_TOOL, self.LoadKey, m_key)
        self.Bind(wx.EVT_TOOL, self.Kill, m_help)
        self.Bind(wx.EVT_TOOL, self.Kill, m_exit)
        toolbar.Realize()

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

    def LoadImage(self, event):
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
            filename, self.dirname = dlg.GetFilename(), dlg.GetDirectory()
            image = wx.Image(os.path.join(self.dirname, filename))
            self.right_panel.DisplayImage(image)
            self.steg.set_image(image)
        dlg.Destroy()

    def LoadFile(self, event):
        """ Load a file """
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "",
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename, self.dirname = dlg.GetFilename(), dlg.GetDirectory()
            bitmap = wx.Image(os.path.join(self.dirname, filename))
            self.steg.set_file(os.path.join(self.dirname, filename))
        dlg.Destroy()

    def LoadKey(self, event):
        self.steg.set_key('dummy')

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
