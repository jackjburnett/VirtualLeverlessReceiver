using System.Net;
using System.Net.Sockets;
using System.Text;
using WindowsInput;
using WindowsInput.Native;

public class VirtualLeverlessReceiver
{
    private TcpListener _server;
    private bool _isRunning;
    private InputSimulator _inputSimulator;
    private int _connectionCounter;  // To assign unique IDs
    private Dictionary<int, TcpClient> _clients = new Dictionary<int, TcpClient>();

    private VirtualLeverlessReceiver(string ipAddress, int port)
    {
        // Initialize InputSimulator
        _inputSimulator = new InputSimulator();

        // Set up the _server
        _server = new TcpListener(IPAddress.Parse(ipAddress), port);
        _server.Start();
        _isRunning = true;

        Console.WriteLine($"_server started on {ipAddress}:{port}");
        ThreadPool.QueueUserWorkItem(ListenerThread);
    }

    private void ListenerThread(object state)
    {
        while (_isRunning)
        {
            TcpClient client = _server.AcceptTcpClient();
            _connectionCounter++;  // Increment the connection counter
            int clientId = _connectionCounter;  // Assign a unique ID to this client
            _clients.Add(clientId, client);  // Track the client with its ID
            Console.WriteLine($"Client {clientId} connected.");
            
            ThreadPool.QueueUserWorkItem(HandleClient, clientId);  // Pass client ID to handle input
        }
    }

    private void HandleClient(object obj)
    {
        int clientId = (int)obj;
        TcpClient client = _clients[clientId];
        NetworkStream stream = client.GetStream();
        byte[] buffer = new byte[1024];
        int bytesRead;

        while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) != 0)
        {
            string message = Encoding.ASCII.GetString(buffer, 0, bytesRead);
            Console.WriteLine($"Received command from Client {clientId}: {message}");
            InterpretCommand(clientId, message);  // Pass the connection ID with the message
        }

        client.Close();
        _clients.Remove(clientId);
    }

    private void InterpretCommand(int clientId, string message)
    {
        // Device 1 (ID 1) sends a "jump" mapped to "W", Device 2 (ID 2) sends "jump" mapped to "Up Arrow"
        if (clientId == 1)
        {
            switch (message.ToLower())
            {
                case "up":
                    _inputSimulator.Keyboard.KeyPress(VirtualKeyCode.VK_W);  // Simulate W key (Jump for Device 1)
                    Console.WriteLine("Simulated W key (Jump for Device 1)");
                    break;
                case "left":
                    _inputSimulator.Keyboard.KeyDown(VirtualKeyCode.VK_A);  // Move left for Device 1
                    Console.WriteLine("Simulated A key (Move Left for Device 1)");
                    break;
                // Add more controls for Device 1 as needed
            }
        }
        else if (clientId == 2)
        {
            switch (message.ToLower())
            {
                case "up":
                    _inputSimulator.Keyboard.KeyPress(VirtualKeyCode.UP);  // Simulate Up Arrow key (Jump for Device 2)
                    Console.WriteLine("Simulated Up Arrow key (Jump for Device 2)");
                    break;
                case "left":
                    _inputSimulator.Keyboard.KeyDown(VirtualKeyCode.LEFT);  // Move left for Device 2
                    Console.WriteLine("Simulated Left Arrow key (Move Left for Device 2)");
                    break;
                // Add more controls for Device 2 as needed
            }
        }
        // You can add more client IDs and custom mappings as needed
    }

    private void Stop()
    {
        _isRunning = false;
        _server.Stop();
    }

    public static void Main(string[] args)
    {
        VirtualLeverlessReceiver server = new VirtualLeverlessReceiver("YOUR_PC_IP_ADDRESS", 5000);  // Replace with your PC's IP address
        Console.ReadLine();
        server.Stop();
    }
}
