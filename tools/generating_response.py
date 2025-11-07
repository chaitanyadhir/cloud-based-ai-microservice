from .retrieval import retriving
from .llm_call import llm_api_call
from loguru import logger

class response_generate:
    def __init__(self, namespace: str = "default"):
        logger.info(f"Initializing response_generate with namespace: {namespace}")
        # Simplified: Use defaults for persist_root and embedding_model
        self.retriever = retriving(namespace=namespace)
        self.llm_caller = llm_api_call()  # Use default API key/model handling

    def query_response(self, user_query: str, prompt_path: str) -> str:
        logger.info(f"Generating response for query: {user_query}")
        # Get relevant context from retriever
        context_docs = self.retriever.retrive_relevant_context(user_query)
        # Join context texts
        context = "\n".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in context_docs])

        # Read and format the prompt template
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        formatted_prompt = prompt_template.format(user_question=user_query, context=context)

        # Call the LLM
        response = self.llm_caller.generate(formatted_prompt)
        logger.info("Successfully generated response.")
        return response

# if __name__ == '__main__':
#     response_generator = response_generate()
#     user_query = "What is the capital of France?"
#     prompt_path = "prompt/main_prompt.txt"
#     response = response_generator.query_response(user_query, prompt_path)
#     print(response)
