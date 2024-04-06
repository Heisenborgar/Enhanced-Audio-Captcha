import random

def getResult(text):
    words = text.split()
    min_words_to_omit = min(2, len(words) // 3)  # Adjust the minimum as needed
    num_words_to_omit = random.randint(min_words_to_omit, len(words) // 1.5)  # Adjust the range as needed
    words_to_omit_indices = random.sample(range(len(words)), num_words_to_omit)
    words = [word for index, word in enumerate(words) if index not in words_to_omit_indices]
    text = ' '.join(words)
    return text