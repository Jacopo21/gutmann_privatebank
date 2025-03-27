import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

def calculate_investment_projection(initial_amount, monthly_contribution, risk_appetite, years):
    risk_parameters = {
        1: {'mean_return': 0.04, 'volatility': 0.05},   # Very Conservative
        2: {'mean_return': 0.05, 'volatility': 0.07},   # Conservative
        3: {'mean_return': 0.06, 'volatility': 0.09},   # Moderately Conservative
        4: {'mean_return': 0.07, 'volatility': 0.11},   # Moderate
        5: {'mean_return': 0.08, 'volatility': 0.14},   # Moderate Aggressive
        6: {'mean_return': 0.10, 'volatility': 0.17},   # Aggressive
        7: {'mean_return': 0.12, 'volatility': 0.20},   # Very Aggressive
        8: {'mean_return': 0.14, 'volatility': 0.25}    # Extremely Aggressive
    }

    params = risk_parameters[risk_appetite]

    num_simulations = 1000
    months = years * 12

    annual_return = params['mean_return']
    annual_volatility = params['volatility']

    monthly_return = (1 + annual_return) ** (1/12) - 1
    monthly_volatility = annual_volatility / np.sqrt(12)

    simulations = np.zeros((num_simulations, months + 1))
    cumulative_investment = np.zeros((num_simulations, months + 1))

    for i in range(num_simulations):
        simulations[i, 0] = initial_amount
        cumulative_investment[i, 0] = initial_amount

        for j in range(1, months + 1):
            monthly_investment = monthly_contribution
            random_return = np.random.normal(monthly_return, monthly_volatility)

            simulations[i, j] = simulations[i, j-1] * (1 + random_return) + monthly_investment
            cumulative_investment[i, j] = cumulative_investment[i, j-1] + monthly_investment

    lower_bound = np.percentile(simulations, 10, axis=0)
    median_projection = np.percentile(simulations, 50, axis=0)
    upper_bound = np.percentile(simulations, 90, axis=0)

    months_array = np.arange(months + 1)
    results = pd.DataFrame({
        'Month': months_array,
        'Year': months_array / 12,
        'Median Projection': median_projection,
        'Lower Bound (10%)': lower_bound,
        'Upper Bound (90%)': upper_bound,
        'Cumulative Investment': cumulative_investment[0]
    })

    return results

def main():
    # Custom page configuration with light beige background
    st.set_page_config(
        page_title="Investment Projection Tool",
        layout="wide",
        page_icon="💹"
    )

    # Custom CSS for light beige background, dark blue text, and Google Font
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:wght@400;700&display=swap');

    body {
        background-color: #FCFCF4;  /* Light Beige */
        color: #00008B;  /* Dark Blue */
        font-family: 'Instrument Serif', serif;
    }
    .stApp {
        background-color: #FCFCF4;
    }
    .stMarkdown, .stTitle, .stHeader {
        color: #00008B;
    }
    .stMetric {
        background-color: rgba(0, 0, 139, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
    .instrument-serif-regular {
        font-family: 'Instrument Serif', serif;
        font-weight: 400;
        font-style: normal;
    }
    .instrument-serif-regular-italic {
        font-family: 'Instrument Serif', serif;
        font-weight: 400;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add the logo image
    st.image(r"C:\Users\JacopoBinati\OneDrive - Venionaire Capital\Desktop\gutmann_privatebank\img\bank_gutmann_cover.jpg", width=600)

    st.title("Gutmann Private Banker's Investment Growth Projection")
    st.subheader("Investment Bank Portfolio Simulator")

    # Sidebar inputs with dark blue text
    with st.sidebar:
        st.header("Investment Parameters", anchor=None)

        initial_amount = st.number_input(
            "Initial Investment Amount",
            min_value=500000,
            max_value=10000000,
            value=1000000,
            step=50000
        )

        monthly_contribution = st.number_input(
            "Monthly Investment",
            min_value=500,
            max_value=30000,
            value=5000,
            step=500
        )

        risk_appetite = st.slider(
            "Risk Appetite",
            min_value=1,
            max_value=8,
            value=4,
            help="1: Very Conservative, 8: Extremely Aggressive"
        )

        investment_horizon = st.slider(
            "Investment Horizon (Years)",
            min_value=1,
            max_value=20,
            value=10
        )

        st.info(f"🔍 Risk Level: {risk_appetite}/8", icon="ℹ️")

    # Calculate projections
    projection_results = calculate_investment_projection(
        initial_amount,
        monthly_contribution,
        risk_appetite,
        investment_horizon
    )

    # Plotting with a light color palette
    fig = go.Figure()

    # Median Projection
    fig.add_trace(go.Scatter(
        x=projection_results['Year'],
        y=projection_results['Median Projection'],
        mode='lines',
        name='Median Projection',
        line=dict(color='#00008B', width=3)  # Dark Blue
    ))

    # Lower Bound
    fig.add_trace(go.Scatter(
        x=projection_results['Year'],
        y=projection_results['Lower Bound (10%)'],
        mode='lines',
        name='Lower Bound (10%)',
        line=dict(color='#4169E1', width=2, dash='dot')  #  Blue
    ))

    # Upper Bound
    fig.add_trace(go.Scatter(
        x=projection_results['Year'],
        y=projection_results['Upper Bound (90%)'],
        mode='lines',
        name='Upper Bound (90%)',
        line=dict(color='#1E90FF', width=2, dash='dot')  #  Blue
    ))

    # Cumulative Investment Line
    fig.add_trace(go.Scatter(
        x=projection_results['Year'],
        y=projection_results['Cumulative Investment'],
        mode='lines',
        name='Cumulative Investment',
        line=dict(color='#708090', width=3, dash='dash')  #  Gray
    ))

    # Layout with light beige theme
    fig.update_layout(
        title='Investment Growth Projection',
        xaxis_title='Years',
        yaxis_title='Portfolio Value ($)',
        height=600,
        paper_bgcolor='rgba(245, 245, 220, 0.5)', 
        plot_bgcolor='rgba(245, 245, 220, 0.5)',  
        font=dict(color='#00008B'),  #  Blue text
        legend_title_font_color='#00008B'
    )

    st.plotly_chart(fig, use_container_width=True)

    final_median = projection_results['Median Projection'].iloc[-1]
    final_investment = projection_results['Cumulative Investment'].iloc[-1]
    total_return = final_median - final_investment

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Final Portfolio Value", f"${final_median:,.0f}")

    with col2:
        st.metric("Total Investment", f"${final_investment:,.0f}")

    with col3:
        st.metric("Total Return", f"${total_return:,.0f}")

if __name__ == "__main__":
    main()
