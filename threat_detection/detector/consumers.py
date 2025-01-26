import json
import numpy as np
import librosa
import tensorflow as tf
import tensorflow_hub as hub
from channels.generic.websocket import AsyncWebsocketConsumer
import io
import os

# Load models once at startup
model_yamnet = hub.load('https://tfhub.dev/google/yamnet/1')
model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), 'YAMNet Threatening Voice Classification.keras'))

class AudioConsumer(AsyncWebsocketConsumer):
    MAX_SEQ_LENGTH = 100  # Maintain original model's expected sequence length
    EMBEDDING_DIM = 1024
    CHUNK_DURATION = 30.0
    
    async def connect(self):
        await self.accept()
        self.sample_rate = 16000

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Process each chunk independently
            result = await self.process_chunk(bytes_data)
            await self.send(json.dumps({'result': result}))

    async def process_chunk(self, bytes_data):
        # Convert bytes to audio array
        audio = self.bytes_to_audio(bytes_data)
        audio = audio/np.max(np.abs(audio)) 
        # Extract features and pad
        embeddings = self.extract_features(audio)
        padded = self.pad_embeddings(embeddings)
        
        return self.predict_threat(padded)

    def bytes_to_audio(self, bytes_data):
        # Load exactly 2 seconds of audio
        audio, _ = librosa.load(io.BytesIO(bytes_data),
                              sr=self.sample_rate,
                              mono=True,
                              duration=self.CHUNK_DURATION)
        return audio.astype(np.float32)

    def pad_embeddings(self, embeddings):
        # YAMNet produces (N, 1024) embeddings where N = (duration / 0.48)
        seq_length = embeddings.shape[0]
        
        if seq_length < self.MAX_SEQ_LENGTH:
            # Pad with zeros at the end
            pad_size = self.MAX_SEQ_LENGTH - seq_length
            padded = tf.pad(embeddings, [[0, pad_size], [0, 0]])
        else:
            # Truncate if longer (unlikely for 2-second chunks)
            padded = embeddings[:self.MAX_SEQ_LENGTH, :]
        
        # Add batch dimension and ensure correct shape
        return tf.reshape(padded, [1, self.MAX_SEQ_LENGTH, self.EMBEDDING_DIM])

    def extract_features(self, audio):
        # Process through YAMNet
        _, embeddings, _ = model_yamnet(audio)
        return embeddings  # Shape (N, 1024)

    def predict_threat(self, padded_embeddings):
        predictions = model.predict(padded_embeddings, verbose=0)
        return "Non-Threat" if predictions[0][0] > 0.5 else "Threat"