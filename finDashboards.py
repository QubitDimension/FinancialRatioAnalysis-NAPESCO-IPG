import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import PercentFormatter
plt.style.use('ggplot')
sns.set_palette("Set2")


if not os.path.exists('dashboards'):
    os.makedirs('dashboards')
    print("Created 'dashboards' directory")

# Dataframes with financial data for both companies
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
    'Current_Liabilities': [7271359, 11883710],
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


def calculate_ratios(df, company_name):
    """
    Calculate comprehensive financial ratios for analysis
    This function computes liquidity, profitability, efficiency, and solvency ratios
    """
    ratios = pd.DataFrame()
    ratios['Year'] = df['Year']
    ratios['Company'] = company_name

    # Liquidity Ratios - measure short-term debt paying ability
    ratios['Current_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']
    ratios['Quick_Ratio'] = (df['Current_Assets'] -
                             df['Inventory']) / df['Current_Liabilities']
    ratios['Cash_Ratio'] = df['Cash_Equivalents'] / df['Current_Liabilities']

    # Profitability Ratios - measure company's ability to generate profits
    ratios['Gross_Profit_Margin'] = df['Gross_Profit'] / df['Revenue']
    ratios['Operating_Profit_Margin'] = df['Operating_Income'] / df['Revenue']
    ratios['Net_Profit_Margin'] = df['Net_Income'] / df['Revenue']
    ratios['ROA'] = df['Net_Income'] / df['Total_Assets']
    ratios['ROE'] = df['Net_Income'] / df['Shareholders_Equity']

    # Efficiency Ratios - measure how well company uses its assets
    ratios['Asset_Turnover'] = df['Revenue'] / df['Total_Assets']
    ratios['Inventory_Turnover'] = df['Cost_of_Sales'] / df['Inventory']
    ratios['Days_Inventory_Outstanding'] = 365 / ratios['Inventory_Turnover']
    ratios['Receivables_Turnover'] = df['Revenue'] / df['Accounts_Receivable']
    ratios['Days_Sales_Outstanding'] = 365 / ratios['Receivables_Turnover']
    ratios['Payables_Turnover'] = df['Cost_of_Sales'] / df['Accounts_Payable']
    ratios['Days_Payables_Outstanding'] = 365 / ratios['Payables_Turnover']

    # Solvency Ratios - measure long-term debt paying ability
    ratios['Debt_Ratio'] = df['Total_Liabilities'] / df['Total_Assets']
    ratios['Debt_to_Equity'] = df['Total_Liabilities'] / \
        df['Shareholders_Equity']
    ratios['Equity_Multiplier'] = df['Total_Assets'] / \
        df['Shareholders_Equity']

    return ratios


# Calculate ratios for both companies
napesco_ratios = calculate_ratios(napesco_df, 'NAPESCO')
ipg_ratios = calculate_ratios(ipg_df, 'IPG')
combined_ratios = pd.concat([napesco_ratios, ipg_ratios], axis=0)


def create_ratio_comparison_chart(combined_df, ratio_name, title, formatted_as_percentage=False, filename=None):
    """
    Create individual ratio comparison charts between the two companies
    """
    plt.figure(figsize=(10, 6))

    napesco_data = combined_df[(combined_df['Company'] == 'NAPESCO')]
    ipg_data = combined_df[(combined_df['Company'] == 'IPG')]

    # Create side-by-side bars for comparison
    width = 0.35
    x = np.arange(len(napesco_data['Year']))

    plt.bar(x - width/2, napesco_data[ratio_name], width, label='NAPESCO')
    plt.bar(x + width/2, ipg_data[ratio_name], width, label='IPG')

    plt.xlabel('Year')
    plt.ylabel(ratio_name.replace('_', ' '))
    plt.title(title)
    plt.xticks(x, napesco_data['Year'])
    plt.legend()

    # Format as percentage if specified
    if formatted_as_percentage:
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))

    plt.tight_layout()

    if filename:
        plt.savefig(f'dashboards/{filename}', dpi=300, bbox_inches='tight')
        print(f"Saved: dashboards/{filename}")

    plt.close()


def create_comprehensive_liquidity_dashboard(napesco_ratios, ipg_ratios, filename=None):
    """
    Create comprehensive dashboard for all liquidity ratios
    Liquidity ratios help assess a company's ability to meet short-term obligations
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Comprehensive Liquidity Analysis',
                 fontsize=16, fontweight='bold')

    # Current Ratio - measures ability to pay short-term debts
    axes[0, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Current_Ratio'], napesco_ratios.iloc[1]['Current_Ratio']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Current_Ratio'], ipg_ratios.iloc[1]['Current_Ratio']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 0].set_title('Current Ratio')
    axes[0, 0].set_ylabel('Ratio')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Quick Ratio - more conservative liquidity measure (excludes inventory)
    axes[0, 1].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Quick_Ratio'], napesco_ratios.iloc[1]['Quick_Ratio']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 1].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Quick_Ratio'], ipg_ratios.iloc[1]['Quick_Ratio']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 1].set_title('Quick Ratio')
    axes[0, 1].set_ylabel('Ratio')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Cash Ratio - most conservative liquidity measure (only cash and equivalents)
    axes[1, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Cash_Ratio'], napesco_ratios.iloc[1]['Cash_Ratio']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Cash_Ratio'], ipg_ratios.iloc[1]['Cash_Ratio']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 0].set_title('Cash Ratio')
    axes[1, 0].set_ylabel('Ratio')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Liquidity Trend Analysis - shows how liquidity positions are changing
    axes[1, 1].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Current_Ratio'], napesco_ratios.iloc[1]['Current_Ratio']],
                    'o-', linewidth=3, markersize=8, label='NAPESCO Current')
    axes[1, 1].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Quick_Ratio'], napesco_ratios.iloc[1]['Quick_Ratio']],
                    's-', linewidth=3, markersize=8, label='NAPESCO Quick')
    axes[1, 1].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Current_Ratio'], ipg_ratios.iloc[1]['Current_Ratio']],
                    '^-', linewidth=3, markersize=8, label='IPG Current')
    axes[1, 1].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Quick_Ratio'], ipg_ratios.iloc[1]['Quick_Ratio']],
                    'd-', linewidth=3, markersize=8, label='IPG Quick')
    axes[1, 1].set_title('Liquidity Trends')
    axes[1, 1].set_ylabel('Ratio')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()

    if filename:
        plt.savefig(f'dashboards/{filename}', dpi=300, bbox_inches='tight')
        print(f"Saved: dashboards/{filename}")

    plt.close()


def create_comprehensive_profitability_dashboard(napesco_ratios, ipg_ratios, filename=None):
    """
    Create comprehensive dashboard for all profitability ratios
    Profitability ratios measure how effectively a company generates profits
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Comprehensive Profitability Analysis',
                 fontsize=16, fontweight='bold')

    # Gross Profit Margin - measures efficiency of production
    axes[0, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Gross_Profit_Margin'], napesco_ratios.iloc[1]['Gross_Profit_Margin']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Gross_Profit_Margin'], ipg_ratios.iloc[1]['Gross_Profit_Margin']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 0].set_title('Gross Profit Margin')
    axes[0, 0].set_ylabel('Percentage')
    axes[0, 0].yaxis.set_major_formatter(PercentFormatter(1.0))
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Operating Profit Margin - measures operational efficiency
    axes[0, 1].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Operating_Profit_Margin'], napesco_ratios.iloc[1]['Operating_Profit_Margin']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 1].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Operating_Profit_Margin'], ipg_ratios.iloc[1]['Operating_Profit_Margin']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 1].set_title('Operating Profit Margin')
    axes[0, 1].set_ylabel('Percentage')
    axes[0, 1].yaxis.set_major_formatter(PercentFormatter(1.0))
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Net Profit Margin - overall profitability after all expenses
    axes[0, 2].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Net_Profit_Margin'], napesco_ratios.iloc[1]['Net_Profit_Margin']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 2].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Net_Profit_Margin'], ipg_ratios.iloc[1]['Net_Profit_Margin']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 2].set_title('Net Profit Margin')
    axes[0, 2].set_ylabel('Percentage')
    axes[0, 2].yaxis.set_major_formatter(PercentFormatter(1.0))
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)

    # ROA - Return on Assets measures asset utilization efficiency
    axes[1, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['ROA'], napesco_ratios.iloc[1]['ROA']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['ROA'], ipg_ratios.iloc[1]['ROA']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 0].set_title('Return on Assets (ROA)')
    axes[1, 0].set_ylabel('Percentage')
    axes[1, 0].yaxis.set_major_formatter(PercentFormatter(1.0))
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # ROE - Return on Equity measures returns to shareholders
    axes[1, 1].bar(['2022', '2023'], [napesco_ratios.iloc[0]['ROE'], napesco_ratios.iloc[1]['ROE']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 1].bar(['2022', '2023'], [ipg_ratios.iloc[0]['ROE'], ipg_ratios.iloc[1]['ROE']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 1].set_title('Return on Equity (ROE)')
    axes[1, 1].set_ylabel('Percentage')
    axes[1, 1].yaxis.set_major_formatter(PercentFormatter(1.0))
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # Profitability Trend Analysis - shows how profitability is evolving
    axes[1, 2].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Gross_Profit_Margin'], napesco_ratios.iloc[1]['Gross_Profit_Margin']],
                    'o-', linewidth=3, markersize=8, label='NAPESCO Gross')
    axes[1, 2].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Net_Profit_Margin'], napesco_ratios.iloc[1]['Net_Profit_Margin']],
                    's-', linewidth=3, markersize=8, label='NAPESCO Net')
    axes[1, 2].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Gross_Profit_Margin'], ipg_ratios.iloc[1]['Gross_Profit_Margin']],
                    '^-', linewidth=3, markersize=8, label='IPG Gross')
    axes[1, 2].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Net_Profit_Margin'], ipg_ratios.iloc[1]['Net_Profit_Margin']],
                    'd-', linewidth=3, markersize=8, label='IPG Net')
    axes[1, 2].set_title('Profitability Trends')
    axes[1, 2].set_ylabel('Percentage')
    axes[1, 2].yaxis.set_major_formatter(PercentFormatter(1.0))
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)

    plt.tight_layout()

    if filename:
        plt.savefig(f'dashboards/{filename}', dpi=300, bbox_inches='tight')
        print(f"Saved: dashboards/{filename}")

    plt.close()


def create_comprehensive_efficiency_dashboard(napesco_ratios, ipg_ratios, filename=None):
    """
    Create comprehensive dashboard for all efficiency ratios
    Efficiency ratios measure how well a company manages its assets and operations
    """
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle('Comprehensive Efficiency Analysis',
                 fontsize=16, fontweight='bold')

    # Asset Turnover - measures how efficiently assets generate revenue
    axes[0, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Asset_Turnover'], napesco_ratios.iloc[1]['Asset_Turnover']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Asset_Turnover'], ipg_ratios.iloc[1]['Asset_Turnover']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 0].set_title('Asset Turnover')
    axes[0, 0].set_ylabel('Times')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Inventory Turnover - measures how quickly inventory is sold
    axes[0, 1].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Inventory_Turnover'], napesco_ratios.iloc[1]['Inventory_Turnover']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 1].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Inventory_Turnover'], ipg_ratios.iloc[1]['Inventory_Turnover']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 1].set_title('Inventory Turnover')
    axes[0, 1].set_ylabel('Times')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Receivables Turnover - measures how quickly receivables are collected
    axes[0, 2].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Receivables_Turnover'], napesco_ratios.iloc[1]['Receivables_Turnover']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 2].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Receivables_Turnover'], ipg_ratios.iloc[1]['Receivables_Turnover']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 2].set_title('Receivables Turnover')
    axes[0, 2].set_ylabel('Times')
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)

    # Payables Turnover - measures how quickly company pays suppliers
    axes[1, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Payables_Turnover'], napesco_ratios.iloc[1]['Payables_Turnover']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Payables_Turnover'], ipg_ratios.iloc[1]['Payables_Turnover']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 0].set_title('Payables Turnover')
    axes[1, 0].set_ylabel('Times')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Days Inventory Outstanding - average days to sell inventory
    axes[1, 1].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Days_Inventory_Outstanding'], napesco_ratios.iloc[1]['Days_Inventory_Outstanding']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 1].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Days_Inventory_Outstanding'], ipg_ratios.iloc[1]['Days_Inventory_Outstanding']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 1].set_title('Days Inventory Outstanding')
    axes[1, 1].set_ylabel('Days')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    # Days Sales Outstanding - average days to collect receivables
    axes[1, 2].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Days_Sales_Outstanding'], napesco_ratios.iloc[1]['Days_Sales_Outstanding']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 2].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Days_Sales_Outstanding'], ipg_ratios.iloc[1]['Days_Sales_Outstanding']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 2].set_title('Days Sales Outstanding')
    axes[1, 2].set_ylabel('Days')
    axes[1, 2].legend()
    axes[1, 2].grid(True, alpha=0.3)

    # Days Payables Outstanding - average days to pay suppliers
    axes[2, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Days_Payables_Outstanding'], napesco_ratios.iloc[1]['Days_Payables_Outstanding']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[2, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Days_Payables_Outstanding'], ipg_ratios.iloc[1]['Days_Payables_Outstanding']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[2, 0].set_title('Days Payables Outstanding')
    axes[2, 0].set_ylabel('Days')
    axes[2, 0].legend()
    axes[2, 0].grid(True, alpha=0.3)

    # Working Capital Cycle (Cash Conversion Cycle) - measures working capital efficiency
    napesco_ccc_2022 = napesco_ratios.iloc[0]['Days_Inventory_Outstanding'] + \
        napesco_ratios.iloc[0]['Days_Sales_Outstanding'] - \
        napesco_ratios.iloc[0]['Days_Payables_Outstanding']
    napesco_ccc_2023 = napesco_ratios.iloc[1]['Days_Inventory_Outstanding'] + \
        napesco_ratios.iloc[1]['Days_Sales_Outstanding'] - \
        napesco_ratios.iloc[1]['Days_Payables_Outstanding']
    ipg_ccc_2022 = ipg_ratios.iloc[0]['Days_Inventory_Outstanding'] + \
        ipg_ratios.iloc[0]['Days_Sales_Outstanding'] - \
        ipg_ratios.iloc[0]['Days_Payables_Outstanding']
    ipg_ccc_2023 = ipg_ratios.iloc[1]['Days_Inventory_Outstanding'] + \
        ipg_ratios.iloc[1]['Days_Sales_Outstanding'] - \
        ipg_ratios.iloc[1]['Days_Payables_Outstanding']

    axes[2, 1].bar(['2022', '2023'], [napesco_ccc_2022, napesco_ccc_2023],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[2, 1].bar(['2022', '2023'], [ipg_ccc_2022, ipg_ccc_2023],
                   width=0.4, label='IPG', alpha=0.8)
    axes[2, 1].set_title('Cash Conversion Cycle')
    axes[2, 1].set_ylabel('Days')
    axes[2, 1].legend()
    axes[2, 1].grid(True, alpha=0.3)

    # Efficiency Trends - shows how operational efficiency is changing
    axes[2, 2].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Asset_Turnover'], napesco_ratios.iloc[1]['Asset_Turnover']],
                    'o-', linewidth=3, markersize=8, label='NAPESCO Asset TO')
    axes[2, 2].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Inventory_Turnover'], napesco_ratios.iloc[1]['Inventory_Turnover']],
                    's-', linewidth=3, markersize=8, label='NAPESCO Inventory TO')
    axes[2, 2].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Asset_Turnover'], ipg_ratios.iloc[1]['Asset_Turnover']],
                    '^-', linewidth=3, markersize=8, label='IPG Asset TO')
    # Scale down IPG inventory turnover for better visualization (it's much higher)
    axes[2, 2].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Inventory_Turnover']/10, ipg_ratios.iloc[1]['Inventory_Turnover']/10],
                    'd-', linewidth=3, markersize=8, label='IPG Inventory TO/10')
    axes[2, 2].set_title('Efficiency Trends')
    axes[2, 2].set_ylabel('Turnover Ratio')
    axes[2, 2].legend()
    axes[2, 2].grid(True, alpha=0.3)

    plt.tight_layout()

    if filename:
        plt.savefig(f'dashboards/{filename}', dpi=300, bbox_inches='tight')
        print(f"Saved: dashboards/{filename}")

    plt.close()


def create_comprehensive_solvency_dashboard(napesco_ratios, ipg_ratios, filename=None):
    """
    Create comprehensive dashboard for all solvency ratios
    Solvency ratios measure a company's ability to meet long-term obligations
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Comprehensive Solvency Analysis',
                 fontsize=16, fontweight='bold')

    # Debt Ratio - measures proportion of assets financed by debt
    axes[0, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Debt_Ratio'], napesco_ratios.iloc[1]['Debt_Ratio']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Debt_Ratio'], ipg_ratios.iloc[1]['Debt_Ratio']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 0].set_title('Debt Ratio')
    axes[0, 0].set_ylabel('Ratio')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Debt to Equity - measures financial leverage
    axes[0, 1].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Debt_to_Equity'], napesco_ratios.iloc[1]['Debt_to_Equity']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[0, 1].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Debt_to_Equity'], ipg_ratios.iloc[1]['Debt_to_Equity']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[0, 1].set_title('Debt-to-Equity Ratio')
    axes[0, 1].set_ylabel('Ratio')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Equity Multiplier - measures financial leverage from assets perspective
    axes[1, 0].bar(['2022', '2023'], [napesco_ratios.iloc[0]['Equity_Multiplier'], napesco_ratios.iloc[1]['Equity_Multiplier']],
                   width=0.4, label='NAPESCO', alpha=0.8)
    axes[1, 0].bar(['2022', '2023'], [ipg_ratios.iloc[0]['Equity_Multiplier'], ipg_ratios.iloc[1]['Equity_Multiplier']],
                   width=0.4, label='IPG', alpha=0.8)
    axes[1, 0].set_title('Equity Multiplier')
    axes[1, 0].set_ylabel('Times')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Solvency Trends - shows how leverage and solvency are changing over time
    axes[1, 1].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Debt_Ratio'], napesco_ratios.iloc[1]['Debt_Ratio']],
                    'o-', linewidth=3, markersize=8, label='NAPESCO Debt Ratio')
    axes[1, 1].plot(['2022', '2023'], [napesco_ratios.iloc[0]['Debt_to_Equity'], napesco_ratios.iloc[1]['Debt_to_Equity']],
                    's-', linewidth=3, markersize=8, label='NAPESCO D/E')
    axes[1, 1].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Debt_Ratio'], ipg_ratios.iloc[1]['Debt_Ratio']],
                    '^-', linewidth=3, markersize=8, label='IPG Debt Ratio')
    axes[1, 1].plot(['2022', '2023'], [ipg_ratios.iloc[0]['Debt_to_Equity'], ipg_ratios.iloc[1]['Debt_to_Equity']],
                    'd-', linewidth=3, markersize=8, label='IPG D/E')
    axes[1, 1].set_title('Solvency Trends')
    axes[1, 1].set_ylabel('Ratio')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()

    if filename:
        plt.savefig(f'dashboards/{filename}', dpi=300, bbox_inches='tight')
        print(f"Saved: dashboards/{filename}")

    plt.close()


def generate_financial_summary_report(napesco_ratios, ipg_ratios):
    """
    Generate a comprehensive text summary of the financial analysis
    This provides key insights and interpretations of the ratio analysis
    """
    print("="*60)
    print("COMPREHENSIVE FINANCIAL ANALYSIS REPORT")
    print("NAPESCO vs IPG - 2022 to 2023 Comparison")
    print("="*60)

    print("\n1. LIQUIDITY ANALYSIS:")
    print("-" * 25)
    print(
        f"NAPESCO Current Ratio: {napesco_ratios.iloc[0]['Current_Ratio']:.2f} (2022) → {napesco_ratios.iloc[1]['Current_Ratio']:.2f} (2023)")
    print(
        f"IPG Current Ratio: {ipg_ratios.iloc[0]['Current_Ratio']:.2f} (2022) → {ipg_ratios.iloc[1]['Current_Ratio']:.2f} (2023)")
    print(f"Interpretation: Both companies show strong liquidity positions above 1.0, with NAPESCO showing superior liquidity ratios.")

    print("\n2. PROFITABILITY ANALYSIS:")
    print("-" * 27)
    print(
        f"NAPESCO Net Profit Margin: {napesco_ratios.iloc[0]['Net_Profit_Margin']:.2%} (2022) → {napesco_ratios.iloc[1]['Net_Profit_Margin']:.2%} (2023)")
    print(
        f"IPG Net Profit Margin: {ipg_ratios.iloc[0]['Net_Profit_Margin']:.2%} (2022) → {ipg_ratios.iloc[1]['Net_Profit_Margin']:.2%} (2023)")
    print(
        f"NAPESCO ROE: {napesco_ratios.iloc[0]['ROE']:.2%} (2022) → {napesco_ratios.iloc[1]['ROE']:.2%} (2023)")
    print(
        f"IPG ROE: {ipg_ratios.iloc[0]['ROE']:.2%} (2022) → {ipg_ratios.iloc[1]['ROE']:.2%} (2023)")
    print(f"Interpretation: NAPESCO demonstrates significantly higher profitability margins and better return on equity.")

    print("\n3. EFFICIENCY ANALYSIS:")
    print("-" * 23)
    print(
        f"NAPESCO Asset Turnover: {napesco_ratios.iloc[0]['Asset_Turnover']:.2f} (2022) → {napesco_ratios.iloc[1]['Asset_Turnover']:.2f} (2023)")
    print(
        f"IPG Asset Turnover: {ipg_ratios.iloc[0]['Asset_Turnover']:.2f} (2022) → {ipg_ratios.iloc[1]['Asset_Turnover']:.2f} (2023)")
    print(f"Interpretation: IPG shows higher asset turnover, indicating more efficient asset utilization for revenue generation.")

    print("\n4. SOLVENCY ANALYSIS:")
    print("-" * 22)
    print(
        f"NAPESCO Debt-to-Equity: {napesco_ratios.iloc[0]['Debt_to_Equity']:.2f} (2022) → {napesco_ratios.iloc[1]['Debt_to_Equity']:.2f} (2023)")
    print(
        f"IPG Debt-to-Equity: {ipg_ratios.iloc[0]['Debt_to_Equity']:.2f} (2022) → {ipg_ratios.iloc[1]['Debt_to_Equity']:.2f} (2023)")
    print(f"Interpretation: Both companies maintain conservative debt levels, with IPG showing higher leverage.")

    print("\n" + "="*60)


def main():
    """
    Main execution function to run the complete financial analysis
    This orchestrates all the analysis functions and generates comprehensive output
    """
    print("Starting Comprehensive Financial Analysis...")
    print("Generating ratio calculations and visualizations...\n")

    # Generate all comprehensive dashboards with descriptive names
    create_comprehensive_liquidity_dashboard(
        napesco_ratios, ipg_ratios, 'napesco_ipg_liquidity_analysis.png')
    create_comprehensive_profitability_dashboard(
        napesco_ratios, ipg_ratios, 'napesco_ipg_profitability_analysis.png')
    create_comprehensive_efficiency_dashboard(
        napesco_ratios, ipg_ratios, 'napesco_ipg_efficiency_analysis.png')
    create_comprehensive_solvency_dashboard(
        napesco_ratios, ipg_ratios, 'napesco_ipg_solvency_analysis.png')

    # Generate individual ratio comparisons for key metrics
    create_ratio_comparison_chart(combined_ratios, 'Current_Ratio',
                                  'Current Ratio Comparison', filename='napesco_ipg_current_ratio_comparison.png')
    create_ratio_comparison_chart(combined_ratios, 'Net_Profit_Margin', 'Net Profit Margin Comparison',
                                  formatted_as_percentage=True, filename='napesco_ipg_net_profit_margin_comparison.png')
    create_ratio_comparison_chart(combined_ratios, 'ROE', 'Return on Equity Comparison',
                                  formatted_as_percentage=True, filename='napesco_ipg_roe_comparison.png')
    create_ratio_comparison_chart(combined_ratios, 'Asset_Turnover',
                                  'Asset Turnover Comparison', filename='napesco_ipg_asset_turnover_comparison.png')

    # Display comprehensive summary report
    generate_financial_summary_report(napesco_ratios, ipg_ratios)

    # Display calculated ratios in tabular format for detailed review
    print("\nDETAILED RATIO TABLES:")
    print("\nNAPESCO Financial Ratios:")
    print(napesco_ratios.round(4))
    print("\nIPG Financial Ratios:")
    print(ipg_ratios.round(4))

    print("\nAnalysis completed successfully!")
    print("All charts have been saved in the 'dashboards' folder for further review and presentation.")


# Execute the main analysis
if __name__ == "__main__":
    main()
