import matplotlib.pyplot as plt
from frouros.detectors.concept_drift import DDM, DDMConfig
from frouros.metrics import PrequentialError
import numpy as np

# Configuration for DDM
config = DDMConfig(
    warning_level=0.8,   # Slightly above expected error rates
    drift_level=1.1,     # Slightly above the warning threshold
    min_num_instances=10    # Minimum number of samples before detection starts
)
detector = DDM(config=config)
metric = PrequentialError(alpha=1.0)

# Initialize tracking lists
errors = []
drift_points = []
warning_points = []

# Generate dummy data
np.random.seed(42)  
n_samples = 1000

# Phase 1: Low error (normal behavior)
y_test_phase1 = np.random.randint(0, 2, size=500)
y_pred_phase1 = y_test_phase1 + np.random.normal(0, 0.1, size=500)

# Phase 2: High error (concept drift)
y_test_phase2 = np.random.randint(0, 2, size=500)
y_pred_phase2 = y_test_phase2 + np.random.normal(0, 1.0, size=500)

# Combine phases to simulate drift
y_test = np.concatenate([y_test_phase1, y_test_phase2])
y_pred = np.concatenate([y_pred_phase1, y_pred_phase2])

# Stream simulation
def stream_test(X_test, y_test, metric, detector):
    for i, (X, y) in enumerate(zip(X_test, y_test)):
        error = abs(X - y)  # Calculate absolute error
        metric_error = metric(error_value=error)
        errors.append(metric_error) 
        
        # Update detector with the current error
        detector.update(value=error)
        status = detector.status
        
        # Check drift and warning status
        if status["drift"]:
            drift_points.append(i)
        elif status["warning"]:
            warning_points.append(i)


# Run the test
stream_test(y_pred, y_test, metric, detector)

# Plot results
plt.figure(figsize=(14, 10))

# Plot error rates
plt.subplot(2, 1, 1)
plt.plot(errors, label='Error Rate', color='blue')
plt.title('Error Rates Over Time')
plt.xlabel('Sample Index')
plt.ylabel('Error Rate')
plt.legend()

# Plot detected drifts and warnings
plt.subplot(2, 1, 2)
accuracy = [1 - (sum(errors[:i + 1]) / (i + 1)) for i in range(len(errors))]
plt.plot(accuracy, label='Accuracy', color='green')
plt.scatter(drift_points, [accuracy[i] for i in drift_points], color='red', label='Detected Drifts')
plt.scatter(warning_points, [accuracy[i] for i in warning_points], color='orange', label='Warning Points')
plt.title('Accuracy Over Time')
plt.xlabel('Sample Index')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()
