using Unity.VisualScripting;
using UnityEngine;

public class beam_driver : MonoBehaviour
{
    public float target_angle = 0.5f;
    //max_angle is symmetric for both sides
    public const float max_angle = 89;

    private ArticulationBody ab;
    void Awake()
    {
        ab = GetComponent<ArticulationBody>();
    }

    void Start()
    {

        var drive = ab.xDrive;
        drive.driveType = ArticulationDriveType.Force;
        drive.damping = 1E5f;
        drive.stiffness = 1E6f;
        drive.forceLimit = 1E5f;
        drive.target = 0;
        drive.lowerLimit = -max_angle;
        drive.upperLimit = max_angle;
        ab.xDrive = drive;
    }
    void FixedUpdate()
    {
        set_angle(target_angle);
    }
    // "angle" is a float with range 0-1, 0 being the maximum left angle and 1 being the maximum right angle
    public void set_angle(float angle)
    {
        if (angle > 1 || angle < 0)
        {
            Debug.LogError($"Target beam angle exceeds allowed range (allowed range 0-1).  Target Angle:{angle}");
        }
        angle -= 0.5f;
        angle *= 2f;
        angle *= -1f;
        angle *= max_angle;
        var drive = ab.xDrive;
        drive.target = angle;
        ab.xDrive = drive;
    }

    public float get_angle()
    {
        float angle_deg = ab.jointPosition[0] * Mathf.Rad2Deg;
        angle_deg += max_angle; //make angle positive in range 0-2*max_angle
        return angle_deg / (2 * max_angle);
    }

    //gets the global position of the beam
    public Vector3 get_pos()
    {
        return transform.position;
    }


}
