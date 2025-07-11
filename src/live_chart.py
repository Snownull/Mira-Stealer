"""
Live Chart Widget
Converted from C# livechart.cs class
Uses matplotlib with tkinter backend for live data visualization
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import time
import random

class LiveChart:
    """Live chart widget for displaying real-time data"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.is_running = False
        self.update_thread = None
        
        # Chart data
        self.max_data_points = 200
        self.data_index = 0
        self.chart_data_lines = [
            np.zeros(self.max_data_points),  # Main line
            np.zeros(self.max_data_points),  # Second line
            np.zeros(self.max_data_points)   # Third line
        ]
        
        # Line colors (matching the original)
        self.line_colors = [
            '#71A8F3',  # Main blue color
            '#2ECC71',  # Green line
            '#F1C40F'   # Yellow/gold line
        ]
        
        # Line styles
        self.line_styles = ['-', '--', '-.']
        
        # Initialize random data
        self._initialize_data()
        
        # Create the chart
        self._create_chart()
        
        # Start updating
        self.start_updates()
    
    def _initialize_data(self):
        """Initialize chart with random data"""
        height_base = 100  # Base height for calculations
        
        for i in range(self.max_data_points):
            self.chart_data_lines[0][i] = random.randint(height_base // 4, height_base // 2)
            self.chart_data_lines[1][i] = random.randint(height_base // 2, 3 * height_base // 4)
            self.chart_data_lines[2][i] = random.randint(height_base // 10, height_base // 3)
    
    def _create_chart(self):
        """Create the matplotlib chart"""
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 4), facecolor='#2C3E50')
        self.ax.set_facecolor('#34495E')
        
        # Configure the axis
        self.ax.grid(True, alpha=0.3, linestyle=':', color='#71A8F3')
        self.ax.set_xlim(0, self.max_data_points)
        self.ax.set_ylim(0, 100)
        
        # Remove axis labels and ticks for cleaner look
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Create line objects
        self.lines = []
        for i in range(3):
            line, = self.ax.plot(
                [], [], 
                color=self.line_colors[i], 
                linestyle=self.line_styles[i],
                linewidth=2 if i == 0 else 1.5,
                alpha=0.8
            )
            self.lines.append(line)
        
        # Create the canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial draw
        self._update_chart()
    
    def _update_chart(self):
        """Update the chart with current data"""
        x_data = np.arange(self.max_data_points)
        
        for i, line in enumerate(self.lines):
            line.set_data(x_data, self.chart_data_lines[i])
        
        # Adjust y-axis limits based on data
        all_data = np.concatenate(self.chart_data_lines)
        if len(all_data) > 0:
            y_min = max(0, np.min(all_data) - 10)
            y_max = np.max(all_data) + 10
            self.ax.set_ylim(y_min, y_max)
        
        self.canvas.draw_idle()
    
    def _update_data(self):
        """Update chart data (similar to original UpdateChart method)"""
        height_base = 100
        
        # Update each line with different patterns
        for line_idx in range(3):
            if line_idx == 0:  # Main line - based on simulated counts
                total_sum = sum(random.randint(0, height_base // 8) for _ in range(8))
                # Smooth the line by averaging with previous point
                prev_idx = (self.data_index - 1) % self.max_data_points
                prev_value = self.chart_data_lines[0][prev_idx]
                self.chart_data_lines[0][self.data_index] = (total_sum + prev_value) // 2
                
            elif line_idx == 1:  # Second line - more dramatic movements
                prev_idx = (self.data_index - 1) % self.max_data_points
                current_value = self.chart_data_lines[1][prev_idx]
                change = random.randint(-height_base // 10, height_base // 10)
                new_value = max(height_base // 4, min(current_value + change, 3 * height_base // 4))
                self.chart_data_lines[1][self.data_index] = new_value
                
            elif line_idx == 2:  # Third line - smoother, lower frequency
                prev_idx = (self.data_index - 1) % self.max_data_points
                base_value = self.chart_data_lines[2][prev_idx]
                small_change = random.randint(-height_base // 20, height_base // 20)
                smooth_value = max(height_base // 10, min(base_value + small_change, height_base // 2))
                self.chart_data_lines[2][self.data_index] = smooth_value
        
        self.data_index = (self.data_index + 1) % self.max_data_points
    
    def _update_loop(self):
        """Background thread for updating chart data"""
        while self.is_running:
            self._update_data()
            
            # Update chart on main thread
            if self.canvas.get_tk_widget().winfo_exists():
                self.canvas.get_tk_widget().after_idle(self._update_chart)
            
            time.sleep(2)  # Update every 2 seconds (matching original timer)
    
    def start_updates(self):
        """Start the chart update loop"""
        if not self.is_running:
            self.is_running = True
            self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
            self.update_thread.start()
    
    def stop_updates(self):
        """Stop the chart update loop"""
        self.is_running = False
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1)
    
    def destroy(self):
        """Clean up the chart"""
        self.stop_updates()
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        if hasattr(self, 'fig'):
            plt.close(self.fig)