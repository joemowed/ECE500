using System.Net.Sockets;
using UnityEngine;
using System.Text;
using System.Net;
using UnityEngine.InputSystem;

public class network : MonoBehaviour {
    public sys sys;
    private UdpClient client;
    private IPEndPoint remoteEndPoint;
    private bool mode_send = true;

    void Start() {
        // 1. Setup the "Sender" to Python (Port 5005)
        remoteEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 5005);
        client = new UdpClient(5006); // Listen for replies on 5006
    }

    void Update() {
        if (mode_send) {
            outbound_packet data;
            data.ball_pos = sys.ball_driver.get_pos();
            data.ball_velocity = sys.ball_driver.get_speed();
            data.target_pos = sys.target_manager.get_target();
            data.target_distance_percent = sys.eval.dist_from_target();
            data.stable_time_percent = sys.eval.stable_time_percent();
            data.is_stable = sys.eval.is_stable;
            send(data);
        } else {
            // 2. Check for incoming data (Receive)
            if (client.Available > 0) {
                IPEndPoint anyIP = new IPEndPoint(IPAddress.Any, 0);
                byte[] data = client.Receive(ref anyIP);
                string text = Encoding.UTF8.GetString(data);
                mode_send = true;
                Debug.Log("Python sent: " + text);
            }
        }
    }

    public void send(outbound_packet message) {
        var json = JsonUtility.ToJson(message);
        byte[] data = Encoding.UTF8.GetBytes(json);
        client.Send(data, data.Length, remoteEndPoint);
        Debug.Log("Sent to Python: " + message);
    }

    void OnApplicationQuit() {
        client.Close();
    }
}

//[StructLayout(LayoutKind.Sequential, Pack = 1)]
public struct outbound_packet {
    public float ball_pos;
    public float ball_velocity;
    public float target_pos;
    public float target_distance_percent;
    public float stable_time_percent;
    public bool is_stable;
}

public struct inbound_packet {
    public float beam_angle;
    public bool reset_system;
}
