# comma.ai Controls Challenge – Feedforward + PID + Adaptive Smoothing Controller

This repository contains my submission for the comma.ai Controls Challenge.  
I began with the baseline PID controller provided in the starter code and developed a **Feedforward + PID + Adaptive Smoothing** controller that significantly improves the TinyPhysics benchmark cost while remaining simple, interpretable, and robust.

---

## 🚘 Controller: `preview_pi_smooth`

**File:** `controllers/preview_pi_smooth.py`

The controller blends **future-preview feedforward**, **PID stabilization**, and **smoothing** to minimize lateral acceleration error and jerk.

---

# 🧩 How the Controller Works

## 1. Baseline PID Feedback  
I reuse the provided `pid` controller to correct residual error between the target and simulated lateral acceleration:

u_ff = k_ff * mean(future_plan.lataccel[:10])
u_raw = u_pid + u_ff


This significantly reduces phase lag and improves tracking on curves.

---

## 3. Adaptive Exponential Smoothing (Jerk Reduction)

To keep the steering command smooth:
$$
u_\text{smooth}(k)
= \alpha \, u_\text{raw}(k)
+ (1 - \alpha) \, u_\text{prev}(k)
$$

Where:

- `alpha = 0.9`
- Steering is clipped to the allowed range `[-2, 2]`

This reduces jerk while maintaining responsiveness to sharp curvature.

---

# 🛠️ Final Tuned Hyperparameters

| Parameter | Value |
|----------|--------|
| Feedforward gain (`k_ff`) | **0.15** |
| Smoothing factor (`alpha`) | **0.9** |
| Steering limits | **[-2, 2]** |

---

# 📈 Performance (5000 TinyPhysics Segments)

Evaluated using the official `eval.py`:

| Metric | Baseline PID | My Controller |
|--------|--------------|----------------|
| **lataccel_cost** | ~1.71 | **1.35 – 1.55** |
| **jerk_cost** | ~25.6 | **~23.5** |
| **total_cost** | ~111 | **≈ 90 – 101** |

Best observed result:

lataccel_cost ≈ 1.347
jerk_cost ≈ 23.55
total_cost ≈ 90.89


This is up to **20% better** than the baseline PID and is *leaderboard-eligible* (`total_cost < 100`).

---

# ▶️ How to Run

From the repository root:

### Baseline PID
```bash
python tinyphysics.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 5000 --controller pid
```
### My Controller
```bash
python tinyphysics.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 5000 --controller preview_pi_smooth
```

### Generate HTML Comparison Report
```bash
python eval.py \
  --model_path ./models/tinyphysics.onnx \
  --data_path ./data \
  --num_segs 5000 \
  --test_controller preview_pi_smooth \
  --baseline_controller pid
```

controls_challenge/
│
├── controllers/
│     ├── pid.py
│     └── preview_pi_smooth.py     ← my submission controller
│
├── models/
│     └── tinyphysics.onnx
│
├── data/
│     └── *.csv (synthetic dataset)
│
├── tinyphysics.py
├── eval.py
└── README.md

🙌 Acknowledgments

Thanks to comma.ai for releasing TinyPhysics, supporting open research, and hosting this challenge.
This controller is intentionally simple, interpretable, and a strong baseline for future extensions such as MPC or RL.


---

If you want, I can also:

⭐ Add badges (Python version, challenge version, score badge)  
📊 Add performance plots directly into the README  
🏆 Rewrite it in a more “research-paper” style  
📁 Create a professional PDF version for your portfolio  

Just tell me!

