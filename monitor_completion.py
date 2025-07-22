#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏰ IEEE Fraud Detection - Pipeline Completion Monitor
Monitors pipeline progress and notifies when complete
"""

import time
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def check_process_running():
    """检查pipeline是否还在运行"""
    try:
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        for line in result.stdout.split('\n'):
            if 'run_pipeline.py' in line and 'grep' not in line:
                return True, "Main Pipeline"
            elif any(script in line for script in ['01_data_exploration.py', '02_feature_engineering.py', '03_baseline_models.py']) and 'grep' not in line:
                return True, "Pipeline Script"
        
        return False, None
    except:
        return False, None

def check_completion_status():
    """检查完成状态"""
    expected_files = [
        # Data exploration outputs
        "results/fraud_distribution.png",
        "results/transaction data_missing_values.png", 
        "results/identity data_missing_values.png",
        "results/transaction_amount_analysis.png",
        
        # Feature engineering outputs
        "data/processed_train_data.pkl",
        "data/engineered_features.csv",
        "models/label_encoders.pkl",
        "models/feature_names.pkl", 
        "models/feature_scaler.pkl",
        
        # Model training outputs
        "models/logistic_regression_model.pkl",
        "models/random_forest_model.pkl",
        "models/naive_bayes_model.pkl", 
        "models/xgboost_model.pkl",
        "models/baseline_results.pkl",
        "results/model_comparison.png",
        "results/feature_importance.png"
    ]
    
    completed_files = []
    missing_files = []
    
    for file_path in expected_files:
        if Path(file_path).exists():
            completed_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    completion_rate = len(completed_files) / len(expected_files) * 100
    
    return completion_rate, completed_files, missing_files

def print_status_update(completion_rate, is_running, process_name):
    """打印状态更新"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"\n[{timestamp}] 📊 Pipeline Status Update:")
    print(f"   • Completion: {completion_rate:.1f}%")
    print(f"   • Process: {'🔄 Running' if is_running else '⏹️ Stopped'} {process_name if process_name else ''}")
    
    if completion_rate < 30:
        print(f"   • Stage: 🔍 Data Exploration")
    elif completion_rate < 60:
        print(f"   • Stage: 🔧 Feature Engineering") 
    elif completion_rate < 90:
        print(f"   • Stage: 🤖 Model Training")
    else:
        print(f"   • Stage: 🎯 Finalizing")

def monitor_pipeline():
    """监控pipeline直到完成"""
    print("⏰ Starting Pipeline Completion Monitor...")
    print("🎯 Will notify you when the IEEE fraud detection pipeline is complete!")
    print("=" * 60)
    
    start_time = time.time()
    last_completion = 0
    check_interval = 30  # Check every 30 seconds
    
    while True:
        try:
            # Check if processes are running
            is_running, process_name = check_process_running()
            
            # Check completion status
            completion_rate, completed_files, missing_files = check_completion_status()
            
            # Print update if significant progress made
            if completion_rate != last_completion or completion_rate == 100:
                print_status_update(completion_rate, is_running, process_name)
                last_completion = completion_rate
            
            # Check if completed
            if completion_rate >= 95 and not is_running:
                elapsed_time = time.time() - start_time
                print("\n" + "=" * 70)
                print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
                print("=" * 70)
                print(f"⏱️  Total time: {elapsed_time/60:.1f} minutes")
                print(f"📊 Files generated: {len(completed_files)}")
                print(f"💾 Output directories: results/, models/, data/")
                
                print(f"\n📋 COMPLETION SUMMARY:")
                print(f"   ✅ Data Exploration: Complete with 4 visualizations")
                print(f"   ✅ Feature Engineering: Complete with processed datasets") 
                print(f"   ✅ Baseline Models: Complete with 4 trained models")
                print(f"   ✅ Evaluation: Complete with comparison plots")
                
                print(f"\n🚀 READY FOR NEXT STEPS:")
                print(f"   • Check results/ for analysis visualizations")
                print(f"   • Review models/ for trained models")
                print(f"   • Proceed to advanced model development")
                print(f"   • Start hyperparameter tuning")
                
                print(f"\n🏆 Your IEEE fraud detection pipeline is ready for competition!")
                break
            
            # Check if stuck (no progress and no running processes)
            elif completion_rate < 100 and not is_running:
                elapsed_time = time.time() - start_time
                if elapsed_time > 300:  # 5 minutes with no activity
                    print(f"\n⚠️  WARNING: Pipeline may have stalled")
                    print(f"   • Completion: {completion_rate:.1f}%")
                    print(f"   • No active processes detected")
                    print(f"   • Consider checking for errors or restarting")
                    break
            
            # Wait before next check
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print(f"\n👋 Monitoring stopped by user")
            print(f"📊 Last known completion: {completion_rate:.1f}%")
            break
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")
            time.sleep(check_interval)

if __name__ == "__main__":
    monitor_pipeline() 