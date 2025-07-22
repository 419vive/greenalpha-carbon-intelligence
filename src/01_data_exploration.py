#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 IEEE Fraud Detection - Data Exploration Script
Created for IEEE-CIS Fraud Detection Competition

目标 (Objectives):
1. 数据结构分析 - Analyze dataset structure and features
2. 数据质量评估 - Assess data quality and missing values 
3. 欺诈模式发现 - Discover fraud patterns and indicators
4. 特征分布理解 - Understand feature distributions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
from pathlib import Path

warnings.filterwarnings('ignore')

# 设置显示选项
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

# 设置图表样式
plt.style.use('default')
sns.set_palette("husl")

def load_data():
    """加载数据集"""
    print("🔄 Loading IEEE fraud detection dataset...")
    
    # 数据文件路径
    data_path = Path("ieee-fraud-detection")
    
    # 加载训练数据
    print("📊 Loading training transaction data...")
    train_transaction = pd.read_csv(data_path / "train_transaction.csv")
    print(f"✅ train_transaction shape: {train_transaction.shape}")
    
    print("📊 Loading training identity data...")
    train_identity = pd.read_csv(data_path / "train_identity.csv")
    print(f"✅ train_identity shape: {train_identity.shape}")
    
    # 内存使用情况
    print(f"\n💾 Memory usage:")
    print(f"train_transaction: {train_transaction.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"train_identity: {train_identity.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    return train_transaction, train_identity

def analyze_data_structure(train_transaction, train_identity):
    """分析数据结构"""
    print("\n" + "="*60)
    print("📊 DATA STRUCTURE ANALYSIS")
    print("="*60)
    
    # 交易数据结构
    print("\n🏦 TRANSACTION DATA STRUCTURE")
    print("-" * 40)
    print(f"Shape: {train_transaction.shape}")
    print(f"Columns: {len(train_transaction.columns)}")
    print(f"First 10 columns: {list(train_transaction.columns[:10])}")
    print("\nData types distribution:")
    print(train_transaction.dtypes.value_counts())
    
    # 身份数据结构
    print("\n🆔 IDENTITY DATA STRUCTURE")
    print("-" * 40)
    print(f"Shape: {train_identity.shape}")
    print(f"Columns: {len(train_identity.columns)}")
    print(f"First 10 columns: {list(train_identity.columns[:10])}")
    print("\nData types distribution:")
    print(train_identity.dtypes.value_counts())
    
    # 显示前几行
    print("\n🔍 Transaction Data Sample:")
    print(train_transaction.head(3))
    
    print("\n🔍 Identity Data Sample:")
    print(train_identity.head(3))

def analyze_target_variable(train_transaction):
    """分析目标变量"""
    print("\n" + "="*60)
    print("🎯 TARGET VARIABLE ANALYSIS")
    print("="*60)
    
    # 欺诈率分析
    fraud_rate = train_transaction['isFraud'].mean()
    fraud_count = train_transaction['isFraud'].sum()
    total_count = len(train_transaction)
    
    print(f"📈 FRAUD STATISTICS:")
    print(f"Total transactions: {total_count:,}")
    print(f"Fraudulent transactions: {fraud_count:,}")
    print(f"Legitimate transactions: {total_count - fraud_count:,}")
    print(f"Fraud rate: {fraud_rate:.4f} ({fraud_rate*100:.2f}%)")
    print(f"Class imbalance ratio: {(1-fraud_rate)/fraud_rate:.1f}:1")
    
    # 创建可视化
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # 条形图
    fraud_counts = train_transaction['isFraud'].value_counts()
    fraud_counts.plot(kind='bar', ax=axes[0], color=['lightblue', 'red'])
    axes[0].set_title('Fraud Distribution (Count)')
    axes[0].set_xlabel('isFraud')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=0)
    
    # 饼图
    fraud_counts.plot(kind='pie', ax=axes[1], autopct='%1.2f%%', 
                     colors=['lightblue', 'red'], labels=['Legitimate', 'Fraudulent'])
    axes[1].set_title('Fraud Distribution (Percentage)')
    axes[1].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('results/fraud_distribution.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    return fraud_rate

def analyze_missing_values(df, name):
    """分析缺失值情况"""
    print(f"\n📊 {name.upper()} - MISSING VALUES ANALYSIS")
    print("-" * 50)
    
    missing = df.isnull().sum()
    missing_pct = 100 * missing / len(df)
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_pct.values
    })
    
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Percentage', ascending=False)
    
    print(f"Total columns: {len(df.columns)}")
    print(f"Columns with missing values: {len(missing_df)}")
    print(f"Columns with >50% missing: {len(missing_df[missing_df['Missing_Percentage'] > 50])}")
    print(f"Columns with >90% missing: {len(missing_df[missing_df['Missing_Percentage'] > 90])}")
    
    if len(missing_df) > 0:
        print(f"\nTop 10 columns with missing values:")
        print(missing_df.head(10).to_string(index=False))
        
        # 可视化缺失值（前20个）
        if len(missing_df) > 0:
            plt.figure(figsize=(12, 8))
            top_missing = missing_df.head(20)
            plt.barh(range(len(top_missing)), top_missing['Missing_Percentage'])
            plt.yticks(range(len(top_missing)), top_missing['Column'])
            plt.xlabel('Missing Percentage (%)')
            plt.title(f'{name} - Top 20 Columns with Missing Values')
            plt.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'results/{name.lower()}_missing_values.png', dpi=150, bbox_inches='tight')
            plt.show()
    
    return missing_df

def analyze_transaction_amounts(train_transaction):
    """分析交易金额"""
    print("\n" + "="*60)
    print("💰 TRANSACTION AMOUNT ANALYSIS")
    print("="*60)
    
    # 按欺诈状态分组分析金额
    amount_stats = train_transaction.groupby('isFraud')['TransactionAmt'].describe()
    print("📊 Transaction amount statistics by fraud status:")
    print(amount_stats)
    
    # 可视化交易金额分布
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 整体金额分布
    train_transaction['TransactionAmt'].hist(bins=50, ax=axes[0,0], alpha=0.7, color='skyblue')
    axes[0,0].set_title('Overall Transaction Amount Distribution')
    axes[0,0].set_xlabel('Transaction Amount ($)')
    axes[0,0].set_ylabel('Frequency')
    
    # 对数金额分布
    np.log1p(train_transaction['TransactionAmt']).hist(bins=50, ax=axes[0,1], alpha=0.7, color='lightgreen')
    axes[0,1].set_title('Log Transaction Amount Distribution')
    axes[0,1].set_xlabel('Log(Transaction Amount + 1)')
    axes[0,1].set_ylabel('Frequency')
    
    # 按欺诈状态分组的金额分布
    for fraud_status, color in zip([0, 1], ['blue', 'red']):
        data = train_transaction[train_transaction['isFraud'] == fraud_status]['TransactionAmt']
        data.hist(bins=50, alpha=0.6, ax=axes[1,0], label=f'Fraud={fraud_status}', color=color)
    axes[1,0].set_title('Transaction Amount by Fraud Status')
    axes[1,0].set_xlabel('Transaction Amount ($)')
    axes[1,0].set_ylabel('Frequency')
    axes[1,0].legend()
    axes[1,0].set_yscale('log')
    
    # 箱线图比较
    fraud_data = [train_transaction[train_transaction['isFraud'] == i]['TransactionAmt'] for i in [0, 1]]
    axes[1,1].boxplot(fraud_data, labels=['Legitimate', 'Fraudulent'])
    axes[1,1].set_title('Transaction Amount Box Plot by Fraud Status')
    axes[1,1].set_ylabel('Transaction Amount ($)')
    axes[1,1].set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('results/transaction_amount_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()

def generate_summary_report(train_transaction, train_identity, fraud_rate, transaction_missing, identity_missing):
    """生成数据探索总结报告"""
    print("\n" + "="*70)
    print("📋 DATA EXPLORATION SUMMARY REPORT")
    print("="*70)
    
    print(f"\n📊 DATASET OVERVIEW:")
    print(f"   • Transaction records: {len(train_transaction):,}")
    print(f"   • Identity records: {len(train_identity):,}")
    print(f"   • Transaction features: {len(train_transaction.columns)}")
    print(f"   • Identity features: {len(train_identity.columns)}")
    print(f"   • Total memory usage: ~{(train_transaction.memory_usage(deep=True).sum() + train_identity.memory_usage(deep=True).sum()) / 1024**2:.0f} MB")
    
    print(f"\n🎯 TARGET VARIABLE INSIGHTS:")
    print(f"   • Fraud rate: {fraud_rate:.4f} ({fraud_rate*100:.2f}%)")
    print(f"   • Class distribution: Highly imbalanced")
    print(f"   • Imbalance ratio: {(1-fraud_rate)/fraud_rate:.0f}:1 (legitimate:fraudulent)")
    print(f"   • Challenge: Need specialized techniques for imbalanced classification")
    
    print(f"\n🔍 DATA QUALITY ASSESSMENT:")
    print(f"   • Transaction missing columns: {len(transaction_missing)}/{len(train_transaction.columns)}")
    print(f"   • Identity missing columns: {len(identity_missing)}/{len(train_identity.columns)}")
    print(f"   • High missing (>50%): Feature engineering required")
    print(f"   • Data quality: Moderate (typical for real-world data)")
    
    print(f"\n💰 TRANSACTION AMOUNT INSIGHTS:")
    amount_stats = train_transaction['TransactionAmt'].describe()
    print(f"   • Range: ${amount_stats['min']:.2f} - ${amount_stats['max']:,.2f}")
    print(f"   • Median: ${amount_stats['50%']:.2f}")
    print(f"   • Mean: ${amount_stats['mean']:.2f}")
    print(f"   • Distribution: Right-skewed (needs log transformation)")
    
    print(f"\n🚀 RECOMMENDED NEXT STEPS:")
    print(f"   1. ⏰ Temporal pattern analysis (transaction timing)")
    print(f"   2. 🔧 Feature engineering for missing values")
    print(f"   3. 🆔 Device/Identity feature exploration")
    print(f"   4. 📊 Feature correlation analysis")
    print(f"   5. 🤖 Baseline model development")
    print(f"   6. ⚖️  Imbalanced data handling strategies")
    
    print(f"\n✅ DATA EXPLORATION COMPLETED SUCCESSFULLY!")
    print(f"🎯 Ready for feature engineering and model development!")

def main():
    """主函数"""
    print("🚀 IEEE Fraud Detection - Data Exploration Starting...")
    print("="*70)
    
    # 创建结果目录
    os.makedirs('results', exist_ok=True)
    
    # 1. 加载数据
    train_transaction, train_identity = load_data()
    
    # 2. 分析数据结构
    analyze_data_structure(train_transaction, train_identity)
    
    # 3. 分析目标变量
    fraud_rate = analyze_target_variable(train_transaction)
    
    # 4. 分析缺失值
    transaction_missing = analyze_missing_values(train_transaction, "Transaction Data")
    identity_missing = analyze_missing_values(train_identity, "Identity Data")
    
    # 5. 分析交易金额
    analyze_transaction_amounts(train_transaction)
    
    # 6. 生成总结报告
    generate_summary_report(train_transaction, train_identity, fraud_rate, 
                          transaction_missing, identity_missing)
    
    print(f"\n🎉 Data exploration completed! Check results/ for visualizations.")

if __name__ == "__main__":
    main() 