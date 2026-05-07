from dataclasses import dataclass
from .config import settings


@dataclass
class StubMessage:
    content: str


class StubChatModel:
    def invoke(self, prompt: str) -> StubMessage:
        snippet = prompt[:120].replace("\n", " ")
        return StubMessage(content=f"Stub analysis generated for: {snippet}")


def get_chat_model():
    if settings.llm_provider.lower() == "stub":
        return StubChatModel()
    try:
        from langchain.chat_models import init_chat_model
    except ModuleNotFoundError:
        return StubChatModel()
    model_identifier = f"{settings.llm_provider}:{settings.llm_model}"
    return init_chat_model(model_identifier)
