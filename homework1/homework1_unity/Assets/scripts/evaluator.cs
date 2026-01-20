using UnityEngine;

public class evaluator : MonoBehaviour {
    public target_manager tm;
    public ball_driver bd;
    private const float target_area = 0.03f; //area where ball is considered in the target zone as a percent of the beam length
    private const float stable_time = 5f; //time ball must be in area to be considered stable
    private const float stable_speed = 0.1f;//max speed of ball to be considered stable
    public float in_target_time { get; private set; }
    public bool is_stable { get; private set; }

    // Update is called once per frame
    void Update() {
        if (is_in_target() && is_below_speed_limit()) {
            in_target_time += Time.deltaTime;
        } else {
            in_target_time = 0f;
        }
        if (in_target_time >= stable_time) {
            is_stable = true;
        } else {
            is_stable = false;
        }

    }
    public float dist_from_target() {
        return Mathf.Abs(tm.get_target() - bd.get_pos());
    }
    private bool is_below_speed_limit() {
        return bd.get_speed() <= stable_speed;
    }
    public bool is_in_target() {
        return dist_from_target() <= target_area;
    }
    //returns what percent of the time required to be stable the ball has been in the target, up to 100% (range 0-1).
    public float stable_time_percent() {
        float result = in_target_time / stable_time;
        return Mathf.Clamp(result, 0, 1);

    }
}
