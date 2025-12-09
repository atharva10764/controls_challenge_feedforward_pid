<div align="center">
<h1>comma Controls Challenge v2</h1>


<h3>
  <a href="https://comma.ai/leaderboard">Leaderboard</a>
  <span> · </span>
  <a href="https://comma.ai/jobs">comma.ai/jobs</a>
  <span> · </span>
  <a href="https://discord.comma.ai">Discord</a>
  <span> · </span>Comma Controls Challenge Submission – Preview Feedforward PI + Adaptive Smoothing Controller

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
  <a href="https://x.com/comma_ai">X</a>
</h3>

</div>

Machine learning models can drive cars, paint beautiful pictures and write passable rap. But they famously suck at doing low level controls. Your goal is to write a good controller. This repo contains a model that simulates the lateral movement of a car, given steering commands. The goal is to drive this "car" well for a given desired trajectory.

## Getting Started
We'll be using a synthetic dataset based on the [comma-steering-control](https://github.com/commaai/comma-steering-control) dataset for this challenge. These are actual car and road states from [openpilot](https://github.com/commaai/openpilot) users.

```
# install required packages
# recommended python==3.11
pip install -r requirements.txt

# test this works
python tinyphysics.py --model_path ./models/tinyphysics.onnx --data_path ./data/00000.csv --debug --controller pid
```

There are some other scripts to help you get aggregate metrics:
```
# batch Metrics of a controller on lots of routes
python tinyphysics.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 100 --controller pid

# generate a report comparing two controllers
python eval.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 100 --test_controller pid --baseline_controller zero

```
You can also use the notebook at [`experiment.ipynb`](https://github.com/commaai/controls_challenge/blob/master/experiment.ipynb) for exploration.

## TinyPhysics
This is a "simulated car" that has been trained to mimic a very simple physics model (bicycle model) based simulator, given realistic driving noise. It is an autoregressive model similar to [ML Controls Sim](https://blog.comma.ai/096release/#ml-controls-sim) in architecture. Its inputs are the car velocity (`v_ego`), forward acceleration (`a_ego`), lateral acceleration due to road roll (`road_lataccel`), current car lateral acceleration (`current_lataccel`), and a steer input (`steer_action`), then it predicts the resultant lateral acceleration of the car.

## Controllers
Your controller should implement a new [controller](https://github.com/commaai/controls_challenge/tree/master/controllers). This controller can be passed as an arg to run in-loop in the simulator to autoregressively predict the car's response.

## Evaluation
Each rollout will result in 2 costs:
- `lataccel_cost`: $\dfrac{\Sigma(\mathrm{actual{\textunderscore}lat{\textunderscore}accel} - \mathrm{target{\textunderscore}lat{\textunderscore}accel})^2}{\text{steps}} * 100$
- `jerk_cost`: $\dfrac{(\Sigma( \mathrm{actual{\textunderscore}lat{\textunderscore}accel_t} - \mathrm{actual{\textunderscore}lat{\textunderscore}accel_{t-1}}) / \Delta \mathrm{t} )^{2}}{\text{steps} - 1} * 100$

It is important to minimize both costs. `total_cost`: $(\mathrm{lat{\textunderscore}accel{\textunderscore}cost} * 50) + \mathrm{jerk{\textunderscore}cost}$

## Submission
Run the following command, then submit `report.html` and your code to [this form](https://forms.gle/US88Hg7UR6bBuW3BA).

Competitive scores (`total_cost<100`) will be added to the leaderboard

```
python eval.py --model_path ./models/tinyphysics.onnx --data_path ./data --num_segs 5000 --test_controller <insert your controller name> --baseline_controller pid
```

## Changelog
- With [this commit](https://github.com/commaai/controls_challenge/commit/fdafbc64868b70d6ec9c305ab5b52ec501ea4e4f) we made the simulator more robust to outlier actions and changed the cost landscape to incentivize more aggressive and interesting solutions.
- With [this commit](https://github.com/commaai/controls_challenge/commit/4282a06183c10d2f593fc891b6bc7a0859264e88) we fixed a bug that caused the simulator model to be initialized wrong.

## Work at comma

Like this sort of stuff? You might want to work at comma!
[comma.ai/jobs](https://comma.ai/jobs)
