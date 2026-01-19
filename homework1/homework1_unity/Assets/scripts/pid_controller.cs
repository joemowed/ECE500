using UnityEngine;

public class pid_controller : MonoBehaviour {
    [Header("References")]
    public ball_driver ball_driver;
    public beam_driver beam_driver;
    public evaluator eval;
    public target_manager tm;

    private float targetPosition; // local X position on beam

    [Header("PID Gains")]
    public float Kp = 15f;
    public float Ki = 0.5f;
    public float Kd = 5f;

    [Header("Limits")]
    public float maxAngle = 15f; // degrees

    private float integral;
    private float lastError;

    void FixedUpdate() {
        targetPosition = tm.get_target();
        // Ball position in beam local space
        float ballPos = ball_driver.get_pos();

        // PID error
        float error = targetPosition - ballPos;

        // Integral term
        integral += error * Time.fixedDeltaTime;

        // Derivative term
        float derivative = (error - lastError) / Time.fixedDeltaTime;
        lastError = error;

        // PID output
        float output = (Kp * error) + (Ki * integral) + (Kd * derivative);

        // Clamp output to beam angle limits
        output = Mathf.Clamp(output, -maxAngle, maxAngle);

        // Apply rotation (around Z for left/right tilt)
        beam_driver.set_angle(output);
    }

}
