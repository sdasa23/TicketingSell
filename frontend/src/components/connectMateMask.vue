<script setup>
import { ref, onMounted } from "vue";
import { useRouter} from "vue-router";
import VueMetamask from "vue-metamask";

const metamask = ref(null);
const router = useRouter();
const account = ref(null);

const connect = async () => {
  try {
    // Get ref target use init methods
    await metamask.value.init();
    account.value = await window.ethereum.request({ method: 'eth_accounts' });
    if (account.value) {
      console.log("MetaMask connected");
      router.push({path:"/homePage"});
    }
  } catch (error) {
    console.error("MetaMask connection failed:", error);
  }
};

onMounted(async () => {
  console.log(router);
  if (window.ethereum) {
    try {
      // check is already connected to MetaMask
      const accounts = await window.ethereum.request({ method: 'eth_accounts' });
      if (accounts.length > 0) {
        account.value = accounts[0];
        console.log("MetaMask already connected");
        if (router) { // ensure router is existed
          router.push({path:"/homePage"});
        } else {
          console.error("Router is not initialized.");
        }
      } else {
        // try to connect MetaMask
        await connect();
      }
    } catch (error) {
      console.error("Connect MetaMask Error:", error);
    }
  } else {
    console.error("MetaMask is not installed");
  }
});



</script>

<template>
  <div class="bg-gradient-to-br from-primary to-accent text-primary-foreground min-h-screen flex flex-col items-center justify-center">
    <svg width="100" height="100" viewBox="0 0 512 492" fill="none" xmlns="http://www.w3.org/2000/svg" class="h-7 w-7">
      <g stroke-linecap="round" stroke-linejoin="round" stroke-width=".25">
        <path d="M478.468 474.862L368.183 442.171L285.013 491.664L226.987 491.64L143.769 442.171L33.5324 474.862L0 362.174L33.5324 237.106L0 131.365L33.5324 0.312256L205.786 102.76H306.214L478.468 0.312256L512 131.365L478.468 237.106L512 362.174L478.468 474.862Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M33.5563 0.312256L205.809 102.832L198.959 173.19L33.5563 0.312256Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M143.793 362.222L219.583 419.696L143.793 442.171V362.222Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M213.525 267.201L198.959 173.238L105.717 237.13L105.669 237.106V237.154L105.957 302.921L143.768 267.201H143.793H213.525Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M478.467 0.312256L306.214 102.832L313.041 173.19L478.467 0.312256Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M368.231 362.222L292.441 419.696L368.231 442.171V362.222Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M406.331 237.154H406.355H406.331V237.106L406.307 237.13L313.065 173.238L298.498 267.201H368.231L406.066 302.921L406.331 237.154Z" fill="#FF5C16" stroke="#FF5C16"></path>
        <path d="M143.769 442.171L33.5324 474.862L0 362.222H143.769V442.171Z" fill="#E34807" stroke="#E34807"></path><path d="M213.502 267.177L234.559 403.013L205.377 327.487L105.91 302.921L143.745 267.177H213.478H213.502Z" fill="#E34807" stroke="#E34807"></path>
        <path d="M368.231 442.171L478.467 474.862L512 362.222H368.231V442.171Z" fill="#E34807" stroke="#E34807"></path><path d="M298.498 267.177L277.441 403.013L306.623 327.487L406.09 302.921L368.231 267.177H298.498Z" fill="#E34807" stroke="#E34807"></path>
        <path d="M0 362.173L33.5324 237.106H105.645L105.909 302.896L205.377 327.463L234.558 402.989L219.559 419.623L143.769 362.149H0V362.173Z" fill="#FF8D5D" stroke="#FF8D5D"></path>
        <path d="M512 362.173L478.467 237.106H406.355L406.09 302.896L306.623 327.463L277.441 402.989L292.441 419.623L368.231 362.149H512V362.173Z" fill="#FF8D5D" stroke="#FF8D5D"></path>
        <path d="M306.214 102.76H256H205.786L198.959 173.118L234.558 402.918H277.441L313.065 173.118L306.214 102.76Z" fill="#FF8D5D" stroke="#FF8D5D"></path>
        <path d="M33.5324 0.312256L0 131.365L33.5324 237.106H105.645L198.935 173.19L33.5324 0.312256Z" fill="#661800" stroke="#661800"></path>
        <path d="M192.661 294.46H159.994L142.206 311.815L205.401 327.415L192.661 294.436V294.46Z" fill="#661800" stroke="#661800"></path>
        <path d="M478.468 0.312256L512 131.365L478.468 237.106H406.355L313.065 173.19L478.468 0.312256Z" fill="#661800" stroke="#661800"></path>
        <path d="M319.387 294.46H352.102L369.89 311.839L306.623 327.463L319.387 294.436V294.46Z" fill="#661800" stroke="#661800"></path>
        <path d="M284.989 446.834L292.441 419.671L277.442 403.037H234.535L219.535 419.671L226.987 446.834" fill="#661800" stroke="#661800"></path>
        <path d="M284.989 446.833V491.687H226.987V446.833H284.989Z" fill="#C0C4CD" stroke="#C0C4CD"></path>
        <path d="M143.793 442.123L227.035 491.664V446.81L219.583 419.648L143.793 442.123Z" fill="#E7EBF6" stroke="#E7EBF6"></path>
        <path d="M368.231 442.123L284.989 491.664V446.81L292.441 419.648L368.231 442.123Z" fill="#E7EBF6" stroke="#E7EBF6"></path>
      </g></svg>
    <h1 class="text-3xl font-bold mb-2">Connect with MetaMask</h1>
    <p class="text-center text-lg mb-6 px-4">To proceed, please connect your MetaMask wallet to access all features.</p>

    <vue-metamask ref="metamask" :init-connect="false"></vue-metamask>
    <!-- <button @click="connect" class="mt-6 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Connect Wallet</button> -->
</div>
</template>

<style scoped>
.bg-gradient-to-br {
  background: linear-gradient(135deg, #f5f5f7, #e5e5ea);
}

.text-primary-foreground {
  color: #2c3e50; 
}

.text-3xl {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: -0.5px;
}

.text-lg {
  font-size: 1.125rem;
  line-height: 1.75rem;
  color: #4a4a4c; 
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

button {
  background-color: #3a3a3c; 
  color: #f5f5f7;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.25s ease-out;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  letter-spacing: 0.3px;
}

button:hover {
  background-color: #4a4a4c;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

svg {
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.08)); 
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px); 
  }
}

.min-h-screen {
  min-height: 100vh;
}

.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.w-full {
  width: 100%;
}

.mt-6 {
  margin-top: 1.5rem;
}

@media (min-width: 768px) {
  .text-3xl {
    font-size: 2.5rem;
  }

  .text-lg {
    font-size: 1.25rem;
  }

  button {
    width: auto;
    padding: 1rem 2rem;
  }
  
  .bg-gradient-to-br {
    background: linear-gradient(135deg, #f5f5f7, #e0e0e5); 
  }
}

.bg-gradient-to-br::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255,255,255,0.8) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255,255,255,0.6) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}
</style>