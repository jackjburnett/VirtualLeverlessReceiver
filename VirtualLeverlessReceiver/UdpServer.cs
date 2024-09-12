using System.Net;
using System.Net.Sockets;
using System.Text;

namespace VirtualLeverlessReceiver;

public class UdpServer(InputSimulator inputSimulator, string ipAddress, int port)
{
    public void Start()
    {
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
                    inputSimulator.SendKeyDown(0x20); // Spacebar virtual key code
                    Thread.Sleep(100); // Brief delay to simulate the key press duration
                    inputSimulator.SendKeyUp(0x20);
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