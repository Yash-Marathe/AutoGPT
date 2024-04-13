"""
A module for handling the finish action.
"""
from sdk.forge_log import ForgeLogger
from .registry import action

logger = ForgeLogger(__name__)


@action(
    name="finish",
    description="Use this to shut down once you have accomplished all of your goals,"
    " or when there are insurmountable problems that make it impossible"
    " for you to finish your task.",
    parameters=[
        {
            "name": "reason",
            "description": "A summary to the user of how the goals were accomplished",
            "type": "string",
            "required": True,
        }
    ],
    output_type="str",  # Return type changed to str
)
async def finish(
    agent,
    task_id: str,
    reason: str,
) -> str:
    """
    A function that takes in a string and exits the program.

    Parameters:
        reason (str): A summary to the user of how the goals were accomplished.

    Returns:
        A result string from create chat completion.

    Suggestions to improve the code:
    * Consider adding more functionality to the finish action, such as cleaning up resources or logging more information.
    """
    logger.info(reason, extra={"title": "Shutting down...\n"})
    return f"Finished with reason: {reason}"  # Return a result string
