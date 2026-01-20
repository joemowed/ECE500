using System;
using UnityEngine;
using UnityEngine.SocialPlatforms;

public class ball_driver : MonoBehaviour {
    private Rigidbody rb;
    private Vector3 impulse;
    public const float end_distance = 0.15f; //how close you can get to the ends of beam when using set_pos().  (0 is on end of beam)
    public GameObject beam;
    private Vector3 local_reset_position;
    public bool is_falling { get; private set; }


    void Start() {
        rb = GetComponent<Rigidbody>();
        local_reset_position = beam.transform.InverseTransformPoint(transform.position);
    }
    void FixedUpdate() {
        if (impulse != Vector3.zero) {
            rb.AddForce(impulse, ForceMode.Impulse);
            impulse = Vector3.zero;
        }
        if (transform.position.y < 0) {
            is_falling = true;
        }
    }
    public float get_pos() {
        // Convert ball position to cube local space
        Vector3 localPos = beam.transform.InverseTransformPoint(transform.position);
        return localPos.x + 0.5f;
    }

    public void set_pos(float position) {
        if (position < end_distance || position > 1 - end_distance) {
            Debug.LogError($"Attempt to set ball outside allowed range. Value: {position} \n(allowed range is {end_distance}-{1 - end_distance})");
            position = Mathf.Clamp(position, end_distance, 1 - end_distance);
        }
        var pos_vector = local_reset_position;
        pos_vector.x = position - 0.5f;
        transform.position = beam.transform.TransformPoint(pos_vector);
    }
    public void push(float impulse) {
        Vector3 imp = new Vector3(0, 0, 0);
        imp.x += impulse;
        this.impulse = imp;
    }

    public float get_speed() {
        return rb.linearVelocity.x;
    }
    public void reset_velocity() {
        rb.angularVelocity = Vector3.zero;
        rb.linearVelocity = Vector3.zero;
    }
}
