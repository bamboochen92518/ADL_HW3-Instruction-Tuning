import matplotlib.pyplot as plt

# Step 3: Create Data
x = [16, 32, 48, 64, 79]
y = [1.5086, 1.251, 1.2049, 1.1793, 1.2664]
plt.xlabel('training step')
plt.ylabel('loss')

# Step 4: Plot the Data
plt.plot(x, y)
plt.xticks(x)
plt.scatter(x, y, color='red', marker='o', label='Data Points')

# Step 5: Show the Chart
plt.show()

