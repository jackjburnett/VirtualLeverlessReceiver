using System.Net;
using System.Net.Sockets;
using System.Text;

namespace VirtualLeverlessReceiver;

public class UdpServer(string ipAddress, int port)
{
    public void Start()
    {
        Console.WriteLine($"Setting up VirtualLeverless Receiver on {ipAddress}:{port}...");
        UdpClient udpServer = new UdpClient(new IPEndPoint(IPAddress.Parse(ipAddress), port));
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, port);

        Console.WriteLine($"Listening for UDP messages on {ipAddress}:{port}...");

        try
        {
            while (true)
            {
                byte[] data = udpServer.Receive(ref remoteEndPoint);
                string message = Encoding.ASCII.GetString(data);

                Console.WriteLine($"Received: {message} from {remoteEndPoint.Address}");

                // Handle the message and simulate key press if needed
                if (message.Equals("SPACEBAR", StringComparison.OrdinalIgnoreCase))
                {
                    //
                }
            }
        }
        catch (SocketException e)
        {
            Console.WriteLine("SocketException: " + e.Message);
        }
        finally
        {
            udpServer.Close();
        }
    }
}