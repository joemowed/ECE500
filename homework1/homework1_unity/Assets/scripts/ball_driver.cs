using System;
using UnityEngine;
using UnityEngine.SocialPlatforms;

public class ball_driver : MonoBehaviour {
    private Rigidbody rb;
    private Vector3 impulse;
    public GameObject beam;

    void Start() {
        rb = GetComponent<Rigidbody>();
    }
    void FixedUpdate() {
        if (impulse != Vector3.zero) {
            rb.AddForce(impulse, ForceMode.Impulse);
            impulse = Vector3.zero;
        }
    }
    public float get_pos() {
        // Convert ball position to cube local space
        Vector3 localPos = beam.transform.InverseTransformPoint(transform.position);
        return localPos.x + 0.5f;
    }

    public void set_pos(Vector3 pos) {
        transform.localPosition = pos;
    }
    public void push(float impulse) {
        Vector3 imp = new Vector3(0, 0, 0);
        imp.x += impulse;
        this.impulse = imp;
    }

    public float get_speed() {
        Debug.Log(rb.linearVelocity.x);
        return rb.linearVelocity.x;
    }
}
