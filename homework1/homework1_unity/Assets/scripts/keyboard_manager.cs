using System;
using UnityEngine;
using UnityEngine.InputSystem;

public class keyboard_manager : MonoBehaviour {
    public bool is_enabled = true;
    // Update is called once per frame
    void Update() {
        var kb = Keyboard.current;

        bool decrement_mode = kb.leftArrowKey.isPressed;
        bool increment_mode = kb.rightArrowKey.isPressed;

        if (decrement_mode == increment_mode) {
            decrement_mode = false;
            increment_mode = false;
        }


        if (!is_enabled) {
            return;
        }

        if (kb.enterKey.wasPressedThisFrame) {
            on_enter_pressed();
            return;
        }
    }

    private void on_enter_pressed() {
        throw new NotImplementedException();
    }
}
