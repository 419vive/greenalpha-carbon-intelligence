#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 IEEE Fraud Detection - Feature Engineering Pipeline
Created for IEEE-CIS Fraud Detection Competition

特征工程策略 (Feature Engineering Strategy):
1. 时间特征 - Temporal features from transaction timestamps
2. 聚合特征 - Aggregation features from user behavior patterns
3. 设备指纹 - Device fingerprinting from identity data
4. 风险评分 - Risk scoring features and anomaly indicators
5. 交互特征 - Interaction features between transaction and identity
"""

import pandas as pd
import numpy as np
import warnings
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

warnings.filterwarnings('ignore')

class FraudFeatureEngineer:
    """欺诈检测特征工程类"""
    
    def __init__(self, save_transformers=True):
        self.save_transformers = save_transformers
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def load_data(self):
        """加载数据"""
        print("🔄 Loading fraud detection dataset...")
        
        data_path = Path("ieee-fraud-detection")
        
        # 加载训练数据
        train_transaction = pd.read_csv(data_path / "train_transaction.csv")
        train_identity = pd.read_csv(data_path / "train_identity.csv")
        
        print(f"✅ Transaction data: {train_transaction.shape}")
        print(f"✅ Identity data: {train_identity.shape}")
        
        return train_transaction, train_identity
    
    def create_temporal_features(self, df):
        """创建时间特征"""
        print("⏰ Creating temporal features...")
        
        # TransactionDT是从参考时间开始的秒数
        df['TransactionDT_hour'] = (df['TransactionDT'] / 3600) % 24
        df['TransactionDT_day'] = (df['TransactionDT'] / (3600 * 24)) % 7
        df['TransactionDT_week'] = (df['TransactionDT'] / (3600 * 24 * 7))
        
        # 时间相关的周期性特征
        df['hour_sin'] = np.sin(2 * np.pi * df['TransactionDT_hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['TransactionDT_hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['TransactionDT_day'] / 7)
        df['day_cos'] = np.cos(2 * np.pi * df['TransactionDT_day'] / 7)
        
        # 是否为工作时间/周末等
        df['is_weekend'] = (df['TransactionDT_day'] >= 5).astype(int)
        df['is_night'] = ((df['TransactionDT_hour'] >= 22) | (df['TransactionDT_hour'] <= 6)).astype(int)
        df['is_business_hours'] = ((df['TransactionDT_hour'] >= 9) & (df['TransactionDT_hour'] <= 17)).astype(int)
        
        temporal_features = [
            'TransactionDT_hour', 'TransactionDT_day', 'TransactionDT_week',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos',
            'is_weekend', 'is_night', 'is_business_hours'
        ]
        
        print(f"✅ Created {len(temporal_features)} temporal features")
        return df, temporal_features
    
    def create_transaction_features(self, df):
        """创建交易相关特征"""
        print("💰 Creating transaction features...")
        
        # 金额相关特征
        df['TransactionAmt_log'] = np.log1p(df['TransactionAmt'])
        df['TransactionAmt_decimal'] = ((df['TransactionAmt'] - df['TransactionAmt'].astype(int)) * 1000).astype(int)
        df['TransactionAmt_isRound'] = (df['TransactionAmt'] == df['TransactionAmt'].round()).astype(int)
        
        # 金额分组特征
        df['amt_range'] = pd.cut(df['TransactionAmt'], 
                                bins=[0, 50, 100, 300, 1000, float('inf')], 
                                labels=[0, 1, 2, 3, 4]).astype(int)
        
        transaction_features = [
            'TransactionAmt_log', 'TransactionAmt_decimal', 
            'TransactionAmt_isRound', 'amt_range'
        ]
        
        print(f"✅ Created {len(transaction_features)} transaction features")
        return df, transaction_features
    
    def create_aggregation_features(self, df):
        """创建聚合特征"""
        print("📊 Creating aggregation features...")
        
        aggregation_features = []
        
        # 按卡片聚合
        if 'card1' in df.columns:
            card_agg = df.groupby('card1')['TransactionAmt'].agg(['count', 'mean', 'std', 'min', 'max'])
            card_agg.columns = [f'card1_{col}' for col in card_agg.columns]
            df = df.merge(card_agg, left_on='card1', right_index=True, how='left')
            aggregation_features.extend(card_agg.columns.tolist())
        
        # 按邮箱域名聚合
        if 'P_emaildomain' in df.columns:
            email_agg = df.groupby('P_emaildomain')['TransactionAmt'].agg(['count', 'mean'])
            email_agg.columns = [f'email_{col}' for col in email_agg.columns]
            df = df.merge(email_agg, left_on='P_emaildomain', right_index=True, how='left')
            aggregation_features.extend(email_agg.columns.tolist())
        
        # 按收件人邮箱域名聚合
        if 'R_emaildomain' in df.columns:
            r_email_agg = df.groupby('R_emaildomain')['TransactionAmt'].agg(['count', 'mean'])
            r_email_agg.columns = [f'r_email_{col}' for col in r_email_agg.columns]
            df = df.merge(r_email_agg, left_on='R_emaildomain', right_index=True, how='left')
            aggregation_features.extend(r_email_agg.columns.tolist())
        
        print(f"✅ Created {len(aggregation_features)} aggregation features")
        return df, aggregation_features
    
    def create_device_features(self, train_transaction, train_identity):
        """创建设备指纹特征"""
        print("📱 Creating device fingerprinting features...")
        
        device_features = []
        
        # 合并身份数据
        df = train_transaction.merge(train_identity, on='TransactionID', how='left')
        
        # 设备信息特征
        device_cols = ['DeviceType', 'DeviceInfo']
        for col in device_cols:
            if col in df.columns:
                # 设备类型编码
                if df[col].dtype == 'object':
                    le = LabelEncoder()
                    df[f'{col}_encoded'] = le.fit_transform(df[col].fillna('unknown'))
                    self.label_encoders[col] = le
                    device_features.append(f'{col}_encoded')
        
        # 浏览器和操作系统特征
        browser_cols = [col for col in df.columns if 'id_' in col and col.endswith('browser')]
        os_cols = [col for col in df.columns if 'id_' in col and col.endswith('os')]
        
        for col in browser_cols + os_cols:
            if col in df.columns and df[col].dtype == 'object':
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col].fillna('unknown'))
                self.label_encoders[col] = le
                device_features.append(f'{col}_encoded')
        
        # 屏幕分辨率特征
        if 'id_33' in df.columns:  # 屏幕分辨率
            df['screen_width'] = df['id_33'].str.extract('(\d+)x').astype(float)
            df['screen_height'] = df['id_33'].str.extract('x(\d+)').astype(float)
            df['screen_ratio'] = df['screen_width'] / (df['screen_height'] + 1e-5)
            device_features.extend(['screen_width', 'screen_height', 'screen_ratio'])
        
        print(f"✅ Created {len(device_features)} device features")
        return df, device_features
    
    def create_risk_features(self, df):
        """创建风险评分特征"""
        print("⚠️ Creating risk scoring features...")
        
        risk_features = []
        
        # 金额异常检测
        df['amt_zscore'] = (df['TransactionAmt'] - df['TransactionAmt'].mean()) / df['TransactionAmt'].std()
        df['amt_is_outlier'] = (np.abs(df['amt_zscore']) > 3).astype(int)
        risk_features.extend(['amt_zscore', 'amt_is_outlier'])
        
        # 交易频率异常（如果有用户标识）
        if 'card1' in df.columns:
            card_freq = df['card1'].value_counts()
            df['card_frequency'] = df['card1'].map(card_freq)
            df['is_high_freq_card'] = (df['card_frequency'] > df['card_frequency'].quantile(0.95)).astype(int)
            risk_features.extend(['card_frequency', 'is_high_freq_card'])
        
        # 时间异常（深夜交易等）
        df['night_transaction_risk'] = (df['is_night'] & (df['TransactionAmt'] > df['TransactionAmt'].median())).astype(int)
        df['weekend_large_transaction'] = (df['is_weekend'] & (df['TransactionAmt'] > df['TransactionAmt'].quantile(0.9))).astype(int)
        risk_features.extend(['night_transaction_risk', 'weekend_large_transaction'])
        
        print(f"✅ Created {len(risk_features)} risk features")
        return df, risk_features
    
    def handle_missing_values(self, df):
        """处理缺失值"""
        print("🔧 Handling missing values...")
        
        # 数值型特征：用中位数填充
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != 'isFraud' and df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
        
        # 分类特征：用'unknown'填充
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna('unknown')
        
        print("✅ Missing values handled")
        return df
    
    def encode_categorical_features(self, df):
        """编码分类特征"""
        print("🏷️ Encoding categorical features...")
        
        categorical_cols = df.select_dtypes(include=['object']).columns
        categorical_cols = [col for col in categorical_cols if col not in ['TransactionID']]
        
        encoded_features = []
        for col in categorical_cols:
            if col not in self.label_encoders:
                le = LabelEncoder()
                df[f'{col}_encoded'] = le.fit_transform(df[col])
                self.label_encoders[col] = le
                encoded_features.append(f'{col}_encoded')
            else:
                # 使用已保存的编码器
                df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
                encoded_features.append(f'{col}_encoded')
        
        print(f"✅ Encoded {len(encoded_features)} categorical features")
        return df, encoded_features
    
    def create_interaction_features(self, df):
        """创建交互特征"""
        print("🔄 Creating interaction features...")
        
        interaction_features = []
        
        # 金额与时间的交互
        if 'TransactionAmt_log' in df.columns and 'TransactionDT_hour' in df.columns:
            df['amt_hour_interaction'] = df['TransactionAmt_log'] * df['TransactionDT_hour']
            interaction_features.append('amt_hour_interaction')
        
        # 卡片与金额的交互
        if 'card1_mean' in df.columns:
            df['amt_vs_card_avg'] = df['TransactionAmt'] / (df['card1_mean'] + 1e-5)
            interaction_features.append('amt_vs_card_avg')
        
        # 设备与时间的交互
        if 'DeviceType_encoded' in df.columns and 'is_night' in df.columns:
            df['device_night_interaction'] = df['DeviceType_encoded'] * df['is_night']
            interaction_features.append('device_night_interaction')
        
        print(f"✅ Created {len(interaction_features)} interaction features")
        return df, interaction_features
    
    def engineer_features(self, train_transaction, train_identity):
        """主要的特征工程函数"""
        print("\n" + "="*60)
        print("🔧 STARTING FEATURE ENGINEERING PIPELINE")
        print("="*60)
        
        all_features = []
        
        # 1. 创建时间特征
        train_transaction, temporal_features = self.create_temporal_features(train_transaction)
        all_features.extend(temporal_features)
        
        # 2. 创建交易特征
        train_transaction, transaction_features = self.create_transaction_features(train_transaction)
        all_features.extend(transaction_features)
        
        # 3. 创建聚合特征
        train_transaction, aggregation_features = self.create_aggregation_features(train_transaction)
        all_features.extend(aggregation_features)
        
        # 4. 创建设备特征
        df_with_identity, device_features = self.create_device_features(train_transaction, train_identity)
        all_features.extend(device_features)
        
        # 5. 创建风险特征
        df_with_identity, risk_features = self.create_risk_features(df_with_identity)
        all_features.extend(risk_features)
        
        # 6. 处理缺失值
        df_with_identity = self.handle_missing_values(df_with_identity)
        
        # 7. 编码分类特征
        df_with_identity, encoded_features = self.encode_categorical_features(df_with_identity)
        all_features.extend(encoded_features)
        
        # 8. 创建交互特征
        df_with_identity, interaction_features = self.create_interaction_features(df_with_identity)
        all_features.extend(interaction_features)
        
        # 保存特征名称
        self.feature_names = all_features
        
        print(f"\n📊 FEATURE ENGINEERING SUMMARY:")
        print(f"   • Original transaction features: {len(train_transaction.columns)}")
        print(f"   • Original identity features: {len(train_identity.columns)}")
        print(f"   • Engineered features: {len(all_features)}")
        print(f"   • Total features in dataset: {len(df_with_identity.columns)}")
        
        # 保存转换器
        if self.save_transformers:
            self.save_feature_transformers()
        
        return df_with_identity, all_features
    
    def save_feature_transformers(self):
        """保存特征转换器"""
        os.makedirs('models', exist_ok=True)
        
        # 保存标签编码器
        joblib.dump(self.label_encoders, 'models/label_encoders.pkl')
        
        # 保存特征名称
        joblib.dump(self.feature_names, 'models/feature_names.pkl')
        
        print("✅ Feature transformers saved to models/")
    
    def prepare_model_data(self, df, target_col='isFraud', test_size=0.2, random_state=42):
        """准备模型训练数据"""
        print("\n📋 Preparing data for modeling...")
        
        # 选择特征列
        feature_cols = [col for col in self.feature_names if col in df.columns]
        
        # 确保没有无限值或NaN
        for col in feature_cols:
            if col in df.columns:
                df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        df[feature_cols] = df[feature_cols].fillna(0)
        
        X = df[feature_cols]
        y = df[target_col]
        
        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # 标准化特征
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # 保存缩放器
        if self.save_transformers:
            joblib.dump(self.scaler, 'models/feature_scaler.pkl')
        
        print(f"✅ Data prepared:")
        print(f"   • Training set: {X_train.shape}")
        print(f"   • Test set: {X_test.shape}")
        print(f"   • Features used: {len(feature_cols)}")
        print(f"   • Fraud rate in train: {y_train.mean():.4f}")
        print(f"   • Fraud rate in test: {y_test.mean():.4f}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test, feature_cols

def main():
    """主函数"""
    print("🚀 IEEE Fraud Detection - Feature Engineering Starting...")
    print("="*70)
    
    # 初始化特征工程器
    fe = FraudFeatureEngineer(save_transformers=True)
    
    # 加载数据
    train_transaction, train_identity = fe.load_data()
    
    # 执行特征工程
    engineered_df, feature_list = fe.engineer_features(train_transaction, train_identity)
    
    # 准备模型数据
    X_train, X_test, y_train, y_test, feature_cols = fe.prepare_model_data(engineered_df)
    
    # 保存处理后的数据
    os.makedirs('data', exist_ok=True)
    
    # 保存训练数据
    train_data = {
        'X_train': X_train,
        'X_test': X_test, 
        'y_train': y_train,
        'y_test': y_test,
        'feature_names': feature_cols
    }
    
    joblib.dump(train_data, 'data/processed_train_data.pkl')
    
    # 保存完整的工程化数据集
    engineered_df.to_csv('data/engineered_features.csv', index=False)
    
    print(f"\n🎉 Feature engineering completed successfully!")
    print(f"✅ Processed data saved to data/")
    print(f"✅ Model transformers saved to models/")
    print(f"🎯 Ready for baseline model training!")

if __name__ == "__main__":
    main() 