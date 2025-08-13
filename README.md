# High Voltage Battery Cell Testing with 10A Current Using a First Order Thevenin Model

This project analyzes the performance of a **high-voltage battery cell** under a **10A load** using a **first-order Thevenin equivalent circuit model**.  
By combining **experimental measurement data** and **polynomial fitting**, the internal resistance (R) and capacitance (C) of the battery are extracted for modeling and simulation.

## Features
- **Open Circuit Voltage (OCV) Analysis**: Polynomial fitting of OCV vs. State of Charge (SOC) from a 1A constant current run.
- **Transient Response Analysis**: Correction of loaded voltage using OCV data for accurate Thevenin parameter extraction.
- **Parameter Estimation**: Calculation of equivalent series resistance and capacitance from step-response data.
- **Visualization**: Plots of raw data, fitted OCV curves, and transient behavior.

## Methodology
1. **Collect OCV Data** – From a low-current discharge (1A constant current), map voltage to SOC and fit a polynomial curve.
2. **Collect Load Data** – Perform a high-current (10A) transient test and log voltage, current, and SOC.
3. **Correct Voltage** – Subtract fitted OCV from loaded voltage to isolate transient effects.
4. **Thevenin Model Fit** – Use exponential decay fitting to determine internal resistance (R) and capacitance (C).
5. **Visualize Results** – Generate plots to compare measured vs. fitted data.

## Tools & Technologies
- **Language**: Python
- **Libraries**: Pandas, NumPy, Matplotlib
- **Data**: CSV logs from high-voltage battery cell tests