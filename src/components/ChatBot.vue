<template>
  <div class="chat-bot">
    <div class="chat-window">
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" :class="{'user-message': message.isUser, 'bot-message': !message.isUser}">
          {{ message.text }}
        </div>
      </div>
      <div class="input-area">
        <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Type your message..." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userInput: '',
      messages: [
        { text: 'Hello! I\'m NUS Kaki, your campus assistant. How can I help you today?', isUser: false }
      ],
      isLoading: false
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '' || this.isLoading) return;

      const userMessage = this.userInput;

      // Add user message to chat
      this.messages.push({ text: userMessage, isUser: true });

      // Clear input
      this.userInput = '';

      // Show loading state
      this.isLoading = true;
      const loadingMessage = { text: 'Thinking...', isUser: false, isLoading: true };
      this.messages.push(loadingMessage);

      try {
        // Call backend API
        const response = await axios.post('http://localhost:3000/api/chat', {
          prompt: userMessage
        });

        // Remove loading message
        this.messages.pop();

        // Add bot response
        if (response.data.success) {
          this.messages.push({
            text: response.data.response,
            isUser: false
          });
        } else {
          this.messages.push({
            text: 'Sorry, I encountered an error. Please try again.',
            isUser: false
          });
        }

      } catch (error) {
        // Remove loading message
        this.messages.pop();

        console.error('Error calling chat API:', error);

        let errorMessage = 'Sorry, I couldn\'t connect to the server. ';
        if (error.response?.data?.error) {
          errorMessage += error.response.data.error;
        } else if (error.code === 'ERR_NETWORK') {
          errorMessage += 'Please make sure the backend server is running on port 3000.';
        } else {
          errorMessage += 'Please try again later.';
        }

        this.messages.push({
          text: errorMessage,
          isUser: false
        });
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.chat-bot {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}
.chat-window {
  width: 400px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: white;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}
.user-message {
  text-align: right;
  margin: 5px 0;
  color: white;
  background: #007bff;
  padding: 8px;
  border-radius: 8px;
}
.bot-message {
  text-align: left;
  margin: 5px 0;
  color: black;
  background: #e9ecef;
  padding: 8px;
  border-radius: 8px;
}
.input-area {
  display: flex;
  border-top: 1px solid #ccc;
}
input {
  flex: 1;
  border: none;
  padding: 10px;
  outline: none;
}
button {
  border: none;
  background: #007bff;
  color: white;
  padding: 10px;
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
</style>
