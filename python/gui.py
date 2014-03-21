import wx
from wx.lib.pubsub import pub
import os
import bdm_steg
from PIL import Image


def max_fit(src_size, tgt_size):
    src_width, src_height = src_size[0], src_size[1]
    tgt_width, tgt_height = tgt_size[0], tgt_size[1]
    ratio_w = float(tgt_width) / src_width
    ratio_h = float(tgt_height) / src_height

    ratio = ratio_w if ratio_w < ratio_h else ratio_h

    return src_width * ratio, src_height * ratio


def wx_image_to_pil(wx_image):
    pil_im = Image.new('RGB', (wx_image.GetWidth(), wx_image.GetHeight()))
    pil_im.fromstring(wx_image.GetData())
    return pil_im


def pil_image_to_wx(pil_image):
    wx_image = wx.EmptyImage(pil_image.size[0], pil_image.size[1])
    wx_image.SetData(pil_image.convert('RGB').tostring())
    return wx_image


class Model(object):
    def __init__(self):
        self._plain = {}
        self._file = {}
        self._key = None

        # derived from other attributes
        self._cipher = None

    @property
    def plain(self):
        return self._plain

    @plain.setter
    def plain(self, image_path):
        self._plain['data'] = wx.Image(image_path)
        self._plain['name'] = os.path.basename(image_path)
        pub.sendMessage("PLAIN CHANGED", message=self.plain)

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file_path):
        # need to convert file to stream
        self._file['data'] = None
        self._file['name'] = os.path.basename(file_path)
        pub.sendMessage("FILE CHANGED", message=self.file)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
        pub.sendMessage("KEY CHANGED", message=self.key)

    @property
    def cipher(self):
        return self._cipher

    @cipher.setter
    def cipher(self):
        self._cipher['data'] = pil_image_to_wx(
            encode(wx_image_to_pil(self.image), self.file, self.key))
        pub.sendMessage("CIPHER CHANGED", self.cipher)


class LeftPanel(wx.Panel):
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        self.parent = parent
        self.width, self.height = self.GetSize()

        self.option1 = wx.CheckBox(self, wx.ID_ANY, label="option1")
        self.option2 = wx.CheckBox(self, wx.ID_ANY, label="option2")
        self.option3 = wx.CheckBox(self, wx.ID_ANY, label="option3")

        # self.SetBackgroundColour((105,210,231))
        self.SetBackgroundColour((167, 219, 216))
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
        if (display_rect[2] < image.GetWidth() or
                display_rect[3] < image.GetHeight()):
            self.parent.Maximize()
            image = image.Scale(*max_fit(image.GetSize(),
                                self.GetSize()),
                                quality=wx.IMAGE_QUALITY_HIGH)
        else:
            image = image.Scale(*self.GetSize(), quality=wx.IMAGE_QUALITY_HIGH)
        wx.StaticBitmap(self, -1, wx.BitmapFromImage(image))


class View(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY)
        self._plain_view = None
        self._file_view = None
        self._key_view = None
        self.encoded_image = None
        self.width, self.height = 512, 480
        self.SetInitialSize((512, 480))

        self.right_panel = RightPanel(parent=self, ID=wx.ID_ANY)
        self.left_panel = LeftPanel(parent=self, ID=wx.ID_ANY)
        self.right_panel.SetBackgroundColour((250, 105, 0))

        self.SetTitle("bdm-steg")

        #initialize toolbar
        self.toolbar = self.CreateToolBar(wx.TB_TEXT | wx.TB_NOICONS)

        # component identifiers
        self.ID_ENCODE = 255
        self.ID_DECODE = 552

        # add tools
        self.t_plain = self.toolbar.AddLabelTool(wx.ID_OPEN, "Load image",
                                                 wx.NullBitmap,
                                                 longHelp="Containing image")
        self.t_file = self.toolbar.AddLabelTool(wx.ID_FILE, "Load file",
                                                wx.NullBitmap,
                                                longHelp="Load file to hide")
        self.t_key = self.toolbar.AddLabelTool(wx.ID_ADD, "Add key",
                                               wx.NullBitmap,
                                               longHelp="Add encryption key")
        self.t_encode = self.toolbar.AddLabelTool(self.ID_ENCODE, "Encode",
                                                  wx.NullBitmap,
                                                  longHelp="Put file in image")
        self.t_decode = self.toolbar.AddLabelTool(self.ID_DECODE, "Decode",
                                                  wx.NullBitmap,
                                                  longHelp="Retrieve file")
        self.t_help = self.toolbar.AddLabelTool(wx.ID_HELP, "Help",
                                                wx.NullBitmap,
                                                longHelp="Get instructions")
        self.t_exit = self.toolbar.AddLabelTool(wx.ID_EXIT, "Exit",
                                                wx.NullBitmap,
                                                longHelp="Exit program")

        # finalize toolbar
        self.toolbar.Realize()

        # status bar
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(3)
        self.status_bar.SetStatusWidths([-1, -1, -1])

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

    def PlainView(self, plain):
        self.right_panel.DisplayImage(plain['data'])
        self.status_bar.SetStatusText("Image loaded: %s" % plain['name'], 0)

    def FileView(self, file):
        self._file_view = file
        self.status_bar.SetStatusText("File loaded: %s" % file['name'], 1)

    def KeyView(self, key):
        self._key_view = key
        self.status_bar.SetStatusText("Key loaded: %s" % key, 2)

    def CipherView(self, value):
        pass


class Controller:
    def __init__(self, app):
        self.model = Model()

        # initial frame
        self.view = View(None)
        self.view.plain_view = self.model.plain
        self.view.file_view = self.model.file
        self.view.key_view = self.model.key
        self.view.cipher_view = self.model.cipher

        # window behavior
        self.view.Bind(wx.EVT_SIZE, self.view.OnSize)
        self.view.Bind(wx.EVT_CLOSE, self.view.Kill)

        # subscribe functions to messages
        pub.subscribe(self.plain_changed, "PLAIN CHANGED")
        pub.subscribe(self.file_changed, "FILE CHANGED")
        pub.subscribe(self.key_changed, "KEY CHANGED")
        pub.subscribe(self.cipher_changed, "CIPHER CHANGED")

        # listen to gui events
        self.view.toolbar.Bind(wx.EVT_TOOL, self.load_plain, self.view.t_plain)
        self.view.toolbar.Bind(wx.EVT_TOOL, self.load_file, self.view.t_file)
        self.view.toolbar.Bind(wx.EVT_TOOL, self.load_key, self.view.t_key)
        self.view.toolbar.Bind(wx.EVT_TOOL, self.encode_plain, self.view.t_encode)
        self.view.toolbar.Bind(wx.EVT_TOOL, self.view.Kill, self.view.t_decode)
        self.view.toolbar.Bind(wx.EVT_TOOL, self.help_dialog, self.view.t_help)
        self.view.toolbar.Bind(wx.EVT_TOOL, self.view.Kill, self.view.t_exit)

        # encode/decode are not yet available
        self.view.toolbar.EnableTool(self.view.ID_ENCODE, False)
        self.view.toolbar.EnableTool(self.view.ID_DECODE, False)

        self.view.Show()

    # MODEL LISTENER FUNCTIONS
    def plain_changed(self, message):
        self.view.PlainView(self.model.plain)

    def file_changed(self, message):
        self.view.FileView(self.model.file)

    def key_changed(self, message):
        self.view.KeyView(self.model.key)

    def cipher_changed(self, message):
        self.view.cipher_view = self.model.cipher

    # GUI LISTENER FUNCTIONS
    def load_plain(self, event):
        """ Load an image """
        dlg = wx.FileDialog(self.view, message="Choose a file", defaultDir="",
                            defaultFile="",
                            wildcard=("Images (*.bmp,*.gif,*.png,*.jpg)|"
                                      "*.bmp;*.gif;*.png;*.jpg|"
                                      "BMP files (*.bmp)|*.bmp|"
                                      "GIF files (*.gif)|*.gif|"
                                      "PNG files (*.png)|*.png|"
                                      "JPG files (*.jpg)|*.jpg"),
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.model.plain = os.path.join(dlg.GetDirectory(),
                                            dlg.GetFilename())
        dlg.Destroy()

        # check if encode/decode should be enabled
        if self.model.key:
            if self.model.file:
                self.view.toolbar.EnableTool(self.view.ID_ENCODE, True)
            self.view.toolbar.EnableTool(self.view.ID_DECODE, True)

    def load_file(self, event):
        """ Load a file """
        dlg = wx.FileDialog(self.view, "Choose a file", defaultDir=""   ,
                            defaultFile="",
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.model.file = os.path.join(dlg.GetDirectory(),
                                           dlg.GetFilename())
        dlg.Destroy()

        # check if encode should be enabled
        if self.model.plain and self.model.key:
            self.view.toolbar.EnableTool(self.view.ID_ENCODE, True)

    def load_key(self, event):
        dlg = wx.TextEntryDialog(self.view, 'Enter key:',
                                 style=wx.OK | wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            self.model.key = dlg.GetValue()
        dlg.Destroy()

        # check if encode/decode should be enabled
        if self.model.plain:
            if self.model.file:
                self.view.toolbar.EnableTool(self.view.ID_ENCODE, True)
            self.view.toolbar.EnableTool(self.view.ID_DECODE, True)

    def help_dialog(self, event):
        pass

    def encode_plain(self, event):
        self.model.cipher

    def save_cipher(self, name):
        bdm-steg.save_png(self.encoded_image)


if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    # import wx.lib.inspection
    # wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
