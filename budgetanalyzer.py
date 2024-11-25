import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# App Title
st.title("Personal Budget Analyzer, Savings Predictor, and Investment Planner")

# Sidebar for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Select a section:", 
    ["Home", "Income Input", "Expense Input", "Spending Analysis", "Savings Prediction", "Investment Planning"]
)

# Home Section
if menu == "Home":
    st.header("Welcome to the Personal Finance Tool")
    st.write("""
        This tool helps you:
        - Analyze your monthly expenses
        - Predict future savings
        - Plan your investments
    """)
    st.image("finance_dashboard.jpg", caption="Manage your finances effectively.")  # Replace with your image path.

# Monthly Income Input Section
elif menu == "Income Input":
    st.header("Enter Your Monthly Income")
    
    # Input for monthly income
    monthly_income = st.number_input(
        "Enter your total monthly income ($):", 
        min_value=0.0, 
        step=100.0
    )
    
    if st.button("Save Income"):
        # Save the income to a file (e.g., text file for simplicity)
        with open("income.txt", "w") as f:
            f.write(str(monthly_income))
        st.success("Monthly income saved successfully!")

# Expense Input Section
elif menu == "Expense Input":
    st.header("Enter Your Monthly Expenses")
    categories = ["Rent", "Utilities", "Groceries", "Transportation", "Entertainment", "Others"]
    expenses = {}

    for category in categories:
        expenses[category] = st.number_input(f"Enter your expense for {category} ($):", min_value=0.0, step=10.0)
    
    if st.button("Save Expenses"):
        expenses_df = pd.DataFrame([expenses])
        expenses_df.to_csv("expenses.csv", index=False)
        st.success("Expenses saved!")

# Spending Analysis Section
elif menu == "Spending Analysis":
    st.header("Spending Analysis")
    try:
        expenses_df = pd.read_csv("expenses.csv")
        st.write("Your Monthly Expenses:")
        st.write(expenses_df)
        
        # Visualize Spending
        fig, ax = plt.subplots()
        expenses_df.sum().plot(kind="pie", ax=ax, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig)
        
        # Compare with income if available
        try:
            with open("income.txt", "r") as f:
                monthly_income = float(f.read())
            total_expenses = expenses_df.sum().sum()
            savings_potential = monthly_income - total_expenses
            st.write(f"Your total expenses: ${total_expenses:.2f}")
            st.write(f"Your monthly savings potential: ${savings_potential:.2f}")
        except FileNotFoundError:
            st.warning("Monthly income not provided. Please input it in the 'Income Input' section.")
    except FileNotFoundError:
        st.warning("No expense data found. Please input expenses first.")

# Savings Prediction Section
elif menu == "Savings Prediction":
    st.header("Predict Your Savings")
    try:
        expenses_df = pd.read_csv("expenses.csv")
        savings_goal = st.number_input("Enter your monthly savings goal ($):", min_value=0.0, step=10.0)
        
        # Simple Linear Regression (dummy data for demo)
        historical_expenses = np.random.rand(12, 1) * 1000  # Random data for demo
        historical_savings = np.random.rand(12) * 500  # Random data for demo
        model = LinearRegression()
        model.fit(historical_expenses, historical_savings)
        future_expense = np.array([[expenses_df.sum().sum()]])
        predicted_savings = model.predict(future_expense)
        st.write(f"Predicted Savings: ${predicted_savings[0]:.2f}")
    except FileNotFoundError:
        st.warning("No expense data found. Please input expenses first.")

# Investment Planning Section
elif menu == "Investment Planning":
    st.header("Investment Planning")
    risk_tolerance = st.selectbox("Select your risk tolerance:", ["Low", "Medium", "High"])
    time_horizon = st.slider("Select your investment time horizon (years):", 1, 30, 5)
    
    st.write(f"Based on your preferences, here are some suggestions:")
    if risk_tolerance == "Low":
        st.write("- Bonds, Treasury Notes")
    elif risk_tolerance == "Medium":
        st.write("- Balanced Mutual Funds, Index Funds")
    else:
        st.write("- Stocks, ETFs")
    
    if st.button("Simulate Investment Growth"):
        years = np.arange(1, time_horizon + 1)
        returns = np.random.normal(0.1, 0.02, len(years))  # Dummy growth rate
        investment_growth = (1 + returns).cumprod()
        fig, ax = plt.subplots()
        ax.plot(years, investment_growth)
        st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Project by Thomas Feely, Lucas Longfellow, Zach Cheney, Michael Duffy")
