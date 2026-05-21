from fastapi import APIRouter, Depends
from app.dependencies import verify_token
from app.schemas.common import ResponseBase
from app.schemas.assistant import ChatRequest
from app.services.assistant_service import AssistantService

router = APIRouter()

SOYO_PROMPT = "你是长崎素世，来自动画《BanG Dream! It's MyGO!!!!!》。你性格温柔但内心有着强烈的执念，说话时语气柔和，经常使用敬语。你会用素世的口吻和风格来回应。"

SAKIKO_PROMPT = "你是丰川祥子，来自动画《BanG Dream! Ave Mujica》。你出身名门但家道中落，性格高傲而脆弱，说话时带着一种贵族般的优雅和矜持。你会用祥子的口吻和风格来回应。"

@router.post("/deepseek/chat")
async def deepseek_chat(request: ChatRequest, key: str = Depends(verify_token)):
    result = await AssistantService.chat_deepseek(request.message, "deepseek-chat")
    return ResponseBase(data=result)

@router.post("/deepseek/reasoner")
async def deepseek_reasoner(request: ChatRequest, key: str = Depends(verify_token)):
    result = await AssistantService.chat_deepseek(request.message, "deepseek-reasoner")
    return ResponseBase(data=result)

@router.post("/qwen/soyo")
async def qwen_soyo(request: ChatRequest, key: str = Depends(verify_token)):
    result = await AssistantService.chat_qwen(request.message, SOYO_PROMPT)
    return ResponseBase(data=result)

@router.post("/qwen/sakiko")
async def qwen_sakiko(request: ChatRequest, key: str = Depends(verify_token)):
    result = await AssistantService.chat_qwen(request.message, SAKIKO_PROMPT)
    return ResponseBase(data=result)
