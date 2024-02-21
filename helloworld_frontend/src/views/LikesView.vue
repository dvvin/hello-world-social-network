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
    is_liked_by_user?: boolean;
}

export default {
    name: 'FeedView',

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        };
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },

    data() {
        return {
            posts: [] as Post[],
            url: null as string | null,
            user: {} as any,
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios.get(`/api/posts/profile/${this.$route.params.id}/likes/`)
                .then(response => {
                    console.log('likesview:', response.data)
                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
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

    <main class="font-m-plus-rounded-1c px-8 py-6 bg-gray-100">
        <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
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
                <div v-for="post in posts" v-bind:key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
                    <FeedItem v-bind:post="post" />
                </div>
            </div>
        </div>
    </main>
</template>
