namespace VirtualLeverlessReceiver;

class Program
{
    static void Main(string[] args)
    {
        if (!ArgumentValidator.ValidateArguments(args, out string ipAddress, out int port))
        {
            return; // Exit if arguments are invalid
        }

        InputSimulator inputSimulator = new InputSimulator();
        UdpServer udpServer = new UdpServer(inputSimulator, ipAddress, port);
        udpServer.Start();
    }
}