from app.models.user import User
from app.schemas.concept import Neo4jConcept

def build_llm_prompt(user: User, analysis: dict) -> str:
    """
    Constructs a sophisticated, multi-faceted prompt for the LLM based on a
    full concept analysis and the student's cognitive profile.
    """
    profile = user.cognitive_profile
    target_concept = analysis['target_concept']

    # --- 1. Build the Student Profile Block ---
    profile_str = (
        f"[STUDENT PROFILE]\n"
        f"Instruction Flow: {profile.instruction_flow.value.capitalize()}\n"
        f"Input Preference: {profile.input_preference.value.capitalize()}\n"
        f"Engagement Style: {profile.engagement_style.value.capitalize()}\n"
        f"Complexity Tolerance: {profile.complexity_tolerance.value.capitalize()}\n"
    )

    # --- 2. Build the Rich Learning Context Block ---
    context_str = f"\n[LEARNING CONTEXT]\n"
    context_str += f"Target Concept: {target_concept.name} (Type: {target_concept.type}, Complexity: {target_concept.complexity})\n"
    
    if analysis['prerequisites']:
        prereqs = ", ".join([p.name for p in analysis['prerequisites']])
        context_str += f"Prerequisites: {prereqs}\n"
        
    if analysis['subtopics']:
        subtopics = ", ".join([s.name for s in analysis['subtopics']])
        context_str += f"Key Subtopics to cover: {subtopics}\n"
        
    if analysis['related_concepts']:
        related = ", ".join([r.name for r in analysis['related_concepts']])
        context_str += f"Connect this to related concepts like: {related}\n"

    # --- 3. Dynamically Generate the Request Block ---
    request_str = "\n[REQUEST]\n"
    request_parts = []

    request_parts.append(f"You are an expert DSA tutor. Your task is to generate a lesson about '{target_concept.name}'.")

    if profile.complexity_tolerance == 'low':
        request_parts.append("Explain it in simple, beginner-friendly terms using a real-world analogy.")
    else:
        request_parts.append("Provide a detailed, in-depth explanation suitable for an intermediate learner.")
        if target_concept.practical_applications:
            apps = ", ".join(target_concept.practical_applications)
            request_parts.append(f"Mention its practical applications, such as {apps}.")

    if profile.input_preference == 'visual' and analysis['subtopics']:
        request_parts.append("Include a mermaid.js flowchart to visualize the relationship between the key subtopics.")
    else:
        request_parts.append("Structure the explanation as clear, well-formatted text.")

    if profile.engagement_style == 'active':
        request_parts.append("Conclude with an interactive challenge or a thought-provoking question to test understanding.")
    else:
        request_parts.append("Conclude with a concise summary of the 3 most important takeaways.")
    
    request_str += " ".join(request_parts)

    return f"{profile_str}{context_str}{request_str}"