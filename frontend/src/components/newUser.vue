<template>
  <div class="container">
    <h1>Are you new user?</h1>
    <button @click="fetchData">Query</button>
    <div v-if="result && result.is_new_user" class="result-card">
      <h2>Result:</h2>
      <p>Wow, you are a new user!!</p>
      <p>We will share some coins for your trial!!</p>
      <p>Now you have {{ result.balance }} EVENT coins!</p>
      <p>This transaction hash is: {{ result.transaction_hash }}</p>
    </div>
    <div v-else-if="result" class="result-card">
      <h2>Result:</h2>
      <p>You are a current user.</p>
      <p>You have {{ result.balance }} EVENT coins!</p>
    </div>
    <div v-if="showFireworks" class="fireworks">
      <div v-for="(firework, index) in fireworks" :key="index" class="firework" :style="firework.style"></div>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref, onMounted  } from 'vue';
  import axios from 'axios';
  
  async function getCurrentUserAddress() {
  if (window.ethereum) {
    try {
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      const accounts = await window.ethereum.request({ method: 'eth_accounts' });
      if (accounts.length > 0) {
        console.log('Current user address:', accounts[0]);
        return accounts[0];
      } else {
        console.log('No accounts found');
        return null;
      }
    } catch (error) {
      console.error('Error fetching accounts:', error);
      return null;
    }
  } else {
    console.error('MetaMask is not installed');
    return null;
  }
}

  const address = ref('');
  const result = ref(null);
  const showFireworks = ref(false); 
  const fireworks = ref([]); 

  onMounted(async () => {
  address.value = await getCurrentUserAddress();
});


  const createFireworks = () => {
    const colors = ['#ff5c16', '#ff8d5d', '#e34807', '#ffffff']; 
    const newFireworks = [];
    for (let i = 0; i < 20; i++) { 
      const color = colors[Math.floor(Math.random() * colors.length)];
      const positionX = Math.random() * 100; 
      const positionY = Math.random() * 100; 
      const delay = Math.random() * 2; 
      newFireworks.push({
        style: {
          left: `${positionX}%`,
          top: `${positionY}%`,
          backgroundColor: color,
          animationDelay: `${delay}s`,
        },
      });
    }
    fireworks.value = newFireworks;
    showFireworks.value = true;
    setTimeout(() => {
      showFireworks.value = false; 
    }, 3000);
  };


    const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/new-user-bonus', {
        params: { address: address.value },
      });
      result.value = response.data;
      if (result.value.is_new_user) {
        createFireworks(); 
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      result.value = 'Error!';
    }
  };

  </script>
  
  <style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #ffffff;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

button {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  font-size: 1rem;
  margin-bottom: 2rem;
}

button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

button:active {
  transform: translateY(0);
}

.result-card {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
}

.result-card h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.result-card p {
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.fireworks {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.firework {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: explode 1.5s ease-out infinite;
}

@keyframes explode {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }

  .result-card {
    padding: 1rem;
  }

  .result-card h2 {
    font-size: 1.5rem;
  }

  .result-card p {
    font-size: 1rem;
  }
}
  </style>