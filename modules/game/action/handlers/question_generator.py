from modules.game.action.base import BaseAction
import random

class QuestionGeneratorAction(BaseAction):

    DOMAINS = [
        "ISLAMIC_EDUCATION",
        "ISLAMIC_CULTURE",
        "ISLAMIC_ECONOMICS",
        "ANCIENT_IRAN",
        "SOCIOLOGY_OF_NATIONS",
        "GENERAL_KNOWLEDGE",
        "GAME_AND_PROJECT"
    ]

    def execute(self, context: dict):

        user_state = context.get("state", "UNKNOWN")
        history = context.get("history", [])

        next_domain = self._select_domain(history)

        question = self._generate_question(next_domain, user_state)

        return {
            "action": "generate_question",
            "domain": next_domain,
            "question": question,
            "style": "human_conversational"
        }

    def _select_domain(self, history):
        if not history:
            return self.DOMAINS[0]

        last_domain = history[-1].get("domain")

        if last_domain not in self.DOMAINS:
            return self.DOMAINS[0]

        current_index = self.DOMAINS.index(last_domain)
        next_index = (current_index + 1) % len(self.DOMAINS)

        return self.DOMAINS[next_index]

    def _generate_question(self, domain, state):

        base_questions = {
            "ISLAMIC_EDUCATION": "اگر بخواهی یک اصل اخلاقی را در زندگی روزمره اجرا کنی، کدام را انتخاب می‌کنی؟",
            "ANCIENT_IRAN": "فکر می‌کنی یک تمدن چگونه بدون جنگ رشد پایدار پیدا می‌کند؟",
            "SOCIOLOGY_OF_NATIONS": "چه چیزی باعث می‌شود یک جامعه به هم اعتماد کند؟",
            "GAME_AND_PROJECT": "اگر بخواهی یک سیستم را بهتر کنی، از کجا شروع می‌کنی؟"
        }

        return base_questions.get(domain, "نظر تو درباره این موضوع چیست؟")
