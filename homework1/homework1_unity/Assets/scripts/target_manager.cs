using System;
using UnityEngine;

public class target_manager : MonoBehaviour {
    public indicator_driver id;
    private float target = 0.5f;
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start() {
        if (id == null) {

            Debug.LogError("No reference to indicator_dirver loaded.", this);
        }
    }

    // Update is called once per frame
    void Update() {
        id.set_pos(target);
    }
    public void set_target(float value) {
        if (value < 0 || value > 1) {
            Debug.LogError($"Attempt to set target to out of range value. (allowed range is 0-1) Value:{value}", this);
            Mathf.Clamp(value, 0, 1);
        }
        target = value;
    }
    public float get_target() => target;
}
