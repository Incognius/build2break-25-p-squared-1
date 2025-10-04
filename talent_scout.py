# talent_scout.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.output_parsers import PydanticOutputParser # Modified import
from langchain.schema.output_parser import StrOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
import re

# NOTE: This file is now correct and does not import from itself.

class Candidate(BaseModel):
    name: str = Field(description="Full name of the candidate. If not found, state 'Name Not Found'")
    source: str = Field(description="Filename of the resume (PDF)")
    justification: str = Field(description="Justification for the candidate's ranking")
    summary: str = Field(description="Brief summary of the candidate's profile")

class CandidateRanking(BaseModel):
    ranking: List[Candidate] = Field(description="A list of candidates ranked by priority")

def create_talent_scout_chain(retriever, llm):
    """
    Creates the main LangChain chain for the TalentScout agent.
    This version has a completely overhauled, stricter prompt for better formatting and completeness.
    """
    
    template = """
    You are an expert HR analyst, TalentScout. Your job is to analyze and rank candidates based on the resume context provided.

    **CONTEXT FROM RESUMES:**
    {context}

    **USER'S QUESTION:**
    {question}

    **INSTRUCTIONS:**
    1.  Analyze each candidate found in the context.
    2.  Extract the full name of each candidate. If a name is not in the resume, state "Name Not Found".
    3.  Provide a numbered priority list, justifying your ranking for each candidate.

    **OUTPUT FORMAT:**

    [Provide a numbered list of candidates, with their name, source, justification, and summary.]
    """
    prompt = PromptTemplate.from_template(template)
    #output_parser = PydanticOutputParser(pydantic_object=CandidateRanking)
    output_parser = StrOutputParser()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )
    
    print("TalentScout chain created successfully (Simplified Prompt Version).")
    return chain