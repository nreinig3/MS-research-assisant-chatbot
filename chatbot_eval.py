# chatbot_eval.py
# Run this manually by pasting chatbot's responses

questions = [
    "What are common side effects of Ocrevus?",
    "Who is eligible for the MS clinical trial NCT07067463?",
    "Can pregnancy worsen MS symptoms?",
    "What's the difference between relapsing and progressive MS?",
    "Is there a cure for multiple sclerosis?",
    "How does diet affect MS progression?",
    "What should I do if I miss a dose of Tecfidera?",
    "Are there any FDA-approved treatments for primary progressive MS?",
    "Can exercise help with MS fatigue?",
    "Should I get the COVID-19 vaccine if I'm on immunosuppressants for MS?"
]

# Manually paste chatbot's response for each question
chatbot_responses = [
    "I don't have that information in my knowledge base. Please consult a \
        healthcare provider or refer to official prescribing information for \
            Ocrevus (ocrelizumab). The provided context does not list common side effects of the medication.",
    "I don't have that information in my knowledge base. The clinical trial \
        NCT04173273 is not mentioned in any of the provided documents. Please \
            consult the clinical trial registry or a healthcare provider for eligibility details.",
    "I don't have that information in my knowledge base. Please consult a healthcare provider."
    # ... etc
]

# Manual rating (I'll fill this in after reviewing the responses)
ratings = {
    "Correct": 0,
    "Partially correct": 0,
    "Hallucinated": 0,
    "Appropriate refusal": 0
}

# After reviewing each response, increment the appropriate rating

print(f"Correct: {ratings['Correct']}/{len(questions)} = {ratings['Correct']/len(questions)*100:.0f}%")
print(f"Hallucinated: {ratings['Hallucinated']}/{len(questions)}")