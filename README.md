# Educational Content Generator with AI Agents

A multi-agent system that generates and reviews educational content using AI. Built with Groq LLMs, Python, and Streamlit.

## 🎯 Features

- **Two AI Agents:**
  - **Generator Agent**: Creates grade-appropriate educational content with explanation and 3 MCQs
  - **Reviewer Agent**: Evaluates content for quality, clarity, and age-appropriateness
- **Automatic Refinement**: If content fails review, it's automatically improved based on feedback

- **Interactive UI**: Clean Streamlit interface showing the complete agent pipeline

## 🏗️ Architecture

```
User Input (Grade + Topic)
    ↓
Generator Agent → Initial Content
    ↓
Reviewer Agent → Review (Pass/Fail + Feedback)
    ↓
[If Fail] Generator Agent → Refined Content
    ↓
Final Output
```

## 📋 Requirements

- Python 3.13+
- uv package manager
- Groq API key

## 🚀 Setup

1. **Clone or navigate to the project directory**

2. **Install dependencies using uv:**

   ```bash
   uv sync
   ```

3. **Set up your Groq API key:**
   - Copy `.env.example` to `.env`
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_actual_key_here
     ```
   - Get your key from: https://console.groq.com/keys

4. **Activate the virtual environment:**

   ```bash
   # Windows
   .venv\Scripts\activate

   # Linux/Mac
   source .venv/bin/activate
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

1. Enter your Groq API key in the sidebar (or set it in `.env`)
2. Select the grade level (1-12)
3. Enter the educational topic
4. Click "Generate Content"
5. View the pipeline flow and results:
   - Initial generation
   - Review feedback
   - Refined output (if needed)

## 🏛️ Project Structure

```
.
├── app.py                  # Streamlit UI
├── generator_agent.py      # Generator Agent class
├── reviewer_agent.py       # Reviewer Agent class
├── pipeline.py            # Pipeline orchestration
├── pyproject.toml         # Dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 Components

### Generator Agent

- **Responsibility**: Generate educational content
- **Input**: `{"grade": int, "topic": str}`
- **Output**: `{"explanation": str, "mcqs": [...]}`
- Uses Groq's LLM to create age-appropriate content

### Reviewer Agent

- **Responsibility**: Evaluate content quality
- **Input**: Content JSON + grade + topic
- **Output**: `{"status": "pass|fail", "feedback": [...]}`
- Evaluates:
  - Age appropriateness
  - Conceptual correctness
  - Clarity

### Pipeline

- Orchestrates both agents
- Handles refinement (max 1 pass)
- Returns all intermediate results for transparency

## 🎓 Example

**Input:**

- Grade: 4
- Topic: "Types of angles"

**Output:**

- Clear explanation of angles
- 3 MCQs with 4 options each
- Review feedback
- Refined version (if needed)

## 📝 Notes

- The system uses Groq's `llama-3.1-8b-instant` model
- Content refinement is limited to one pass to avoid infinite loops
- All agent interactions are visible in the UI for transparency

## 🤝 Contributing

Feel free to submit issues or pull requests!

## 📄 License

MIT License
