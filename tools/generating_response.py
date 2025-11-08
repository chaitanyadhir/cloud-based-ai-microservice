from .retrieval import retriving
from .llm_call import llm_api_call
from loguru import logger
import functools

class response_generate:
    def __init__(self, namespace: str = "default", prompt_path: str = "prompt/main_prompt.txt"):
        logger.info(f"Initializing response_generate with namespace: {namespace}")
        self.retriever = retriving(namespace=namespace)
        self.llm_caller = llm_api_call()
        self.prompt_template = self._load_prompt_template(prompt_path)
        self.cache = {}

    def _load_prompt_template(self, prompt_path: str) -> str:
        logger.info(f"Loading prompt template from {prompt_path}")
        with open(prompt_path, 'r') as f:
            return f.read()

    def reload_retriever_db(self):
        logger.info("Reloading retriever database.")
        self.retriever.reload_db()

    def query_response(self, user_query: str) -> str:
        logger.info(f"Generating response for query: {user_query}")

        if user_query in self.cache:
            logger.info("Returning cached response.")
            return self.cache[user_query]

        context_docs = self.retriever.retrive_relevant_context(user_query)
        context = "\n".join([doc.page_content if hasattr(doc, 'page_content') else str(doc) for doc in context_docs])
        formatted_prompt = self.prompt_template.format(user_question=user_query, context=context)

        response = self.llm_caller.generate(formatted_prompt)
        
        self.cache[user_query] = response
        logger.info("Successfully generated and cached response.")
        return response

# if __name__ == '__main__':
#     response_generator = response_generate()
#     user_query = "What is the capital of France?"
#     prompt_path = "prompt/main_prompt.txt"
#     response = response_generator.query_response(user_query, prompt_path)
#     print(response)
