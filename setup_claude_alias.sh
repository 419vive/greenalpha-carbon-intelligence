#!/bin/bash
# Setup Claude CLI alias for easy terminal access

CLAUDE_CLI_PATH="$(pwd)/claude_cli.py"

echo "🤖 Setting up Claude CLI alias..."

# Add alias to .zshrc (since user is using zsh)
if [ -f ~/.zshrc ]; then
    # Check if alias already exists
    if ! grep -q "alias claude=" ~/.zshrc; then
        echo "" >> ~/.zshrc
        echo "# Claude CLI alias" >> ~/.zshrc
        echo "alias claude='python $CLAUDE_CLI_PATH'" >> ~/.zshrc
        echo "✅ Added Claude CLI alias to ~/.zshrc"
    else
        echo "⚠️  Claude alias already exists in ~/.zshrc"
    fi
else
    echo "❌ ~/.zshrc not found"
fi

# Add alias to .bash_profile as backup
if [ -f ~/.bash_profile ]; then
    if ! grep -q "alias claude=" ~/.bash_profile; then
        echo "" >> ~/.bash_profile
        echo "# Claude CLI alias" >> ~/.bash_profile
        echo "alias claude='python $CLAUDE_CLI_PATH'" >> ~/.bash_profile
        echo "✅ Added Claude CLI alias to ~/.bash_profile"
    fi
fi

echo ""
echo "🎉 Claude CLI setup complete!"
echo ""
echo "To use Claude CLI immediately:"
echo "  source ~/.zshrc"
echo "  claude --setup    # First time setup with API key"
echo "  claude -m 'Hello Claude!'"
echo "  claude --interactive"
echo ""
echo "After sourcing, you can use 'claude' from anywhere in your terminal!" 