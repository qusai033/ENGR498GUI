# Plot Time vs. FD
plt.figure(figsize=(10, 6))
plt.plot(data['Time (s)'], data['Feature Data (FD)'], label='Feature Data (FD)', color='blue', linewidth=2)

# Add labels and title
plt.xlabel('Time (s)', fontsize=14)
plt.ylabel('Feature Data (FD)', fontsize=14)
plt.title('Time vs. Feature Data (FD)', fontsize=16)

# Add a grid and legend
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)

# Show the plot
plt.show()
