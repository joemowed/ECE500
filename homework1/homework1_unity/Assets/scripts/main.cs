using UnityEngine;

public class main : MonoBehaviour {
    public bar_ui distance_bar;
    public bar_ui target_eval_bar;
    public evaluator eval;
    public Color target_bar_stable_color;
    public Color target_bar_unstable_color;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() {

    }

    // Update is called once per frame
    void Update() {
        update_dist_bar();
        update_target_bar();

    }
    private void update_dist_bar() {

        distance_bar.set_value(eval.dist_from_target());
    }
    private void update_target_bar() {
        target_eval_bar.set_value(eval.target_time_percent());
        if (eval.is_stable) {
            target_eval_bar.set_foreground_color(target_bar_stable_color);
        } else {

            target_eval_bar.set_foreground_color(target_bar_unstable_color);
        }
    }
}
