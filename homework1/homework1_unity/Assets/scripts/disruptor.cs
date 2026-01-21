using UnityEngine;

public class disruptor : MonoBehaviour {
    public sys sys;
    private const float interval_max_time = 20f;
    private const float interval_min_time = 1f;
    private float elapsed_time = 0f;
    private float curr_interval = 0f;
    public bool is_enabled = true;
    void FixedUpdate() {
        if (!is_enabled) {
            return;
        }

        elapsed_time += Time.fixedDeltaTime;


        if (elapsed_time >= curr_interval) {
            curr_interval = Random.Range(interval_min_time, interval_max_time);
            elapsed_time = 0;
            sys.reset_target();
        }


    }

}
