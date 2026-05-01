# llama-server Prompt Runner

This project contains a small Python script that:
- reads `./input.txt` completely as a single prompt,
- sends it to a running `llama-server` endpoint,
- prints the response to console,
- writes the same response to `./output.txt`.

## 1) Create venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Install dependency

```bash
pip install llama-cpp-python
```

## 3) Start your llama-server

Example command:

```bash
./build/bin/llama-server \
  -m ~/models/Qwen3.6-27B-LTSpice-v64-Q4_K_S.gguf \
  --port 8080 \
  -t 8 \
  --ctx-size 100000 \
  --temp 0.6 \
  --top-p 0.95 \
  --top-k 20 \
  --min-p 0.00 \
  --presence-penalty 0.0 \
  -ngl 99 \
  -np 2 \
  -fa 1 \
  --cache-ram 2048 \
  --chat-template-kwargs '{"enable_thinking": false}' \
  --metrics
```

## 4) Run the client script

```bash
source .venv/bin/activate
python3 send_input_to_llama_server.py
```

Optional args:

```bash
python3 send_input_to_llama_server.py \
  --input ./input.txt \
  --output ./output.txt \
  --url http://127.0.0.1:8080/v1/chat/completions \
  --model Qwen3.6-27B-LTSpice-v64-Q4_K_S.gguf \
  --max-tokens 2048
```

## Files

- `send_input_to_llama_server.py`: client script
- `input.txt`: prompt source
- `output.txt`: response output (created after successful run)
