using System.Linq;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine;

public class agent : Agent {
    public sys sys;
    private int current_episode = 0;
    private float cumulative_reward = 0f;
    public override void Initialize() {
        Debug.Log("Agent started");
        current_episode = 0;
        cumulative_reward = 0;
    }
    public override void OnEpisodeBegin() {
        current_episode++; //track the number of episodes
        cumulative_reward = 0f; //reset reward 
        sys.random_reset(); //reset w/ random start for the new run

    }
    public override void CollectObservations(VectorSensor sensor) {
        sensor.AddObservation(sys.ball_driver.get_pos());
        sensor.AddObservation(sys.ball_driver.get_speed());
        sensor.AddObservation(sys.beam_driver.get_angle());
        sensor.AddObservation(sys.target_manager.get_target());
        sensor.AddObservation(sys.eval.is_in_target());
        sensor.AddObservation(sys.eval.dist_from_target());
    }
    public override void OnActionReceived(ActionBuffers actions) {
        set_beam(actions.ContinuousActions);
        AddReward(-2f / MaxStep); //slap the agent for going slow
        //update the reward after the step penalty above
        cumulative_reward = GetCumulativeReward();
        if (sys.eval.is_stable) {
            goal_reached();
        }
        if (sys.ball_driver.is_falling) {
            AddReward(-1.0f);
            cumulative_reward = GetCumulativeReward();
            EndEpisode();

        }
    }
    private void set_beam(ActionSegment<float> action_segment) {
        float angle = action_segment[0];
        sys.beam_driver.set_angle(angle);

    }
    private void goal_reached() {
        AddReward(1.0f);
        cumulative_reward = GetCumulativeReward();
        EndEpisode();
    }
}
