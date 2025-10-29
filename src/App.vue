/* eslint-disable */
<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <img src="@/assets/logo.png" alt="Logo" class="logo" />
        <div class="title">
          <h1>NUS Kaki</h1>
          <p>Your NUS Campus Assistant</p>
        </div>
      </div>
    </header>
    <main class="app-main">
      <section class="quick-actions">
        <h2>Quick Actions:</h2>
        <div class="actions">
          <button class="action-button" style="background: linear-gradient(to right, #ff7a18, #ff3e3e);" @click="openLink('https://www.nus.edu.sg/campusmap')">
            <span class="icon">📍</span> Campus Map
          </button>
          <button class="action-button" style="background: linear-gradient(to right, #007bff, #0056b3);" @click="openLink('https://uci.nus.edu.sg/campus-life/campus-services/retail-dining')">
            <span class="icon">🍽️</span> Dining Options
          </button>
          <button class="action-button" style="background: linear-gradient(to right, #6f42c1, #5a32a3);" @click="openLink('https://nus.edu.sg/nuslibraries')">
            <span class="icon">📚</span> Libraries
          </button>
          <button class="action-button" style="background: linear-gradient(to right, #20c997, #17a2b8);" @click="openLink('https://nus.edu.sg/nuslibraries/spaces/facilities')">
            <span class="icon">☕</span> Study Spots
          </button>
          <button class="action-button" style="background: linear-gradient(to right, #e83e8c, #d63384);" @click="openLink('https://osa.nus.edu.sg/events')">
            <span class="icon">📅</span> Events
          </button>
          <button class="action-button" style="background: linear-gradient(to right, #6610f2, #520dc2);" @click="openLink('https://nuscollege.nus.edu.sg/college-life/campus-facilities')">
            <span class="icon">🏠</span> Facilities
          </button>
        </div>
      </section>
      <section class="chat-window">
        <div class="messages">
          <div v-for="(message, index) in messages" :key="index" class="message" :class="{'user-message-wrapper': message.isUser}">
            <!-- Bot message with avatar -->
            <div v-if="!message.isUser" class="avatar-container">
              <img src="@/assets/images/botavatar.jpg" alt="NUS Kaki Avatar" class="avatar" />
              <div class="bot-name">NUS Kaki</div>
            </div>

            <div class="message-content" :class="{'user-bubble': message.isUser, 'bot-bubble': !message.isUser}">
              <p>{{ message.text }}</p>
            </div>

            <span class="timestamp">{{ message.timestamp }}</span>
          </div>
        </div>
        <div class="input-area">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Ask about campus facilities, dining, events..."
            :disabled="isLoading"
          />
          <button class="send-button" @click="sendMessage" :disabled="isLoading">
            {{ isLoading ? '⏳' : '➤' }}
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      userInput: '',
      messages: [
        {
          text: "Hello! 👋 I'm NUS Kaki. I'm here to help students and alumni navigate campus life, discover facilities, and get personalized recommendations. What would you like to know?",
          isUser: false,
          timestamp: this.getCurrentTime()
        }
      ],
      isLoading: false
    };
  },
  methods: {
    getCurrentTime() {
      const now = new Date();
      return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    },

    async sendMessage() {
      if (this.userInput.trim() === '' || this.isLoading) return;

      const userMessage = this.userInput.trim();

      // Add user message to chat
      this.messages.push({
        text: userMessage,
        isUser: true,
        timestamp: this.getCurrentTime()
      });

      // Clear input
      this.userInput = '';

      // Show loading state
      this.isLoading = true;
      this.messages.push({
        text: 'Thinking...',
        isUser: false,
        isLoading: true,
        timestamp: this.getCurrentTime()
      });

      // Scroll to bottom
      this.$nextTick(() => {
        const messagesDiv = document.querySelector('.messages');
        if (messagesDiv) {
          messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
      });

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
            isUser: false,
            timestamp: this.getCurrentTime()
          });
        } else {
          this.messages.push({
            text: 'Sorry, I encountered an error. Please try again.',
            isUser: false,
            timestamp: this.getCurrentTime()
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
          isUser: false,
          timestamp: this.getCurrentTime()
        });
      } finally {
        this.isLoading = false;

        // Scroll to bottom
        this.$nextTick(() => {
          const messagesDiv = document.querySelector('.messages');
          if (messagesDiv) {
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
          }
        });
      }
    },

    handleQuickAction(action) {
      this.userInput = action;
      this.sendMessage();
    },

    openLink(url) {
      window.open(url, '_blank');
    }
  }
};
</script>

<style scoped>
.app-container {
  font-family: Arial, sans-serif;
  background: #fdfdfd; /* Changed to a solid color to avoid layering effect */
  color: #333;
  min-height: 100vh; /* Ensures the container covers the viewport height */
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(to right, #ff7a18, #ff4500, #1212b1); /* Adjusted gradient: more orange on the left, deep blue on the right */
  color: white;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-content {
  display: flex;
  align-items: center;
}

.logo {
  width: 80px; /* Increased width */
  height: 80px; /* Increased height */
  margin-right: 20px;
}

.title h1 {
  margin: 0;
  font-size: 24px;
}

.title p {
  margin: 0;
  font-size: 14px;
}

.app-main {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #ffffff; /* Added solid background to avoid gradient layering */
}

.quick-actions {
  margin-bottom: 20px;
  text-align: center;
}

.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.action-button {
  border: none;
  border-radius: 12px; /* Increased border radius for smoother button edges */
  color: white;
  padding: 12px 24px; /* Adjusted padding for better button proportions */
  font-size: 16px; /* Slightly larger font for better readability */
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease; /* Added hover effects */
}

.action-button:hover {
  transform: scale(1.05); /* Slight zoom effect on hover */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover */
}

.chat-window {
  width: 100%;
  max-width: 1000px;
  height: 100%; /* Ensures it fills the available space */
  background: #ffffff; /* Solid background to avoid layering */
  border-radius: 16px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}

.user-message-wrapper {
  flex-direction: row-reverse;
  align-items: flex-end;
}

.message-content {
  max-width: 500px;
  padding: 12px 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
}

.message-content p {
  margin: 0;
  word-wrap: break-word;
  line-height: 1.5;
}

.bot-bubble {
  background: #f5f5f5;
  color: #333;
  border-bottom-left-radius: 4px;
}

.user-bubble {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border-bottom-right-radius: 4px;
  margin-left: auto;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.bot-name {
  text-align: center;
  font-size: 12px;
  font-weight: bold;
  color: #666;
}

.timestamp {
  font-size: 11px;
  color: #999;
  margin-top: auto;
  align-self: flex-end;
}

.input-area {
  display: flex;
  border-top: 1px solid #ccc;
  padding: 12px; /* Adjusted padding for better proportions */
  gap: 10px; /* Added gap for spacing between input and button */
}

input {
  flex: 1;
  border: none;
  padding: 12px;
  border-radius: 12px; /* Enhanced border radius for smoother edges */
  outline: none;
  background: #f5f5f5;
  font-size: 16px; /* Slightly larger font for better readability */
}

.send-button {
  border: none;
  background: #ff7a18;
  color: white;
  padding: 12px 24px; /* Increased width for better visibility */
  border-radius: 12px; /* Enhanced border radius for smoother edges */
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease; /* Added hover effects */
}

.send-button:hover {
  background: #e65c00;
  transform: scale(1.05); /* Slight zoom effect on hover */
}
</style>
