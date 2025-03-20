<template>
  <div class="home-page">
    <header class="header">
      <button class="new-user-button" @click="handleNewUser">New User Bonus</button>
    </header>

    <main class="main-content">
      <section class="user-info">
        <h1>Welcome, User</h1>
        <p>Your address: {{ user.name }}</p>
        <p>Account Balance: {{ user.balance }}</p>
      </section>
      <section class="market-buttons">
        <button @click="goToFirstMarket">First Market</button>
        <button @click="goToSecondMarket">Second Market</button>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

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
});
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f0f0f0;
}

.header {
  position: sticky; /* 粘性定位 */
  top: 0; /* 固定在顶部 */
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
  background-color: #333;
  z-index: 1000; /* 确保 header 在最上层 */
}

.main-content {
  flex: 1; /* 占据剩余空间 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 60px; /* 根据 header 的高度调整 */
}

.new-user-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}
.user-info {
  margin-bottom: 2rem;
  text-align: center;
}

.market-buttons button {
  margin: 0.5rem;
  padding: 1rem 2rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
</style>