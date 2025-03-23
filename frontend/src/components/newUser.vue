<template>
    <div class="container">
        <h1>Are you fresh?</h1>
        <button @click="fetchData">Query</button>
        <div v-if="result && result.is_new_user">
            <h2>Result:</h2>
            <p>Wow, Your are a new user!! </p>
            <p>We will give you many many EVENT coins!</p>
            <p>Now you have {{ result.balance}}  EVENT coins!</p>
            <p>This transaction hash is :{{ result.transaction_hash }}</p>
        </div>
        <div v-else-if="result">
            <h2>Result:</h2>
            <p>Sorry, you are not fresh </p>
            <p>But you have {{ result.balance}}  EVENT coins!</p>
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
  onMounted(async () => {
  address.value = await getCurrentUserAddress();
});
  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/new-user-bonus', {
        params: { address: address.value }
      });
      result.value = response.data;
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
    background-color: #f0f0f0;
  }
  
  input {
    margin-bottom: 1rem;
    padding: 0.5rem;
    font-size: 1rem;
  }
  
  button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
  }
  
  h2 {
    margin-top: 1rem;
  }
  </style>