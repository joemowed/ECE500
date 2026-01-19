using TMPro;
using UnityEngine;

public class sys : MonoBehaviour {
    public bar_ui distance_bar;
    public bar_ui target_eval_bar;
    public evaluator eval;
    public pid_controller pid_controller;
    public Color target_bar_stable_color;
    public Color target_bar_unstable_color;
    public bool is_pid_mode = true;
    public TMP_Text mode_indicator_text;
    public beam_driver beam_driver;
    public ball_driver ball_driver;
    public target_manager target_manager;
    public bool is_controller_paused = false;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() {

    }

    // Update is called once per frame
    void Update() {
        pid_controller.paused = is_controller_paused;
        update_dist_bar();
        update_target_bar();
        update_mode_indicator();
    }
    private void update_dist_bar() {

        distance_bar.set_value(eval.dist_from_target());
    }
    public void random_reset() {
        float end_distance = ball_driver.end_distance;
        beam_driver.reset_beam();
        ball_driver.reset_velocity();
        ball_driver.set_pos(Random.Range(end_distance, 1 - end_distance));
        target_manager.set_target(Random.Range(end_distance, 1 - end_distance));
    }
    private void update_mode_indicator() {
        if (is_pid_mode) {
            mode_indicator_text.text = "PID Mode";
        } else {

            mode_indicator_text.text = "NN Mode";
        }
    }
    private void update_target_bar() {
        target_eval_bar.set_value(eval.stable_time_percent());
        if (eval.is_stable) {
            target_eval_bar.set_foreground_color(target_bar_stable_color);
        } else {

            target_eval_bar.set_foreground_color(target_bar_unstable_color);
        }
    }
}
