import plotly.express as px
import plotly.graph_objects as go

try:
    from data.ai_model_data import DATA_AS_OF
except ImportError:
    from src.data.ai_model_data import DATA_AS_OF


def create_model_pricing_scatter(model_data):
    """Create a scatter plot of context window vs. blended price, sized by
    agentic score and colored by provider region (colorblind-friendly)."""
    plot_data = model_data.copy()
    plot_data["Blended Price ($/1M tok)"] = (
        plot_data["Input Price ($/1M tok)"] + plot_data["Output Price ($/1M tok)"]
    ) / 2

    fig = px.scatter(
        plot_data,
        x="Context Window (tokens)",
        y="Blended Price ($/1M tok)",
        size="Agentic/Tool-Use Score",
        color="Provider Region",
        hover_name="Model Family",
        hover_data=["Lab / Provider", "Capability Tier"],
        log_x=True,
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="AI Model Pricing vs. Context Window",
    )
    fig.update_layout(
        meta={
            "aria-label": f"Scatter plot comparing AI model context window, blended pricing, "
            f"and agentic score by provider region, as of {DATA_AS_OF}."
        }
    )
    return fig


def create_model_capability_radar(model_data):
    """Create a radar chart comparing frontier-tier model families across
    normalized capability dimensions (colorblind-friendly)."""
    categories = [
        "Context (norm.)",
        "Price Efficiency (norm.)",
        "Agentic Score",
        "Modality Breadth",
    ]

    fig = go.Figure()
    frontier = model_data[model_data["Capability Tier"] == "Frontier"]
    color_palette = px.colors.qualitative.Safe

    max_context = frontier["Context Window (tokens)"].max()
    max_price = (
        frontier["Input Price ($/1M tok)"] + frontier["Output Price ($/1M tok)"]
    ).max()

    for idx, (_, row) in enumerate(frontier.iterrows()):
        blended_price = row["Input Price ($/1M tok)"] + row["Output Price ($/1M tok)"]
        values = [
            round(row["Context Window (tokens)"] / max_context * 100, 1),
            round(100 - (blended_price / max_price * 100), 1),
            row["Agentic/Tool-Use Score"],
            len(row["Modality"].split(",")) / 4 * 100,
        ]

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories,
                name=row["Model Family"],
                fill="toself",
                line=dict(color=color_palette[idx % len(color_palette)]),
                hovertemplate="<b>%{theta}</b><br>%{r:,.1f}<br><extra></extra>",
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Frontier Model Capability Comparison",
        margin=dict(t=100),
        meta={
            "aria-label": f"Radar chart comparing frontier AI model families on normalized "
            f"context, price efficiency, agentic score, and modality breadth, as of {DATA_AS_OF}."
        },
    )

    return fig


def create_model_pricing_bar(model_data):
    """Create a grouped bar chart of input vs. output pricing per model
    (colorblind-friendly)."""
    plot_data = model_data.melt(
        id_vars=["Model Family"],
        value_vars=["Input Price ($/1M tok)", "Output Price ($/1M tok)"],
        var_name="Price Type",
        value_name="Price ($/1M tok)",
    )

    fig = px.bar(
        plot_data,
        x="Model Family",
        y="Price ($/1M tok)",
        color="Price Type",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Model Pricing: Input vs. Output ($/1M tokens)",
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        meta={
            "aria-label": f"Grouped bar chart comparing input and output token pricing "
            f"across AI model families, as of {DATA_AS_OF}."
        },
    )
    return fig
