import os
import json
import asyncpg

async def get_db_pool():
    return await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        ssl="require"
    )

async def store_user_response(conn, form_response_id, email, name, raw_responses):
    await conn.execute(
        """
        INSERT INTO user_responses (form_response_id, email, name, submitted_at, raw_responses)
        VALUES ($1, $2, $3, CURRENT_TIMESTAMP, $4)
        """,
        form_response_id, email, name, json.dumps(raw_responses)
    )

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