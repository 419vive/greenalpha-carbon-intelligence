# SERENA MCP Setup Guide for IEEE Fraud Detection Project

## 🎯 Current Status: ACTIVE ✅

SERENA MCP is now running and configured for your IEEE fraud detection project!

## 🌐 Access Points

### Web Dashboard
- **URL**: http://localhost:8000
- **Features**: Real-time logs, server control, project monitoring
- **Status**: ✅ Running in background

### MCP Server Details
- **Transport**: SSE (Server-Sent Events)
- **Port**: 8000
- **Project**: Auto-activated for current directory
- **Web Dashboard**: Enabled

## 🚀 How to Use SERENA MCP

### 1. Integration with IDEs

**For Claude Desktop/Code:**
```json
{
    "mcpServers": {
        "serena": {
            "url": "http://localhost:8000/sse"
        }
    }
}
```

**For Cursor/Windsurf/Cline:**
- Add MCP server: `http://localhost:8000/sse`
- Enable all SERENA tools for maximum capability

### 2. Direct CLI Usage

```bash
# Start SERENA MCP server (if not running)
uvx --from git+https://github.com/oraios/serena serena-mcp-server --transport sse --port 8000 --project $(pwd)

# Index project for faster performance
uvx --from git+https://github.com/oraios/serena index-project

# Stop server (via web dashboard or Ctrl+C)
```

## 🔧 Available SERENA Tools

### Code Understanding & Navigation
- `semantic_search` - Find code by meaning, not just text
- `goto_definition` - Navigate to symbol definitions
- `find_references` - Find all usages of symbols
- `get_symbols` - Extract all symbols from files

### Code Editing & Generation
- `edit_code` - Intelligent code modifications
- `apply_edits` - Batch edit operations
- `create_file` - Generate new files with context

### Project Management  
- `shell_execute` - Run commands and tests
- `get_project_structure` - Analyze project layout
- `memory_tools` - Persistent project knowledge

### Analysis & Documentation
- `analyze_code` - Deep code analysis
- `generate_docs` - Create documentation
- `explain_code` - Code explanation and comments

## 🎯 Recommended Workflow for Fraud Detection

### Phase 1: Data Exploration
1. **Ask SERENA to analyze CSV structure:**
   - "Analyze the structure of ieee-fraud-detection/*.csv files"
   - "What are the key columns and data types?"
   - "Generate initial data profiling code"

2. **Exploratory Data Analysis:**
   - "Create EDA notebook for fraud detection"
   - "Identify missing values and data quality issues"
   - "Generate visualization code for fraud patterns"

### Phase 2: Feature Engineering
1. **Feature Discovery:**
   - "Suggest feature engineering strategies for fraud detection"
   - "Identify time-based patterns in transactions"
   - "Create feature importance analysis"

2. **Implementation:**
   - "Build feature engineering pipeline"
   - "Implement categorical encoding strategies"
   - "Create feature selection functions"

### Phase 3: Model Development
1. **Baseline Models:**
   - "Implement logistic regression baseline"
   - "Add random forest and XGBoost models"
   - "Create model comparison framework"

2. **Advanced Models:**
   - "Implement deep learning approaches"
   - "Add ensemble methods"
   - "Optimize hyperparameters"

## 💡 SERENA Best Practices

### 1. Project Activation
- SERENA automatically activated for current directory
- Project memory persists across sessions
- Use project-specific configurations

### 2. Tool Usage
- Combine semantic search with code editing
- Use shell execution for testing and validation
- Leverage memory tools for complex workflows

### 3. Performance Optimization
- Index large projects for faster tool response
- Use specific queries for better semantic search
- Batch similar operations when possible

## 🐛 Troubleshooting

### Server Issues
```bash
# Check if server is running
curl http://localhost:8000/health

# Restart server if needed
pkill -f serena-mcp-server
uvx --from git+https://github.com/oraios/serena serena-mcp-server --transport sse --port 8000 --project $(pwd)
```

### Performance Issues
```bash
# Re-index project
uvx --from git+https://github.com/oraios/serena index-project

# Clear cache if needed
rm -rf .serena/cache
```

## 📊 Project Integration

SERENA is configured to understand:
- **Python**: Full language server support
- **Jupyter Notebooks**: Notebook analysis and editing
- **CSV Data**: Structure analysis and manipulation
- **Documentation**: Markdown and text file handling

## 🎉 Ready to Start!

Your SERENA MCP setup is complete and optimized for fraud detection analysis. The AI assistant now has access to powerful semantic code understanding and editing capabilities.

**Next Steps:**
1. Visit http://localhost:8000 to see the web dashboard
2. Start asking SERENA to analyze your fraud detection data
3. Use the recommended workflow above for systematic development

---

**Happy coding with AI assistance! 🤖⚡** 