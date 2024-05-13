import random
import re

class MarkovModel:
    def __init__(self, order=1):
        self.order = order
        self.transitions = {}
    
    def train(self, text):
        words = re.findall(r"[\w']+|[.,!?;]", text)
        for i in range(len(words) - self.order):
            context = tuple(words[i:i+self.order])
            next_word = words[i+self.order]
            if context not in self.transitions:
                self.transitions[context] = {}
            if next_word not in self.transitions[context]:
                self.transitions[context][next_word] = 0
            self.transitions[context][next_word] += 1
    
    def generate(self, length=10, start_word=None):
        if start_word:
            start_context = tuple(start_word.split())
            if len(start_context) != self.order:
                raise ValueError("Start word must have the same order as the model")
            current_context = start_context
            generated_text = list(start_context)
        else:
            current_context = random.choice(list(self.transitions.keys()))
            generated_text = list(current_context)
        
        while len(generated_text) < length:
            if current_context not in self.transitions:
                break
            next_word = random.choices(
                list(self.transitions[current_context].keys()),
                weights=self.transitions[current_context].values()
            )[0]
            generated_text.append(next_word)
            current_context = tuple(generated_text[-self.order:])
            if next_word in ".!?":
                break
        
        return ' '.join(generated_text)

# Example usage
text = "This is a sample text for training a Markov model. It includes punctuation, sentence boundaries, and the ability to generate text based on a specific starting word or phrase."
model = MarkovModel(order=2)
model.train(text)

# Generate text with a specific starting word
start_word = "This is"
generated_text_start = model.generate(length=50, start_word=start_word)
print("Generated text starting with '{}':".format(start_word))
print(generated_text_start)

# Generate text without a specific starting word
generated_text_random = model.generate(length=50)
print("\nGenerated random text:")
print(generated_text_random)
