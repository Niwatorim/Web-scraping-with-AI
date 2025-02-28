#using ollama
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model='llama3.1') #used AI model

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_ollama(dom_chunk, description):
    prompt = ChatPromptTemplate.from_template(template) #use the template above
    chain = prompt | model #means first we bring the prompt then call the model
    
    results = [] #where we store results for each batch

    for i, chunk in enumerate(dom_chunk, start = 1): #for loop per each dom chunk
        response = chain.invoke({
            'dom_content':chunk, # attributing the passed values to the template
            'parse_description':description
        })

        print(f'Parsed batch {i} of {len(dom_chunk)}') #for testing to see how much work is being done
        results.append(response) #adds to response list

    return '\n'.join(results) #returns each value, for each batch new line

