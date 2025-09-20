from transformers import pipeline
from typing import Dict, List
import numpy as np
import torch

from app.schemas.cognitive_profile import CognitiveProfileUpdate, InstructionFlow, InputPreference, LearningAutonomy, ComplexityTolerance
from app.models.cognitive_profile import CognitiveProfile # Import the DB model

class MLCognitiveAnalyzerService:
    def __init__(self, adaptation_rate=0.1, decay_rate=0.05):
        self.adaptation_rate = adaptation_rate
        self.decay_rate = decay_rate
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="MoritzLaurer/deberta-v3-base-zeroshot-v1"
        )
        self.dimensions = self._define_dimensions()

    def _define_dimensions(self) -> Dict[str, List]:
        """Maps our internal dimension names to the Enum options."""
        return {
            'instruction_flow': list(InstructionFlow),
            'input_preference': list(InputPreference),
            'learning_autonomy': list(LearningAutonomy),
            'complexity_tolerance': list(ComplexityTolerance),
        }

    def analyze_prompt(self, prompt: str, current_profile: CognitiveProfile) -> (CognitiveProfileUpdate, float):
        """
        Analyzes a prompt using the ML model against a provided cognitive profile.
        This method is now stateless.
        """
        prompt = prompt.strip()
        
        # Create a mutable dictionary of the user's current profile scores.
        # This simulates the ML-based profile scores, starting from the DB state.
        # A more advanced version could store these scores in the DB.
        profile_scores = {
            dim: {opt.value: 0.5 for opt in options} for dim, options in self.dimensions.items()
        }
        
        dominant_styles = {}
        confidence_scores = []

        for dim, options in self.dimensions.items():
            option_labels = [opt.value for opt in options]
            result = self.classifier(prompt, option_labels, multi_label=False)
            
            top_label = result['labels'][0]
            confidence = result['scores'][0]
            
            # Apply decay to all scores in the dimension
            for opt in profile_scores[dim]:
                profile_scores[dim][opt] = max(0.0, profile_scores[dim][opt] * (1 - self.decay_rate))

            # Adapt the top-scoring label
            profile_scores[dim][top_label] = min(1.0, profile_scores[dim][top_label] + confidence * self.adaptation_rate)

            # Determine the new dominant style for this dimension
            dominant_style = max(profile_scores[dim], key=profile_scores[dim].get)
            dominant_styles[dim] = dominant_style
            confidence_scores.append(profile_scores[dim][dominant_style])

        update_schema = CognitiveProfileUpdate(**dominant_styles)
        overall_confidence = np.mean(confidence_scores)

        return update_schema, overall_confidence

ml_cognitive_analyzer_service = MLCognitiveAnalyzerService()