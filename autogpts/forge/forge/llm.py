import os
import pathlib
import typing

import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential

from .sdk.forge_log import ForgeLogger
from litellm import completion, acompletion

class OpenAIApiError(Exception):
    """Custom exception for handling any errors related to the OpenAI API."""

LOG = ForgeLogger(__name__)


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def chat_completion_request(
    model: str, messages: list, **kwargs
) -> typing.Union[typing.Dict[str, typing.Any], OpenAIApiError]:
    """Generate a response to a list of messages using OpenAI's API.

    Args:
        model (str): The OpenAI model to use for generating the response.
        messages (list): A list of message dictionaries containing 'role' and 'content' keys.
        **kwargs: Additional keyword arguments to pass to the OpenAI API.

    Returns:
        dict or OpenAIApiError: A dictionary containing the generated response or an error.
    """
    try:
        kwargs["model"] = model
        kwargs["messages"] = messages

        resp = await acompletion(**kwargs)
        return resp
    except openai.AuthenticationError as e:
        LOG.exception("Authentication Error")
        raise OpenAIApiError("Authentication Error") from e
    except openai.InvalidRequestError as e:
        LOG.exception("Invalid Request Error")
        raise OpenAIApiError("Invalid Request Error") from e


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
async def create_embedding_request(
    messages: list,
) -> typing.Union[typing.Dict[str, typing.Any], OpenAIApiError]:
    """Generate an embedding for a list of messages using OpenAI's API.

    Args:
        messages (list): A list of message dictionaries containing 'role' and 'content' keys.

    Returns:
        dict or OpenAIApiError: A dictionary containing the generated embedding or an error.
    """
    try:
        return await openai.Embedding.acreate(
            input=[f"{m['role']}: {m['content']}" for m in messages],
            engine="text-embedding-ada-002",
        )
    except openai.OpenAIError as e:
        LOG.error("Unable to generate embedding response")
        LOG.error(f"Exception: {e}")
        raise OpenAIApiError("Unable to generate embedding response") from e


@retry(wait=wait_random_exponential
