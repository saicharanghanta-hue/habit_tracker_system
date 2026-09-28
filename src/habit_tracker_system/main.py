import sys
from habit_tracker_system.crew import HabitTrackerCrew


def run():
    """Run the Habit Tracker Crew."""
    inputs = {
        "habit_id": "1",
        "habit_name": "Morning Workout",
        "recent_logs": "Day 1: DONE, Day 2: DONE, Day 3: SKIPPED, Day 4: PENDING"
    }
    
    print("--- Starting Habit Tracker CrewAI Pipeline ---")
    result = HabitTrackerCrew().crew().kickoff(inputs=inputs)
    print("\n--- Final Coaching Plan Output ---")
    print(result)


if __name__ == "__main__":
    run()

