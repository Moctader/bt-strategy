import matplotlib.pyplot as plt
from frouros.detectors.concept_drift import DDM, DDMConfig
from frouros.metrics import PrequentialError
import pandas as pd

# Adjusted configuration parameters based on observed errors
config = DDMConfig(
    warning_level=1.00060,  # Set warning level close to typical error values
    drift_level=1.00076,    # Set drift level slightly higher than typical error values
    min_num_instances=1    # Minimum number of instances before checking for concept drift
)
detector = DDM(config=config)
metric = PrequentialError(alpha=1.0)

# Initialize lists to store drift-related data
errors = []
drift_points = []
warning_points = []

def stream_test(X_test, y_test, metric, detector):
    """Simulate data stream over X_test and y_test. Track concept drift and errors."""
    for i, (X, y) in enumerate(zip(X_test, y_test)):
        error = float(abs(X - y))  # Simple absolute error
        metric_error = metric(error_value=error)  # Update metric
        print(f"Error at step {i}: {metric_error:.6f}")
        
        # Store error for plotting
        errors.append(metric_error)
        
        # Update DDM and check for drift/warning status
        _ = detector.update(value=error)
        status = detector.status
        
        if status["drift"]:
            drift_points.append(i)
            print(f"Concept drift detected at step {i}. Accuracy: {1 - metric_error:.6f}")
        elif status["warning"]:
            warning_points.append(i)

    print(f"Final accuracy: {1 - metric_error:.4f}")

# Load test data
data = pd.read_csv('../models/results/predictions_vs_actual.csv')    
y_pred = data['y_pred']
y_test = data['y_test']

# Run the stream test
stream_test(y_pred, y_test, metric, detector)

print(warning_points)
# Visualization
plt.figure(figsize=(14, 10))

# Plot error rates
plt.subplot(2, 1, 1)
plt.plot(errors, label='Error Rate', color='blue')
#plt.axvline(x=500, color='red', linestyle='--', label='True Drift Point')
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
#plt.axvline(x=500, color='red', linestyle='--', label='True Drift Point')
plt.title('Accuracy Over Time')
plt.xlabel('Sample Index')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.show()