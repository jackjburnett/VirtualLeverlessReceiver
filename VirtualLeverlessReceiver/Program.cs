namespace VirtualLeverlessReceiver;

class Program
{
    static void Main(string[] args)
    {
        if (!ArgumentValidator.ValidateArguments(args, out string ipAddress, out int port))
        {
            return; // Exit if arguments are invalid
        }
        UdpServer udpServer = new UdpServer(ipAddress, port);
        udpServer.Start();
    }
}