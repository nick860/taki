using System;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp15
{
    class Program
    {
        static void Main(string[] args)
        {
            int port = 50005;
            IPAddress localAddr = IPAddress.Parse("192.168.1.214");              // server
            TcpListener server = new TcpListener(localAddr, port);
            server.Start();
            byte[] bytes = new byte[256];
            int i;
            string data = null;
            TcpClient client = server.AcceptTcpClient();
            Console.WriteLine("Connected –wait for data");
            NetworkStream stream = client.GetStream();
            while ((i = stream.Read(bytes, 0, bytes.Length)) != 0)          // Loop to receive all data
            {
                data = Encoding.ASCII.GetString(bytes, 0, i);   // Translate data to a ASCII.
                Console.WriteLine(string.Format("Received: {0}", data));
                data = data.ToUpper();                                      // Process the data sent by the client.
                byte[] msg = Encoding.ASCII.GetBytes(data);
                stream.Write(msg, 0, msg.Length);                           // Send back a response.
                Console.WriteLine(string.Format("Sent: {0}", data));
            }
            client.Close();                                                 // Shutdown and end connection
        }
    }
}
