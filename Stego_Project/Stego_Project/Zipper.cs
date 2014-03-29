using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Ionic.Zip;
using System.IO;
namespace Stego_Project
{
    class Zipper
    {
        //Zip file with specified password and return stream of zipped file
        public static void zipFile(string filename, string password, out Stream file)
        {
            file = new MemoryStream(); //initialize memory stream
            //Create zip object
            using (ZipFile zip = new ZipFile())
            {
                zip.Password = password; //set password
                zip.AddFile(filename); //add file to zip directory
                zip.Save(file); //save file to a stream
            }
            
        }

        //Unzips passed file with provided password and returns extracted file
        public static void unzipFile(ref Stream file, string password, string unpackDirectory)
        {
            file.Flush();
            file.Seek(0, SeekOrigin.Begin);
            //create zip object
            using (ZipFile zip = ZipFile.Read(file))
            {
                foreach (ZipEntry entry in zip)
                {
                    //extract entry with password
                    entry.ExtractWithPassword(unpackDirectory, password);
                }
            }
        }
    }
}
