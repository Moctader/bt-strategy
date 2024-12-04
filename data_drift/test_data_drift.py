import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate two datasets
# Dataset 1 (Train) - Normal distribution
train_data = np.random.normal(loc=0, scale=1, size=1000)

# Dataset 2 (Test - Same distribution) - Normal distribution
test_data_same = np.random.normal(loc=0, scale=1, size=700)

# Dataset 3 (Test - Different distribution) - Uniform distribution
test_data_different = np.random.uniform(low=-3, high=3, size=700)

# Function to compute and plot CDF
def plot_cdf(data, label):
    sorted_data = np.sort(data)
    cdf_y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    plt.step(sorted_data, cdf_y, where="post", label=label)

# Step 2: Plot the CDFs
plt.figure(figsize=(12, 6))

# Plot Train data CDF
plot_cdf(train_data, "Train Data (Normal)")

# Plot Test data CDF (same distribution)
plot_cdf(test_data_same, "Test Data (Same Distribution - Normal)")

# Plot Test data CDF (different distribution)
plot_cdf(test_data_different, "Test Data (Different Distribution - Uniform)")

# Customize plot
plt.title("Comparison of CDFs for Different Datasets")
plt.xlabel("Data values")
plt.ylabel("CDF")
plt.grid(True)
plt.legend()
plt.show()
