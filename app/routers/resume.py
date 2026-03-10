from fastapi import APIRouter, HTTPException
import logging, json
from ai.utils import call_llm, load_prompt
from models.extract import Resume
from tenacity import RetryError

router = APIRouter()

@router.post("/extract/resume")
async def extract_resume(text: str):
    system_msg = load_prompt("resume.txt")

    for attempt in range(2):  # max 2 retries
        try:
            response = call_llm(system_msg, text, temperature=0.1, json_mode=True)
            data = json.loads(response.choices[0].message.content)

            # Validate against schema
            resume = Resume(**data)

            logging.info(
                f"/extract/resume | IN: {response.usage.prompt_tokens} | OUT: {response.usage.completion_tokens}"
            )

            return {"resume": resume.dict(), "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            }}

        except Exception as e:
            if attempt == 1:
                raise HTTPException(status_code=500, detail=f"Resume extraction failed: {str(e)}")
            else:
                # Correction prompt
                text = f"Please strictly return JSON matching this schema: {Resume.model_json_schema()}"