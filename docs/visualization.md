# Visualization Guide

This guide covers the visualization components and best practices used in the AI Cloud Dashboard.

## Visualization Components

### Chart Types

#### Time Series Charts
```python
import plotly.graph_objects as go

def create_time_series(data, metric_name):
    """Create time series visualization"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['timestamp'],
            y=data['value'],
            mode='lines+markers',
            name=metric_name
        )
    )
    fig.update_layout(
        title=f"{metric_name} Over Time",
        xaxis_title="Time",
        yaxis_title="Value",
        hovermode='x unified'
    )
    return fig
```

#### Comparison Charts
```python
def create_provider_comparison(data):
    """Create provider comparison visualization"""
    fig = go.Figure(data=[
        go.Bar(
            name=provider,
            x=list(metrics.keys()),
            y=list(metrics.values())
        )
        for provider, metrics in data.items()
    ])
    fig.update_layout(
        barmode='group',
        title="Cloud Provider Comparison",
        xaxis_title="Metrics",
        yaxis_title="Value"
    )
    return fig
```

#### Performance Dashboards
```python
def create_performance_dashboard(metrics_data):
    """Create performance metrics dashboard"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "CPU Usage", "Memory Usage",
            "Network I/O", "Disk I/O"
        )
    )
    
    # Add traces for each metric
    add_metric_traces(fig, metrics_data)
    
    fig.update_layout(height=800, showlegend=True)
    return fig
```

### Interactive Features

#### Tooltips and Hovers
```python
def configure_tooltips(fig):
    """Configure interactive tooltips"""
    fig.update_traces(
        hovertemplate="<br>".join([
            "Time: %{x}",
            "Value: %{y:.2f}",
            "Change: %{customdata[0]:.2%}",
            "<extra></extra>"
        ])
    )
```

#### Drill-Down Capabilities
```python
def add_drill_down(fig, detailed_data):
    """Add drill-down functionality"""
    fig.update_traces(
        customdata=detailed_data,
        clickmode='event+select'
    )
    return fig
```

#### Dynamic Updates
```python
def update_chart_data(fig, new_data):
    """Update chart with new data"""
    with fig.batch_update():
        fig.data[0].x = new_data['timestamp']
        fig.data[0].y = new_data['value']
```

## Chart Configurations

### Theme Configuration
```python
def apply_theme(fig):
    """Apply consistent theme to visualization"""
    fig.update_layout(
        template="plotly_dark",
        font=dict(family="Arial, sans-serif"),
        title_font_size=24,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
```

### Responsive Design
```python
def make_responsive(fig):
    """Make visualization responsive"""
    fig.update_layout(
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        )
    )
```

### Color Schemes
```python
class ColorScheme:
    PRIMARY_COLORS = [
        '#1f77b4',  # blue
        '#ff7f0e',  # orange
        '#2ca02c',  # green
        '#d62728',  # red
        '#9467bd'   # purple
    ]
    
    @classmethod
    def get_color(cls, index):
        """Get color by index"""
        return cls.PRIMARY_COLORS[index % len(cls.PRIMARY_COLORS)]
```

## Data Visualization Types

### Market Intelligence

#### Market Share Visualization
```python
def create_market_share_pie(data):
    """Create market share pie chart"""
    fig = go.Figure(data=[
        go.Pie(
            labels=list(data.keys()),
            values=list(data.values()),
            hole=.3
        )
    ])
    fig.update_layout(title="Cloud Provider Market Share")
    return fig
```

#### Growth Trends
```python
def create_growth_trend(data):
    """Create growth trend visualization"""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['date'],
            y=data['growth_rate'],
            mode='lines+markers',
            fill='tozeroy'
        )
    )
    return fig
```

### Performance Metrics

#### Resource Utilization
```python
def create_resource_gauge(value, title):
    """Create resource utilization gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [0, 100]}}
    ))
    return fig
```

#### Latency Analysis
```python
def create_latency_heatmap(data):
    """Create latency heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=data['values'],
        x=data['regions'],
        y=data['times'],
        colorscale='RdYlBu_r'
    ))
    return fig
```

## Best Practices

### Performance Optimization

#### Lazy Loading
```python
class LazyChart:
    def __init__(self, data_func):
        self.data_func = data_func
        self._figure = None

    @property
    def figure(self):
        """Lazy load figure"""
        if self._figure is None:
            self._figure = self.data_func()
        return self._figure
```

#### Data Aggregation
```python
def aggregate_for_visualization(data, resolution='1h'):
    """Aggregate data for visualization"""
    return data.resample(resolution).agg({
        'value': 'mean',
        'min': 'min',
        'max': 'max'
    })
```

### Accessibility

#### Color Blind Friendly
```python
def apply_colorblind_friendly_palette(fig):
    """Apply colorblind-friendly colors"""
    colorblind_palette = [
        '#018571',  # teal
        '#d8b365',  # tan
        '#5ab4ac',  # light teal
        '#8c510a'   # brown
    ]
    fig.update_traces(marker_color=colorblind_palette)
```

#### Text Alternatives
```python
def add_accessibility_features(fig):
    """Add accessibility features"""
    fig.update_layout(
        annotations=[
            dict(
                text="Chart description for screen readers",
                showarrow=False,
                visible=False
            )
        ]
    )
```

## Error Handling

### Data Validation
```python
def validate_visualization_data(data):
    """Validate data for visualization"""
    if data.empty:
        raise ValueError("No data available for visualization")
    if data.isnull().any().any():
        logger.warning("Missing values in visualization data")
```

### Fallback Displays
```python
def create_fallback_visualization():
    """Create fallback visualization"""
    fig = go.Figure()
    fig.add_annotation(
        text="Data temporarily unavailable",
        showarrow=False,
        font=dict(size=20)
    )
    return fig
```

## Additional Resources

- [Plotly Documentation](https://plotly.com/python/)
- [Chart Design Guide](chart-design.md)
- [Accessibility Guidelines](accessibility.md)
- [Performance Optimization](performance.md)
