using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Stego_Project
{
    public partial class Form_PasswordPrompt : Form
    {
        public Form_PasswordPrompt()
        {
            InitializeComponent();
        }

        private void button_AcceptPassword_Click(object sender, EventArgs e)
        {
            if (this.textBox_Password.Text == "")
            {
                MessageBox.Show("Password was not specified!\nPlease enter a password",
                       "Warning", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                return;
            }
            this.Close();
        }

        private void button_DeclinePassword_Click(object sender, EventArgs e)
        {
            this.textBox_Password.Text = "";
            this.Close();
        }

        public string getPasswordText()
        {
            return this.textBox_Password.Text;
        }
    }
}
