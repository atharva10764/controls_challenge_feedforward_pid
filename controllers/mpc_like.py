from . import BaseController
import numpy as np


class Controller(BaseController):
    """
    Simple MPC-like controller with gradient descent
    on a 1D lateral acceleration model.

    This is intentionally simple: it optimizes
    a sequence of steering commands U over a short horizon
    to track the future target lataccel and avoid huge changes in U.
    """

    def __init__(self):
        self.dt = 0.1
        self.N = 10            # horizon length
        self.tau = 0.25        # time constant for accel dynamics

        # cost weights
        self.w_err = 50.0      # tracking error weight
        self.w_jerk = 0.5      # smoothness / jerk penalty

        # steering limits
        self.u_min = -2.0
        self.u_max = 2.0

        self.u_prev = 0.0

    def reset(self):
        self.u_prev = 0.0

    def _predict_accel(self, a0, U):
        """
        Given initial accel a0 and control sequence U (len N),
        simulate accel over horizon.
        """
        a = a0
        accels = []
        for u in U:
            a = a + (self.dt / self.tau) * (u - a)
            accels.append(a)
        return np.array(accels)

    def update(self, target_lataccel, current_lataccel, state, future_plan):
        # build reference lataccel horizon from future_plan
        future = np.array(future_plan.lataccel, dtype=float)
        if len(future) >= self.N:
            ref = future[:self.N]
        else:
            # pad with last value
            ref = np.pad(future, (0, self.N - len(future)), mode="edge") if len(future) > 0 \
                  else np.full(self.N, float(target_lataccel))

        # initialize control sequence with previous u
        U = np.full(self.N, self.u_prev, dtype=float)

        lr = 0.05      # gradient descent step size
        iters = 30     # number of GD iterations

        for _ in range(iters):
            # predict accel over horizon
            pred = self._predict_accel(current_lataccel, U)

            # ----- cost gradients -----

            # 1) tracking error: w_err * (pred - ref)^2
            # approximate gradient w.r.t U by pushing error directly on U
            grad = 2.0 * self.w_err * (pred - ref)

            # 2) smoothness / jerk: w_jerk * sum (u_k - u_{k-1})^2
            # finite difference of U relative to last applied u
            dU = np.diff(np.concatenate(([self.u_prev], U)))   # length N
            # simple per-step gradient term: 2 * w_jerk * dU
            grad += 2.0 * self.w_jerk * dU

            # gradient descent update
            U -= lr * grad

            # clamp to steering limits
            U = np.clip(U, self.u_min, self.u_max)

        # apply first control in optimized sequence
        u0 = float(U[0])
        self.u_prev = u0
        return u0
