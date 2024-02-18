<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import Toast from '@/components/Toast.vue';
import { useUserStore } from '@/stores/user';

export default defineComponent({
  setup() {
    const userStore = useUserStore();

    return {
      userStore
    };
  },

  components: {
    Toast
  },

  beforeCreate() {
    this.userStore.initStore()

    const token = this.userStore.user.access;

    if (token) {
      axios.defaults.headers.common["Authorization"] = "Bearer " + token;
    } else {
      axios.defaults.headers.common["Authorization"] = "";
    }
  }
});
</script>


<template>
  <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin>
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c&display=swap" rel="stylesheet">
  </head>

  <nav class="sticky top-0 z-50 font-m-plus-rounded-1c px-8 border-b border-gray-200 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">

        <RouterLink :to="{ name: 'feed' }">
          <a href="#">
            <img src="/hw_logo_trans.png" alt="Logo" class="h-20">
          </a>
        </RouterLink>

        <div v-if="userStore.user.isAuthenticated" class="menu-center flex space-x-12">
          <RouterLink :to="{ name: 'feed' }" class="text-purple-700">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25">
              </path>
            </svg>
          </RouterLink>

          <RouterLink :to="{ name: 'chat' }">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M8.625 9.75a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375m-13.5 3.01c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.184-4.183a1.14 1.14 0 01.778-.332 48.294 48.294 0 005.83-.498c1.585-.233 2.708-1.626 2.708-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z">
              </path>
            </svg>
          </RouterLink>

          <RouterLink :to="{ name: 'notifications' }">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0">
              </path>
            </svg>
          </RouterLink>

          <RouterLink :to="{ name: 'search' }">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
            </svg>
          </RouterLink>
        </div>

        <div class="menu-right">
          <template v-if="userStore.user.isAuthenticated">
            <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }">
              <img :src="userStore.user.avatar ?? ''" class="w-12 rounded-full">
            </RouterLink>
          </template>

          <template v-else>
            <RouterLink :to="{ name: 'login' }">
              <button type="button"
                class="mr-2 mb-2 text-white bg-emerald-500 hover:bg-emerald-600 focus:ring-4 focus:outline-none
               focus:ring-emerald-200 dark:focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-2">
                <strong>
                  Login
                </strong>
              </button>
            </RouterLink>

            <RouterLink :to="{ name: 'signup' }">
              <button type="button"
                class="text-white bg-violet-500 hover:bg-violet-600 focus:ring-4 focus:outline-none
               focus:ring-violet-200 dark:focus:ring-violet-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-2">
                <strong>
                  Sign Up
                </strong>
              </button>
            </RouterLink>
          </template>
        </div>
      </div>
    </div>
  </nav>

  <main class="min-h-screen bg-gray-100">
    <RouterView />
  </main>

  <Toast />
</template>

<style scoped>
</style>
