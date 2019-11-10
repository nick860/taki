using System;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ConsoleApp15
{
    class Program
    {
        static void Main(string[] args)
        {
            StreamWriter file = new StreamWriter(@"C:\takifolder\cardfile.txt");

            int port = 48003;
            IPAddress localAddr = IPAddress.Parse("192.168.1.214");                         // server
            TcpListener server = new TcpListener(localAddr, port);
            server.Start();
            byte[] bytes = new byte[256];
            int i;
            string data = null;
            Console.WriteLine("awaiting connection");
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Connected –wait for data");
            NetworkStream stream = client.GetStream();
            while ((i = stream.Read(bytes, 0, bytes.Length)) != 0)                          // Loop to receive all data
            {
                data = Encoding.ASCII.GetString(bytes, 0, i);                               // Translate data to a ASCII.
                Console.WriteLine(string.Format("Received data"));

                string signs = data;
                string[] cards = signs.Split(';');
                for (int j = 0; j < cards.Length; j++)                                      // Process the data sent by the client.
                {
                    cards[j] = (j + 1).ToString() + ". " + cards[j];
                    file.WriteLine(cards[j]);
                }

                byte[] msg = Encoding.ASCII.GetBytes("transferred the data successfully");
                stream.Write(msg, 0, msg.Length);                                           // Send back a response.
                Console.WriteLine("now we wait again");
            }
            client.Close();                                                                 // Shutdown and end connection
        }
    }
}
