import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_performance_radar(performance_data):
    """Create radar chart for performance metrics by provider."""
    # Calculate average metrics per provider
    avg_metrics = performance_data.groupby("Provider").agg({
        "Latency (ms)": "mean",
        "Uptime (%)": "mean",
        "IOPS": "mean",
        "Network Throughput (Gbps)": "mean"
    }).reset_index()
    
    fig = go.Figure()
    
    for provider in avg_metrics["Provider"]:
        provider_data = avg_metrics[avg_metrics["Provider"] == provider]
        fig.add_trace(go.Scatterpolar(
            r=[
                provider_data["Latency (ms)"].iloc[0],
                provider_data["Uptime (%)"].iloc[0],
                provider_data["IOPS"].iloc[0] / 1000,  # Scale down for visualization
                provider_data["Network Throughput (Gbps)"].iloc[0]
            ],
            theta=["Latency", "Uptime", "IOPS (K)", "Network"],
            name=provider,
            fill="toself"
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Performance Metrics by Provider"
    )
    
    return fig

def create_latency_heatmap(performance_data):
    """Create heatmap of latency across regions and providers."""
    latency_pivot = performance_data.pivot(
        index="Provider",
        columns="Region",
        values="Latency (ms)"
    )
    
    fig = px.imshow(
        latency_pivot,
        title="Latency by Region and Provider (ms)",
        color_continuous_scale="RdYlGn_r"  # Reverse scale: red=high latency, green=low latency
    )
    
    # Add text annotations
    for i in range(len(latency_pivot.index)):
        for j in range(len(latency_pivot.columns)):
            fig.add_annotation(
                text=f"{latency_pivot.iloc[i, j]:.1f}",
                x=j,
                y=i,
                showarrow=False,
                font=dict(color="white")
            )
    
    return fig

def create_sla_comparison(sla_data):
    """Create bar chart comparing SLAs across providers."""
    fig = go.Figure()
    
    for provider in ["AWS", "Azure", "GCP", "Alibaba", "Tencent"]:
        fig.add_trace(go.Bar(
            name=provider,
            x=sla_data["Service Type"],
            y=sla_data[provider],
            text=sla_data[provider].apply(lambda x: f"{x}%"),
            textposition="auto"
        ))
    
    fig.update_layout(
        title="SLA Comparison by Service Type",
        barmode="group",
        yaxis=dict(
            title="SLA (%)",
            range=[99.5, 100]  # Zoom in on the relevant range
        )
    )
    
    return fig

def create_cost_comparison(cost_data):
    """Create grouped bar chart for cost comparison."""
    # Melt the dataframe for easier plotting
    melted_data = cost_data.melt(
        id_vars=["Service"],
        var_name="Provider",
        value_name="Cost"
    )
    
    fig = px.bar(
        melted_data,
        x="Service",
        y="Cost",
        color="Provider",
        title="Service Cost Comparison",
        barmode="group",
        text=melted_data["Cost"].apply(lambda x: f"${x:.4f}")
    )
    
    fig.update_layout(
        xaxis_title="Service Type",
        yaxis_title="Cost (USD)",
        xaxis=dict(tickangle=45)
    )
    
    return fig

def create_tco_analysis(tco_data):
    """Create visualization for TCO analysis."""
    fig = go.Figure()
    
    # Add bars for different time periods
    fig.add_trace(go.Bar(
        name="Monthly Cost",
        x=tco_data["Provider"],
        y=tco_data["Monthly Cost"],
        text=tco_data["Monthly Cost"].apply(lambda x: f"${x:,.2f}"),
        textposition="auto"
    ))
    
    fig.add_trace(go.Bar(
        name="Yearly Cost",
        x=tco_data["Provider"],
        y=tco_data["Yearly Cost"],
        text=tco_data["Yearly Cost"].apply(lambda x: f"${x:,.2f}"),
        textposition="auto"
    ))
    
    fig.add_trace(go.Bar(
        name="3-Year TCO",
        x=tco_data["Provider"],
        y=tco_data["3-Year TCO"],
        text=tco_data["3-Year TCO"].apply(lambda x: f"${x:,.2f}"),
        textposition="auto"
    ))
    
    # Add savings as a line
    fig.add_trace(go.Scatter(
        name="Savings vs. Highest",
        x=tco_data["Provider"],
        y=tco_data["Savings vs. Highest"] * 100,  # Scale for visibility
        text=tco_data["Savings vs. Highest"].apply(lambda x: f"{x:.1f}%"),
        mode="lines+markers+text",
        yaxis="y2",
        line=dict(color="green", width=2),
        textposition="top center"
    ))
    
    fig.update_layout(
        title="Total Cost of Ownership Analysis",
        barmode="group",
        yaxis=dict(title="Cost (USD)"),
        yaxis2=dict(
            title="Savings (%)",
            overlaying="y",
            side="right",
            range=[0, 100]
        )
    )
    
    return fig
