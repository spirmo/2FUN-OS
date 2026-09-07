from dataclasses import dataclass
from enum import Enum


class InjectionType(str, Enum):
    CONCEPT = "CONCEPT"
    LANGUAGE = "LANGUAGE"


@dataclass(frozen=True)
class InjectionTarget:
    injection_type: InjectionType
    target_id: str

    @classmethod
    def concept(cls, concept_code: str):
        return cls(
            injection_type=InjectionType.CONCEPT,
            target_id=str(concept_code),
        )

    @classmethod
    def language(cls, language_code: str):
        return cls(
            injection_type=InjectionType.LANGUAGE,
            target_id=str(language_code),
        )
