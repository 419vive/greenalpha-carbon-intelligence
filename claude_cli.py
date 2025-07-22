#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Claude CLI - Terminal Interface for Claude AI
Simple CLI wrapper for Anthropic's Claude using the Python API
"""

import os
import sys
import argparse
from anthropic import Anthropic
import json
from pathlib import Path

class ClaudeCLI:
    def __init__(self):
        self.client = None
        self.config_file = Path.home() / '.claude_cli_config'
        self.load_config()
    
    def load_config(self):
        """Load API key from config file or environment"""
        api_key = None
        
        # Try to load from environment first
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Try to load from config file
        if not api_key and self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key')
            except:
                pass
        
        if api_key:
            self.client = Anthropic(api_key=api_key)
            return True
        return False
    
    def save_config(self, api_key):
        """Save API key to config file"""
        config = {'api_key': api_key}
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ API key saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
            return False
    
    def setup_api_key(self):
        """Interactive API key setup"""
        print("🔑 Claude CLI Setup")
        print("=" * 40)
        print("To use Claude CLI, you need an Anthropic API key.")
        print("Get one at: https://console.anthropic.com/")
        print()
        
        api_key = input("Enter your Anthropic API key: ").strip()
        
        if api_key:
            # Test the API key
            try:
                test_client = Anthropic(api_key=api_key)
                # Try a simple test message
                response = test_client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=10,
                    messages=[{"role": "user", "content": "Hi"}]
                )
                
                # If we get here, the API key works
                self.save_config(api_key)
                self.client = test_client
                print("✅ API key verified and saved!")
                return True
                
            except Exception as e:
                print(f"❌ API key verification failed: {e}")
                return False
        else:
            print("❌ No API key provided")
            return False
    
    def chat(self, message, model="claude-3-haiku-20240307", max_tokens=4000):
        """Send a message to Claude"""
        if not self.client:
            print("❌ Claude CLI not configured. Run: python claude_cli.py --setup")
            return False
        
        try:
            print(f"🤖 Claude ({model}):")
            print("-" * 40)
            
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": message}]
            )
            
            print(response.content[0].text)
            print()
            return True
            
        except Exception as e:
            print(f"❌ Error communicating with Claude: {e}")
            return False
    
    def interactive_mode(self):
        """Start interactive chat mode"""
        if not self.client:
            print("❌ Claude CLI not configured. Run: python claude_cli.py --setup")
            return
        
        print("🤖 Claude Interactive Mode")
        print("=" * 40)
        print("Type 'exit' or 'quit' to end the session")
        print("Type '/help' for commands")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', '/exit', '/quit']:
                    print("👋 Goodbye!")
                    break
                elif user_input == '/help':
                    print("\n📚 Commands:")
                    print("  /help    - Show this help")
                    print("  /clear   - Clear screen")
                    print("  /model   - Show current model")
                    print("  exit     - Exit interactive mode")
                    print()
                elif user_input == '/clear':
                    os.system('clear' if os.name == 'posix' else 'cls')
                elif user_input == '/model':
                    print("🎛️  Current model: claude-3-haiku-20240307")
                    print()
                elif user_input:
                    self.chat(user_input)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

def main():
    parser = argparse.ArgumentParser(description="Claude CLI - Terminal interface for Claude AI")
    parser.add_argument('--setup', action='store_true', help='Setup API key')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive mode')
    parser.add_argument('--message', '-m', type=str, help='Send a single message')
    parser.add_argument('--model', type=str, default='claude-3-haiku-20240307', 
                       choices=['claude-3-opus-20240229', 'claude-3-haiku-20240307', 'claude-3-haiku-20240307'],
                       help='Claude model to use')
    
    args = parser.parse_args()
    
    cli = ClaudeCLI()
    
    if args.setup:
        cli.setup_api_key()
    elif args.message:
        cli.chat(args.message, model=args.model)
    elif args.interactive:
        cli.interactive_mode()
    else:
        # Default behavior - show help and suggest setup if not configured
        if not cli.client:
            print("🤖 Claude CLI")
            print("=" * 40)
            print("Welcome to Claude CLI!")
            print()
            print("First time setup:")
            print("  python claude_cli.py --setup")
            print()
            print("Usage examples:")
            print("  python claude_cli.py -m 'Hello Claude!'")
            print("  python claude_cli.py --interactive")
            print()
            print("Need help? python claude_cli.py --help")
        else:
            print("🤖 Claude CLI is ready!")
            print("Usage: python claude_cli.py -m 'your message' or --interactive")

if __name__ == "__main__":
    main() 