<script lang="ts">
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import { useUserStore } from '@/stores/user';

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
    name: 'ProfileView',

    setup() {
        const userStore = useUserStore();

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
            user: {} as any,
            body: '',
        }
    },

    mounted() {
        this.getFeed()
    },

    watch: {
        '$route.params.id': {
            handler: function () {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        getFeed() {
            axios
                .get(`http://127.0.0.1:8000/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    this.posts = response.data.posts
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            axios
                .post('http://127.0.0.1:8000/api/posts/create/', {
                    'body': this.body
                })
                .then(response => {
                    this.posts.unshift(response.data)
                    this.body = ''
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
    </head>

    <main class="font-m-plus-rounded-1c px-8 py-6 bg-gray-100">
        <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
            <div class="main-left col-span-1">
                <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                    <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">

                    <p><strong>{{ user.name }}</strong></p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">182 friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>
                </div>
            </div>

            <div class="main-center col-span-2 space-y-4">
                <div v-if="userStore.user.id === user.id" class="bg-white border border-gray-200 rounded-lg">
                    <form v-on:submit.prevent="submitForm" method="post">
                        <div class="p-4">
                            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                                placeholder="Say helloWorld!"></textarea>
                        </div>

                        <div class="p-4 border-t border-gray-100 flex justify-between">
                            <button :disabled="!body.trim()" class="inline-block px-4 py-2.5 mt-2 bg-violet-600 focus:ring-4
                        focus:outline-none focus:ring-violet-200 dark:focus:ring-violet-800 text-white rounded-lg">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 fill-gray-200" viewBox="0 0 24 24">
                                    <path
                                        d="M22 13a1 1 0 0 0-1 1v4.213A2.79 2.79 0 0 1 18.213 21H5.787A2.79 2.79 0 0 1 3 18.213V14a1
                                    1 0 0 0-2 0v4.213A4.792 4.792 0 0 0 5.787 23h12.426A4.792 4.792 0 0 0 23 18.213V14a1 1 0 0 0-1-1Z"
                                        data-original="#000000" />
                                    <path d="M6.707 8.707 11 4.414V17a1 1 0 0 0 2 0V4.414l4.293 4.293a1 1 0 0 0 1.414-1.414l-6-6a1
                                    1 0 0 0-1.414 0l-6 6a1 1 0 0 0 1.414 1.414Z" data-original="#000000" />
                                </svg>
                            </button>

                            <button :disabled="!body.trim()" type="submit" class="text-white bg-gradient-to-r from-violet-500
                             to-emerald-500 hover:bg-gradient-to-l focus:ring-4 focus:outline-none focus:ring-violet-200
                             dark:focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mt-2">
                                <strong>Post</strong>
                            </button>

                        </div>
                    </form>
                </div>

                <div v-for="post in posts" v-bind:key="post.id" class="p-4 bg-white border border-gray-200 rounded-lg">
                    <FeedItem v-bind:post="post" />
                </div>
            </div>

            <div class="main-right col-span-1 space-y-4">
                <PeopleYouMayKnow />
                <Trends />
            </div>
        </div>
    </main>
</template>
