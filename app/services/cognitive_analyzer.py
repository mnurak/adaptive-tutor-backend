from app.schemas.cognitive_profile import (
    CognitiveProfileUpdate, InstructionFlow, InputPreference, LearningAutonomy, ComplexityTolerance
)

# A mapping of keywords to cognitive traits
# In a real system, this would be a complex ML model.
KEYWORD_MAPPING = {
    # Instruction Flow
    InstructionFlow.global_: ["detail", "how", "why", "explain", "concept"],
    InstructionFlow.sequential: ["step-by-step", "process", "steps", "procedure", "how to"],
    
    # Input Preference
    InputPreference.visual: ["chart", "diagram", "visualize", "draw", "picture", "graph"],
    InputPreference.verbal: ["explain", "describe", "list", "tell me", "words"],

    # Learning Autonomy
    LearningAutonomy.guided: ["guide me", "help me", "your help", "show me"],
    LearningAutonomy.independent: ["let me try", "i want to solve", "give me a hint"],

    # Complexity Tolerance
    ComplexityTolerance.low: ["simple", "basic", "easy", "fundamental", "break it down"],
    ComplexityTolerance.high: ["advanced", "complex", "in-depth", "thorough", "elaborate"],
}

class CognitiveAnalyzerService:
    """
    Analyzes a user's prompt to infer their current cognitive state.
    """
    def analyze_prompt(self, prompt: str) -> tuple[CognitiveProfileUpdate, float]:
        """
        Analyzes the prompt and returns an updated cognitive profile and a confidence score.

        Args:
            prompt: The student's text query.

        Returns:
            A tuple containing a CognitiveProfileUpdate schema and a confidence score.
        """
        prompt_lower = prompt.lower()
        detected_traits = {}
        found_keywords = 0

        # Analyze each cognitive dimension based on keywords
        for trait, keywords in KEYWORD_MAPPING.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    found_keywords += 1
                    # Map the detected trait enum to its corresponding profile field
                    if isinstance(trait, InstructionFlow):
                        detected_traits["instruction_flow"] = trait
                    elif isinstance(trait, InputPreference):
                        detected_traits["input_preference"] = trait
                    elif isinstance(trait, LearningAutonomy):
                        detected_traits["learning_autonomy"] = trait
                    elif isinstance(trait, ComplexityTolerance):
                        detected_traits["complexity_tolerance"] = trait
                    break # Move to the next trait once a keyword is found

        # Calculate a simple confidence score
        # (Number of dimensions with detected keywords) / (Total dimensions we're analyzing)
        confidence = len(detected_traits) / 4.0 if found_keywords > 0 else 0.0
        
        # Ensure confidence is between a reasonable range (e.g., 0.1 to 0.9)
        confidence = min(max(confidence, 0.1), 0.9)

        # Create a Pydantic model for the update
        updated_profile = CognitiveProfileUpdate(**detected_traits)
        
        return updated_profile, confidence

cognitive_analyzer_service = CognitiveAnalyzerService()