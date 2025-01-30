import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def create_market_share_treemap(market_data):
    """Create treemap visualization for market share data."""
    # Add total market size for better visualization
    total_market = market_data['Market Share (%)'].sum()
    
    # Create hover text with both market share and growth
    market_data['Hover_Text'] = market_data.apply(
        lambda x: f"Market Share: {x['Market Share (%)']}%<br>"
                 f"YoY Growth: {x['YoY Growth (%)']}%",
        axis=1
    )
    
    fig = px.treemap(
        market_data,
        path=[px.Constant(f"Global Cloud Market (Total: {total_market}%)"), "Region", "Provider"],
        values="Market Share (%)",
        color="YoY Growth (%)",
        color_continuous_scale="RdYlBu",
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
        coloraxis_colorbar_title="YoY Growth (%)"
    )
    
    return fig

def create_growth_trends_line(growth_data):
    """Create line plot for growth trends."""
    return px.line(
        growth_data.melt(id_vars=['Date'], var_name='Region', value_name='Growth'),
        x='Date',
        y='Growth',
        color='Region',
        title="Regional Market Growth Trends",
        labels={'Growth': 'Growth Rate (%)', 'Date': 'Year'},
        markers=True
    )

def create_provider_comparison_radar(market_data):
    """Create radar chart for provider comparison."""
    categories = ['Market Share', 'Growth Rate', 'Performance', 'Security']
    
    fig = go.Figure()
    providers = market_data['Provider'].unique()[:5]  # Top 5 providers
    
    for provider in providers:
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
            hovertemplate="<b>%{theta}</b><br>" +
                         "%{r:,.1f}<br>" +
                         "<extra></extra>"
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
