from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize the Ollama LLM model
model = OllamaLLM(model='llama3.1')

# Template for the LLM prompt
template = """
You are a Hadith analysis assistant. Follow these rules:
1. Find hadiths relevant to: {user_prompt}
2. From this content: {content}
3. Return ONLY the matching hadiths in a markdown table with columns: Relevance Score, Hadith Text
4. If no matches, say "No relevant hadiths found."
"""

async def sort(description, content_chunks):
    """Sort and filter hadiths based on relevance using the LLM"""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    results = []
    
    # Process each chunk of content
    for chunk in content_chunks:
        response = await chain.ainvoke({
            "user_prompt": description,
            "content": chunk
        })
        results.append(response)
        print(f'Parsed batch {len(results)} of {len(content_chunks)}')  # Dev message
    
    return "\n".join(str(r) for r in results)  # Combine all results into a single string