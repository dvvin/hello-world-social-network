<script lang="ts">
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

interface Post {
    body: string;
    created_at_formatted: string;
    created_by: {
        email: string;
        id: string;
        name: string;
    };
    id: string;
}

export default {
    name: 'FriendsView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        };
    },

    components: {
        PeopleYouMayKnow,
        Trends,
    },

    data() {
        return {
            user: {} as any,
            friendshipRequests: [] as any,
            friends: [] as any
        }
    },

    mounted() {
        this.getFriends()
    },

    watch: {
        '$route.params.id': {
            immediate: true,
            handler: 'getFriends'
        }
    },

    methods: {
        getFriends() {
            axios
                .get(`/api/friends/${this.$route.params.id}/`)
                .then(response => {
                    console.log('friendsview:', response.data)
                    this.friendshipRequests = response.data.requests
                    this.friends = response.data.friends
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        handleRequest(status: string, pk: number) {
            axios
                .post(`/api/friends/${pk}/${status}/`)
                .then(response => {
                    if (status === 'rejected') {
                        this.toastStore.showToast('5000', 'You rejected the request.', 'bg-red-300')
                        this.friendshipRequests = this.friendshipRequests.filter((request: { created_by: { id: number } }) => request.created_by.id !== pk);
                    }

                    else {
                        this.toastStore.showToast('5000', 'You accepted the request.', 'bg-emerald-300')
                        this.getFriends();
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>

<template>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin>
        <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c&display=swap" rel="stylesheet">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    </head>

    <div class="font-m-plus-rounded-1c pt-6 max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class="ml-2 h-64 w-64 mb-6 object-cover rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div v-if="friendshipRequests.length > 0" class="p-4 bg-white border border-gray-200 rounded-lg">
                <h2 class="mb-6 text-xl">Friendship requests</h2>
                <div class="grid grid-cols-4 gap-4">
                    <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="friendshipRequest in friendshipRequests"
                        v-bind:key="friendshipRequest.id">
                        <RouterLink :to="{ name: 'profile', params: { id: friendshipRequest.created_by.id } }">
                            <img :src="friendshipRequest.created_by.get_avatar" class="mb-6 h-28 w-28 object-cover rounded-full">
                        </RouterLink>

                        <RouterLink :to="{ name: 'profile', params: { id: friendshipRequest.created_by.id } }">
                            <p>
                                <strong>
                                    {{ friendshipRequest.created_by.name }}
                                </strong>
                            </p>
                        </RouterLink>
                        <div class="mt-6 flex space-x-8 justify-around">
                            <RouterLink :to="{ name: 'friends', params: { id: friendshipRequest.created_by.id } }">
                                <p class="text-xs text-gray-500">{{ friendshipRequest.created_by.friends_count }}
                                    friends
                                </p>
                            </RouterLink>

                            <p class="text-xs text-gray-500">{{ friendshipRequest.created_by.posts_count }} posts</p>
                        </div>
                        <div class="mt-6 space-x-4" @click.stop>
                            <button class="inline-block mt-[-8px] py-2 px-2.5 bg-emerald-600 text-xs text-white rounded-lg"
                                @click="handleRequest('accepted', friendshipRequest.created_by.id)">
                                <i class=" fa-solid fa-check"></i>
                            </button>
                            <button class="inline-block mt-[-8px] py-2 px-3 bg-red-600 text-xs text-white rounded-lg"
                                @click="handleRequest('rejected', friendshipRequest.created_by.id)">
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h2 class="mb-6 text-xl">{{ user.name }}'s Friends</h2>
                <div class="grid grid-cols-4 gap-4">
                    <div class="block" v-for="user in friends" v-bind:key="user.id">
                        <div class="p-4 text-center bg-gray-100 rounded-lg">
                            <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                                <img :src="user.get_avatar" class="mb-6 h-28 w-28 object-cover rounded-full">
                            </RouterLink>

                            <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                                <p>
                                    <strong>{{ user.name }}</strong>
                                </p>
                            </RouterLink>
                            <div class="mt-6 flex space-x-8 justify-around">
                                <RouterLink :to="{ name: 'friends', params: { id: user.id } }">
                                    <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                                </RouterLink>
                                <p class="text-xs text-gray-500">
                                    {{ user.posts_count }} {{ user.posts_count === 1 ? 'post' : 'posts' }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <div class="pt-60">
                <Trends />
            </div>
        </div>
    </div>
</template>
