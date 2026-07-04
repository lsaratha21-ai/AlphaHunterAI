"""Streamlit Dashboard for AlphaHunter AI."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="AlphaHunter AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎯 AlphaHunter AI")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.radio(
    "Navigate to:",
    [
        "📊 Dashboard",
        "🔥 Heat Map",
        "🔄 Sector Rotation",
        "💼 Portfolio",
        "📈 Charts",
        "⚠️ Risk Meter",
        "💡 Recommendations",
        "📰 News",
        "🎙️ Management Guidance"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Settings")
time_period = st.sidebar.selectbox("Time Period", ["1D", "1W", "1M", "3M", "6M", "1Y"])

# Mock data generators
def generate_stock_data(n=20):
    """Generate mock stock data."""
    sectors = ["Technology", "Healthcare", "Finance", "Energy", "Consumer", "Industrial"]
    data = []
    for i in range(n):
        sector = random.choice(sectors)
        price = random.uniform(100, 1000)
        change = random.uniform(-5, 5)
        score = random.uniform(0, 100)
        data.append({
            "Symbol": f"STOCK{i+1:03d}",
            "Name": f"Company {i+1}",
            "Sector": sector,
            "Price": round(price, 2),
            "Change %": round(change, 2),
            "Score": round(score, 1),
            "Action": "Buy" if score > 70 else "Sell" if score < 30 else "Hold"
        })
    return pd.DataFrame(data)

def generate_sector_data():
    """Generate mock sector rotation data."""
    sectors = ["Technology", "Healthcare", "Finance", "Energy", "Consumer", "Industrial"]
    data = []
    for sector in sectors:
        data.append({
            "Sector": sector,
            "Score": random.uniform(0, 100),
            "Rotation": random.choice(["Inflow", "Outflow", "Neutral"]),
            "Government": random.uniform(-50, 50),
            "Order Book": random.uniform(-50, 50),
            "News": random.uniform(-50, 50),
            "Institutional": random.uniform(-50, 50)
        })
    return pd.DataFrame(data)

def generate_portfolio_data():
    """Generate mock portfolio data."""
    holdings = []
    total_value = 100000
    for i in range(10):
        weight = random.uniform(5, 20)
        value = total_value * (weight / 100)
        holdings.append({
            "Symbol": f"STOCK{i+1:03d}",
            "Name": f"Company {i+1}",
            "Shares": random.randint(10, 100),
            "Avg Cost": random.uniform(100, 500),
            "Current Price": random.uniform(100, 500),
            "Value": round(value, 2),
            "Weight %": round(weight, 1),
            "Gain/Loss %": round(random.uniform(-20, 30), 2)
        })
    return pd.DataFrame(holdings)

# Dashboard Page
if page == "📊 Dashboard":
    st.title("📊 AlphaHunter AI Dashboard")
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Portfolio Value", "₹1,25,43,210", "+2.4%")
    with col2:
        st.metric("Today's P&L", "+₹2,43,210", None)
    with col3:
        st.metric("Top Pick", "STOCK001", "+5.2%")
    with col4:
        st.metric("Risk Score", "Medium", None)
    
    st.markdown("---")
    
    # Top 20 Stocks
    st.subheader("🏆 Top 20 Stocks by Score")
    stock_data = generate_stock_data(20)
    
    # Color coding for action
    def highlight_action(val):
        if val == "Buy":
            return "background-color: #90EE90"
        elif val == "Sell":
            return "background-color: #FFB6C1"
        return ""
    
    styled_df = stock_data.style.applymap(highlight_action, subset=["Action"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Performers")
        top_performers = stock_data.nlargest(5, "Change %")
        fig = px.bar(top_performers, x="Symbol", y="Change %", color="Change %",
                     title="Top 5 Gainers", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sector Distribution")
        sector_counts = stock_data["Sector"].value_counts()
        fig = px.pie(values=sector_counts.values, names=sector_counts.index,
                     title="Sector Distribution")
        st.plotly_chart(fig, use_container_width=True)

# Heat Map Page
elif page == "🔥 Heat Map":
    st.title("🔥 Market Heat Map")
    st.markdown("---")
    
    stock_data = generate_stock_data(50)
    
    # Create pivot table for heatmap
    pivot_data = stock_data.pivot_table(values="Change %", index="Sector", columns="Symbol", aggfunc="mean")
    
    fig = px.imshow(
        pivot_data,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        title="Market Heat Map by Sector"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Stock Performance Table")
    st.dataframe(stock_data, use_container_width=True, hide_index=True)

# Sector Rotation Page
elif page == "🔄 Sector Rotation":
    st.title("🔄 Sector Rotation Analysis")
    st.markdown("---")
    
    sector_data = generate_sector_data()
    
    # Sector scores
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Sector Scores")
        fig = px.bar(sector_data, x="Sector", y="Score", color="Score",
                     title="Sector Scores", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Rotation Signals")
        rotation_counts = sector_data["Rotation"].value_counts()
        fig = px.pie(values=rotation_counts.values, names=rotation_counts.index,
                     title="Rotation Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.subheader("Government Impact")
        fig = px.bar(sector_data, x="Sector", y="Government",
                     title="Government Policy Impact", color="Government",
                     color_continuous_scale="RdYlGn")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Detailed Sector Analysis")
    st.dataframe(sector_data, use_container_width=True, hide_index=True)

# Portfolio Page
elif page == "💼 Portfolio":
    st.title("💼 Portfolio Overview")
    st.markdown("---")
    
    # Portfolio summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Value", "₹1,25,43,210", "+2.4%")
    with col2:
        st.metric("Invested Amount", "₹1,20,00,000", None)
    with col3:
        st.metric("Unrealized P&L", "+₹5,43,210", "+4.5%")
    with col4:
        st.metric("Number of Holdings", "10", None)
    
    st.markdown("---")
    
    portfolio_data = generate_portfolio_data()
    
    # Portfolio table
    def highlight_gain_loss(val):
        if val > 0:
            return "color: green"
        elif val < 0:
            return "color: red"
        return "color: black"
    
    styled_portfolio = portfolio_data.style.applymap(highlight_gain_loss, subset=["Gain/Loss %"])
    st.subheader("Holdings")
    st.dataframe(styled_portfolio, use_container_width=True, hide_index=True)
    
    # Portfolio allocation chart
    st.subheader("Portfolio Allocation")
    fig = px.pie(portfolio_data, values="Value", names="Symbol",
                 title="Portfolio Allocation by Stock")
    st.plotly_chart(fig, use_container_width=True)

# Charts Page
elif page == "📈 Charts":
    st.title("📈 Technical Charts")
    st.markdown("---")
    
    # Stock selector
    selected_stock = st.selectbox("Select Stock", [f"STOCK{i:03d}" for i in range(1, 21)])
    
    # Generate mock price data
    dates = pd.date_range(end=datetime.now(), periods=90)
    prices = [random.uniform(100, 200) for _ in range(90)]
    
    price_df = pd.DataFrame({
        "Date": dates,
        "Price": prices
    })
    
    # Price chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=price_df["Date"], y=price_df["Price"],
                             mode='lines', name='Price'))
    fig.update_layout(title=f"{selected_stock} - Price Chart",
                     xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart
    volumes = [random.uniform(100000, 1000000) for _ in range(90)]
    volume_df = pd.DataFrame({
        "Date": dates,
        "Volume": volumes
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=volume_df["Date"], y=volume_df["Volume"],
                        name='Volume'))
    fig.update_layout(title=f"{selected_stock} - Volume Chart",
                     xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(fig, use_container_width=True)

# Risk Meter Page
elif page == "⚠️ Risk Meter":
    st.title("⚠️ Risk Assessment")
    st.markdown("---")
    
    # Overall risk score
    overall_risk = random.randint(30, 80)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Risk Score", f"{overall_risk}/100",
                  "Medium" if 40 <= overall_risk <= 60 else "Low" if overall_risk < 40 else "High")
    with col2:
        st.metric("Portfolio Beta", f"{random.uniform(0.8, 1.5):.2f}", None)
    with col3:
        st.metric("Volatility", f"{random.uniform(15, 35):.1f}%", None)
    
    st.markdown("---")
    
    # Risk gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = overall_risk,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Level"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk breakdown
    st.subheader("Risk Breakdown")
    risk_categories = ["Market Risk", "Sector Risk", "Concentration Risk", "Liquidity Risk"]
    risk_values = [random.randint(20, 80) for _ in range(4)]
    
    risk_df = pd.DataFrame({
        "Risk Category": risk_categories,
        "Score": risk_values
    })
    
    fig = px.bar(risk_df, x="Risk Category", y="Score", color="Score",
                 title="Risk Category Scores", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

# Recommendations Page
elif page == "💡 Recommendations":
    st.title("💡 AI Recommendations")
    st.markdown("---")
    
    stock_data = generate_stock_data(10)
    
    for _, row in stock_data.iterrows():
        with st.expander(f"{row['Symbol']} - {row['Name']} ({row['Action']})"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{row['Score']}/100")
            with col2:
                st.metric("Price", f"₹{row['Price']}")
            with col3:
                st.metric("Change", f"{row['Change %']}%")
            
            st.write(f"**Reasoning:** This stock shows strong {row['Action'].lower()} signals based on:")
            st.write(f"- Financial Score: {random.randint(50, 90)}")
            st.write(f"- Technical Score: {random.randint(50, 90)}")
            st.write(f"- Sector Score: {random.randint(50, 90)}")
            st.write(f"- Overall Score: {row['Score']}")
            
            if row['Action'] == "Buy":
                st.success(f"Target: ₹{row['Price'] * 1.15:.2f} | Stop Loss: ₹{row['Price'] * 0.90:.2f}")
            elif row['Action'] == "Sell":
                st.error(f"Target: ₹{row['Price'] * 0.85:.2f} | Stop Loss: ₹{row['Price'] * 1.10:.2f}")
            else:
                st.info("Hold position")

# News Page
elif page == "📰 News":
    st.title("📰 Market News")
    st.markdown("---")
    
    # Mock news data
    news_items = []
    for i in range(10):
        sentiment = random.choice(["Positive", "Negative", "Neutral"])
        news_items.append({
            "Headline": f"Market update {i+1}: Key development in the sector",
            "Source": random.choice(["Reuters", "Bloomberg", "Economic Times", "Moneycontrol"]),
            "Time": f"{random.randint(1, 24)}h ago",
            "Sentiment": sentiment,
            "Impact": "High" if sentiment != "Neutral" else "Low"
        })
    
    news_df = pd.DataFrame(news_items)
    
    def highlight_sentiment(val):
        if val == "Positive":
            return "background-color: #90EE90"
        elif val == "Negative":
            return "background-color: #FFB6C1"
        return ""
    
    styled_news = news_df.style.applymap(highlight_sentiment, subset=["Sentiment"])
    st.dataframe(styled_news, use_container_width=True, hide_index=True)
    
    # Sentiment distribution
    st.subheader("News Sentiment Distribution")
    sentiment_counts = news_df["Sentiment"].value_counts()
    fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                 title="News Sentiment")
    st.plotly_chart(fig, use_container_width=True)

# Management Guidance Page
elif page == "🎙️ Management Guidance":
    st.title("🎙️ Management Guidance Analysis")
    st.markdown("---")
    
    # Mock guidance data
    companies = [f"STOCK{i:03d}" for i in range(1, 11)]
    guidance_data = []
    
    for company in companies:
        guidance_data.append({
            "Company": company,
            "Revenue Outlook": random.choice(["Positive", "Neutral", "Negative"]),
            "Margin Outlook": random.choice(["Positive", "Neutral", "Negative"]),
            "Demand": random.choice(["Strong", "Moderate", "Weak"]),
            "Order Book": random.choice(["Strong", "Moderate", "Weak"]),
            "Capex": random.choice(["Increasing", "Stable", "Decreasing"]),
            "Expansion": random.choice(["Aggressive", "Moderate", "Conservative"]),
            "Confidence": random.choice(["High", "Medium", "Low"]),
            "Overall Sentiment": random.choice(["Positive", "Neutral", "Negative"])
        })
    
    guidance_df = pd.DataFrame(guidance_data)
    
    def highlight_guidance(val):
        if val in ["Positive", "Strong", "Increasing", "Aggressive", "High"]:
            return "background-color: #90EE90"
        elif val in ["Negative", "Weak", "Decreasing", "Conservative", "Low"]:
            return "background-color: #FFB6C1"
        return ""
    
    styled_guidance = guidance_df.style.applymap(highlight_guidance)
    st.dataframe(styled_guidance, use_container_width=True, hide_index=True)
    
    # Overall sentiment distribution
    st.subheader("Management Sentiment Overview")
    sentiment_counts = guidance_df["Overall Sentiment"].value_counts()
    fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                 title="Management Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue outlook by company
    st.subheader("Revenue Outlook by Company")
    fig = px.bar(guidance_df, x="Company", y="Revenue Outlook",
                 color="Revenue Outlook", title="Revenue Outlook")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("© 2024 AlphaHunter AI. All rights reserved.")
st.markdown("Built with ❤️ using Streamlit")
