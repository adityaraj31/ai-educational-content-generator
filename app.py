import streamlit as st
import os
from dotenv import load_dotenv
from pipeline import ContentPipeline
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Educational Content Generator",
    page_icon="📚",
    layout="wide"
)

# Title and description
st.title("📚 AI Educational Content Generator")
st.markdown("""
This application uses two AI agents to generate educational content:
- **Generator Agent**: Creates explanations and MCQs tailored to the grade level
- **Reviewer Agent**: Evaluates content quality and provides feedback
- **Automatic Refinement**: If content fails review, it's automatically improved
""")

# Sidebar for inputs
st.sidebar.header("Configuration")

# API Key input
api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    value=os.getenv("GROQ_API_KEY", ""),
    help="Enter your Groq API key"
)

st.sidebar.markdown("---")
st.sidebar.header("Content Parameters")

# Grade selection
grade = st.sidebar.number_input(
    "Grade Level",
    min_value=1,
    max_value=12,
    value=4,
    help="Select the target grade level"
)

# Topic input
topic = st.sidebar.text_input(
    "Topic",
    value="Types of angles",
    help="Enter the educational topic"
)

# Generate button
generate_button = st.sidebar.button("🚀 Generate Content", type="primary", use_container_width=True)

# Main content area
if generate_button:
    if not api_key:
        st.error("⚠️ Please provide a Groq API key in the sidebar.")
    elif not topic:
        st.error("⚠️ Please enter a topic.")
    else:
        with st.spinner("🤖 AI Agents are working..."):
            try:
                # Initialize pipeline
                pipeline = ContentPipeline(api_key)
                
                # Generate content
                result = pipeline.generate_content(grade, topic)
                initial_content, initial_review, refined_content, refined_review = result
                
                # Store in session state
                st.session_state.initial_content = initial_content
                st.session_state.initial_review = initial_review
                st.session_state.refined_content = refined_content
                st.session_state.refined_review = refined_review
                st.session_state.grade = grade
                st.session_state.topic = topic
                
                st.success("✅ Content generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display results if available
if 'initial_content' in st.session_state:
    st.markdown("---")
    st.header("📋 Generation Pipeline Results")
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["🔄 Pipeline Flow", "📝 Initial Generation", "✨ Final Output"])
    
    with tab1:
        st.subheader("Agent Pipeline Flow")
        
        # Show pipeline steps
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Step 1: Generator Agent")
            st.info("Generated initial content")
            status1 = "✅ Complete"
            st.markdown(f"**Status:** {status1}")
        
        with col2:
            st.markdown("### Step 2: Reviewer Agent")
            review_status = st.session_state.initial_review.get('status', 'unknown')
            if review_status == 'pass':
                st.success("Content passed review!")
                status2 = "✅ PASS"
            else:
                st.warning("Content needs refinement")
                status2 = "⚠️ FAIL"
            st.markdown(f"**Status:** {status2}")
        
        with col3:
            st.markdown("### Step 3: Refinement")
            if st.session_state.refined_content:
                st.info("Content was refined")
                status3 = "✅ Complete"
                refined_status = st.session_state.refined_review.get('status', 'unknown') if st.session_state.refined_review else 'unknown'
                if refined_status == 'pass':
                    st.success("Refined content passed!")
                else:
                    st.warning("Refined content reviewed")
            else:
                st.success("No refinement needed")
                status3 = "➖ Skipped"
            st.markdown(f"**Status:** {status3}")
    
    with tab2:
        st.subheader(f"Initial Generation - Grade {st.session_state.grade}: {st.session_state.topic}")
        
        # Display initial content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📖 Explanation")
            st.write(st.session_state.initial_content.get('explanation', 'No explanation generated'))
            
            st.markdown("#### ❓ Multiple Choice Questions")
            mcqs = st.session_state.initial_content.get('mcqs', [])
            for i, mcq in enumerate(mcqs, 1):
                with st.expander(f"Question {i}: {mcq.get('question', 'N/A')}"):
                    options = mcq.get('options', [])
                    for opt in options:
                        st.write(f"- {opt}")
                    st.success(f"**Correct Answer:** {mcq.get('answer', 'N/A')}")
        
        with col2:
            st.markdown("#### 🔍 Review Feedback")
            review_status = st.session_state.initial_review.get('status', 'unknown')
            
            if review_status == 'pass':
                st.success("**Status: PASS** ✅")
            else:
                st.error("**Status: FAIL** ❌")
            
            feedback = st.session_state.initial_review.get('feedback', [])
            if feedback:
                st.markdown("**Issues Found:**")
                for fb in feedback:
                    st.warning(f"• {fb}")
            else:
                st.info("No issues found")
    
    with tab3:
        st.subheader("Final Output")
        
        # Determine which content to show
        if st.session_state.refined_content:
            final_content = st.session_state.refined_content
            final_review = st.session_state.refined_review
            st.info("📝 Showing refined content (after addressing feedback)")
        else:
            final_content = st.session_state.initial_content
            final_review = st.session_state.initial_review
            st.success("✨ Initial content was approved - no refinement needed!")
        
        # Display final content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📖 Explanation")
            st.write(final_content.get('explanation', 'No explanation generated'))
            
            st.markdown("#### ❓ Multiple Choice Questions")
            mcqs = final_content.get('mcqs', [])
            for i, mcq in enumerate(mcqs, 1):
                with st.expander(f"Question {i}: {mcq.get('question', 'N/A')}", expanded=True):
                    options = mcq.get('options', [])
                    for opt in options:
                        st.write(f"- {opt}")
                    st.success(f"**Correct Answer:** {mcq.get('answer', 'N/A')}")
            
            # Download button for content
            content_json = json.dumps(final_content, indent=2)
            st.download_button(
                label="📥 Download Content (JSON)",
                data=content_json,
                file_name=f"content_grade{st.session_state.grade}_{st.session_state.topic.replace(' ', '_')}.json",
                mime="application/json"
            )
        
        with col2:
            if final_review:
                st.markdown("#### 🔍 Final Review")
                review_status = final_review.get('status', 'unknown')
                
                if review_status == 'pass':
                    st.success("**Status: PASS** ✅")
                else:
                    st.warning("**Status: FAIL** ⚠️")
                
                feedback = final_review.get('feedback', [])
                if feedback:
                    st.markdown("**Feedback:**")
                    for fb in feedback:
                        st.info(f"• {fb}")
                else:
                    st.info("No additional feedback")

else:
    # Welcome message
    st.info("👈 Configure the parameters in the sidebar and click 'Generate Content' to start!")
    
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("""
    1. **Generator Agent** creates educational content (explanation + 3 MCQs) based on grade and topic
    2. **Reviewer Agent** evaluates the content for:
        - Age appropriateness
        - Conceptual correctness
        - Clarity
    3. If the review fails, the content is **automatically refined** with feedback
    4. The final approved content is displayed with full transparency of the process
    """)
    
    st.markdown("---")
    st.markdown("### Getting Started:")
    st.markdown("""
    1. Get your Groq API key from [https://console.groq.com/keys](https://console.groq.com/keys)
    2. Enter it in the sidebar
    3. Select a grade level and topic
    4. Click 'Generate Content'
    """)
