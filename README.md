# IEEE Fraud Detection Project with SERENA MCP

## 📊 Competition Context

### The Challenge
Imagine standing at the checkout counter with a long line behind you, and the cashier announces your card has been declined. While embarrassing, fraud prevention systems save consumers millions annually. **IEEE Computational Intelligence Society (IEEE-CIS)** and **Vesta Corporation** are partnering to improve fraud detection accuracy while enhancing customer experience.

### Our Mission
- **Improve fraud detection efficacy** for millions worldwide
- **Reduce false positives** that embarrass legitimate customers  
- **Help businesses** reduce fraud losses and increase revenue
- **Benchmark ML models** on challenging real-world e-commerce data

### The Dataset
Real-world e-commerce transactions from **Vesta Corporation** featuring:
- **Device characteristics** and behavioral patterns
- **Product features** and transaction details
- **Identity information** linked to transactions
- **Large-scale dataset** requiring advanced ML techniques

## 🚀 SERENA MCP Setup

SERENA is now configured and ready to use! This powerful coding agent toolkit provides:

- **Semantic Code Retrieval**: Understanding code at the symbol level
- **Intelligent Editing**: Context-aware code modifications  
- **Language Server Integration**: Support for Python, TypeScript, Go, Rust, C#, Java and more
- **Project Memory**: Persistent knowledge about your codebase
- **Shell Integration**: Execute commands and tests seamlessly

### Quick Start Commands

```bash
# Start SERENA MCP Server (stdio mode for IDE integration)
uvx --from git+https://github.com/oraios/serena serena-mcp-server --project $(pwd)

# Start SERENA MCP Server (SSE mode for web access)
uvx --from git+https://github.com/oraios/serena serena-mcp-server --transport sse --port 8000 --project $(pwd)

# Index project for faster performance
uvx --from git+https://github.com/oraios/serena index-project
```

## 📊 Dataset Information

### Files Overview
- `train_transaction.csv` (652MB) - **Training transaction data** with fraud labels
- `train_identity.csv` (25MB) - **Training identity information** (device, network, etc.)
- `test_transaction.csv` (585MB) - **Test transaction data** for predictions
- `test_identity.csv` (25MB) - **Test identity information**
- `sample_submission.csv` (5.8MB) - **Submission format** example

### Key Characteristics
- **Real-world e-commerce transactions** from Vesta Corporation
- **Wide range of features**: device type, product features, behavioral patterns
- **Large-scale dataset**: ~1.3GB total, hundreds of thousands of transactions
- **Binary classification**: Fraudulent (1) vs Legitimate (0) transactions
- **Evaluation metric**: ROC-AUC (Area Under ROC Curve)

## 🛠️ Project Structure

```
project 3/
├── README.md                    # This file
├── SERENA_QUICKSTART.md        # Quick start guide
├── ieee-fraud-detection/        # Original dataset
│   ├── train_transaction.csv   # Training transactions (652MB)
│   ├── train_identity.csv      # Training identity data (25MB)
│   ├── test_transaction.csv    # Test transactions (585MB)
│   ├── test_identity.csv       # Test identity data (25MB)
│   └── sample_submission.csv   # Submission format (5.8MB)
├── src/                         # Source code
├── notebooks/                   # Jupyter notebooks
├── models/                      # Trained models
├── data/                        # Processed data
├── results/                     # Analysis results
└── docs/                        # Documentation
```

## 🎯 Competition Strategy

### Phase 1: Data Understanding 📊
- **Exploratory Data Analysis** (EDA) of transaction patterns
- **Feature analysis** and correlation studies
- **Fraud pattern identification** in training data
- **Data quality assessment** and missing value analysis

### Phase 2: Feature Engineering 🔧
- **Temporal features** from transaction timestamps
- **Aggregation features** from user behavior
- **Device fingerprinting** from identity data
- **Interaction features** between transaction and identity

### Phase 3: Model Development 🤖
- **Baseline models**: Logistic Regression, Random Forest
- **Advanced models**: XGBoost, LightGBM, CatBoost
- **Deep learning**: Neural networks for complex patterns
- **Ensemble methods**: Combining multiple model predictions

### Phase 4: Validation & Optimization 📈
- **Cross-validation** strategies for reliable evaluation
- **Hyperparameter tuning** for optimal performance
- **Feature selection** to reduce overfitting
- **ROC-AUC optimization** as primary metric

## 🚀 Getting Started with SERENA

1. **Activate SERENA MCP for this project:**
   ```bash
   # SERENA will automatically detect and index the project
   uvx --from git+https://github.com/oraios/serena serena-mcp-server --project $(pwd)
   ```

2. **Start data exploration with SERENA:**
   - "Analyze the structure of ieee-fraud-detection CSV files"
   - "Generate EDA code for fraud detection analysis"
   - "Identify key features and patterns in transaction data"

3. **Build ML pipeline with SERENA:**
   - "Create feature engineering pipeline for fraud detection"
   - "Implement baseline models and evaluation framework"
   - "Generate ensemble model code for fraud classification"

## 📝 Development Log

### ✅ Completed
- SERENA MCP successfully installed and configured
- Project structure established with organized directories
- Dataset verified (5 CSV files, ~1.3GB total)
- Competition context and strategy documented

### 🎯 Next Steps
- [ ] **Data exploration**: Profile dataset structure and characteristics
- [ ] **EDA development**: Create comprehensive exploratory analysis
- [ ] **Feature engineering**: Design and implement feature pipelines
- [ ] **Baseline models**: Implement and evaluate initial models
- [ ] **Advanced modeling**: Develop ensemble and deep learning approaches

## 🔧 SERENA MCP Integration

SERENA MCP is configured with:
- **Context**: `desktop-app` (optimized for development environment)
- **Mode**: `interactive, editing` (full interactive coding capabilities)
- **Project Auto-activation**: Current directory indexed for fraud detection
- **Web Dashboard**: Available at http://localhost:8000

### Use SERENA to:
- **Analyze dataset structure** and generate profiling code
- **Create EDA visualizations** for fraud pattern discovery
- **Implement feature engineering** pipelines and transformations
- **Build and optimize ML models** for fraud classification
- **Debug and test implementations** with intelligent assistance
- **Document findings** and create comprehensive reports

---

**Ready to tackle fraud detection with AI-powered development! 🤖🚀**

*"Improving fraud detection to save consumers millions while enhancing customer experience"* 