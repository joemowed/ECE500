using UnityEngine;
using UnityEngine.InputSystem;

public class keyboard_manager : MonoBehaviour {
    public bool is_enabled = true;
    [SerializeField] private sys sys;
    [SerializeField] private target_manager target_manager;
    [SerializeField] private beam_driver beam_driver;
    [SerializeField] private ball_driver ball_driver;
    [SerializeField] private pid_controller pid_controller;
    [SerializeField] private float target_move_speed, beam_rotate_speed, ball_move_speed;
    private Keyboard kb;

    void Awake() {
        //null checks 
        if (target_manager == null) {
            Debug.LogError("No indicator_driver set for keyboard.", this);
        }
        if (beam_driver == null) {
            Debug.LogError("No beam_driver set for keyboard.", this);
        }
        if (ball_driver == null) {
            Debug.LogError("No ball_driver set for keyboard.", this);
        }
        if (target_move_speed <= 0) {
            Debug.LogError("target_move_speed invalid or not assigned for keyboard.", this);
        }
        if (beam_rotate_speed <= 0) {
            Debug.LogError("beam_rotate_speed invalid or not assigned for keyboard.", this);
        }
        if (ball_move_speed <= 0) {
            Debug.LogError("ball_move_speed invalid or not assigned for keyboard.", this);
        }
    }


    // Update is called once per frame
    void Update() {
        kb = Keyboard.current;

        bool decrement_mode = kb.leftArrowKey.isPressed;
        bool increment_mode = kb.rightArrowKey.isPressed;
        float direction_mult = 0;

        if (decrement_mode == increment_mode) {
            direction_mult = 0;
        } else {
            direction_mult = (decrement_mode) ? -1f : direction_mult;
            direction_mult = (increment_mode) ? 1f : direction_mult;
        }

        if (direction_mult != 0) {
            sys.is_controller_paused = true;
            handle_arrow_pressed(direction_mult);

        } else {
            sys.is_controller_paused = false;
        }

        if (!is_enabled) {
            return;
        }

        if (kb.enterKey.wasPressedThisFrame) {
            on_enter_pressed();
            return;
        }
        if (kb.altKey.wasPressedThisFrame) {
            toggleMode();
        }


    }
    private void toggleMode() {
        sys.is_pid_mode = !sys.is_pid_mode;
    }
    private void on_enter_pressed() {
        sys.random_reset();
    }
    private void handle_arrow_pressed(float direction_mult) {
        if (kb.ctrlKey.isPressed) {
            rotate_beam(direction_mult);
            return;
        }
        if (kb.shiftKey.isPressed) {
            move_ball(direction_mult);
            return;
        }
        move_target(direction_mult);

    }
    private void rotate_beam(float direction_mult) {

        float new_angle = beam_driver.target_angle;
        new_angle += direction_mult * beam_rotate_speed * Time.deltaTime;
        new_angle = Mathf.Clamp(new_angle, 0, 1);
        beam_driver.set_angle(new_angle);
    }
    private void move_ball(float direction_mult) {
        var impulse = direction_mult * ball_move_speed * Time.deltaTime;
        ball_driver.push(impulse);
    }
    private void move_target(float direction_mult) {
        var new_pos = target_manager.get_target();
        new_pos += direction_mult * target_move_speed * Time.deltaTime;
        new_pos = Mathf.Clamp(new_pos, 0, 1);
        target_manager.set_target(new_pos);
    }
}
