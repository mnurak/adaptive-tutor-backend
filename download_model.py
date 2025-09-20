from transformers import pipeline

print("Downloading and caching the zero-shot classification model...")
# Use the correct, fine-tuned model here as well
pipeline("zero-shot-classification", model="MoritzLaurer/deberta-v3-base-zeroshot-v1")
print("Model download complete.")