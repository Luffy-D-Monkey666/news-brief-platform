# 安装Ollama并拉取模型
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2:7b

# 或使用Llama 3
# ollama pull llama3

echo "Ollama安装完成！"
echo "请确保Ollama服务正在运行: ollama serve"
