<script lang="ts">
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user'

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

        return {
            userStore
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

    methods: {
        getFriends() {
            axios
                .get(`http://127.0.0.1:8000/api/friends/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.friendshipRequests = response.data.requests
                    this.friends = response.data.friends
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        handleRequest(status: string, pk: number) {
            console.log('handleRequest', status)

            axios
                .post(`http://127.0.0.1:8000/api/friends/${pk}/${status}/`)
                .then(response => {
                    console.log('data', response.data)
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

    <div class="font-m-plus-rounded-1c max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <h2 class="mb-6 text-xl">Friendship requests</h2>
            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4" v-if="friendshipRequests.length">


                <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="friendshipRequest in friendshipRequests"
                    v-bind:key="friendshipRequest.id">
                    <img src="https://i.pravatar.cc/100?img=70" class="mb-6 mx-auto rounded-full">

                    <p>
                        <strong>
                            <RouterLink :to="{ name: 'profile', params: { 'id': friendshipRequest.created_by.id } }">{{
                                friendshipRequest.created_by.name }}</RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ friendshipRequest.created_by.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>

                    <div class="mt-6 space-x-4">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
                            @click="handleRequest('accepted', friendshipRequest.created_by.id)">Accept</button>
                        <button class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg"
                            @click="handleRequest('rejected', friendshipRequest.created_by.id)">Reject</button>
                    </div>
                </div>
            </div>

            <h2 class="mb-6 text-xl">Friends</h2>
            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4" v-if="friends.length">

                <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="user in friends" v-bind:key="user.id">
                    <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                    <p>
                        <strong>
                            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }">{{ user.name }}</RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>
