using Unity.VisualScripting;
using UnityEngine;

public class beam_driver : MonoBehaviour {
    public float target_angle = 0.5f;
    //max_angle is symmetric for both sides
    public const float max_angle = 89;
    private ArticulationReducedSpace reset_position;
    private ArticulationDrive reset_drive;


    private ArticulationBody ab;
    void Awake() {
        ab = GetComponent<ArticulationBody>();
    }

    void Start() {

        reset_position = ab.jointPosition;

        var drive = ab.xDrive;
        drive.driveType = ArticulationDriveType.Force;
        drive.damping = 1E2f;
        drive.stiffness = 1E3f;
        drive.forceLimit = 1E2f;
        drive.target = 0f;
        drive.lowerLimit = -max_angle;
        drive.upperLimit = max_angle;
        ab.xDrive = drive;
        reset_drive = drive;
    }
    void FixedUpdate() {
        update_angle(target_angle);
    }
    private void update_angle(float angle) {
        angle -= 0.5f;
        angle *= 2f;
        angle *= -1f;
        angle *= max_angle;
        var drive = ab.xDrive;
        drive.target = angle;
        ab.xDrive = drive;
    }
    // "angle" is a float with range 0-1, 0 being the maximum left angle and 1 being the maximum right angle
    public void set_angle(float angle) {
        if (angle > 1 || angle < 0) {
            Debug.LogError($"Target beam angle exceeds allowed range (allowed range 0-1).  Target Angle:{angle}");
            angle = Mathf.Clamp(angle, 0, 1);
        }
        target_angle = angle;
    }
    public void reset_beam() {
        set_angle(0.5f);
        ab.xDrive = reset_drive;
        ab.jointPosition = reset_position;
    }
    public float get_angle() {
        float angle_deg = ab.jointPosition[0] * Mathf.Rad2Deg;
        angle_deg += max_angle; //make angle positive in range 0-2*max_angle
        return angle_deg / (2 * max_angle);
    }


    //gets the global position of the beam
    public Vector3 get_pos() => transform.position;


}
