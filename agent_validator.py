import sys

class InvalidInputError(Exception):
    """Custom exception for invalid agent inputs."""
    pass

def process_agent_input(input_data: dict) -> str:
    """
    Simulates an agent processing an input, explicitly rejecting invalid ones.

    Args:
        input_data: A dictionary representing the agent's input.
                    Expected keys: 'command', 'value'.

    Returns:
        A success message if the input is valid.

    Raises:
        InvalidInputError: If the input_data is invalid according to agent rules.
    """
    # --- Article's core concept: Explicitly reject invalid inputs ---
    # Rule 1: Input must be a dictionary
    if not isinstance(input_data, dict):
        raise InvalidInputError("Input must be a dictionary.")

    # Rule 2: Must contain 'command' and 'value' keys
    if 'command' not in input_data or 'value' not in input_data:
        raise InvalidInputError("Input must contain 'command' and 'value' keys.")

    command = input_data['command']
    value = input_data['value']

    # Rule 3: 'command' must be a non-empty string
    if not isinstance(command, str) or not command.strip():
        raise InvalidInputError("Command must be a non-empty string.")

    # Rule 4: 'value' must be an integer and positive for 'set_level' command
    if command == "set_level":
        if not isinstance(value, int) or value <= 0:
            raise InvalidInputError(f"For 'set_level' command, value must be a positive integer. Received: {value}")
    # Rule 5: 'value' must be a non-empty string for 'send_message' command
    elif command == "send_message":
        if not isinstance(value, str) or not value.strip():
            raise InvalidInputError(f"For 'send_message' command, value must be a non-empty string. Received: {value}")
    else:
        # Rule 6: Reject unknown commands
        raise InvalidInputError(f"Unknown command: '{command}'. Valid commands are 'set_level', 'send_message'.")

    # If all checks pass, the input is considered valid and processed.
    return f"Agent successfully processed command '{command}' with value '{value}'."

def main():
    # --- Article's concept: "Rejection Corpus" for testing ---
    # A corpus of known invalid inputs to test the agent's rejection logic.
    rejection_corpus = [
        None,                                   # Not a dictionary
        "not a dict",                           # Not a dictionary
        {},                                     # Missing keys
        {'command': 'test'},                    # Missing 'value'
        {'value': 10},                          # Missing 'command'
        {'command': '', 'value': 1},            # Empty command string
        {'command': 'set_level', 'value': 'abc'}, # Invalid value type
        {'command': 'set_level', 'value': 0},   # Non-positive integer
        {'command': 'send_message', 'value': ''}, # Empty message string
        {'command': 'unknown_cmd', 'value': 100} # Unknown command
    ]

    # A corpus of known valid inputs
    valid_corpus = [
        {'command': 'set_level', 'value': 5},
        {'command': 'send_message', 'value': 'Hello Agent!'},
        {'command': 'set_level', 'value': 1},
        {'command': 'send_message', 'value': 'Status Report'}
    ]

    print("--- Testing Agent with Valid Inputs ---")
    for i, input_data in enumerate(valid_corpus):
        try:
            print(f"\nInput {i+1} (Valid): {input_data}")
            result = process_agent_input(input_data)
            print(f"  Result: {result}")
        except InvalidInputError as e:
            print(f"  ERROR: Unexpected rejection for valid input! {e}")
        except Exception as e:
            print(f"  ERROR: An unexpected error occurred: {e}")

    print("\n--- Testing Agent with Invalid Inputs (Rejection Corpus) ---")
    for i, input_data in enumerate(rejection_corpus):
        try:
            print(f"\nInput {i+1} (Invalid): {input_data}")
            result = process_agent_input(input_data)
            # This line should ideally not be reached for invalid inputs
            print(f"  ERROR: Agent processed invalid input! Result: {result}")
        except InvalidInputError as e:
            # This is the expected behavior for invalid inputs
            print(f"  EXPECTED REJECTION: {e}")
        except Exception as e:
            print(f"  ERROR: An unexpected error occurred for invalid input: {e}")

if __name__ == "__main__":
    main()
