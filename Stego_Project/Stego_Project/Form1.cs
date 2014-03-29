using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace Stego_Project
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void tableLayoutPanel_Images_Paint(object sender, PaintEventArgs e)
        {

        }

        private void radioButton_Encrypt_CheckedChanged(object sender, EventArgs e)
        {
            this.button_OpenFile_ExtractTo.Text = "Choose File";
            this.button_Save_To.Visible = true;
            this.textBox_SaveTo.Visible = true;
        }

        private void radioButton_Extract_CheckedChanged(object sender, EventArgs e)
        {
            this.button_Save_To.Visible = false;
            this.textBox_SaveTo.Visible = false;
            this.button_OpenFile_ExtractTo.Text = "Extract To";
        }

        private void button_OpenImage_Click(object sender, EventArgs e)
        {
            //Clear previous images
            this.pictureBox_ProcessedImage.Image = null;
            //Get Open File Dialog
            OpenFileDialog fileChooser = new OpenFileDialog();
            fileChooser.Filter = "Image files (PNG, GIF, TIFF, JPG, JPEG)|*.png;*.gif;" +
            "*.tiff;*.jpg;*.jpeg";
            
            fileChooser.RestoreDirectory = true;
            //Let user to choose image
            if (fileChooser.ShowDialog() == DialogResult.OK)
            {
                //load image into picture box
                this.pictureBox_OriginalImage.Image = Image.FromFile(fileChooser.FileName);
                this.textBox_Image.Text = fileChooser.FileName;
            }
        }

        private void button_OpenFile_Click(object sender, EventArgs e)
        {
            if (this.radioButton_Encrypt.Checked == true)
            { //Open File
                //Get file chooser
                OpenFileDialog fileChooser = new OpenFileDialog();
                fileChooser.Filter = "All (*.*)|*.*";
                fileChooser.RestoreDirectory = true;
                //Let user to choose file
                if (fileChooser.ShowDialog() == DialogResult.OK)
                {
                    //Put file directory name into textbox
                    this.textBox_File.Text = fileChooser.FileName;
                }
            }
            else
            { //Extract to directory
                FolderBrowserDialog folderChooser = new FolderBrowserDialog();
                if (folderChooser.ShowDialog() == DialogResult.OK)
                {
                    this.textBox_File.Text = folderChooser.SelectedPath;
                }
            }
        }

        private void button_GO_Click(object sender, EventArgs e)
        {
            if (this.radioButton_Encrypt.Checked == true)
            {//Encrypt
                //Check that all files are specified
                if (this.textBox_Image.Text == "")
                {
                    MessageBox.Show("Image was not specified!\nPlease choose image","Warning",
                        MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                if(this.textBox_File.Text == "")
                {
                    MessageBox.Show("File was not specified!\nPlease choose file", "Warning",
                        MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                if(this.textBox_SaveTo.Text == "")
                {
                    MessageBox.Show("Directory was not specified!\nPlease select directory to save to", 
                        "Warning", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                //Prompt user for password
                Form_PasswordPrompt prompt = new Form_PasswordPrompt();
                prompt.StartPosition = FormStartPosition.CenterScreen;
                prompt.ShowDialog();
                if (prompt.getPasswordText() == "")
                    return;
                //file stream
                Stream file;
                //Zip file
                Zipper.zipFile(this.textBox_File.Text, prompt.getPasswordText(), out file);
                //Create bitmap of the image
                Bitmap originalImage = new Bitmap(this.pictureBox_OriginalImage.Image);
                //Hide file
                Stegalicious.Stego.HideMessage(file, originalImage);
                //Show processed image
                this.pictureBox_ProcessedImage.Image = (Image)originalImage;
                originalImage.Save(this.textBox_SaveTo.Text);
            }
            else
            {//decrypt
                if (this.textBox_Image.Text == "")
                {
                    MessageBox.Show("Image was not specified!\nPlease choose image", "Warning",
                        MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                if (this.textBox_File.Text == "")
                {
                    MessageBox.Show("Extract directory was not specified!\nPlease choose directory to" + 
                    "extract file to", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    return;
                }
                
                //Prompt user for password
                Form_PasswordPrompt prompt = new Form_PasswordPrompt();
                prompt.StartPosition = FormStartPosition.CenterScreen;
                prompt.ShowDialog();
                if (prompt.getPasswordText() == "")
                    return;
                //Get password, stream and bitmap objects
                string password = prompt.getPasswordText();
                Stream file = new MemoryStream();
                Bitmap image = new Bitmap(this.pictureBox_OriginalImage.Image);
                //Extract message
                Stegalicious.Stego.ExtractMessage(image, ref file);
                //Unzip message with password
                Zipper.unzipFile(ref file, password, this.textBox_File.Text);
            }
        }

        private void button_Save_To_Click(object sender, EventArgs e)
        {
            SaveFileDialog saveDialog = new SaveFileDialog();
            saveDialog.Filter = "Image files (PNG, GIF, TIFF, JPG, JPEG)|*.png;*.gif;*.tiff;*.jpg;*.jpeg";
            saveDialog.RestoreDirectory = true;
            if (saveDialog.ShowDialog() == DialogResult.OK)
            {
                this.textBox_SaveTo.Text = saveDialog.FileName;
            }
        }

        
    }
}
