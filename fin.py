import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter
plt.style.use('ggplot')
sns.set_palette("Set2")

# Create dataframes with financial data for both companies
# Financial data for NAPESCO
napesco_data = {
    'Year': [2022, 2023],
    'Revenue': [37184789, 39522799],
    'Cost_of_Sales': [27854616, 28650618],
    'Gross_Profit': [9330173, 10872181],
    'Operating_Income': [7287144, 9123378],
    'Net_Income': [6824101, 8595511],
    'Current_Assets': [40462604, 37040597],
    'Inventory': [5479455, 4531445],
    'Accounts_Receivable': [13366220, 12655113],
    'Cash_Equivalents': [2180992, 2660961],
    'Total_Assets': [53151614, 70683248],
    'Current_Liabilities': [7271369, 11883710],
    'Total_Liabilities': [10888314, 14717109],
    'Shareholders_Equity': [42263300, 55966139],
    'Operating_Cash_Flow': [10956411, 12565079],
    'Depreciation': [2183024, 2535625],
    'Accounts_Payable': [7057298, 11650349],
    'EPS_Fils': [70.35, 88.66]
}

# Financial data for IPG
ipg_data = {
    'Year': [2022, 2023],
    'Revenue': [1646039000, 1067544000],
    'Cost_of_Sales': [1621337000, 1049408000],
    'Gross_Profit': [24702000, 18136000],
    'Operating_Income': [8037000, 8205000],
    'Net_Income': [7656000, 7818000],
    'Current_Assets': [316031000, 375971000],
    'Inventory': [51741000, 27236000],
    'Accounts_Receivable': [72997000, 187345000],
    'Cash_Equivalents': [108513000, 79298000],
    'Total_Assets': [439037000, 493470000],
    'Current_Liabilities': [291838000, 359199000],
    'Total_Liabilities': [338975000, 388821000],
    'Shareholders_Equity': [100062000, 104649000],
    'Operating_Cash_Flow': [15399000, -16691000],
    'Depreciation': [1806000, 1677000],
    'Accounts_Payable': [90011000, 149771000],
    'EPS_Fils': [42.35, 43.24]
}

napesco_df = pd.DataFrame(napesco_data)
ipg_df = pd.DataFrame(ipg_data)

# Calculate ratios for both companies


def calculate_ratios(df, company_name):
    ratios = pd.DataFrame()
    ratios['Year'] = df['Year']
    ratios['Company'] = company_name

    # Liquidity Ratios
    ratios['Current_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']
    ratios['Quick_Ratio'] = (df['Current_Assets'] -
                             df['Inventory']) / df['Current_Liabilities']
    ratios['Cash_Ratio'] = df['Cash_Equivalents'] / df['Current_Liabilities']

    # Profitability Ratios
    ratios['Gross_Profit_Margin'] = df['Gross_Profit'] / df['Revenue']
    ratios['Operating_Profit_Margin'] = df['Operating_Income'] / df['Revenue']
    ratios['Net_Profit_Margin'] = df['Net_Income'] / df['Revenue']
    ratios['ROA'] = df['Net_Income'] / df['Total_Assets']
    ratios['ROE'] = df['Net_Income'] / df['Shareholders_Equity']

    # Efficiency Ratios
    ratios['Asset_Turnover'] = df['Revenue'] / df['Total_Assets']
    ratios['Inventory_Turnover'] = df['Cost_of_Sales'] / df['Inventory']
    ratios['Days_Inventory_Outstanding'] = 365 / ratios['Inventory_Turnover']
    ratios['Receivables_Turnover'] = df['Revenue'] / df['Accounts_Receivable']
    ratios['Days_Sales_Outstanding'] = 365 / ratios['Receivables_Turnover']
    ratios['Payables_Turnover'] = df['Cost_of_Sales'] / df['Accounts_Payable']
    ratios['Days_Payables_Outstanding'] = 365 / ratios['Payables_Turnover']

    # Solvency Ratios
    ratios['Debt_Ratio'] = df['Total_Liabilities'] / df['Total_Assets']
    ratios['Debt_to_Equity'] = df['Total_Liabilities'] / \
        df['Shareholders_Equity']
    ratios['Equity_Multiplier'] = df['Total_Assets'] / \
        df['Shareholders_Equity']

    return ratios


napesco_ratios = calculate_ratios(napesco_df, 'NAPESCO')
ipg_ratios = calculate_ratios(ipg_df, 'IPG')

# Combine ratios for both companies
combined_ratios = pd.concat([napesco_ratios, ipg_ratios], axis=0)

# 1. Create and save visualization to compare key ratios between companies


def create_ratio_comparison_chart(combined_df, ratio_name, title, formatted_as_percentage=False, filename=None):
    plt.figure(figsize=(10, 6))

    napesco_data = combined_df[(combined_df['Company'] == 'NAPESCO')]
    ipg_data = combined_df[(combined_df['Company'] == 'IPG')]

    width = 0.35
    x = np.arange(len(napesco_data['Year']))

    plt.bar(x - width/2, napesco_data[ratio_name], width, label='NAPESCO')
    plt.bar(x + width/2, ipg_data[ratio_name], width, label='IPG')

    plt.xlabel('Year')
    plt.ylabel(ratio_name.replace('_', ' '))
    plt.title(title)
    plt.xticks(x, napesco_data['Year'])
    plt.legend()

    if formatted_as_percentage:
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))

    plt.tight_layout()

    if filename:
        plt.savefig(filename)
        print(f"Saved: {filename}")

    plt.close()  # Close the figure to free up memory

# 2. Create and save a comprehensive dashboard of key financial metrics


def create_financial_dashboard(napesco_ratios, ipg_ratios, filename=None):
    fig, axes = plt.subplots(3, 2, figsize=(15, 15))

    # Profitability comparison
    axes[0, 0].set_title('Profitability Comparison')
    axes[0, 0].plot(napesco_ratios['Year'], napesco_ratios['Net_Profit_Margin'],
                    'o-', label='NAPESCO Net Profit Margin')
    axes[0, 0].plot(ipg_ratios['Year'], ipg_ratios['Net_Profit_Margin'],
                    's-', label='IPG Net Profit Margin')
    axes[0, 0].plot(napesco_ratios['Year'],
                    napesco_ratios['ROE'], '^-', label='NAPESCO ROE')
    axes[0, 0].plot(ipg_ratios['Year'], ipg_ratios['ROE'],
                    'd-', label='IPG ROE')
    axes[0, 0].set_ylabel('Ratio Value')
    axes[0, 0].legend()
    axes[0, 0].yaxis.set_major_formatter(PercentFormatter(1.0))

    # Liquidity comparison
    axes[0, 1].set_title('Liquidity Comparison')
    axes[0, 1].plot(napesco_ratios['Year'], napesco_ratios['Current_Ratio'],
                    'o-', label='NAPESCO Current Ratio')
    axes[0, 1].plot(ipg_ratios['Year'], ipg_ratios['Current_Ratio'],
                    's-', label='IPG Current Ratio')
    axes[0, 1].plot(napesco_ratios['Year'], napesco_ratios['Quick_Ratio'],
                    '^-', label='NAPESCO Quick Ratio')
    axes[0, 1].plot(ipg_ratios['Year'], ipg_ratios['Quick_Ratio'],
                    'd-', label='IPG Quick Ratio')
    axes[0, 1].set_ylabel('Ratio Value')
    axes[0, 1].legend()

    # Efficiency comparison
    axes[1, 0].set_title('Efficiency Comparison')
    axes[1, 0].plot(napesco_ratios['Year'], napesco_ratios['Asset_Turnover'],
                    'o-', label='NAPESCO Asset Turnover')
    axes[1, 0].plot(ipg_ratios['Year'], ipg_ratios['Asset_Turnover'],
                    's-', label='IPG Asset Turnover')
    axes[1, 0].set_ylabel('Ratio Value')
    axes[1, 0].legend()

    # Solvency comparison
    axes[1, 1].set_title('Solvency Comparison')
    axes[1, 1].plot(napesco_ratios['Year'],
                    napesco_ratios['Debt_Ratio'], 'o-', label='NAPESCO Debt Ratio')
    axes[1, 1].plot(ipg_ratios['Year'], ipg_ratios['Debt_Ratio'],
                    's-', label='IPG Debt Ratio')
    axes[1, 1].plot(napesco_ratios['Year'], napesco_ratios['Debt_to_Equity'],
                    '^-', label='NAPESCO Debt-to-Equity')
    axes[1, 1].plot(ipg_ratios['Year'], ipg_ratios['Debt_to_Equity'],
                    'd-', label='IPG Debt-to-Equity')
    axes[1, 1].set_ylabel('Ratio Value')
    axes[1, 1].legend()

    # Working Capital Cycle
    axes[2, 0].set_title('Working Capital Cycle')
    axes[2, 0].plot(napesco_ratios['Year'],
                    napesco_ratios['Days_Inventory_Outstanding'], 'o-', label='NAPESCO DIO')
    axes[2, 0].plot(ipg_ratios['Year'],
                    ipg_ratios['Days_Inventory_Outstanding'], 's-', label='IPG DIO')
    axes[2, 0].plot(napesco_ratios['Year'],
                    napesco_ratios['Days_Sales_Outstanding'], '^-', label='NAPESCO DSO')
    axes[2, 0].plot(ipg_ratios['Year'],
                    ipg_ratios['Days_Sales_Outstanding'], 'd-', label='IPG DSO')
    axes[2, 0].plot(napesco_ratios['Year'],
                    napesco_ratios['Days_Payables_Outstanding'], '*-', label='NAPESCO DPO')
    axes[2, 0].plot(ipg_ratios['Year'],
                    ipg_ratios['Days_Payables_Outstanding'], 'x-', label='IPG DPO')
    axes[2, 0].set_ylabel('Days')
    axes[2, 0].legend()

    # DuPont Analysis
    axes[2, 1].set_title('DuPont Analysis Components (2023)')

    napesco_2023 = napesco_ratios[napesco_ratios['Year'] == 2023]
    ipg_2023 = ipg_ratios[ipg_ratios['Year'] == 2023]

    companies = ['NAPESCO', 'IPG']
    net_profit_margin = [napesco_2023['Net_Profit_Margin'].values[0],
                         ipg_2023['Net_Profit_Margin'].values[0]]
    asset_turnover = [napesco_2023['Asset_Turnover'].values[0],
                      ipg_2023['Asset_Turnover'].values[0]]
    equity_multiplier = [napesco_2023['Equity_Multiplier'].values[0],
                         ipg_2023['Equity_Multiplier'].values[0]]

    x = np.arange(len(companies))
    width = 0.25

    axes[2, 1].bar(x - width, net_profit_margin,
                   width, label='Net Profit Margin')
    axes[2, 1].bar(x, asset_turnover, width, label='Asset Turnover')
    axes[2, 1].bar(x + width, equity_multiplier,
                   width, label='Equity Multiplier')
    axes[2, 1].set_xticks(x)
    axes[2, 1].set_xticklabels(companies)
    axes[2, 1].legend()

    fig.tight_layout()

    if filename:
        plt.savefig(filename)
        print(f"Saved: {filename}")

    plt.close()  # Close the figure to free up memory

# 3. Create and save a radar chart for multidimensional financial comparison


def create_radar_chart(napesco_ratios, ipg_ratios, filename=None):
    # Extract 2023 data
    napesco_2023 = napesco_ratios[napesco_ratios['Year'] == 2023].iloc[0]
    ipg_2023 = ipg_ratios[ipg_ratios['Year'] == 2023].iloc[0]

    # Define categories and values
    categories = ['Profitability\n(Net Profit Margin)',
                  'Liquidity\n(Current Ratio)',
                  'Efficiency\n(Asset Turnover)',
                  'Solvency\n(Equity Multiplier)',
                  'Working Capital\nManagement\n(Cash Conversion Cycle)']

    # For demonstration, we'll use normalized values to make the chart readable
    # In practice, we'd need to normalize these properly based on industry benchmarks
    napesco_values = [
        napesco_2023['Net_Profit_Margin'],  # Profitability
        min(napesco_2023['Current_Ratio']/5, 1),  # Liquidity (capped at 1)
        napesco_2023['Asset_Turnover']/4,  # Efficiency
        1 - (napesco_2023['Equity_Multiplier']/5),  # Solvency (inverted)
        1 - min((napesco_2023['Days_Sales_Outstanding'] - napesco_2023['Days_Payables_Outstanding'] +
                napesco_2023['Days_Inventory_Outstanding'])/200, 1)  # Working Capital (inverted, lower is better)
    ]

    ipg_values = [
        ipg_2023['Net_Profit_Margin'],  # Profitability
        min(ipg_2023['Current_Ratio']/5, 1),  # Liquidity (capped at 1)
        ipg_2023['Asset_Turnover']/4,  # Efficiency
        1 - (ipg_2023['Equity_Multiplier']/5),  # Solvency (inverted)
        1 - min((ipg_2023['Days_Sales_Outstanding'] - ipg_2023['Days_Payables_Outstanding'] +
                ipg_2023['Days_Inventory_Outstanding'])/200, 1)  # Working Capital (inverted)
    ]

    # Create radar chart
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # close the loop

    napesco_values += napesco_values[:1]
    ipg_values += ipg_values[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.plot(angles, napesco_values, 'o-', linewidth=2, label='NAPESCO')
    ax.fill(angles, napesco_values, alpha=0.25)
    ax.plot(angles, ipg_values, 'o-', linewidth=2, label='IPG')
    ax.fill(angles, ipg_values, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 1)
    ax.set_title('Financial Performance Comparison (2023)')
    ax.legend(loc='upper right')
    ax.grid(True)

    if filename:
        plt.savefig(filename)
        print(f"Saved: {filename}")

    plt.close()  # Close the figure to free up memory

# 4. Create and save correlation heatmap for ratio relationships


def create_correlation_heatmap(ratios_df, company_name, filename=None):
    # Select numerical columns for correlation analysis
    correlation_columns = ['Current_Ratio', 'Quick_Ratio', 'Gross_Profit_Margin',
                           'Net_Profit_Margin', 'ROA', 'ROE', 'Asset_Turnover',
                           'Inventory_Turnover', 'Debt_Ratio', 'Debt_to_Equity']

    company_data = ratios_df[ratios_df['Company']
                             == company_name][correlation_columns]

    # Create correlation matrix
    corr_matrix = company_data.corr()

    # Create heatmap
    plt.figure(figsize=(12, 10))
    heatmap = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1,
                          linewidths=0.5, fmt=".2f")
    plt.title(f'Correlation Between Financial Ratios - {company_name}')
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
        print(f"Saved: {filename}")

    plt.close()  # Close the figure to free up memory

# 5. Create and save the financial efficiency matrix


def create_efficiency_matrix(napesco_ratios, ipg_ratios, filename=None):
    # Extract 2023 data
    napesco_2023 = napesco_ratios[napesco_ratios['Year'] == 2023].iloc[0]
    ipg_2023 = ipg_ratios[ipg_ratios['Year'] == 2023].iloc[0]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Define the mean lines for creating quadrants
    roe_mean = (napesco_2023['ROE'] + ipg_2023['ROE']) / 2
    liquidity_mean = (
        napesco_2023['Current_Ratio'] + ipg_2023['Current_Ratio']) / 2

    # Create quadrant lines
    ax.axhline(y=liquidity_mean, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=roe_mean, color='gray', linestyle='--', alpha=0.5)

    # Plot the companies
    ax.scatter(napesco_2023['ROE'], napesco_2023['Current_Ratio'],
               s=200, color='blue', label='NAPESCO 2023')
    ax.scatter(ipg_2023['ROE'], ipg_2023['Current_Ratio'],
               s=200, color='green', label='IPG 2023')

    # Add annotations
    ax.annotate('Higher profitability,\nHigher liquidity',
                xy=(0.75, 0.75), xycoords='axes fraction', fontsize=12)
    ax.annotate('Lower profitability,\nHigher liquidity',
                xy=(0.25, 0.75), xycoords='axes fraction', fontsize=12)
    ax.annotate('Higher profitability,\nLower liquidity',
                xy=(0.75, 0.25), xycoords='axes fraction', fontsize=12)
    ax.annotate('Lower profitability,\nLower liquidity',
                xy=(0.25, 0.25), xycoords='axes fraction', fontsize=12)

    ax.set_title(
        'Financial Efficiency Matrix: Profitability vs. Liquidity (2023)')
    ax.set_xlabel('Return on Equity (ROE)')
    ax.set_ylabel('Current Ratio')
    ax.legend()
    ax.grid(alpha=0.3)

    # Format axes as percentages for ROE
    ax.xaxis.set_major_formatter(PercentFormatter(1.0))

    if filename:
        plt.savefig(filename)
        print(f"Saved: {filename}")

    plt.close()  # Close the figure to free up memory


# Execute each chart one by one and save individually
print("Creating and saving individual charts:")

# Create comparison charts for key ratios
create_ratio_comparison_chart(combined_ratios, 'Net_Profit_Margin', 'Net Profit Margin Comparison',
                              True, 'net_profit_margin_comparison.png')

create_ratio_comparison_chart(combined_ratios, 'Current_Ratio', 'Current Ratio Comparison',
                              False, 'current_ratio_comparison.png')

create_ratio_comparison_chart(combined_ratios, 'Asset_Turnover', 'Asset Turnover Comparison',
                              False, 'asset_turnover_comparison.png')

create_ratio_comparison_chart(combined_ratios, 'Debt_to_Equity', 'Debt to Equity Comparison',
                              False, 'debt_to_equity_comparison.png')

# Create comprehensive dashboard
create_financial_dashboard(napesco_ratios, ipg_ratios,
                           'financial_dashboard.png')

# Create radar chart
create_radar_chart(napesco_ratios, ipg_ratios, 'radar_chart.png')

# Create correlation heatmaps
create_correlation_heatmap(combined_ratios, 'NAPESCO',
                           'napesco_correlation_heatmap.png')
create_correlation_heatmap(combined_ratios, 'IPG',
                           'ipg_correlation_heatmap.png')

# Create financial efficiency matrix
create_efficiency_matrix(napesco_ratios, ipg_ratios,
                         'financial_efficiency_matrix.png')

print("Financial ratio analysis complete. All visualizations have been saved individually.")
