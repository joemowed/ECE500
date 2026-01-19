using UnityEngine;

public class indicator_driver : MonoBehaviour {
    private const float speed = 10f;
    private Vector3 target_pos;
    //  Sets the indicator to the position given. "pos" is a float, with 0 representing
    //  the left end and 1 representing the right end of the beam
    public void set_pos(float pos) {
        //translate the position to a coordinate relative to the beam
        pos -= 0.5f;
        var new_pos = transform.localPosition;
        new_pos.x = pos;
        target_pos = new_pos;
    }
    void Update() {
        transform.localPosition = Vector3.Lerp(transform.localPosition, target_pos, Time.deltaTime * speed);
    }
}
