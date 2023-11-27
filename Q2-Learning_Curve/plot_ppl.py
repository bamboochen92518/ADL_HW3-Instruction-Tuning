import matplotlib.pyplot as plt

# Step 3: Create Data
x = [16, 32, 48, 64, 79]
y = [4.16314, 3.82961, 3.74060, 3.64477, 3.63617]
plt.xlabel('training step')
plt.ylabel('ppl')

# Step 4: Plot the Data
plt.plot(x, y)
plt.xticks(x)
plt.scatter(x, y, color='red', marker='o', label='Data Points')

# Step 5: Show the Chart
plt.show()

