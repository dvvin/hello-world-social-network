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
  },

  data() {
    return {
      notifications: [] as any
    }
  },

  mounted() {
    this.getNotifications()
  },

  methods: {
    getNotifications() {
      axios
        .get('/api/notifications')
        .then(response => {
          this.notifications = response.data
        })
        .catch(error => {
          console.log('error', error)
        })
    },

    logout() {
      this.userStore.removeToken()

      this.$router.push('/login')
    },
  }
});
</script>


<template>
  <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin>
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
  </head>

  <nav class="sticky top-0 z-50 font-m-plus-rounded-1c px-8 border-b border-gray-200 bg-white">
    <div class="max-w-7xl mx-auto">
      <div class="flex items-center justify-between">

        <RouterLink :to="{ name: 'home' }">
          <a href="#">
            <img src="/hw_logo_trans.png" alt="Logo" class="h-20">
          </a>
        </RouterLink>

        <div v-if="userStore.user.isAuthenticated" class="menu-center flex space-x-12">
          <RouterLink :to="{ name: 'feed' }" v-slot="{ isActive }">
            <div :class="{ 'text-purple-700': isActive, 'text-black': !isActive }"
              class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150 relative cursor-pointer">
              <i class="fa-solid fa-house fa-lg pl-0.5"></i>
            </div>
          </RouterLink>

          <RouterLink :to="{ name: 'chat' }" v-slot="{ isActive }">
            <div :class="{ 'text-purple-700': isActive, 'text-black': !isActive }"
              class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150 cursor-pointer">
              <i class="fa-regular fa-envelope fa-lg pl-0.5"></i>
            </div>
          </RouterLink>

          <RouterLink :to="{ name: 'notifications' }" v-slot="{ isActive }">
            <div :class="{ 'text-purple-700': isActive, 'text-black': !isActive }"
              class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150 relative cursor-pointer">
              <i class="fa-regular fa-bell fa-lg pl-1"></i>
              <span v-if="notifications.length > 0"
                class="absolute top-0 right-0 inline-flex items-center justify-center px-2
                py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
                {{ notifications.length }}
              </span>
            </div>
          </RouterLink>

          <RouterLink :to="{ name: 'search' }" v-slot="{ isActive }">
            <div :class="{ 'text-purple-700': isActive, 'text-black': !isActive }"
              class="w-10 h-10 p-2 rounded-full hover:bg-gray-200 transition-colors duration-150 relative cursor-pointer">
              <i class="fa-solid fa-magnifying-glass fa-lg pl-0.5"></i>
            </div>
          </RouterLink>

        </div>

        <div class="menu-right">
          <template v-if="userStore.user.isAuthenticated">
            <div class="flex items-center">
                <button @click="logout" type="button" class="mr-5 text-white bg-red-500 hover:bg-red-600 focus:ring-4 focus:outline-none
        focus:ring-red-200 dark:focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                  <strong>
                    Logout
                  </strong>
                </button>

              <RouterLink :to="{ name: 'profile', params: { id: userStore.user.id } }">
                <img :src="userStore.user.avatar ?? ''" class="h-12 w-12 object-cover rounded-full">
              </RouterLink>
            </div>
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
