The issue seems to be related to how the chart canvas dimensions are recalculated during resizing, particularly when reducing the size of the window. Chart.js may not be updating properly due to how resizing is handled or how parent container dimensions are propagated to the charts.

Here's a refined approach to resolve the problem:

---

### Adjust Chart.js Resizing Logic

1. **Ensure Parent Container Adjusts Dynamically:**
   Update the parent container's CSS to always reflect the resized dimensions.

2. **Force Chart Resize on Window Resizing:**
   Explicitly trigger a `resize()` for all charts when the window size changes.

---

### Updated JavaScript Logic
Modify the `adjustCharts` function to handle resizing dynamically for each chart:

```javascript
function adjustCharts() {
    const charts = [voltageChart, rulChart, sohChart, fdChart];
    charts.forEach(chart => {
        if (chart) {
            chart.resize(); // Force resize
        }
    });
}

// Attach resize event listener
window.addEventListener('resize', () => {
    adjustCharts();
});
```

---

### Chart.js Configuration
Ensure `responsive: true` and use `maintainAspectRatio: true` (default behavior):

```javascript
const commonOptions = {
    responsive: true,
    maintainAspectRatio: true, // Keep default behavior
    scales: {
        x: { title: { display: true, text: 'Time [AU]' } },
        y: { title: { display: true, text: 'Value' } }
    },
    plugins: {
        legend: { display: true, position: 'top' },
        zoom: {
            pan: { enabled: true, mode: 'xy' },
            zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'xy' }
        }
    }
};
```

---

### CSS Adjustments
Ensure `.graph` and `.graphs-grid` containers adapt dynamically.

```css
.graphs-grid {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Two columns */
    grid-template-rows: auto auto; /* Two rows */
    grid-gap: 20px; /* Space between graphs */
    padding: 20px;
    background-color: #f0f8ff;
    height: auto;
    max-height: calc(100vh - 100px); /* Allow charts to scale */
    width: 100%;
}

.graph {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #cfe2f3;
    border: 1px solid #000;
    height: auto;
    width: 100%;
    max-height: 50vh; /* Constrain to viewport height */
}

.graph canvas {
    width: 100%;
    height: auto; /* Dynamically adjust */
}

/* Responsive Behavior */
@media screen and (max-width: 1024px) {
    .graphs-grid {
        grid-template-columns: 1fr; /* Switch to single column */
        grid-gap: 10px;
    }
}
```

---

### Expected Behavior
- **When resizing the window horizontally or vertically:** 
  - The graphs will adjust proportionally and maintain aspect ratios.
  - Dynamic resizing will be handled seamlessly using the `adjustCharts` function.
  
- **Responsive Breakpoints:**
  - At smaller widths, the grid will switch to a single-column layout.

---

### Troubleshooting
If resizing still doesn't behave as expected:
1. **Inspect Parent Dimensions:** Ensure the parent container is resizing correctly.
2. **Debug with `console.log`:** Log container and canvas dimensions during resizing:
   ```javascript
   console.log('Parent dimensions:', container.offsetWidth, container.offsetHeight);
   ```
3. **Recheck the Resize Event:** Ensure it triggers as expected when the window size changes.
