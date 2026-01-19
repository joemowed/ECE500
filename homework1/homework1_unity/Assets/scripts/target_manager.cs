using System;
using UnityEngine;

public class target_manager : MonoBehaviour
{
    public indicator_driver id;
    public float target = 0.5f;


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        if (id == null)
        {
            Debug.LogError("No reference to indicator_dirver loaded.", this);
        }
    }

    // Update is called once per frame
    void Update()
    {
        id.set_pos(target);
    }
}
