from enum import Enum


class Environments(str, Enum):
    """Перечисление всех возможных видов окружений"""
    production = "prod"
    preproduction = "preprod"
    stage = "stage"


class Domains(str, Enum):
    """Перечисление всех возможных типов пользователей"""
    canary = "canary"
    regular = "regular"
