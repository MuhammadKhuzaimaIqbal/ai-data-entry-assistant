from fastapi import APIRouter, HTTPException
import logging, json
from ai.utils import call_llm, load_prompt
from models.extract import BusinessCard
from tenacity import RetryError

router = APIRouter()

@router.post("/extract/business-card")
async def extract_business_card(text: str):
    system_msg = load_prompt("business_card.txt")

    for attempt in range(2):  # max 2 retries
        try:
            response = call_llm(system_msg, text, temperature=0.1, json_mode=True)
            data = json.loads(response.choices[0].message.content)

            # Validate against schema
            card = BusinessCard(**data)

            logging.info(
                f"/extract/business-card | IN: {response.usage.prompt_tokens} | OUT: {response.usage.completion_tokens}"
            )

            return {"business_card": card.dict(), "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            }}

        except Exception as e:
            if attempt == 1:  # after 2 tries, fail
                raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
            else:
                # Correction prompt
                text = f"Please strictly return JSON matching this schema: {BusinessCard.model_json_schema()}"