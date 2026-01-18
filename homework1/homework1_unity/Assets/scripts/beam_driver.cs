using UnityEngine;

public class beam_driver : MonoBehaviour
{
    public float targetAngleDegrees = 0f;

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
        drive.lowerLimit = -89f;
        drive.upperLimit = 89f;
        ab.xDrive = drive;
    }
    void FixedUpdate()
    {
        set_angle(targetAngleDegrees);
    }

    public void set_angle(float angleDeg)
    {
        var drive = ab.xDrive;
        drive.target = angleDeg;
        ab.xDrive = drive;
    }

    public float get_angle()
    {
        return ab.jointPosition[0] * Mathf.Rad2Deg;
    }

    //gets the global position of the beam
    public Vector3 get_pos()
    {
        return transform.position;
    }


}
