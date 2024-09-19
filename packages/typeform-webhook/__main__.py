import os
import json
import asyncpg
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

# Global variables for reuse across invocations
db_pool = None
anthropic_client = None

async def init_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            ssl="require"
        )

def init_anthropic():
    global anthropic_client
    if anthropic_client is None:
        anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def process_webhook(args):
    try:
        await init_db_pool()
        init_anthropic()
        
        # Parse incoming request body from Typeform
        data = json.loads(args.get('__ow_body', '{}'))
        
        form_response = data.get('form_response', {})
        form_response_id = form_response.get('token')
        answers = form_response.get('answers', [])
        hidden_fields = form_response.get('hidden', {})
        
        email = hidden_fields.get('email', '')
        name = hidden_fields.get('name', '')
        raw_responses = {a['field']['ref']: a.get('text', a.get('choice', {}).get('label', '')) for a in answers}
        
        # Store response in DB
        async with db_pool.acquire() as conn:
            await store_user_response(conn, form_response_id, email, name, raw_responses)
        
        # Process with Claude
        anthropic = anthropic_client
        analysis = await run_analysis(anthropic, raw_responses)
        
        # Store analysis results
        async with db_pool.acquire() as conn:
            await store_analysis_results(conn, form_response_id, analysis)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "message": "Webhook processed successfully"})
        }
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)})
        }

async def store_user_response(conn, form_response_id, email, name, raw_responses):
    await conn.execute(
        """
        INSERT INTO user_responses (form_response_id, email, name, submitted_at, raw_responses)
        VALUES ($1, $2, $3, CURRENT_TIMESTAMP, $4)
        """,
        form_response_id, email, name, json.dumps(raw_responses)
    )

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

async def store_analysis_results(conn, form_response_id, analysis):
    user_response = await conn.fetchrow(
        "SELECT id FROM user_responses WHERE form_response_id = $1",
        form_response_id
    )
    if user_response:
        await conn.execute(
            """
            INSERT INTO analysis_results (
                user_response_id, initial_analysis, core_values, 
                psychological_analysis, life_narrative, 
                growth_opportunities, final_report
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            user_response['id'],
            analysis['Initial Analysis'],
            analysis['Core Values'],
            analysis['Psychological Drivers'],
            analysis['Life Narrative'],
            analysis['Growth Opportunities'],
            analysis['Final Report']
        )
    else:
        raise Exception("User response not found")

def initial_analysis_prompt(raw_responses, previous_results):
    return f"""You are a skilled life coach and psychologist tasked with analyzing a user's detailed responses to a self-discovery questionnaire. Your goal is to provide an in-depth initial analysis that identifies:

1. **Recurring Themes**: Highlight any common themes or patterns that appear throughout the responses.
2. **Core Values and Motivations**: Extract key values and motivations that seem important to the user.
3. **Significant Life Experiences**: Note any impactful events or experiences that have shaped the user's perspective.
4. **Emotional Tone**: Observe the emotional undertones in their answers (e.g., excitement, frustration, hope).

**Instructions:**

- **Use Direct Quotes**: Where appropriate, include brief quotes from the user's responses to support your analysis.
- **Be Empathetic and Objective**: Present your findings in a compassionate yet unbiased manner.
- **Structure**: Organize your analysis into clear sections with headings.

**User Responses:**

{json.dumps(raw_responses)}

**Example Format:**

---

**Recurring Themes:**

- Theme 1: Description with supporting quotes.
- Theme 2: Description with supporting quotes.

**Core Values and Motivations:**

- Value 1: Explanation.
- Value 2: Explanation.

**Significant Life Experiences:**

- Experience 1: Impact and insights.

**Emotional Tone:**

- Observations about the user's emotional expressions.

---"""

def core_values_prompt(raw_responses, previous_results):
    return f"""Using the initial analysis provided, identify the top three core values that are most prominent for the user. For each core value, create a detailed profile that includes:

1. **Definition**: Provide a clear and concise definition of the value.
2. **Manifestation**: Describe how this value shows up in the user's life, citing specific examples from their responses.
3. **Significance**: Explain why this value is important to the user and how it influences their decisions and actions.
4. **Conflicts or Synergies**: Identify any potential conflicts with other values or how it complements them.

**Instructions:**

- **Personalization**: Tailor the explanations to the user's unique experiences.
- **Support with Evidence**: Reference specific parts of the user's responses.
- **Empathetic Tone**: Write in a way that resonates with the user's feelings and perspectives.

**Initial Analysis:**

{previous_results['Initial Analysis']}

**Example Format:**

---

**Core Value 1: [Value Name]**

- **Definition**: [Provide definition]
- **Manifestation**: [Explain with examples]
- **Significance**: [Describe importance]
- **Conflicts or Synergies**: [Discuss relationships with other values]

**Core Value 2: [Value Name]**

[Repeat the structure]

---"""

def psychological_drivers_prompt(raw_responses, previous_results):
    return f"""Delve deeper into the user's psyche to uncover subtle psychological aspects. Your analysis should cover:

1. **Hidden Motivations**: Identify underlying drivers that may not be overtly stated.
2. **Cognitive Biases and Blind Spots**: Highlight any biases that could affect the user's perception or decisions.
3. **Emotional Patterns**: Observe recurring emotional responses or themes.
4. **Resilience and Coping**: Assess how the user deals with challenges, including strengths and areas for improvement.

**Instructions:**

- **Evidence-Based**: Use specific examples from the user's responses to support each point.
- **Non-Judgmental Language**: Present findings respectfully without assigning blame.
- **Actionable Insights**: Where appropriate, suggest areas for self-reflection.

**Previous Analyses:**

- **Initial Analysis**: {previous_results['Initial Analysis']}
- **Core Values**: {previous_results['Core Values']}

**Example Format:**

---

**Hidden Motivations:**

- Observation 1: Explanation with supporting evidence.
- Observation 2: Explanation with supporting evidence.

**Cognitive Biases and Blind Spots:**

- Bias 1: Description and impact.
- Bias 2: Description and impact.

**Emotional Patterns:**

- Pattern 1: Details and examples.

**Resilience and Coping:**

- Strengths: List and explain.
- Areas for Development: List and explain.

---"""

def life_narrative_prompt(raw_responses, previous_results):
    return f"""Synthesize the information from previous analyses to craft a cohesive life narrative for the user. This narrative should:

1. **Life Story Highlights**: Outline significant events and experiences that have shaped the user.
2. **Sense of Purpose**: Describe what gives the user a sense of meaning.
3. **Value-Behavior Alignment**: Identify where the user's actions align or misalign with their stated values.
4. **Internal Conflicts and Harmonies**: Explore any inner tensions or areas of congruence.

**Instructions:**

- **Narrative Style**: Write in the third person, presenting the user's story empathetically.
- **Integrate Insights**: Weave in findings from previous analyses.
- **Encouraging Tone**: Maintain a supportive and uplifting tone.

**Previous Analyses:**

{previous_results['Initial Analysis']}
{previous_results['Core Values']}
{previous_results['Psychological Drivers']}

**Example Format:**

---

[Begin the life narrative here, structured into paragraphs or sections.]

---"""

def growth_opportunities_prompt(raw_responses, previous_results):
    return f"""Develop a personalized growth plan for the user that includes:

1. **Actionable Steps**:

   - List 3-5 specific actions the user can take.
   - For each step, explain how it aligns with their core values and addresses identified growth areas.

2. **Potential Challenges and Strategies**:

   - Identify possible obstacles for each action.
   - Provide practical strategies to overcome these challenges.

3. **Recommended Resources**:

   - Suggest 2-3 books, articles, or workshops.
   - Briefly describe how each resource is relevant.

**Instructions:**

- **Empathetic Language**: Use encouraging and motivational language.
- **Personalization**: Tailor recommendations to the user's interests and needs.
- **Positivity Focus**: Emphasize the user's strengths and potential.

**Previous Analyses:**

{previous_results['Initial Analysis']}
{previous_results['Core Values']}
{previous_results['Psychological Drivers']}
{previous_results['Life Narrative']}

**Example Format:**

---

**Actionable Steps:**

1. **Step 1**: Description and alignment with values.
   - **Challenges**: Potential obstacle.
   - **Strategies**: How to overcome it.

[Repeat for each step]

**Recommended Resources:**

- **Resource 1**: Title and brief description.
- **Resource 2**: Title and brief description.

---"""

def final_report_prompt(raw_responses, previous_results):
    return f"""Assemble a personalized and comprehensive report for the user that brings together all previous analyses. The report should be structured as follows:

1. **Introduction**:

   - Briefly explain what the Values Prism is and how it benefits the user.
   - Set the tone for a supportive and insightful journey.

2. **Core Values**:

   - Present the top three core values with detailed explanations.
   - Include how these values manifest in the user's life.

3. **Psychological Insights**:

   - Discuss underlying drivers, cognitive biases, emotional patterns, and resilience.
   - Use specific examples from the user's responses.

4. **Life Narrative and Purpose**:

   - Provide an overview of the user's life story.
   - Highlight their sense of purpose and meaning.

5. **Growth Opportunities**:

   - Outline actionable steps for personal development.
   - Address potential challenges and suggest resources.

6. **Conclusion**:

   - Offer an encouraging message.
   - Emphasize the importance of ongoing self-reflection and growth.

**Instructions:**

- **Tailored Writing**: Write directly to the user, making the report feel personal.
- **Engaging Style**: Use clear language, headings, and bullet points where appropriate.
- **Positive and Empowering Tone**: Focus on strengths and opportunities.

**Previous Analyses:**

{previous_results['Initial Analysis']}
{previous_results['Core Values']}
{previous_results['Psychological Drivers']}
{previous_results['Life Narrative']}
{previous_results['Growth Opportunities']}

**Example Format:**

---

**Introduction**

[Write the introduction]

**Core Values**

- **Value 1**: Detailed description.
- **Value 2**: Detailed description.

**Psychological Insights**

[Discuss insights with examples]

**Life Narrative and Purpose**

[Provide the narrative]

**Growth Opportunities**

[Outline steps and resources]

**Conclusion**

[Offer closing remarks]

---"""

# DigitalOcean Functions entry point
def main(args):
    import asyncio
    return asyncio.get_event_loop().run_until_complete(process_webhook(args))
