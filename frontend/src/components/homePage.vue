<template>
  <div class="home-page">
    <header class="header">
      <button class="new-user-button" @click="handleNewUser">New User Bonus</button>
    </header>

    <main class="main-content">
      <section class="user-info">
        <h1>Welcome, User</h1>
        <p>Your address: {{ user.name }}</p>
        <p>Account Balance: {{ user.balance }} <button @click="add_token_into_wallet()" style="float: right;">add token to wallet</button></p>
        
      </section>
      <section class="market-buttons">
        <button @click="goToFirstMarket">Primary Market</button>
        <button @click="goToSecondMarket">Second-hand Market</button>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
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

  async function getTokenInf(){
      const response = await axios.get('http://localhost:8000/get-token-address');
      return response;
  }

  async function getTokenBalance(user_address){
      const balance = await axios.get('http://localhost:8000/get-token-balance',{
        params: {user_address : user_address} 
      });
      return balance.data
  }

  async function add_token_into_wallet(){
    const response = await getTokenInf();
    console.log(response)
    await window.ethereum.request({
      "method": "wallet_watchAsset",
      "params": {
        type: "ERC20",
        options: {
          address: response.data.address,
          symbol: response.data.symbol,
          decimals: response.data.decimal,
          image: response.data.image
        }
      }
    })
  }

const user = ref({
  name: '',
  balance: ''
});

const router = useRouter();

const handleNewUser = () => {
  router.push("/newUser");
  console.log('New User button clicked');
};

const goToFirstMarket = () => {
  router.push({ path: '/firstMarket' });
};

const goToSecondMarket = () => {
  router.push({ path: '/secondMarket' });
};

onMounted(async () => {
  user.value.name = await getCurrentUserAddress();
  user.value.balance = await getTokenBalance(user.value.name);
});
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: #ffffff;
}

.header {
  position: sticky;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  background-color: rgba(0, 0, 0, 0.2); 
  backdrop-filter: blur(10px); 
  z-index: 1000;
}

.new-user-button {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.new-user-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.new-user-button:active {
  transform: translateY(0);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.user-info {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 1rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  max-width: 500px;
  width: 100%;
}

.user-info h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.user-info p {
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.user-info button {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.user-info button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.user-info button:active {
  transform: translateY(0);
}

.market-buttons {
  display: flex;
  gap: 1rem;
}

.market-buttons button {
  background-color: #4a90e2;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.market-buttons button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
}

.market-buttons button:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .user-info {
    padding: 1rem;
  }

  .market-buttons {
    flex-direction: column;
    width: 100%;
  }

  .market-buttons button {
    width: 100%;
  }
}
</style>