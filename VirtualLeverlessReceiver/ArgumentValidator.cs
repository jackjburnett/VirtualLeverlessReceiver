using System.Net;

namespace VirtualLeverlessReceiver;

public static class ArgumentValidator
{
    public static bool TryParseIPAddress(string input, out string ipAddress)
    {
        ipAddress = "0.0.0.0"; // Default value
        if (IPAddress.TryParse(input, out IPAddress ip))
        {
            ipAddress = input;
            return true;
        }
        return false;
    }

    public static bool TryParsePort(string input, out int port)
    {
        return int.TryParse(input, out port) && port >= 1 && port <= 65535;
    }

    public static bool ValidateArguments(string[] args, out string ipAddress, out int port)
    {
        ipAddress = "0.0.0.0"; // Default value
        port = 8080; // Default value

        if (args.Length > 2)
        {
            Console.WriteLine("Too many arguments. Usage: MyProgram.exe [ipAddress] [port]");
            return false;
        }

        if (args.Length == 2)
        {
            if (TryParseIPAddress(args[0], out ipAddress) && TryParsePort(args[1], out port))
            {
                return true;
            }
            else
            {
                Console.WriteLine("Invalid IP address or port number.");
                return false;
            }
        }
        else if (args.Length == 1)
        {
            if (TryParseIPAddress(args[0], out ipAddress))
            {
                return true;
            }
            else if (TryParsePort(args[0], out port))
            {
                return true;
            }
            else
            {
                Console.WriteLine("Invalid IP address or port number.");
                return false;
            }
        }

        return true; // Use default values
    }
}