using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine;

public class agent : Agent {
    private int current_episode = 0;
    private float cumulative_reward = 0f;
    public override void Initialize() {
        Debug.Log("Agent started");
        current_episode = 0;
        cumulative_reward = 0;
    }
    public override void OnEpisodeBegin() {
    }
    public override void CollectObservations(VectorSensor sensor) {
    }
    public override void OnActionReceived(ActionBuffers actions) {
    }
}
