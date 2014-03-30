using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Ionic.Zip;
using System.IO;
using System.Windows.Forms;
namespace Stego_Project
{
    class Zipper
    {
        //Zip file with specified password and return stream of zipped file
        public static void zipFile(string filename, string password, out MemoryStream file)
        {
            file = new MemoryStream(); //initialize memory stream
            /*FileStream fs = new FileStream(filename, FileMode.Open, FileAccess.Read);
            byte[] bytes = new byte[fs.Length];
            fs.Read(bytes, 0, (int)fs.Length);
            file.Write(bytes, 0, (int)fs.Length);
            fs.Close();
            file.Seek(0, SeekOrigin.Begin);
            //Create zip object*/
            using (ZipFile zip = new ZipFile())
            {
                zip.Password = password; //set password
                //zip.AddEntry(filename, file);
                zip.AddFile(filename); //add file to zip directory
                zip.Save(file); //save file to a stream
                //zip.Save("testFile.zip"); //save file to a stream
               
            }
            file.Seek(0, SeekOrigin.Begin);
            //file.Flush();
        }

        //Unzips passed file with provided password and returns extracted file
        public static void unzipFile(MemoryStream file, string password, string unpackDirectory)
        {
            //Reset stream
            file.Seek(0, SeekOrigin.Begin);
            /*FileStream fs = new FileStream("outfile.pdf", FileMode.Create);
            byte[] streamContent = new Byte[file.Length];
            file.Read(streamContent, 0, streamContent.Length);
            fs.Write(streamContent, 0, streamContent.Length);
            fs.Close();*/
                        
            //create zip object
            using (ZipFile zip = ZipFile.Read(file))
            {
                foreach (ZipEntry entry in zip)
                {
                    
                    //extract entry with password
                    try
                    {
                        entry.ExtractWithPassword(unpackDirectory, password);
                    }
                    catch (Exception e)
                    {
                        MessageBox.Show(e.Message, "Warning", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
                    }
                   // entry.Extract(unpackDirectory);
                    
                }
            }
        }
    }
}
