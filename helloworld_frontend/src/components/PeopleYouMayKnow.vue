<script lang="ts">
import axios from 'axios'

export default {
    data() {
        return {
            users: [] as any
        }
    },

    mounted() {
        this.getFriendSuggestions()
    },

    methods: {
        getFriendSuggestions() {
            axios
                .get('/api/friends/suggested/')
                .then(response => {
                    this.users = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}


</script>

<template>
    <div class="fixed w-[308px] p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">People you may know</h3>

        <div class="space-y-4">
            <div class="flex items-center justify-between" v-for="user in users" v-bind:key="user.id">
                <div class="flex items-center space-x-2">
                    <img :src="user.get_avatar" class="h-[40px] w-[40px] object-cover rounded-full">

                    <p class="text-xs"><strong>{{ user.name }}</strong></p>
                </div>

                <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
                    class="py-2 px-3 bg-violet-600 focus:ring-4
                        focus:outline-none focus:ring-violet-200 dark:focus:ring-violet-800 text-white text-xs rounded-lg">
                    Show
                </RouterLink>
            </div>
        </div>
    </div>
</template>
