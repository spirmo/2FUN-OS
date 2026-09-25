from modules.game.action.handlers.learning_loop import LearningLoopAction
from modules.game.action.handlers.drift_monitoring import DriftMonitoringAction
from modules.game.action.handlers.question_generator import QuestionGeneratorAction
from modules.game.action.handlers.continue_monitoring import ContinueMonitoringAction


ACTION_REGISTRY = {
    "learning_loop": LearningLoopAction(),
    "drift_monitoring": DriftMonitoringAction(),
    "generate_question": QuestionGeneratorAction(),
    "continue_monitoring": ContinueMonitoringAction(),
}
