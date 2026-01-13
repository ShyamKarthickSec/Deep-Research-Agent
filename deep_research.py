import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from clarifier_agent import clarifier_agent, ClarifyingQuestions
from agents import Runner

load_dotenv(override=True)

# Default fallback questions in case the clarifier agent fails
DEFAULT_QUESTIONS = [
    "What specific aspect or subtopic should the research focus on?",
    "What time period or date range is most relevant?",
    "Are there any specific geographic regions or countries of interest?",
    "What level of technical detail or depth are you looking for?"
]

async def generate_questions(query: str, state: dict):
    """Generate clarifying questions for the user's query."""
    if not query or not query.strip():
        yield (
            state,
            "",
            "⚠️ Please enter a research query first.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )
        return
    
    # Update state with query
    state["query"] = query.strip()
    
    # Show status
    yield (
        state,
        "",
        "🤔 Generating clarifying questions...",
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False)
    )
    
    try:
        # Call the clarifier agent
        result = await Runner.run(
            clarifier_agent,
            f"Research query: {query}",
        )
        questions = result.final_output_as(ClarifyingQuestions).questions
        
        # Ensure we have exactly 4 questions
        if len(questions) != 4:
            questions = DEFAULT_QUESTIONS[:4]
    except Exception as e:
        print(f"Clarifier agent failed: {e}, using default questions")
        questions = DEFAULT_QUESTIONS[:4]
    
    # Store questions in state
    state["questions"] = questions
    
    # Format questions for display
    questions_md = "## 📝 Clarifying Questions\n\n"
    questions_md += "Please answer these questions to help refine the research:\n\n"
    for i, q in enumerate(questions, 1):
        questions_md += f"{i}. {q}\n"
    
    # Create answer placeholders
    answers_text = "\n\n".join([f"**Q{i}:** {q}\n**A{i}:** " for i, q in enumerate(questions, 1)])
    
    yield (
        state,
        questions_md,
        "✅ Questions generated! Please fill in your answers above.",
        gr.update(value=answers_text, visible=True),
        gr.update(visible=True),
        gr.update(visible=True)
    )

async def run_research(query: str, answers_text: str, state: dict):
    """Run the deep research with the refined prompt."""
    if not state.get("query") or not state.get("questions"):
        yield "⚠️ Please generate clarifying questions first."
        return
    
    # Update status
    yield "🚀 Starting deep research...\n\n"
    
    # Parse answers from the text box
    answers = []
    lines = answers_text.split("\n")
    for line in lines:
        if line.startswith("**A") and ":" in line:
            answer = line.split(":", 1)[1].strip()
            if answer:
                answers.append(answer)
    
    # Build refined prompt
    refined_prompt = f"""Original Query: {state['query']}

Clarifying Information:
"""
    for i, (q, a) in enumerate(zip(state['questions'], answers), 1):
        answer_text = answers[i-1] if i-1 < len(answers) else "(not answered)"
        refined_prompt += f"\nQ{i}: {q}\nA{i}: {answer_text}\n"
    
    refined_prompt += f"\n\nBased on the above query and clarifications, conduct comprehensive research."
    
    # Run the existing research pipeline with the refined prompt
    async for chunk in ResearchManager().run(refined_prompt):
        yield chunk

def reset_ui():
    """Reset the entire UI to initial state."""
    return (
        {},  # Clear state
        "",  # Clear query
        "",  # Clear questions display
        "",  # Clear status
        gr.update(value="", visible=False),  # Clear and hide answers
        gr.update(visible=False),  # Hide run button
        gr.update(visible=False),  # Hide reset button
        ""  # Clear report
    )

# Build the UI
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# 🔬 Shyam's Deep Research Assistant")
    gr.Markdown("*Enhanced with intelligent clarification for better research results*")
    
    # State to hold query, questions, and answers
    state = gr.State({})
    
    with gr.Group():
        gr.Markdown("### Step 1: Enter Your Research Query")
        query_textbox = gr.Textbox(
            label="What topic would you like to research today?",
            placeholder="e.g., Impact of artificial intelligence on healthcare",
            lines=2
        )
        clarify_button = gr.Button("🎯 Next: Clarify", variant="primary", size="lg")
    
    with gr.Group():
        gr.Markdown("### Step 2: Refine Your Research")
        questions_display = gr.Markdown("")
        status_text = gr.Markdown("")
        
        answers_textbox = gr.Textbox(
            label="Your Answers",
            placeholder="Fill in your answers after each A1:, A2:, etc.",
            lines=12,
            visible=False
        )
        
        with gr.Row():
            run_button = gr.Button("🚀 Run Deep Research", variant="primary", size="lg", visible=False)
            reset_button = gr.Button("🔄 Reset", variant="secondary", visible=False)
    
    with gr.Group():
        gr.Markdown("### Research Report")
        report = gr.Markdown("")
    
    # Wire up the event handlers
    clarify_button.click(
        fn=generate_questions,
        inputs=[query_textbox, state],
        outputs=[state, questions_display, status_text, answers_textbox, run_button, reset_button]
    )
    
    run_button.click(
        fn=run_research,
        inputs=[query_textbox, answers_textbox, state],
        outputs=report
    )
    
    reset_button.click(
        fn=reset_ui,
        inputs=[],
        outputs=[state, query_textbox, questions_display, status_text, answers_textbox, run_button, reset_button, report]
    )

ui.launch(inbrowser=True)

