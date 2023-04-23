import torch
from transformers import BertTokenizer, BertForMaskedLM
import re

device = "cuda" if torch.cuda.is_available() else "cpu"

def mask_tokens(sentence, tokenizer):
    tokens = tokenizer.tokenize(sentence)
    masked_sentence = "".join(tokens)
    return masked_sentence


def generate_prediction(masked_sentence, tokenizer, model, top_k=5):
    inputs = tokenizer.encode_plus(masked_sentence, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)

    mask_token_indices = torch.where(input_ids[0] == tokenizer.mask_token_id)[0]
    all_predicted_tokens = []
    all_top_k_values = []

    for mask_token_index in mask_token_indices:
        logits = outputs.logits[0, mask_token_index]
        probs = torch.softmax(logits, dim=-1)
        top_k_values, top_k_indices = torch.topk(probs, top_k, sorted=True)

        predicted_tokens = [tokenizer.convert_ids_to_tokens(idx.item()) for idx in top_k_indices]
        all_predicted_tokens.append(predicted_tokens)
        all_top_k_values.append(top_k_values)

    return all_predicted_tokens, all_top_k_values


from itertools import product

def beam_search(masked_sentence, tokenizer, model, beam_width=5):
    if tokenizer.mask_token not in masked_sentence:
        return [(masked_sentence, 1.0)]

    first_mask_index = masked_sentence.index(tokenizer.mask_token)
    all_predicted_tokens, all_top_k_values = generate_prediction(masked_sentence, tokenizer, model, top_k=beam_width)

    new_sentences = []

    for tokens, values in zip(product(*all_predicted_tokens), product(*all_top_k_values)):
        filled_sentence = masked_sentence
        for token in tokens:
            filled_sentence = filled_sentence.replace(tokenizer.mask_token, token, 1)
        prob = 1.0
        for value in values:
            prob *= value.item()
        new_sentences.append((filled_sentence, prob))

    top_sentences = []

    for sentence, prob in new_sentences:
        next_sentences = beam_search(sentence, tokenizer, model, beam_width)
        top_sentences.extend([(sent, p * prob) for sent, p in next_sentences])

    top_sentences.sort(key=lambda x: x[1], reverse=True)
    return top_sentences[:beam_width]



def main():
    model_name = "bert-base-chinese"
    model = BertForMaskedLM.from_pretrained(model_name).to(device)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    # Load the saved model parameters
    # saved_model_path = "../checkpoints/model_1.pth"
    # saved_state = torch.load(saved_model_path, map_location=device)

    # Apply the loaded state to the new model instance
    # model.load_state_dict(saved_state)
    model.eval()  # Set the model to evaluation mode

    sentence_mask = "欲 出 未 出 光 辣 达, 千 山 万 山 如 火 发. 须 臾 走 向 天 上 来, 逐 却 残 星 赶 [MASK][MASK] ."

    masked_sentence = mask_tokens(sentence_mask, tokenizer)
    print(f"Masked sentence: {masked_sentence}")

    top_sentences = beam_search(masked_sentence, tokenizer, model, beam_width=5)
    print("Top predictions:")
    for sentence, prob in top_sentences:
        print(f"{sentence} (probability: {prob})")

main()
