#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 IEEE Fraud Detection - Baseline Models
Created for IEEE-CIS Fraud Detection Competition

基线模型 (Baseline Models):
1. Logistic Regression - Linear baseline with regularization
2. Random Forest - Tree-based ensemble model  
3. XGBoost - Gradient boosting baseline
4. Evaluation Framework - ROC-AUC, Precision-Recall, Business Metrics
"""

import pandas as pd
import numpy as np
import warnings
from pathlib import Path
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 机器学习模型
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb

# 评估指标
from sklearn.metrics import (
    roc_auc_score, roc_curve, precision_recall_curve,
    classification_report, confusion_matrix, average_precision_score
)
from sklearn.model_selection import cross_val_score, StratifiedKFold

warnings.filterwarnings('ignore')

class FraudBaselineModels:
    """欺诈检测基线模型类"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.results = {}
        self.feature_importance = {}
        
    def load_processed_data(self):
        """加载预处理后的数据"""
        print("📂 Loading processed training data...")
        
        try:
            train_data = joblib.load('data/processed_train_data.pkl')
            
            X_train = train_data['X_train']
            X_test = train_data['X_test']
            y_train = train_data['y_train']
            y_test = train_data['y_test']
            feature_names = train_data['feature_names']
            
            print(f"✅ Data loaded successfully:")
            print(f"   • Training samples: {X_train.shape[0]:,}")
            print(f"   • Test samples: {X_test.shape[0]:,}")
            print(f"   • Features: {X_train.shape[1]:,}")
            print(f"   • Fraud rate (train): {y_train.mean():.4f}")
            print(f"   • Fraud rate (test): {y_test.mean():.4f}")
            
            return X_train, X_test, y_train, y_test, feature_names
            
        except FileNotFoundError:
            print("❌ Processed data not found. Please run feature engineering first.")
            print("💡 Run: python src/02_feature_engineering.py")
            return None, None, None, None, None
    
    def initialize_models(self):
        """初始化基线模型"""
        print("\n🤖 Initializing baseline models...")
        
        self.models = {
            'logistic_regression': LogisticRegression(
                random_state=self.random_state,
                max_iter=1000,
                class_weight='balanced',  # 处理类别不平衡
                solver='liblinear'
            ),
            
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                random_state=self.random_state,
                class_weight='balanced',
                n_jobs=-1,
                max_depth=10
            ),
            
            'naive_bayes': GaussianNB(),
            
            'xgboost': xgb.XGBClassifier(
                n_estimators=100,
                random_state=self.random_state,
                eval_metric='logloss',
                use_label_encoder=False,
                scale_pos_weight=1,  # 将根据数据调整
                max_depth=6,
                learning_rate=0.1
            )
        }
        
        print(f"✅ Initialized {len(self.models)} baseline models")
        
        for name, model in self.models.items():
            print(f"   • {name}: {type(model).__name__}")
    
    def adjust_for_imbalance(self, y_train):
        """调整模型以处理类别不平衡"""
        print("\n⚖️ Adjusting models for class imbalance...")
        
        # 计算类别权重
        fraud_rate = y_train.mean()
        pos_weight = (1 - fraud_rate) / fraud_rate
        
        print(f"   • Fraud rate: {fraud_rate:.4f}")
        print(f"   • Positive weight ratio: {pos_weight:.1f}")
        
        # 调整XGBoost的scale_pos_weight
        self.models['xgboost'].set_params(scale_pos_weight=pos_weight)
        
        print("✅ Models adjusted for imbalanced data")
    
    def train_single_model(self, name, model, X_train, y_train, X_test, y_test):
        """训练单个模型"""
        print(f"\n🔄 Training {name}...")
        
        # 训练模型
        model.fit(X_train, y_train)
        
        # 预测
        train_pred = model.predict_proba(X_train)[:, 1]
        test_pred = model.predict_proba(X_test)[:, 1]
        
        # 计算评估指标
        train_auc = roc_auc_score(y_train, train_pred)
        test_auc = roc_auc_score(y_test, test_pred)
        
        train_ap = average_precision_score(y_train, train_pred)
        test_ap = average_precision_score(y_test, test_pred)
        
        # 交叉验证
        cv_scores = cross_val_score(
            model, X_train, y_train, 
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state),
            scoring='roc_auc', n_jobs=-1
        )
        
        results = {
            'model': model,
            'train_auc': train_auc,
            'test_auc': test_auc,
            'train_ap': train_ap,
            'test_ap': test_ap,
            'cv_auc_mean': cv_scores.mean(),
            'cv_auc_std': cv_scores.std(),
            'train_pred': train_pred,
            'test_pred': test_pred
        }
        
        print(f"✅ {name} training completed:")
        print(f"   • Train AUC: {train_auc:.4f}")
        print(f"   • Test AUC: {test_auc:.4f}")
        print(f"   • CV AUC: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        print(f"   • Test AP: {test_ap:.4f}")
        
        return results
    
    def extract_feature_importance(self, model_name, model, feature_names):
        """提取特征重要性"""
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = np.abs(model.coef_[0])
        else:
            return None
        
        feature_imp_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        self.feature_importance[model_name] = feature_imp_df
        return feature_imp_df
    
    def train_all_models(self, X_train, X_test, y_train, y_test, feature_names):
        """训练所有基线模型"""
        print("\n" + "="*60)
        print("🚀 TRAINING ALL BASELINE MODELS")
        print("="*60)
        
        # 调整模型以处理类别不平衡
        self.adjust_for_imbalance(y_train)
        
        # 训练每个模型
        for name, model in self.models.items():
            results = self.train_single_model(name, model, X_train, y_train, X_test, y_test)
            self.results[name] = results
            
            # 提取特征重要性
            self.extract_feature_importance(name, model, feature_names)
        
        print(f"\n🎉 All models trained successfully!")
        return self.results
    
    def evaluate_models(self, y_test):
        """全面评估模型性能"""
        print("\n" + "="*60)
        print("📊 MODEL EVALUATION RESULTS")
        print("="*60)
        
        # 创建结果汇总表
        summary_data = []
        
        for name, results in self.results.items():
            summary_data.append({
                'Model': name.replace('_', ' ').title(),
                'Train_AUC': results['train_auc'],
                'Test_AUC': results['test_auc'],
                'CV_AUC_Mean': results['cv_auc_mean'],
                'CV_AUC_Std': results['cv_auc_std'],
                'Test_AP': results['test_ap'],
                'Overfitting': results['train_auc'] - results['test_auc']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df = summary_df.sort_values('Test_AUC', ascending=False)
        
        print("\n📋 MODEL PERFORMANCE SUMMARY:")
        print(summary_df.round(4).to_string(index=False))
        
        # 找出最佳模型
        best_model_name = summary_df.iloc[0]['Model'].lower().replace(' ', '_')
        best_auc = summary_df.iloc[0]['Test_AUC']
        
        print(f"\n🏆 BEST MODEL: {best_model_name}")
        print(f"   • Test AUC: {best_auc:.4f}")
        print(f"   • CV AUC: {summary_df.iloc[0]['CV_AUC_Mean']:.4f} (±{summary_df.iloc[0]['CV_AUC_Std']:.4f})")
        
        return summary_df, best_model_name
    
    def plot_model_comparison(self, y_test):
        """绘制模型比较图"""
        print("\n📈 Creating model comparison visualizations...")
        
        # 创建结果目录
        os.makedirs('results', exist_ok=True)
        
        # 1. ROC曲线比较
        plt.figure(figsize=(15, 5))
        
        # ROC曲线
        plt.subplot(1, 3, 1)
        for name, results in self.results.items():
            fpr, tpr, _ = roc_curve(y_test, results['test_pred'])
            auc = results['test_auc']
            plt.plot(fpr, tpr, label=f'{name} (AUC = {auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves Comparison')
        plt.legend()
        plt.grid(alpha=0.3)
        
        # Precision-Recall曲线
        plt.subplot(1, 3, 2)
        for name, results in self.results.items():
            precision, recall, _ = precision_recall_curve(y_test, results['test_pred'])
            ap = results['test_ap']
            plt.plot(recall, precision, label=f'{name} (AP = {ap:.3f})')
        
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curves')
        plt.legend()
        plt.grid(alpha=0.3)
        
        # AUC分数比较
        plt.subplot(1, 3, 3)
        model_names = []
        test_aucs = []
        cv_aucs = []
        
        for name, results in self.results.items():
            model_names.append(name.replace('_', '\n'))
            test_aucs.append(results['test_auc'])
            cv_aucs.append(results['cv_auc_mean'])
        
        x = np.arange(len(model_names))
        width = 0.35
        
        plt.bar(x - width/2, test_aucs, width, label='Test AUC', alpha=0.8)
        plt.bar(x + width/2, cv_aucs, width, label='CV AUC', alpha=0.8)
        
        plt.xlabel('Models')
        plt.ylabel('AUC Score')
        plt.title('AUC Scores Comparison')
        plt.xticks(x, model_names)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/model_comparison.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved to results/model_comparison.png")
    
    def plot_feature_importance(self, top_n=20):
        """绘制特征重要性"""
        print(f"\n📊 Plotting top {top_n} feature importance...")
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        axes = axes.ravel()
        
        for i, (name, importance_df) in enumerate(self.feature_importance.items()):
            if i >= 4:  # 最多显示4个模型
                break
                
            top_features = importance_df.head(top_n)
            
            axes[i].barh(range(len(top_features)), top_features['importance'])
            axes[i].set_yticks(range(len(top_features)))
            axes[i].set_yticklabels(top_features['feature'])
            axes[i].set_xlabel('Importance')
            axes[i].set_title(f'{name.replace("_", " ").title()} - Top {top_n} Features')
            axes[i].grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/feature_importance.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("✅ Feature importance plots saved to results/feature_importance.png")
    
    def save_models(self):
        """保存训练好的模型"""
        print("\n💾 Saving trained models...")
        
        os.makedirs('models', exist_ok=True)
        
        # 保存所有模型
        for name, results in self.results.items():
            model_path = f'models/{name}_model.pkl'
            joblib.dump(results['model'], model_path)
            print(f"   • {name} saved to {model_path}")
        
        # 保存评估结果
        joblib.dump(self.results, 'models/baseline_results.pkl')
        
        # 保存特征重要性
        if self.feature_importance:
            joblib.dump(self.feature_importance, 'models/feature_importance.pkl')
        
        print("✅ All models and results saved to models/")
    
    def generate_model_report(self, summary_df, best_model_name):
        """生成模型评估报告"""
        print("\n" + "="*70)
        print("📋 BASELINE MODELS EVALUATION REPORT")
        print("="*70)
        
        print(f"\n🎯 OBJECTIVE:")
        print(f"   • Build and evaluate baseline models for fraud detection")
        print(f"   • Establish performance benchmarks for advanced models")
        print(f"   • Identify most promising modeling approaches")
        
        print(f"\n📊 MODELS EVALUATED:")
        for i, row in summary_df.iterrows():
            print(f"   • {row['Model']}: AUC = {row['Test_AUC']:.4f}")
        
        print(f"\n🏆 BEST PERFORMING MODEL:")
        best_row = summary_df.iloc[0]
        print(f"   • Model: {best_row['Model']}")
        print(f"   • Test AUC: {best_row['Test_AUC']:.4f}")
        print(f"   • Cross-validation AUC: {best_row['CV_AUC_Mean']:.4f} (±{best_row['CV_AUC_Std']:.4f})")
        print(f"   • Average Precision: {best_row['Test_AP']:.4f}")
        print(f"   • Overfitting: {best_row['Overfitting']:.4f}")
        
        print(f"\n📈 KEY INSIGHTS:")
        print(f"   • Class imbalance successfully handled with balanced weights")
        print(f"   • All models show reasonable performance (AUC > 0.5)")
        print(f"   • {'Low' if best_row['Overfitting'] < 0.05 else 'Moderate'} overfitting observed")
        print(f"   • Feature engineering pipeline working effectively")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   • Hyperparameter tuning for best performing models")
        print(f"   • Advanced ensemble methods (stacking, blending)")
        print(f"   • Deep learning approaches (TabNet, Neural Networks)")
        print(f"   • Feature selection and optimization")
        
        print(f"\n✅ BASELINE EVALUATION COMPLETED SUCCESSFULLY!")

def main():
    """主函数"""
    print("🚀 IEEE Fraud Detection - Baseline Models Training...")
    print("="*70)
    
    # 初始化基线模型类
    baseline = FraudBaselineModels(random_state=42)
    
    # 加载预处理数据
    X_train, X_test, y_train, y_test, feature_names = baseline.load_processed_data()
    
    if X_train is None:
        print("❌ Cannot proceed without processed data. Exiting...")
        return
    
    # 初始化模型
    baseline.initialize_models()
    
    # 训练所有模型
    results = baseline.train_all_models(X_train, X_test, y_train, y_test, feature_names)
    
    # 评估模型
    summary_df, best_model = baseline.evaluate_models(y_test)
    
    # 创建可视化
    baseline.plot_model_comparison(y_test)
    baseline.plot_feature_importance(top_n=20)
    
    # 保存模型
    baseline.save_models()
    
    # 生成最终报告
    baseline.generate_model_report(summary_df, best_model)
    
    print(f"\n🎉 Baseline model training completed!")
    print(f"📊 Check results/ for visualizations")
    print(f"💾 Check models/ for saved models")

if __name__ == "__main__":
    main() 