<script lang="ts">
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
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
    name: 'ProfileView',

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
        FeedItem
    },

    data() {
        return {
            posts: [] as Post[],
            user: {
                id: null
            } as any,
            body: '',
            url: null as string | null
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
        onFileChange(e: any) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        sendFriendshipRequest() {
            axios
                .post(`http://127.0.0.1:8000/api/friends/${this.user.id}/request/`)
                .then(response => {
                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast('5000', 'The request has already been sent!', 'bg-red-300')
                    }

                    else {
                        this.toastStore.showToast('5000', 'The request was sent!', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

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
            let formData = new FormData();
            const fileInput = this.$refs.file as HTMLInputElement;

            const isFileSelected = fileInput && fileInput.files && fileInput.files[0];

            if (this.body.trim() !== '' || isFileSelected) {
                if (fileInput && fileInput.files && fileInput.files[0]) {
                    formData.append('image', fileInput.files[0]);
                }

                formData.append('body', this.body);

                axios.post('http://127.0.0.1:8000/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                }).then(response => {
                    this.posts.unshift(response.data);
                    this.body = '';
                    if (fileInput) {
                        fileInput.value = '';
                    }
                    this.url = null;
                    this.user.posts_count += 1;
                }).catch(error => {
                    console.log('error', error);
                });
            }
        },

        logout() {
            this.userStore.removeToken()

            this.$router.push('/login')
        },

        sendDirectMessage() {
            axios
                .get(`http://127.0.0.1:8000/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    this.$router.push('/chat')
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
                    <img :src="user.get_avatar" class="mb-6 rounded-full">

                    <p><strong>{{ user.name }}</strong></p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <button @click="sendFriendshipRequest" v-if="userStore.user.id !== user.id"
                            class="inline-block mt-[-8px] py-2 px-2 bg-purple-600 text-xs text-white rounded-lg">
                            <i class="fa-solid fa-user-plus fa-lg"></i>
                        </button>

                        <button @click="logout" v-if="userStore.user.id === user.id"
                            class="inline-block mt-[-8px] py-2 px-2 bg-red-600 text-xs text-white rounded-lg">
                            logout
                        </button>

                        <RouterLink to="/profile/edit" v-if="userStore.user.id === user.id"
                            class="inline-block mt-[-8px] py-2 px-2 bg-violet-600 text-xs text-white rounded-lg">
                            edit
                        </RouterLink>

                        <button @click="sendDirectMessage" v-if="userStore.user.id !== user.id"
                            class="inline-block mt-[-8px] py-2 px-2.5 bg-purple-600 text-xs text-white rounded-lg">
                            <i class="fa-regular fa-envelope fa-lg"></i>
                        </button>

                        <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">
                            {{ user.friends_count }} friends
                        </RouterLink>

                        <p class="text-xs text-gray-500">
                            {{ user.posts_count }} {{ user.posts_count === 1 ? 'post' : 'posts' }}
                        </p>

                        <!-- To implement later:
                        <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500">
                            {{ user.friends_count }} likes
                        </RouterLink> -->

                    </div>


                </div>
            </div>

            <div class="main-center col-span-2 space-y-4">
                <div v-if="userStore.user.id === user.id" class="bg-white border border-gray-200 rounded-lg">
                    <form v-on:submit.prevent="submitForm" method="post">
                        <div class="p-4">
                            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                                placeholder="Say helloWorld!">
                            </textarea>

                            <div id="preview" v-if="url">
                                <img :src="url" class="w-[100px] mt-3 rounded-xl" />
                            </div>
                        </div>

                        <div class="p-4 border-t border-gray-100 flex justify-between">
                            <label :disabled="!body.trim()"
                                class="inline-block px-4 py-2.5 mt-2 bg-violet-600 hover:bg-violet-700 focus:ring-4
                        dark:focus:ring-emerald-300focus:outline-none focus:ring-violet-200 dark:focus:ring-violet-800 text-white rounded-lg">
                                <input type="file" ref="file" class="hidden" @change="onFileChange" />
                                <i class="fa-solid fa-plus fa-lg"></i>
                            </label>

                            <button type="submit" class="text-white bg-gradient-to-r from-violet-500
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
                <div class="pt-60">
                    <Trends />
                </div>
            </div>
        </div>
    </main>
</template>
