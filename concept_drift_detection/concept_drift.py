import matplotlib.pyplot as plt
from frouros.detectors.concept_drift import DDM, DDMConfig
from frouros.metrics import PrequentialError
import pandas as pd

config = DDMConfig(
    warning_level=0.000001,
    drift_level=0.000002,
    min_num_instances=1 
)
detector = DDM(config=config)
metric = PrequentialError(alpha=1.0)

def stream_test(y_pred, y_test, metric, detector):
    """Simulate data stream over y_pred and y_test and detect concept drift."""
    drift_points = []
    warning_points = []
    cumulative_error = 0
    errors = []

    for i, (pred, actual) in enumerate(zip(y_pred, y_test)):
        # Calculate error
        error = float(abs(pred - actual))
        errors.append(error)

        # Update the detector with the error
        detector.update(error)
        cumulative_error += error

        # Check for drift and warning
        status = detector.status
        if status["drift"]:
            drift_points.append(i)
            accuracy = 1 - (cumulative_error / (i + 1))
            print(f"Concept drift detected at step {i}. Accuracy: {accuracy:.6f}")
        elif status["warning"]:
            warning_points.append(i)
            accuracy = 1 - (cumulative_error / (i + 1))
            print(f"Warning detected at step {i}. Accuracy: {accuracy:.4f}")

    # Final accuracy
    final_accuracy = 1 - (cumulative_error / len(y_pred))
    print(f"Final accuracy: {final_accuracy:.4f}\n")
    
    return drift_points, warning_points, errors


# 4. Load test data
data = pd.read_csv('../models/results/predictions_vs_actual.csv')    
y_pred = data['y_pred']
y_test = data['y_test']

# 5. Run stream test
drift_points, warning_points, errors = stream_test(y_pred, y_test, metric, detector)

# 6. Visualize results
plt.figure(figsize=(12, 6))

# Plot error rates
plt.subplot(2, 1, 1)
plt.plot(errors, label='Error Rate', color='blue')
plt.axvline(x=500, color='red', linestyle='--', label='True Drift Point')
plt.title('Error Rates Over Time')
plt.xlabel('Sample Index')
plt.ylabel('Error Rate')
plt.legend()

# Plot detected drifts and warnings
plt.subplot(2, 1, 2)
plt.plot(range(len(errors)), [1 - (sum(errors[:i + 1]) / (i + 1)) for i in range(len(errors))], label='Accuracy', color='green')
plt.scatter(drift_points, [1 - (sum(errors[:i + 1]) / (i + 1)) for i in drift_points], color='red', label='Detected Drifts')
plt.scatter(warning_points, [1 - (sum(errors[:i + 1]) / (i + 1)) for i in warning_points], color='orange', label='Warning Points')
plt.axvline(x=500, color='red', linestyle='--', label='True Drift Point')
plt.title('Accuracy Over Time')
plt.xlabel('Sample Index')
plt.ylabel('Accuracy')
plt.legend()





plt.tight_layout()
plt.show()