using UnityEngine;

public class main : MonoBehaviour {
    public bar_ui bar_ui;
    public evaluator eval;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() {

    }

    // Update is called once per frame
    void Update() {
        bar_ui.set_value(eval.dist_from_target());

    }
}
