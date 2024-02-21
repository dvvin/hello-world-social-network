<script lang="ts">
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'

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
    name: 'FeedView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },

    data() {
        return {
            posts: [] as Post[],
            body: '',
            url: null as string | null
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        onFileChange(e: any) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
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

                axios.post('/api/posts/create/', formData, {
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
                }).catch(error => {
                    console.log('error', error);
                });
            }
        },

        deletePost(id: string) {
            this.posts = this.posts.filter((post: Post) => post.id !== id);
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
                <PeopleYouMayKnow />
            </div>

            <div class="main-center col-span-2 space-y-4">
                <div class="bg-white border border-gray-200 rounded-lg">
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
                    <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
                </div>
            </div>

            <div class="main-right col-span-1 space-y-4">
                <Trends />
            </div>
        </div>
    </main>
</template>
