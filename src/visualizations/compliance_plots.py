import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_compliance_heatmap(compliance_data):
    """Create heatmap visualization for compliance matrix."""
    # Convert checkmarks to numeric values for heatmap
    value_map = {"✅": 1, "⚠️": 0.5, "❌": 0}
    numeric_data = compliance_data.copy()
    
    for col in ["US Providers", "EU Providers", "China Providers"]:
        numeric_data[col] = numeric_data[col].map(value_map)
    
    fig = px.imshow(
        numeric_data.set_index("Requirement")[["US Providers", "EU Providers", "China Providers"]],
        color_continuous_scale=["red", "yellow", "green"],
        title="Compliance Requirements Coverage"
    )
    
    # Add text annotations
    for i, req in enumerate(compliance_data["Requirement"]):
        for j, col in enumerate(["US Providers", "EU Providers", "China Providers"]):
            fig.add_annotation(
                text=compliance_data.iloc[i][col],
                x=j,
                y=i,
                showarrow=False,
                font=dict(size=16)
            )
    
    return fig

def create_security_score_gauge(security_data):
    """Create gauge chart for security scores."""
    avg_risk_score = security_data["Risk Score"].mean()
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_risk_score,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Average Security Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 60], "color": "red"},
                {"range": [60, 80], "color": "yellow"},
                {"range": [80, 100], "color": "green"}
            ]
        }
    ))
    
    return fig

def create_data_residency_map(residency_data):
    """Create choropleth map for data residency."""
    # Convert residency data to format suitable for choropleth
    regions = []
    for continent, data in residency_data.items():
        for region in data["regions"]:
            regions.append({
                "Region": region,
                "Continent": continent,
                "Providers": len(data["providers"]),
                "Compliance": len(data["compliance"])
            })
    
    df = pd.DataFrame(regions)
    
    fig = go.Figure()
    
    # Add traces for each continent
    for continent in residency_data.keys():
        continent_data = df[df["Continent"] == continent]
        fig.add_trace(go.Scattergeo(
            lon=[0],  # Placeholder, would need actual coordinates
            lat=[0],  # Placeholder, would need actual coordinates
            text=continent_data.apply(
                lambda x: f"{x['Region']}<br>"
                         f"Providers: {x['Providers']}<br>"
                         f"Compliance: {x['Compliance']}",
                axis=1
            ),
            mode="markers",
            name=continent,
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title="Global Data Residency Map",
        geo=dict(
            showland=True,
            showcountries=True,
            showocean=True,
            countrywidth=0.5,
            landcolor="rgb(243, 243, 243)",
            oceancolor="rgb(204, 229, 255)",
            projection_scale=1
        )
    )
    
    return fig

def create_certification_timeline(security_data):
    """Create timeline visualization for security certifications."""
    fig = go.Figure()
    
    for idx, row in security_data.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["Last Audit"]],
            y=[row["Provider"]],
            mode="markers+text",
            name=row["Provider"],
            text=f"Score: {row['Risk Score']}",
            textposition="middle right",
            hovertext=f"Certifications: {', '.join(row['Certifications'])}",
            marker=dict(
                size=20,
                color=row["Risk Score"],
                colorscale="Viridis",
                showscale=True
            )
        ))
    
    fig.update_layout(
        title="Security Certification Timeline",
        xaxis_title="Last Audit Date",
        yaxis_title="Provider",
        showlegend=False
    )
    
    return fig
