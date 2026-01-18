using UnityEngine;

public class indicator_driver : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
    }
    //  Sets the indicator to the position given. "pos" is a float, with 0 representing
    //  the left end and 1 representing the right end of the beam
    public void set_pos(float pos)
    {
        //translate the position to a coordinate relative to the beam
        pos -= 0.5f;
        var new_pos = transform.localPosition;
        new_pos.x = pos;
        transform.localPosition = new_pos;
    }
}
