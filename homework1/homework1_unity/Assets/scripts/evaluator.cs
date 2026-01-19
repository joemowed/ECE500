using UnityEngine;

public class evaluator : MonoBehaviour {
    public target_manager tm;
    public ball_driver bd;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() {

    }

    // Update is called once per frame
    void Update() {

    }
    public float dist_from_target() {
        //return Mathf.Abs(tm.get_target() - bd.get_pos());
        return 0;
    }
}
