namespace Stego_Project
{
    partial class Form_PasswordPrompt
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
            this.textBox_Password = new System.Windows.Forms.TextBox();
            this.label_PasswordText = new System.Windows.Forms.Label();
            this.button_AcceptPassword = new System.Windows.Forms.Button();
            this.button_DeclinePassword = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // textBox_Password
            // 
            this.textBox_Password.Location = new System.Drawing.Point(12, 25);
            this.textBox_Password.Name = "textBox_Password";
            this.textBox_Password.Size = new System.Drawing.Size(334, 20);
            this.textBox_Password.TabIndex = 0;
            this.textBox_Password.UseSystemPasswordChar = true;
            // 
            // label_PasswordText
            // 
            this.label_PasswordText.AutoSize = true;
            this.label_PasswordText.Location = new System.Drawing.Point(9, 9);
            this.label_PasswordText.Name = "label_PasswordText";
            this.label_PasswordText.Size = new System.Drawing.Size(140, 13);
            this.label_PasswordText.TabIndex = 1;
            this.label_PasswordText.Text = "Please enter your password:";
            // 
            // button_AcceptPassword
            // 
            this.button_AcceptPassword.Location = new System.Drawing.Point(96, 67);
            this.button_AcceptPassword.Name = "button_AcceptPassword";
            this.button_AcceptPassword.Size = new System.Drawing.Size(75, 23);
            this.button_AcceptPassword.TabIndex = 2;
            this.button_AcceptPassword.Text = "Ok";
            this.button_AcceptPassword.UseVisualStyleBackColor = true;
            this.button_AcceptPassword.Click += new System.EventHandler(this.button_AcceptPassword_Click);
            // 
            // button_DeclinePassword
            // 
            this.button_DeclinePassword.Location = new System.Drawing.Point(186, 67);
            this.button_DeclinePassword.Name = "button_DeclinePassword";
            this.button_DeclinePassword.Size = new System.Drawing.Size(75, 23);
            this.button_DeclinePassword.TabIndex = 3;
            this.button_DeclinePassword.Text = "Cancel";
            this.button_DeclinePassword.UseVisualStyleBackColor = true;
            this.button_DeclinePassword.Click += new System.EventHandler(this.button_DeclinePassword_Click);
            // 
            // Form_PasswordPrompt
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(377, 102);
            this.Controls.Add(this.button_DeclinePassword);
            this.Controls.Add(this.button_AcceptPassword);
            this.Controls.Add(this.label_PasswordText);
            this.Controls.Add(this.textBox_Password);
            this.Name = "Form_PasswordPrompt";
            this.Text = "Please Enter Password";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox_Password;
        private System.Windows.Forms.Label label_PasswordText;
        private System.Windows.Forms.Button button_AcceptPassword;
        private System.Windows.Forms.Button button_DeclinePassword;
    }
}