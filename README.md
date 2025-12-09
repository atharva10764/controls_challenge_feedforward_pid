Comma Controls Challenge Submission – Preview Feedforward PI + Adaptive Smoothing Controller

This repository contains my controller submission for the comma.ai Controls Challenge.
I designed a Preview Feedforward PI controller with Adaptive Smoothing, which achieves significantly lower total cost compared to the baseline PID controller used in the starter code.

🚗 Controller Summary

The controller combines feedforward prediction, PI feedback, and adaptive smoothing to minimize lateral acceleration error and steering jerk.

1. Feedforward (Preview) Term

Uses the first element of the future lateral acceleration plan:

u_ff = k_ff * future_plan.lataccel[0]


This anticipates upcoming curvature and reduces lag.

2. PI Feedback Term
error = target_lataccel - current_lataccel
u_fb = k_p * error + k_i * ∑ error


This corrects tracking drift and improves stability.

3. Adaptive Command Smoothing

To reduce jerk while remaining responsive, we use a dynamic smoothing factor:

u_smooth(k) = α * u_raw(k) + (1 − α) * u_prev(k)


If the controller needs a large correction → increase responsiveness

If the correction is small → increase smoothing (reduces jerk)

This adaptivity is crucial for reducing total cost.

📊 Performance (5000 SYNTHETIC Segments)
Metric	Baseline PID	My Controller
lataccel_cost	~1.71	1.35
jerk_cost	~25.6	23.55
total_cost	~111	90.89

➡️ ~20% improvement over PID baseline

📁 Repository Structure
controllers/
  ├── pid.py
  ├── preview_pi_smooth.py   ← My controller
models/
  └── tinyphysics.onnx
tinyphysics.py
eval_report.txt              ← Included evaluation results

▶️ Reproducing My Results

Use the following command:

python tinyphysics.py \
  --model_path ./models/tinyphysics.onnx \
  --data_path ./data \
  --num_segs 5000 \
  --controller preview_pi_smooth


This runs the evaluation on the full dataset and prints:

lataccel_cost

jerk_cost

total_cost

A histogram visualization is also shown at the end.

🧠 Why This Controller Works Well

Feedforward term handles anticipated curvature

PI term fixes residual tracking errors

Adaptive smoothing balances jerk reduction with responsiveness

Stable across many synthetic test segments

Extremely simple and computationally cheap

This simplicity + performance makes it a strong submission for the challenge.

📬 Submission Details

Controller name: preview_pi_smooth

Key strengths: low jerk, responsive at high curvature, robust on long rollouts

Eval report: see eval_report.txt

Command used: (same as above)

🙌 Acknowledgments

Thanks to comma.ai for the challenge and public dataset.
This submission is open for review, experimentation, and improvement.

