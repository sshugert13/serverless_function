import os
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from prompts import (
    initial_analysis_prompt,
    core_values_prompt,
    psychological_drivers_prompt,
    life_narrative_prompt,
    growth_opportunities_prompt,
    final_report_prompt
)

def get_anthropic_client():
    return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def run_analysis(anthropic, raw_responses):
    analysis_steps = [
        ("Initial Analysis", initial_analysis_prompt),
        ("Core Values", core_values_prompt),
        ("Psychological Drivers", psychological_drivers_prompt),
        ("Life Narrative", life_narrative_prompt),
        ("Growth Opportunities", growth_opportunities_prompt),
        ("Final Report", final_report_prompt)
    ]
    
    results = {}
    for step_name, prompt_func in analysis_steps:
        prompt = prompt_func(raw_responses, results)
        completion = anthropic.completions.create(
            model="claude-2",
            prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
            max_tokens_to_sample=2000
        )
        results[step_name] = completion.completion
    
    return results