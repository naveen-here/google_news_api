from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load Mistral LLM model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3-Instruct-v0.3")
token="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"

def generate_summary(retrieved_articles):
    # Combine the titles and snippets of the retrieved articles
    context = ""
    for article in retrieved_articles:
        context += f"Title: {article['title']}\nSource: {article['source']}\nDate: {article['published_date']}\nSnippet: {article['snippet']}\n\n"

    # Encode the context and generate a response from Mistral
    inputs = tokenizer(context, return_tensors="pt", truncation=True, max_length=2048)
    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, max_length=512, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

    # Decode the generated response
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return summary

# Example usage: Fetching relevant articles and generating a summary
keyword = "Sheikh Hasina"  # For example, searching articles related to Sheikh Hasina
retrieved_articles = retrieve_relevant_articles(keyword)
summary = generate_summary(retrieved_articles)

print("Generated Summary:")
print(summary)
