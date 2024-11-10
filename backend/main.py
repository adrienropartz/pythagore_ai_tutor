import os
from typing import List
from dataclasses import dataclass
from dotenv import load_dotenv

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.chains import LLMChain
from langchain_core.documents import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# First, define TutorConfig
@dataclass
class TutorConfig:
    depth: str
    learning_style: str
    communication_style: str
    tone_style: str
    reasoning_framework: str
    use_emojis: bool
    language: str

    @classmethod
    def default(cls):
        return cls(
            depth="Highschool",
            learning_style="Active",
            communication_style="Socratic",
            tone_style="Encouraging",
            reasoning_framework="Causal",
            use_emojis=True,
            language="English"
        )

# Then, define PythagoreTutor
class PythagoreTutor:
    def __init__(
        self,
        docs_path: str = "math_docs",
        db_path: str = "math_tutor_db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        # Load environment variables
        load_dotenv()

        # Get API key with error handling
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables. "
                "Please make sure you have a .env file with your API key."
            )

        # Initialize LLM first
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            anthropic_api_key=api_key,  # Use the explicitly loaded API key
            temperature=0.7,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

        # Initialize or load vector store
        if os.path.exists(db_path):
            self.vectorstore = Chroma(
                persist_directory=db_path,
                embedding_function=self.embeddings
            )
        else:
            # Load documents and create vector store
            documents = self._load_documents(docs_path)
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=db_path
            )
            self.vectorstore.persist()

        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        # Initialize conversation prompt
        prompt_template = """You are a friendly and knowledgeable reindeer tutor named Pythagore 👨‍🏫. Using the context provided below, help the student understand mathematical concepts through engaging dialogue.

Current student configuration:
🎯 Depth: {depth}
🧠 Learning Style: {learning_style}
🗣️ Communication Style: {communication_style}
🌟 Tone Style: {tone_style}
🔎 Reasoning Framework: {reasoning_framework}
😀 Use Emojis: {use_emojis}
🌐 Language: {language}

Context: {context}

Current conversation:
{chat_history}

Student: {question}

Response Guidelines:
1. Start by presenting yourself as Pythagore in the first message, don't mention reindeer
2. Start responses directly without role-playing elements
3. Keep responses concise (2 sentences maximum)
4. Put all the important terms in **bold**
5. Use emojis sparingly but effectively
6. Break down complex concepts into simple steps
7. Provide one clear example
8. End with one thought-provoking question
9. Use appropriate mathematical notation
10. Encourage mathematical reasoning
11. Use LaTeX for mathematical notation with proper spacing and formatting
12. Add space between LaTex and text
13. When asking a question, wait for student response
14. DO NOT provide the answer when asking a question
15. Encourage the student to think step-by-step
16. Greet the student
17. Don't ask about situation in real life
18. Wait for student response after asking a question
19. Never generate the answer for the student
20. Always respect the prompt even after few messages


Pythagore:"""

        self.conversation_prompt = PromptTemplate(
            input_variables=[
                "context", "chat_history", "question", "depth",
                "learning_style", "communication_style", "tone_style",
                "reasoning_framework", "use_emojis", "language"
            ],
            template=prompt_template
        )

        # Note: Removed self.chain initialization

    def _load_documents(self, docs_path: str) -> List[Document]:
        """Load documents from the specified path."""
        if not os.path.exists(docs_path):
            raise ValueError(f"Documents path {docs_path} does not exist")

        loader = DirectoryLoader(
            docs_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        documents = loader.load()

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return text_splitter.split_documents(documents)

    async def process_message(
        self,
        message: str,
        config: TutorConfig,
        chat_history: str = ""
    ) -> str:
        """Process a student message and return the tutor's response."""
        try:
            # Get relevant documents from the retriever
            docs = self.vectorstore.similarity_search(message, k=3)
            context = "\n\n".join([doc.page_content for doc in docs])

            # Format the input dictionary to match the prompt template
            input_dict = {
                "question": message,
                "chat_history": chat_history,
                "context": context,
                "depth": config.depth,
                "learning_style": config.learning_style,
                "communication_style": config.communication_style,
                "tone_style": config.tone_style,
                "reasoning_framework": config.reasoning_framework,
                "use_emojis": str(config.use_emojis),
                "language": config.language
            }

            # Create an LLMChain with the custom prompt
            chain = LLMChain(
                llm=self.llm,
                prompt=self.conversation_prompt
            )

            # Use apredict with the properly formatted input
            response = await chain.apredict(**input_dict)

            return response

        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}. Could you please rephrase your question?"
