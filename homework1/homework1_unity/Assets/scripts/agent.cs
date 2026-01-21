using System.Linq;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using Unity.VisualScripting;
using UnityEngine;

public class agent : Agent {
    public sys sys;
    private int current_episode = 0;
    private float episode_time = 0f;
    private float debug_log_angle;
    private const float max_expected_ball_vel = 10f;
    private int step;
    public override void Initialize() {
        Debug.Log("Agent started");
        current_episode = 0;
    }
    public override void OnEpisodeBegin() {
        current_episode++; //track the number of episodes
        episode_time = 0;
        sys.random_reset(); //reset w/ random start for the new run

    }
    public override void CollectObservations(VectorSensor sensor) {
        // Collect raw observations
        float ballPos = sys.ball_driver.get_pos();
        float beamAngle = sys.beam_driver.get_angle();
        float targetPos = sys.target_manager.get_target();
        float inTarget = sys.eval.is_in_target() ? 1f : 0f;
        float distFromTarget = sys.eval.dist_from_target();
        float ballVel = sys.ball_driver.get_speed() / max_expected_ball_vel;
        ballVel = Mathf.Clamp(ballVel, -1f, 1f);

        // Add observations to the sensor
        sensor.AddObservation(ballPos);
        sensor.AddObservation(ballVel);
        sensor.AddObservation(beamAngle);
        sensor.AddObservation(targetPos);
        sensor.AddObservation(inTarget);
        sensor.AddObservation(distFromTarget);

        // Print observations for debugging
        // if (step == 50) {
        //     Debug.Log(
        //         $"OBS | ballPos={ballPos:F3} " +
        //         $"ballVel={ballVel:F3} " +
        //         $"beamAngle={beamAngle:F3} " +
        //         $"targetPos={targetPos:F3} " +
        //         $"inTarget={inTarget:F0} " +
        //         $"distFromTarget={distFromTarget:F3}" +
        //         $"angle={debug_log_angle:F3}"
        //     );
        //     step = 0;
        // } else {
        //     step++;
        // }
    }

    public override void OnActionReceived(ActionBuffers actions) {
        set_beam(actions.ContinuousActions);
        episode_time += Time.fixedDeltaTime;
        //update the reward after the step penalty above
        AddReward(normalize_reward((0.3f - sys.eval.dist_from_target()) * 0.1f));
        if (sys.eval.is_stable) {
            Debug.Log(normalize_reward(1f));
            AddReward(normalize_reward(1f));
        }

        if (sys.eval.is_stable_complete) {
            goal_reached();
        }
        if (sys.ball_driver.is_falling) {
            AddReward(-10.0f);
            EndEpisode();

        }
    }
    private void set_beam(ActionSegment<float> action_segment) {
        float delta_angle = action_segment[0];
        float angle = sys.beam_driver.get_angle() + delta_angle / 2f;

        var angle_diff = 0.5f - angle;
        angle_diff = angle_diff * angle_diff * 1f;

        AddReward(-normalize_reward(angle_diff));
        angle = Mathf.Clamp(angle, 0f, 1f);
        sys.beam_driver.set_angle(angle);

    }
    private void goal_reached() {
        AddReward(10.0f);
        EndEpisode();
    }
    private float normalize_reward(float reward) {
        return reward * Time.fixedDeltaTime;
    }
}
