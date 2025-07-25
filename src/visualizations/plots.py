import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_market_share_treemap(market_data):
    """Create treemap visualization for market share data (colorblind-friendly)."""
    # Add total market size for better visualization
    total_market = market_data['Market Share (%)'].sum()
    
    # Create hover text with both market share and growth
    market_data['Hover_Text'] = market_data.apply(
        lambda x: f"Market Share: {x['Market Share (%)']}%<br>"
                 f"YoY Growth: {x['YoY Growth (%)']}%",
        axis=1
    )
    
    # Use colorblind-friendly palette (e.g., 'Viridis')
    fig = px.treemap(
        market_data,
        path=[px.Constant(f"Global Cloud Market (Total: {total_market}%)"), "Region", "Provider"],
        values="Market Share (%)",
        color="YoY Growth (%)",
        color_continuous_scale="Viridis",
        custom_data=["Hover_Text"],
        title="Global Cloud Market Share and Growth (2024)"
    )
    
    # Update hover template to show custom hover text
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>%{customdata[0]}<extra></extra>"
    )
    
    # Update layout for better readability
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        coloraxis_colorbar_title="YoY Growth (%)",
        # Accessibility: Add ARIA label for screen readers (Streamlit will render as HTML)
        title={
            'text': "Global Cloud Market Share and Growth (2024)",
            'font': {'size': 20},
        }
    )
    
    return fig

def create_growth_trends_line(growth_data):
    """Create line plot for growth trends (colorblind-friendly)."""
    return px.line(
        growth_data.melt(id_vars=['Date'], var_name='Region', value_name='Growth'),
        x='Date',
        y='Growth',
        color='Region',
        color_discrete_sequence=px.colors.qualitative.Safe,  # Colorblind-friendly
        title="Regional Market Growth Trends",
        labels={'Growth': 'Growth Rate (%)', 'Date': 'Year'},
        markers=True
    )

def create_provider_comparison_radar(market_data):
    """Create radar chart for provider comparison (colorblind-friendly)."""
    categories = ['Market Share', 'Growth Rate', 'Performance', 'Security']
    
    fig = go.Figure()
    providers = market_data['Provider'].unique()[:5]  # Top 5 providers
    color_palette = px.colors.qualitative.Safe  # Colorblind-friendly
    
    for idx, provider in enumerate(providers):
        provider_data = market_data[market_data['Provider'] == provider].iloc[0]
        # Sample metrics for demonstration
        values = [
            provider_data['Market Share (%)'],
            provider_data['YoY Growth (%)'],
            85 + np.random.randint(-10, 10),  # Random performance score
            90 + np.random.randint(-10, 10)   # Random security score
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            name=provider,
            fill='toself',
            line=dict(color=color_palette[idx % len(color_palette)]),
            hovertemplate="<b>%{theta}</b><br>" + "%{r:,.1f}<br>" + "<extra></extra>"
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix="%"
            )
        ),
        showlegend=True,
        title="Provider Comparison Matrix",
        margin=dict(t=100)
    )
    
    return fig
