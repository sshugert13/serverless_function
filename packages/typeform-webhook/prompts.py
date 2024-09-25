import json
from config import (
    INITIAL_ANALYSIS_PROMPT,
    CORE_VALUES_PROMPT,
    PSYCHOLOGICAL_DRIVERS_PROMPT,
    LIFE_NARRATIVE_PROMPT,
    GROWTH_OPPORTUNITIES_PROMPT,
    FINAL_REPORT_PROMPT
)

def initial_analysis_prompt(raw_responses, previous_results):
    return INITIAL_ANALYSIS_PROMPT.format(raw_responses=json.dumps(raw_responses))

def core_values_prompt(raw_responses, previous_results):
    return CORE_VALUES_PROMPT.format(previous_results=previous_results['Initial Analysis'])

def psychological_drivers_prompt(raw_responses, previous_results):
    return PSYCHOLOGICAL_DRIVERS_PROMPT.format(
        initial_analysis=previous_results['Initial Analysis'],
        core_values=previous_results['Core Values']
    )

def life_narrative_prompt(raw_responses, previous_results):
    return LIFE_NARRATIVE_PROMPT.format(
        initial_analysis=previous_results['Initial Analysis'],
        core_values=previous_results['Core Values'],
        psychological_drivers=previous_results['Psychological Drivers']
    )

def growth_opportunities_prompt(raw_responses, previous_results):
    return GROWTH_OPPORTUNITIES_PROMPT.format(
        initial_analysis=previous_results['Initial Analysis'],
        core_values=previous_results['Core Values'],
        psychological_drivers=previous_results['Psychological Drivers'],
        life_narrative=previous_results['Life Narrative']
    )

def final_report_prompt(raw_responses, previous_results):
    return FINAL_REPORT_PROMPT.format(
        initial_analysis=previous_results['Initial Analysis'],
        core_values=previous_results['Core Values'],
        psychological_drivers=previous_results['Psychological Drivers'],
        life_narrative=previous_results['Life Narrative'],
        growth_opportunities=previous_results['Growth Opportunities']
    )