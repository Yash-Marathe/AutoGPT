from __future__ import annotations

import json
import logging
import numpy as np
from typing import Any, Literal, List, Optional

import ftfy
from pydantic import BaseModel
from autogpt.config import Config
from autogpt.core.resource.model_providers import (
    ChatMessage,
    ChatModelProvider,
    EmbeddingModelProvider,
)
from autogpt.processing.text import chunk_content, split_text, summarize_text
from autogpt.embeddings.embedding import Embedding

logger = logging.getLogger(__name__)

MemoryDocType = Literal["webpage", "text_file", "code_file", "agent_history"]


class MemoryItem(BaseModel, arbitrary_types_allowed=True):
    """Memory object containing raw content as well as embeddings"""

    raw_content: str
    summary: str
    chunks: List[str]
    chunk_summaries: List[str]
    e_summary: Embedding
    e_chunks: List[Embedding]
    metadata: dict[str, Any]

    def relevance_for(self, query: str, e_query: Optional[Embedding] = None) -> float:
        """Calculate the relevance of the memory item for a given query"""
        return MemoryItemRelevance.calculate_scores(self, e_query)[1]

    def __eq__(self, other: MemoryItem) -> bool:
        """Check if two memory items are equal"""
        if not isinstance(other, MemoryItem):
            return False

        return (
            self.raw_content == other.raw_content
            and self.chunks == other.chunks
            and self.chunk_summaries == other.chunk_summaries
            and np.allclose(
                self.e_summary.vector, other.e_summary.vector, equal_nan=True
            )
            and np.allclose(
                np.array(self.e_chunks).reshape(-1, self.e_chunks[0].vector.size),
                np.array(other.e_chunks).reshape(-1, other.e_chunks[0].vector.size),
                equal_nan=True,
            )
        )


class MemoryItemFactory:
    def __init__(
        self,
        llm_provider: ChatModelProvider,
        embedding_provider: EmbeddingModelProvider,
    ):
        self.llm_provider = llm_provider
        self.embedding_provider = embedding_provider

    async def from_text(
        self,
        text: str,
        source_type: MemoryDocType,
        config: Config,
        metadata: dict = {},
        how_to_summarize: str | None = None,
        question_for_summary: str | None = None,
    ) -> MemoryItem:
        logger.debug(f"Memorizing text:\n{'-'*32}\n{text}\n{'-'*32}\n")

        text = ftfy.fix_text(text)

        chunks = []
        chunk_summaries = []

        for chunk, _ in (
            split_text(
                text=text,
                config=config,
                max_chunk_length=1000,
                tokenizer=self.llm_provider.get_tokenizer(config.fast_llm),
            )
            if source_type != "code_file"
            else chunk_content(
                content=text,
                max_chunk_length=1000,
                tokenizer=self.llm_provider.get_tokenizer(config.fast_llm),
            )
        ):
            chunks.append(chunk)
            try:
                summary, _ = await summarize_text(
                    text=chunk,
                    instruction=how_to_summarize,
                    question=question_for_summary,
                    llm_provider=self.llm_provider,
                    config=config,
                )
                chunk_summaries.append(summary)
            except Exception as e:
                logger.warning(f"Failed to summarize chunk: {e}")
                chunk_summaries.append("")

        e_chunks = [
            get_embedding(chunk, config, self.embedding_provider) for chunk in chunks
        ]

        summary = (
            chunk_summaries[0]
            if len(chunks) == 1
            else await summarize_text(
                text="\n\n".join(chunk_summaries),
                instruction=how_to_summarize,
                question=question_for_summary,
                llm_provider=self.llm_provider,
                config=config,
            )[0]
        )

        e_summary = get_embedding(summary, config, self.embedding_provider)

        metadata["source_type"] = source_type

        return MemoryItem(
            raw_content=text,
            summary=summary,
            chunks=chunks,
            chunk_summaries=chunk_summaries,
            e_summary=e_summary,
            e_chunks=e_chunks,
            metadata=metadata,
        )

    # ... other methods follow ...


class MemoryItemRelevance(BaseModel):
    """
    Class that encapsulates memory relevance search functionality and data.
    Instances contain a MemoryItem and its relevance scores for a given query.
    """

    memory_item: MemoryItem
    for_query: str
    summary_relevance_score: float
    chunk_relevance_scores: List
