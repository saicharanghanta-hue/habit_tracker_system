from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class HabitStatus(str, Enum):
    DONE = "DONE"
    SKIPPED = "SKIPPED"
    PENDING = "PENDING"


class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    target_frequency_days: int = Field(default=1)  # Daily = 1
    current_streak: int = Field(default=0)
    longest_streak: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    logs: List["HabitLog"] = Relationship(back_populates="habit")


class HabitLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(foreign_key="habit.id", index=True)
    log_date: date = Field(default_factory=date.today, index=True)
    status: HabitStatus = Field(default=HabitStatus.PENDING)
    notes: Optional[str] = None

    habit: Optional[Habit] = Relationship(back_populates="logs")


class StreakEngine:
    """Core 3-State Engine Logic for Habit Logs."""

    @staticmethod
    def calculate_streak(logs: List[HabitLog]) -> tuple[int, int]:
        """Calculates current and longest streak from ordered historical logs.
        
        Rules:
        - DONE: Increments current streak.
        - SKIPPED: Preserves streak (does not increment or reset).
        - PENDING / Missed: Resets current streak to 0.
        """
        sorted_logs = sorted(logs, key=lambda x: x.log_date, reverse=True)
        current_streak = 0
        longest_streak = 0
        temp_streak = 0

        for log in sorted_logs:
            if log.status == HabitStatus.DONE:
                temp_streak += 1
            elif log.status == HabitStatus.SKIPPED:
                continue  # Grace state: streak frozen
            elif log.status == HabitStatus.PENDING:
                if current_streak == 0:
                    current_streak = temp_streak
                temp_streak = 0

            if temp_streak > longest_streak:
                longest_streak = temp_streak

        if current_streak == 0:
            current_streak = temp_streak

        return current_streak, longest_streak

