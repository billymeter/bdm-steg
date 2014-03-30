namespace Stego_Project
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.panel_Inputs = new System.Windows.Forms.Panel();
            this.textBox_SaveTo = new System.Windows.Forms.TextBox();
            this.button_Save_To = new System.Windows.Forms.Button();
            this.button_GO = new System.Windows.Forms.Button();
            this.radioButton_Extract = new System.Windows.Forms.RadioButton();
            this.radioButton_Encrypt = new System.Windows.Forms.RadioButton();
            this.button_OpenFile_ExtractTo = new System.Windows.Forms.Button();
            this.button_OpenImage = new System.Windows.Forms.Button();
            this.textBox_File = new System.Windows.Forms.TextBox();
            this.textBox_Image = new System.Windows.Forms.TextBox();
            this.tableLayoutPanel_Images = new System.Windows.Forms.TableLayoutPanel();
            this.pictureBox_OriginalImage = new System.Windows.Forms.PictureBox();
            this.pictureBox_ProcessedImage = new System.Windows.Forms.PictureBox();
            this.progressBar = new System.Windows.Forms.ProgressBar();
            this.panel_Inputs.SuspendLayout();
            this.tableLayoutPanel_Images.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox_OriginalImage)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox_ProcessedImage)).BeginInit();
            this.SuspendLayout();
            // 
            // panel_Inputs
            // 
            this.panel_Inputs.Controls.Add(this.progressBar);
            this.panel_Inputs.Controls.Add(this.textBox_SaveTo);
            this.panel_Inputs.Controls.Add(this.button_Save_To);
            this.panel_Inputs.Controls.Add(this.button_GO);
            this.panel_Inputs.Controls.Add(this.radioButton_Extract);
            this.panel_Inputs.Controls.Add(this.radioButton_Encrypt);
            this.panel_Inputs.Controls.Add(this.button_OpenFile_ExtractTo);
            this.panel_Inputs.Controls.Add(this.button_OpenImage);
            this.panel_Inputs.Controls.Add(this.textBox_File);
            this.panel_Inputs.Controls.Add(this.textBox_Image);
            this.panel_Inputs.Dock = System.Windows.Forms.DockStyle.Top;
            this.panel_Inputs.Location = new System.Drawing.Point(0, 0);
            this.panel_Inputs.Name = "panel_Inputs";
            this.panel_Inputs.Size = new System.Drawing.Size(598, 111);
            this.panel_Inputs.TabIndex = 0;
            // 
            // textBox_SaveTo
            // 
            this.textBox_SaveTo.Location = new System.Drawing.Point(328, 80);
            this.textBox_SaveTo.Name = "textBox_SaveTo";
            this.textBox_SaveTo.Size = new System.Drawing.Size(262, 20);
            this.textBox_SaveTo.TabIndex = 8;
            // 
            // button_Save_To
            // 
            this.button_Save_To.Location = new System.Drawing.Point(238, 77);
            this.button_Save_To.Name = "button_Save_To";
            this.button_Save_To.Size = new System.Drawing.Size(84, 23);
            this.button_Save_To.TabIndex = 1;
            this.button_Save_To.Text = "Save To";
            this.button_Save_To.UseVisualStyleBackColor = true;
            this.button_Save_To.Click += new System.EventHandler(this.button_Save_To_Click);
            // 
            // button_GO
            // 
            this.button_GO.Location = new System.Drawing.Point(12, 58);
            this.button_GO.Name = "button_GO";
            this.button_GO.Size = new System.Drawing.Size(75, 23);
            this.button_GO.TabIndex = 7;
            this.button_GO.Text = "GO!";
            this.button_GO.UseVisualStyleBackColor = true;
            this.button_GO.Click += new System.EventHandler(this.button_GO_Click);
            // 
            // radioButton_Extract
            // 
            this.radioButton_Extract.AutoSize = true;
            this.radioButton_Extract.Location = new System.Drawing.Point(12, 35);
            this.radioButton_Extract.Name = "radioButton_Extract";
            this.radioButton_Extract.Size = new System.Drawing.Size(77, 17);
            this.radioButton_Extract.TabIndex = 6;
            this.radioButton_Extract.Text = "Extract File";
            this.radioButton_Extract.UseVisualStyleBackColor = true;
            this.radioButton_Extract.CheckedChanged += new System.EventHandler(this.radioButton_Extract_CheckedChanged);
            // 
            // radioButton_Encrypt
            // 
            this.radioButton_Encrypt.AutoSize = true;
            this.radioButton_Encrypt.Checked = true;
            this.radioButton_Encrypt.Location = new System.Drawing.Point(12, 12);
            this.radioButton_Encrypt.Name = "radioButton_Encrypt";
            this.radioButton_Encrypt.Size = new System.Drawing.Size(80, 17);
            this.radioButton_Encrypt.TabIndex = 5;
            this.radioButton_Encrypt.TabStop = true;
            this.radioButton_Encrypt.Text = "Encrypt File";
            this.radioButton_Encrypt.UseVisualStyleBackColor = true;
            this.radioButton_Encrypt.CheckedChanged += new System.EventHandler(this.radioButton_Encrypt_CheckedChanged);
            // 
            // button_OpenFile_ExtractTo
            // 
            this.button_OpenFile_ExtractTo.Location = new System.Drawing.Point(238, 47);
            this.button_OpenFile_ExtractTo.Name = "button_OpenFile_ExtractTo";
            this.button_OpenFile_ExtractTo.Size = new System.Drawing.Size(84, 23);
            this.button_OpenFile_ExtractTo.TabIndex = 4;
            this.button_OpenFile_ExtractTo.Text = "Choose File";
            this.button_OpenFile_ExtractTo.UseVisualStyleBackColor = true;
            this.button_OpenFile_ExtractTo.Click += new System.EventHandler(this.button_OpenFile_Click);
            // 
            // button_OpenImage
            // 
            this.button_OpenImage.Location = new System.Drawing.Point(238, 12);
            this.button_OpenImage.Name = "button_OpenImage";
            this.button_OpenImage.Size = new System.Drawing.Size(84, 23);
            this.button_OpenImage.TabIndex = 3;
            this.button_OpenImage.Text = "Choose Image";
            this.button_OpenImage.UseVisualStyleBackColor = true;
            this.button_OpenImage.Click += new System.EventHandler(this.button_OpenImage_Click);
            // 
            // textBox_File
            // 
            this.textBox_File.Location = new System.Drawing.Point(328, 50);
            this.textBox_File.Name = "textBox_File";
            this.textBox_File.Size = new System.Drawing.Size(262, 20);
            this.textBox_File.TabIndex = 2;
            // 
            // textBox_Image
            // 
            this.textBox_Image.Location = new System.Drawing.Point(328, 15);
            this.textBox_Image.Name = "textBox_Image";
            this.textBox_Image.Size = new System.Drawing.Size(262, 20);
            this.textBox_Image.TabIndex = 1;
            // 
            // tableLayoutPanel_Images
            // 
            this.tableLayoutPanel_Images.CellBorderStyle = System.Windows.Forms.TableLayoutPanelCellBorderStyle.Inset;
            this.tableLayoutPanel_Images.ColumnCount = 2;
            this.tableLayoutPanel_Images.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel_Images.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel_Images.Controls.Add(this.pictureBox_OriginalImage, 0, 0);
            this.tableLayoutPanel_Images.Controls.Add(this.pictureBox_ProcessedImage, 1, 0);
            this.tableLayoutPanel_Images.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel_Images.Location = new System.Drawing.Point(0, 111);
            this.tableLayoutPanel_Images.Name = "tableLayoutPanel_Images";
            this.tableLayoutPanel_Images.RowCount = 1;
            this.tableLayoutPanel_Images.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel_Images.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel_Images.Size = new System.Drawing.Size(598, 293);
            this.tableLayoutPanel_Images.TabIndex = 0;
            this.tableLayoutPanel_Images.Paint += new System.Windows.Forms.PaintEventHandler(this.tableLayoutPanel_Images_Paint);
            // 
            // pictureBox_OriginalImage
            // 
            this.pictureBox_OriginalImage.BackColor = System.Drawing.SystemColors.ButtonHighlight;
            this.pictureBox_OriginalImage.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pictureBox_OriginalImage.Location = new System.Drawing.Point(5, 5);
            this.pictureBox_OriginalImage.Name = "pictureBox_OriginalImage";
            this.pictureBox_OriginalImage.Size = new System.Drawing.Size(290, 283);
            this.pictureBox_OriginalImage.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox_OriginalImage.TabIndex = 8;
            this.pictureBox_OriginalImage.TabStop = false;
            // 
            // pictureBox_ProcessedImage
            // 
            this.pictureBox_ProcessedImage.BackColor = System.Drawing.SystemColors.ButtonHighlight;
            this.pictureBox_ProcessedImage.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pictureBox_ProcessedImage.Location = new System.Drawing.Point(303, 5);
            this.pictureBox_ProcessedImage.Name = "pictureBox_ProcessedImage";
            this.pictureBox_ProcessedImage.Size = new System.Drawing.Size(290, 283);
            this.pictureBox_ProcessedImage.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.pictureBox_ProcessedImage.TabIndex = 9;
            this.pictureBox_ProcessedImage.TabStop = false;
            // 
            // progressBar
            // 
            this.progressBar.Location = new System.Drawing.Point(5, 87);
            this.progressBar.Name = "progressBar";
            this.progressBar.Size = new System.Drawing.Size(216, 22);
            this.progressBar.Step = 1;
            this.progressBar.TabIndex = 9;
            this.progressBar.Visible = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(598, 404);
            this.Controls.Add(this.tableLayoutPanel_Images);
            this.Controls.Add(this.panel_Inputs);
            this.Name = "Form1";
            this.Text = "BDM-Stego";
            this.panel_Inputs.ResumeLayout(false);
            this.panel_Inputs.PerformLayout();
            this.tableLayoutPanel_Images.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox_OriginalImage)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox_ProcessedImage)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Panel panel_Inputs;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel_Images;
        private System.Windows.Forms.Button button_GO;
        private System.Windows.Forms.RadioButton radioButton_Extract;
        private System.Windows.Forms.RadioButton radioButton_Encrypt;
        private System.Windows.Forms.Button button_OpenFile_ExtractTo;
        private System.Windows.Forms.Button button_OpenImage;
        private System.Windows.Forms.TextBox textBox_File;
        private System.Windows.Forms.TextBox textBox_Image;
        private System.Windows.Forms.PictureBox pictureBox_OriginalImage;
        private System.Windows.Forms.PictureBox pictureBox_ProcessedImage;
        private System.Windows.Forms.TextBox textBox_SaveTo;
        private System.Windows.Forms.Button button_Save_To;
        private System.Windows.Forms.ProgressBar progressBar;
    }
}

