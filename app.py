import streamlit as st
import pandas as pd
import plotly.express as px

# Page Settings
st.set_page_config(
    page_title="NIFTY50 Investment Intelligence",
    layout="wide"
)

# Load Data
risk_df = pd.read_csv("data/risk_metrics.csv")
portfolio_df = pd.read_csv("data/portfolio_metrics.csv")
stock_df = pd.read_csv("data/NIFTY50_all.csv")
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
conservative = pd.read_csv("data/conservative_portfolio.csv")
balanced = pd.read_csv("data/balanced_portfolio.csv")
aggressive = pd.read_csv("data/aggressive_portfolio.csv")

# Title
st.title("📈 NIFTY50 Investment Intelligence Platform")

# Sidebar
page = st.sidebar.selectbox(
    "Select Module",
    [
        "Overview",
        "Stock Explorer",
        "Risk Analysis",
        "Portfolio Builder",
        "Investment Insights"
    ]
)

# Overview Page
if page == "Overview":

    st.header("Project Overview")

    st.write("### Dataset Summary")

    st.write(f"Total Companies Analysed: {portfolio_df['Symbol'].nunique()}")

    st.write("Dataset Period: 2000 - 2021")

    st.write("Total Records: 235,192")

    st.write("""
    This platform transforms historical NIFTY-50 market data into
    actionable investment intelligence using technical indicators,
    risk analytics, portfolio construction and machine learning.
    """)

    st.write("### Project Modules")

    st.markdown("""
    - Stock Prediction Engine
    - Risk Assessment Module
    - Portfolio Construction Module
    - Investment Insights
    - Explainable Recommendations
    """)
    col1,col2,col3 = st.columns(3)

    col1.metric("Companies",65)
    col2.metric("Records","235K+")
    col3.metric("Period","2000-2021")
    
elif page == "Stock Explorer":

    st.header("📈 Stock Explorer")

    stock = st.selectbox(
        "Select Stock",
        sorted(stock_df['Symbol'].unique())
    )

    company = stock_df[stock_df['Symbol']==stock]

    st.write(f"Showing analysis for {stock}")
    import plotly.express as px

    fig = px.line(
       company,
       x='Date',
       y='Close',
       title=f'{stock} Closing Price'
    )

    fig.update_layout(
       xaxis_title='Date',
       yaxis_title='Closing Price (₹)'
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Risk Analysis":

    st.header("⚠️ Risk Analysis")

    stock = st.selectbox(
        "Select Stock",
        sorted(risk_df['Symbol'].unique())
    )

    stock_risk = risk_df[risk_df['Symbol'] == stock]

    col1,col2 = st.columns(2)

    col1.metric(
        "Volatility",
        round(stock_risk['Volatility'].values[0],3)
    )

    col2.metric(
        "Sharpe Ratio",
        round(stock_risk['Sharpe_Ratio'].values[0],3)
    )

    col1.metric(
        "Sortino Ratio",
        round(stock_risk['Sortino_Ratio'].values[0],3)
    )

    col2.metric(
        "Maximum Drawdown",
        round(stock_risk['Max_Drawdown'].values[0],3)
    )

    st.subheader("Interpretation")

    vol = stock_risk['Volatility'].values[0]
    sharpe = stock_risk['Sharpe_Ratio'].values[0]
    sortino = stock_risk['Sortino_Ratio'].values[0]

    if sharpe > 1:
        st.success("Strong risk-adjusted performance.")
    elif sharpe > 0.5:
        st.info("Moderate risk-adjusted performance.")
    else:
        st.warning("Weak risk-adjusted performance.")

    if vol > 0.5:
        st.warning("High volatility stock.")

    else:
        st.success("Relatively stable stock.")

elif page == "Portfolio Builder":

    st.header("💼 Portfolio Builder")

    portfolio_type = st.selectbox(
        "Investor Profile",
        ["Conservative","Balanced","Aggressive"]
    )

    if portfolio_type=="Conservative":
        portfolio=conservative

    elif portfolio_type=="Balanced":
        portfolio=balanced

    else:
        portfolio=aggressive

    st.subheader(f"{portfolio_type} Portfolio")

    st.dataframe(
        portfolio[
            ['Symbol','Weight','Justification']
        ]
    )
    fig = px.pie(
    portfolio,
    names='Symbol',
    values='Weight',
    title='Portfolio Allocation'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.download_button(
    "Download Portfolio",
    portfolio.to_csv(index=False),
    file_name=f"{portfolio_type}_portfolio.csv",
    mime="text/csv"
    )

elif page == "Investment Insights":

    st.header("💡 Investment Insights")

    best_return = portfolio_df.loc[
        portfolio_df['Total_Return'].idxmax()
    ]

    best_sharpe = risk_df.loc[
        risk_df['Sharpe_Ratio'].idxmax()
    ]

    lowest_vol = risk_df.loc[
        risk_df['Volatility'].idxmin()
    ]

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Highest Return Stock",
        best_return['Symbol']
    )

    col2.metric(
        "Best Sharpe Ratio",
        best_sharpe['Symbol']
    )

    col3.metric(
        "Lowest Volatility",
        lowest_vol['Symbol']
    )    

    st.subheader("Top Investment Opportunities")

    st.write(
       f"🏆 Highest Historical Return: "
       f"{best_return['Symbol']} "
       f"({best_return['Total_Return']:.2f}%)"
    )

    st.write(
       f"📈 Best Risk Adjusted Performance: "
       f"{best_sharpe['Symbol']} "
       f"(Sharpe Ratio = {best_sharpe['Sharpe_Ratio']:.2f})"
    )

    st.write(
       f"🛡️ Most Stable Stock: "
       f"{lowest_vol['Symbol']} "
       f"(Volatility = {lowest_vol['Volatility']:.2f})"
    )

    st.subheader("Investor Recommendations")

    st.success(
       "Conservative Investors: Choose the Conservative Portfolio for stability and lower risk."
    )

    st.info(
       "Balanced Investors: Choose the Balanced Portfolio for a mix of growth and stability."
    )

    st.warning(
       "Aggressive Investors: Choose the Aggressive Portfolio for maximum growth potential with higher risk."
    )

    top10 = portfolio_df.sort_values(
      'Total_Return',
      ascending=False
      ).head(10)

    st.subheader("Top 10 Performing Stocks")

    st.dataframe(
      top10[['Symbol','Total_Return']]
    )     
    fig = px.bar(
    top10,
    x='Symbol',
    y='Total_Return',
    title='Top 10 Performing Stocks'
    )

    st.plotly_chart(fig, use_container_width=True)

    