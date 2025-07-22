#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 IEEE Fraud Detection - Pipeline Progress Checker
Created to monitor the training pipeline progress
"""

import os
import time
from pathlib import Path
import subprocess
import sys

def check_file_exists(file_path, description):
    """检查文件是否存在并显示状态"""
    path = Path(file_path)
    if path.exists():
        if file_path.endswith('.csv') or file_path.endswith('.pkl'):
            size_mb = path.stat().st_size / (1024*1024)
            print(f"   ✅ {description} ({size_mb:.1f} MB)")
        else:
            print(f"   ✅ {description}")
        return True
    else:
        print(f"   ⏳ {description} (not yet created)")
        return False

def check_pipeline_progress():
    """检查pipeline进度"""
    print("📊 IEEE Fraud Detection Pipeline - Progress Check")
    print("="*60)
    
    # 检查是否有pipeline在运行
    try:
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        running_processes = []
        for line in result.stdout.split('\n'):
            if 'run_pipeline.py' in line and 'grep' not in line:
                running_processes.append('Main Pipeline')
            elif '01_data_exploration.py' in line and 'grep' not in line:
                running_processes.append('Data Exploration')
            elif '02_feature_engineering.py' in line and 'grep' not in line:
                running_processes.append('Feature Engineering')
            elif '03_baseline_models.py' in line and 'grep' not in line:
                running_processes.append('Baseline Models')
        
        if running_processes:
            print(f"🔄 ACTIVE PROCESSES:")
            for process in running_processes:
                print(f"   • {process}")
        else:
            print("⏹️  NO PIPELINE PROCESSES RUNNING")
    
    except Exception as e:
        print(f"❓ Process check failed: {e}")
    
    print(f"\n📁 STAGE 1: DATA EXPLORATION")
    stage1_files = [
        ("results/fraud_distribution.png", "Fraud Distribution Plot"),
        ("results/transaction data_missing_values.png", "Transaction Missing Values"),
        ("results/identity data_missing_values.png", "Identity Missing Values"),
        ("results/transaction_amount_analysis.png", "Transaction Amount Analysis")
    ]
    
    stage1_complete = 0
    for file_path, description in stage1_files:
        if check_file_exists(file_path, description):
            stage1_complete += 1
    
    print(f"   📊 Stage 1 Progress: {stage1_complete}/{len(stage1_files)} files")
    
    print(f"\n📁 STAGE 2: FEATURE ENGINEERING")
    stage2_files = [
        ("data/processed_train_data.pkl", "Processed Training Data"),
        ("data/engineered_features.csv", "Engineered Features Dataset"),
        ("models/label_encoders.pkl", "Label Encoders"),
        ("models/feature_names.pkl", "Feature Names"),
        ("models/feature_scaler.pkl", "Feature Scaler")
    ]
    
    stage2_complete = 0
    for file_path, description in stage2_files:
        if check_file_exists(file_path, description):
            stage2_complete += 1
    
    print(f"   🔧 Stage 2 Progress: {stage2_complete}/{len(stage2_files)} files")
    
    print(f"\n📁 STAGE 3: BASELINE MODELS")
    stage3_files = [
        ("models/logistic_regression_model.pkl", "Logistic Regression Model"),
        ("models/random_forest_model.pkl", "Random Forest Model"),
        ("models/naive_bayes_model.pkl", "Naive Bayes Model"),
        ("models/xgboost_model.pkl", "XGBoost Model"),
        ("models/baseline_results.pkl", "Baseline Results"),
        ("results/model_comparison.png", "Model Comparison Plot"),
        ("results/feature_importance.png", "Feature Importance Plot")
    ]
    
    stage3_complete = 0
    for file_path, description in stage3_files:
        if check_file_exists(file_path, description):
            stage3_complete += 1
    
    print(f"   🤖 Stage 3 Progress: {stage3_complete}/{len(stage3_files)} files")
    
    # 总体进度
    total_files = len(stage1_files) + len(stage2_files) + len(stage3_files)
    total_complete = stage1_complete + stage2_complete + stage3_complete
    overall_progress = (total_complete / total_files) * 100
    
    print(f"\n📊 OVERALL PROGRESS: {total_complete}/{total_files} ({overall_progress:.1f}%)")
    print("=" * int(overall_progress/2.5))
    
    # 状态建议
    if overall_progress == 0:
        print(f"\n🔄 STATUS: Pipeline starting...")
        print(f"💡 TIP: Data exploration usually takes 2-3 minutes")
    elif overall_progress < 25:
        print(f"\n🔄 STATUS: Data exploration in progress...")
        print(f"💡 TIP: Large dataset analysis takes time")
    elif overall_progress < 50:
        print(f"\n🔄 STATUS: Feature engineering in progress...")
        print(f"💡 TIP: Creating 100+ engineered features")
    elif overall_progress < 90:
        print(f"\n🔄 STATUS: Model training in progress...")
        print(f"💡 TIP: Training multiple ML models with cross-validation")
    elif overall_progress == 100:
        print(f"\n🎉 STATUS: Pipeline completed successfully!")
        print(f"🚀 TIP: Check results/ and models/ directories")
    else:
        print(f"\n⚡ STATUS: Almost done...")
        print(f"💡 TIP: Final model evaluations completing")
    
    return overall_progress

def main():
    """主函数"""
    try:
        progress = check_pipeline_progress()
        
        if progress < 100:
            print(f"\n🔄 Pipeline still running. Run this script again to check progress.")
            print(f"⏱️  Estimated remaining time: {(100-progress)*0.15:.1f} minutes")
        else:
            print(f"\n✅ Pipeline completed! Ready for advanced model development.")
            
    except KeyboardInterrupt:
        print(f"\n👋 Progress check interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error checking progress: {e}")

if __name__ == "__main__":
    main() 