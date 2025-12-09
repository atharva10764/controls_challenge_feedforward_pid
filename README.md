# comma.ai Controls Challenge – Feedforward PID Controller

This repository contains my solution to the comma.ai Controls Challenge.  
I started from the provided PID controller and ended up with a **feedforward + PID + smoothing** controller that significantly improves the TinyPhysics benchmark cost.

---

## Controller: `preview_pi_ff`

**File:** `controllers/preview_pi_smooth.py`

The final controller combines three ideas:

1. **Baseline PID feedback**  
   I reuse comma’s provided `pid` controller as a stabilizing feedback term that reacts to lateral acceleration tracking error.

2. **Feedforward from previewed lateral acceleration**  
   Using `future_plan.lataccel` (a ~5 second preview of the desired lateral acceleration), I compute a simple feedforward steering term:
   - Take the mean of the first ~1 second of `future_plan.lataccel`
   - Multiply by a gain `k_ff = 0.15`
   - Add this to the PID output

   This reduces lag between the desired and actual lateral acceleration, especially in curves, since the controller no longer waits for error to appear before acting.

3. **Light smoothing of the combined command**  
   I apply an exponential smoothing filter to the combined feedforward + PID steering command with `alpha = 0.9`:

    $$u_\text{smooth}(k) = \alpha \, u_\text{raw}(k) + (1 - \alpha) \, u_\text{prev}(k)$$

   This slightly reduces steering jerk without degrading tracking.

The final tuned parameters are:

- `k_ff = 0.15`
- `alpha = 0.9`
- `steer_range = [-2, 2]` (matching `tinyphysics.py`)

---

## How to run

From the repo root:

```bash
# Baseline PID on TinyPhysics
python tinyphysics.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 5000 --controller pid

# My controller
python tinyphysics.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 5000 --controller preview_pi_smooth

# Comparison report (HTML) between PID and my controller
python eval.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 5000 --test_controller preview_pi_smooth --baseline_controller pid
