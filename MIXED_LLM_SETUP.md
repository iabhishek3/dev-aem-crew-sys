# Mixed LLM Provider Setup

This project now supports using different LLM providers for different agents, allowing you to optimize for stability and performance.

## Current Configuration

### Agents and Their LLMs:

1. **webdesigner** → Uses Anthropic Claude (via `MODEL` env var)
   - Good for design analysis and vision tasks
   - Default: `claude-3-5-sonnet-20241022`

2. **component_developer** → Uses Anthropic Claude (via `MODEL` env var)
   - Good for HTML/CSS generation
   - Default: `claude-3-5-sonnet-20241022`

3. **aem_developer** → Uses OpenAI GPT (via `AEM_MODEL` env var)
   - Better stability for complex multi-step AEM conversion tasks
   - Default: `gpt-4o`
   - Falls back to Anthropic if `AEM_MODEL` is not set or `OPENAI_API_KEY` is missing

## Setup Instructions

### 1. Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-proj-...` or `sk-...`)

### 2. Update .env File

Open `.env` and replace `your-openai-api-key-here` with your actual OpenAI API key:

```env
# Model specifically for AEM agent (use OpenAI for better stability)
AEM_MODEL=gpt-4o
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 3. Test the Setup

Run the test script to verify the AEM agent is using OpenAI:

```bash
python test_aem_agent.py
```

You should see the agent create AEM component files successfully.

## Available Models

### OpenAI Models (for AEM_MODEL):
- `gpt-4o` - Latest, most capable (recommended)
- `gpt-4-turbo` - Fast and capable
- `gpt-4` - Reliable, slightly slower
- `gpt-3.5-turbo` - Cheaper, less capable

### Anthropic Models (for MODEL):
- `claude-3-5-sonnet-20241022` - Good balance (recommended)
- `claude-3-opus-20240229` - Most powerful but slow
- `claude-3-haiku-20240307` - Fastest/cheapest

## Switching Back to All Anthropic

If you want to use Anthropic for all agents:

1. Remove or comment out the `AEM_MODEL` line in `.env`:
   ```env
   # AEM_MODEL=gpt-4o
   ```

2. The AEM agent will automatically fall back to using `MODEL` (Anthropic)

## Cost Considerations

### OpenAI Pricing (approximate):
- GPT-4o: $2.50 per 1M input tokens, $10 per 1M output tokens
- GPT-4-turbo: $10 per 1M input tokens, $30 per 1M output tokens

### Anthropic Pricing (approximate):
- Claude 3.5 Sonnet: $3 per 1M input tokens, $15 per 1M output tokens
- Claude 3 Opus: $15 per 1M input tokens, $75 per 1M output tokens

**Tip:** Using OpenAI just for the AEM agent (which does the heavy lifting) while keeping Anthropic for the lighter design/component tasks is a good balance of cost and performance.

## Troubleshooting

### "OpenAI API key not found"
- Make sure you've added your OpenAI API key to `.env`
- Ensure there are no extra spaces or quotes around the key

### "Model not found" error
- Check that the model name is correct
- Some older models may not be available on your OpenAI account

### AEM agent still using Anthropic
- Verify `AEM_MODEL` is set in `.env`
- Check that the model name starts with `gpt` (e.g., `gpt-4o`)
- Restart your Python process after changing `.env`

## Why This Hybrid Approach?

Based on extensive testing:

✅ **OpenAI GPT-4o** for AEM agent:
- More stable API responses
- Better at complex multi-step file generation tasks
- Faster than Claude Opus for similar quality

✅ **Anthropic Claude Sonnet** for design/component agents:
- Excellent vision capabilities for design analysis
- Good HTML/CSS generation
- Cost-effective for simpler tasks

This gives you the best of both worlds!
