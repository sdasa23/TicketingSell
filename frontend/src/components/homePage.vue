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
  background: #f5f5f7; 
  color: #2c3e50;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.6;
}

.header {
  position: sticky;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding: 1.5rem;
  background: rgba(245, 245, 247, 0.92); 
  backdrop-filter: blur(12px);
  z-index: 1000;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  border-bottom: 1px solid #e0e0e0; 
}

.new-user-button {
  background: #3a3a3c; 
  color: #f5f5f7;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease-out;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.new-user-button:hover {
  background: #4a4a4c;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
}

.user-info {
  background: rgba(255, 255, 255, 0.95);
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
  margin-bottom: 3rem;
  max-width: 600px;
  width: 100%;
  border: 1px solid #e5e5ea; 
}

.user-info h1 {
  font-size: 2.25rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.user-info p {
  font-size: 1.125rem;
  margin-bottom: 2rem;
  color: #4a4a4c;
  line-height: 1.7;
}

.user-info button {
  background: #3a3a3c;
  color: #f5f5f7;
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease-out;
  font-weight: 500;
}

.user-info button:hover {
  background: #4a4a4c;
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.market-buttons {
  display: flex;
  gap: 1.5rem;
}

.market-buttons button {
  background: rgba(255, 255, 255, 0.98); 
  color: #3a3a3c;
  border: 1px solid #e5e5ea;
  padding: 1.25rem 2.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease-out;
  font-weight: 500;
  min-width: 200px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.market-buttons button:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
  border-color: #d8d8dc;
}

@keyframes softFadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.user-info {
  animation: softFadeIn 0.5s ease-out forwards;
}

.market-buttons button {
  animation: softFadeIn 0.5s var(--delay) ease-out forwards;
  opacity: 0;
}

.market-buttons button:nth-child(1) {
  --delay: 0.1s;
}

.market-buttons button:nth-child(2) {
  --delay: 0.2s;
}

@media (max-width: 768px) {
  .header {
    padding: 1.25rem;
  }
  
  .user-info {
    padding: 2.5rem 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  }

  .market-buttons {
    flex-direction: column;
    width: 100%;
    gap: 1rem;
  }

  .market-buttons button {
    width: 100%;
    padding: 1.5rem;
  }
}
</style>