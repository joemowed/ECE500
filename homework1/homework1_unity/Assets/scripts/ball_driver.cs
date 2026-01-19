using UnityEngine;

public class ball_driver : MonoBehaviour {
    private Rigidbody rb;
    private Vector3 impulse;

    void Start() {
        rb = GetComponent<Rigidbody>();
    }
    void FixedUpdate() {
        if (impulse != Vector3.zero) {
            rb.AddForce(impulse, ForceMode.Impulse);
            impulse = Vector3.zero;
        }
    }
    //gets the global position of the ball
    public Vector3 get_pos() => transform.localPosition;

    public void set_pos(Vector3 pos) {
        transform.localPosition = pos;
    }
    public void push(float impulse) {
        Vector3 imp = new Vector3(0, 0, 0);
        imp.x += impulse;
        this.impulse = imp;
    }
}
