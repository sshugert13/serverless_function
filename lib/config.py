INITIAL_ANALYSIS_PROMPT = """You are a skilled life coach and psychologist tasked with analyzing a user's detailed responses to a self-discovery questionnaire. Your goal is to provide an in-depth initial analysis that identifies:

1. **Recurring Themes**: Highlight any common themes or patterns that appear throughout the responses.
2. **Core Values and Motivations**: Extract key values and motivations that seem important to the user.
3. **Significant Life Experiences**: Note any impactful events or experiences that have shaped the user's perspective.
4. **Emotional Tone**: Observe the emotional undertones in their answers (e.g., excitement, frustration, hope).

**Instructions:**

- **Use Direct Quotes**: Where appropriate, include brief quotes from the user's responses to support your analysis.
- **Be Empathetic and Objective**: Present your findings in a compassionate yet unbiased manner.
- **Structure**: Organize your analysis into clear sections with headings.

**User Responses:**

{raw_responses}

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

CORE_VALUES_PROMPT = """Using the initial analysis provided, identify the top three core values that are most prominent for the user. For each core value, create a detailed profile that includes:

1. **Definition**: Provide a clear and concise definition of the value.
2. **Manifestation**: Describe how this value shows up in the user's life, citing specific examples from their responses.
3. **Significance**: Explain why this value is important to the user and how it influences their decisions and actions.
4. **Conflicts or Synergies**: Identify any potential conflicts with other values or how it complements them.

**Instructions:**

- **Personalization**: Tailor the explanations to the user's unique experiences.
- **Support with Evidence**: Reference specific parts of the user's responses.
- **Empathetic Tone**: Write in a way that resonates with the user's feelings and perspectives.

**Initial Analysis:**

{previous_results}

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

PSYCHOLOGICAL_DRIVERS_PROMPT = """Delve deeper into the user's psyche to uncover subtle psychological aspects. Your analysis should cover:

1. **Hidden Motivations**: Identify underlying drivers that may not be overtly stated.
2. **Cognitive Biases and Blind Spots**: Highlight any biases that could affect the user's perception or decisions.
3. **Emotional Patterns**: Observe recurring emotional responses or themes.
4. **Resilience and Coping**: Assess how the user deals with challenges, including strengths and areas for improvement.

**Instructions:**

- **Evidence-Based**: Use specific examples from the user's responses to support each point.
- **Non-Judgmental Language**: Present findings respectfully without assigning blame.
- **Actionable Insights**: Where appropriate, suggest areas for self-reflection.

**Previous Analyses:**

- **Initial Analysis**: {initial_analysis}
- **Core Values**: {core_values}

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

LIFE_NARRATIVE_PROMPT = """Synthesize the information from previous analyses to craft a cohesive life narrative for the user. This narrative should:

1. **Life Story Highlights**: Outline significant events and experiences that have shaped the user.
2. **Sense of Purpose**: Describe what gives the user a sense of meaning.
3. **Value-Behavior Alignment**: Identify where the user's actions align or misalign with their stated values.
4. **Internal Conflicts and Harmonies**: Explore any inner tensions or areas of congruence.

**Instructions:**

- **Narrative Style**: Write in the third person, presenting the user's story empathetically.
- **Integrate Insights**: Weave in findings from previous analyses.
- **Encouraging Tone**: Maintain a supportive and uplifting tone.

**Previous Analyses:**

{initial_analysis}
{core_values}
{psychological_drivers}

**Example Format:**

---

[Begin the life narrative here, structured into paragraphs or sections.]

---"""

GROWTH_OPPORTUNITIES_PROMPT = """Develop a personalized growth plan for the user that includes:

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

{initial_analysis}
{core_values}
{psychological_drivers}
{life_narrative}

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

FINAL_REPORT_PROMPT = """Assemble a personalized and comprehensive report for the user that brings together all previous analyses. The report should be structured as follows:

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

{initial_analysis}
{core_values}
{psychological_drivers}
{life_narrative}
{growth_opportunities}

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