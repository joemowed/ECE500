import numpy as np
import tensorflow as tf

# 1. Define the model
model = tf.keras.Sequential(
    [
        # Input layer matches the 6 fields in outbound_packet
        tf.keras.layers.Input(shape=(6,)),
        # Hidden layers (you can adjust neurons for more 'intelligence')
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        # Output layer: 2 neurons (beam_angle and reset_system)
        tf.keras.layers.Dense(2),
    ]
)

model.compile(optimizer="adam", loss="mse")

model.summary()


def dict_to_array(out_pkt):
    # Order: ball_pos, ball_velocity, target_pos, target_dist, stable_time, is_stable
    return np.array(
        [
            [
                out_pkt["ball_pos"],
                out_pkt["ball_velocity"],
                out_pkt["target_pos"],
                out_pkt["target_distance_percent"],
                out_pkt["stable_time_percent"],
                float(out_pkt["is_stable"]),  # Convert bool to 1.0 or 0.0
            ]
        ],
        dtype=np.float32,
    )


def array_to_dict(prediction):
    # Extract values from the model's output array
    return {
        "beam_angle": float(prediction[0][0]),
        "reset_system": bool(prediction[0][1] > 0.5),  # Thresholding for the bool
    }
