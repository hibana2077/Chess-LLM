RESPONSE_FORMAT_THINK = """
**Please respond in the following format (must be valid JSON):**
```json
{{
    "analysis": "Your detailed analysis of the current position, including threats, opportunities, strategic considerations, etc.",
    "candidate_moves": [ # maximum 3 candidate moves, only think about moves that are legal
        {{
            "move": "UCI format of the move",
            "evaluation": "Evaluation and reasoning for this move"
        }}
    ],
    "chosen_move": "UCI format of the chosen move",
    "reasoning": "Main reasons and strategic goals for choosing this move"
}}
```
"""

RESPONSE_FORMAT_WITHOUT_THINK = """
**Please respond in the following format (must be valid JSON):**
```json
{{
    "chosen_move": "UCI format of the chosen move"
}}
```
"""