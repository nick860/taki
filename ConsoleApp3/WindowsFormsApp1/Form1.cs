using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.Threading;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        System.Net.Sockets.TcpClient clientSocket = new System.Net.Sockets.TcpClient();
        NetworkStream serverStream = default(NetworkStream);
        string readData = null;
        static string myid = null;

        public Form1()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            textBox1.Text = "client started ...";
            clientSocket.Connect("127.0.0.1", 8888);
            serverStream = clientSocket.GetStream();
            label1.Text = "Client Socket Program - Server Connected ...";
            //NetworkStream serverStream = clientSocket.GetStream();
            byte[] outStream = System.Text.Encoding.ASCII.GetBytes(textBox2.Text + "$");
            serverStream.Write(outStream, 0, outStream.Length);
            serverStream.Flush();
            firstMessage();

            Thread ctThread = new Thread(getMessage);
            ctThread.Start();

            //byte[] inStream = new byte[10025];
            //byte[] bytesFrom = new byte[10025];
            //serverStream.Read(inStream, 0, bytesFrom.Length);
            //string returndata = System.Text.Encoding.ASCII.GetString(inStream);
            //msg("Data from Server : " + returndata);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
        }

        private void msg()
        {
            if (this.InvokeRequired)
                this.Invoke(new MethodInvoker(msg));


            else
                textBox1.Text = textBox1.Text + Environment.NewLine + " >> " + readData;
        }

        private void getMessage()
        {
            byte[] bytesFrom = new byte[10025];
            while (true)
            {
                serverStream = clientSocket.GetStream(); //bytesFrom.Length
                int buffSize = 0;
                byte[] inStream = new byte[10025];
                buffSize = bytesFrom.Length;
                serverStream.Read(inStream, 0, buffSize);
                string returndata = System.Text.Encoding.ASCII.GetString(inStream);
                readData = "" + returndata;
                //string id = readData.Substring(readData.Length - Math.Min(2, readData.Length));
                //myid = id;
                
                msg();
            }
        }

        private void firstMessage()
        {
            byte[] bytesFrom = new byte[10025];
            serverStream = clientSocket.GetStream(); 
            int buffSize = 0;
            byte[] inStream = new byte[10025];
            buffSize = bytesFrom.Length;
            serverStream.Read(inStream, 0, buffSize);
            string returndata = System.Text.Encoding.ASCII.GetString(inStream);
            readData = "" + returndata;
            //readData = "" + returndata.Substring(returndata.Length - 1, 1);
            //string id = returndata.Substring(returndata.Length - 1, 1);
            Char c = returndata.Last();
            label1.Text = c.ToString();
            msg();

        }

        private void button1_Click(object sender, EventArgs e)
        {

            byte[] outStream = System.Text.Encoding.ASCII.GetBytes(textBox2.Text + "$");
            serverStream.Write(outStream, 0, outStream.Length);
            serverStream.Flush();
        }
    }
}
