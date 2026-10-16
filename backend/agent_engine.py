import asyncio
import json
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key"))

async def analyze_person(linkedin_data: dict, instagram_data: dict) -> dict:
    prompt = f"""
    Analyze this individual from their public social profiles.
    LinkedIn text: {linkedin_data.get('raw_text')}
    Instagram text: {instagram_data.get('raw_text')}

    Return ONLY a valid JSON object with these keys:
    - name: string
    - needs: list of 3 strings
    - hobbies: list of 3 strings
    - interests: list of 3 strings
    - core_values: list of 3 strings
    - persona_summary: string
    """
    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(res.choices[0].message.content)

async def simulate_date(agent_a: dict, agent_b: dict) -> dict:
    convo_prompt = f"""
    Simulate a 4-turn speed-date conversation between two people.
    Person A: {agent_a['name']}, Hobbies: {agent_a['hobbies']}, Values: {agent_a['core_values']}
    Person B: {agent_b['name']}, Hobbies: {agent_b['hobbies']}, Values: {agent_b['core_values']}

    Return a JSON object with:
    - dialogue: list of objects with "speaker" and "message"
    - compatibility_score: number between 1 and 100
    - chemistry_notes: 2 sentences explaining why they match or clash
    """
    res = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": convo_prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(res.choices[0].message.content)
