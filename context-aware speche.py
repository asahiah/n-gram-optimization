import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Bidirectional, LSTM, Dense, Attention
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import transformers  # Hugging Face Transformers for context-aware embeddings

# Sample training data (real-word contextual errors)
data = [
    ("I went to their house.", "I went to their house."),   # Correct sentence
    ("I went to there house.", "I went to their house."),   # Contextual error (their vs. there)
    ("She will loose the game.", "She will lose the game."), # Real-word error (loose vs. lose)
    ("We should recieve the package.", "We should receive the package.") # Misspelling
]

# Tokenizer for sentence-level processing
tokenizer = Tokenizer()
tokenizer.fit_on_texts([sentence for pair in data for sentence in pair])
vocab_size = len(tokenizer.word_index) + 1

# Convert sentences to sequences
X = [tokenizer.texts_to_sequences([m])[0] for m, _ in data]
Y = [tokenizer.texts_to_sequences([c])[0] for _, c in data]

# Pad sequences
max_len = max(max(len(x), len(y)) for x, y in zip(X, Y))
X = pad_sequences(X, maxlen=max_len, padding='post')
Y = pad_sequences(Y, maxlen=max_len, padding='post')

# Load contextual embeddings (pretrained BERT embeddings)
bert_model = transformers.TFAutoModel.from_pretrained("bert-base-uncased")
input_text = Input(shape=(max_len,))
embedding = bert_model(input_text)[0]  # Extract BERT embeddings

# BiLSTM model with attention
bilstm = Bidirectional(LSTM(256, return_sequences=True))(embedding)

# Attention Layer for sentence-level corrections
attention = Attention()([bilstm, bilstm])
dense = Dense(vocab_size, activation='softmax')(attention)

model = tf.keras.Model(input_text, dense)

# Compile Model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train Model
model.fit(X, Y, epochs=50, verbose=1)

# Spell correction function with sentence context
def correct_sentence(sentence):
    seq = pad_sequences([tokenizer.texts_to_sequences([sentence])[0]], maxlen=max_len, padding='post')
    pred = model.predict(seq)
    corrected_seq = [np.argmax(p) for p in pred[0]]
    corrected_sentence = ' '.join([tokenizer.index_word[i] for i in corrected_seq if i > 0])
    return corrected_sentence

# Test correction
print(correct_sentence("She will loose the game."))  # Expected output: "She will lose the game."
