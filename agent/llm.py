"""Thin model wrapper. One method, so swapping providers means editing one file."""
import os


class AnthropicLLM:
    def __init__(self, model: str):
        import anthropic  # imported here so --mock works without the package configured
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
        self.model = model

    def complete(self, system: str, user: str, role: str = "", max_tokens: int = 4000) -> str:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def get_models(mock: bool):
    if mock:
        from .mock import MockLLM
        m = MockLLM()
        return m, m
    gen = AnthropicLLM(os.getenv("GEN_MODEL", "claude-sonnet-5-5"))
    judge = AnthropicLLM(os.getenv("JUDGE_MODEL", "claude-opus-5-5"))
    return gen, judge
