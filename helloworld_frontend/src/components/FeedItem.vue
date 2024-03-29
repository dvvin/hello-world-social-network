<script lang="ts">
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        };
    },

    props: {
        post: {
            type: Object,
            default: () => ({})
        },

        likedByUser: {
            type: Boolean,
            default: false
        }
    },

    emits: ['deletePost'],

    data() {
        return {
            isLiked: this.post.is_liked_by_user,
            showLikesList: false,
            usersWhoLiked: [] as any,
            showButton: false
        };
    },

    mounted() {
        this.fetchLikes(this.post.id);
    },

    methods: {
        likePost(id: string) {
            axios.post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message === 'like created') {
                        this.post.likes_count += 1;
                        this.isLiked = true;
                    }

                    else if (response.data.message === 'like removed') {
                        this.post.likes_count = Math.max(this.post.likes_count - 1, 0);
                        this.isLiked = false;
                    }

                    this.fetchLikes(id);
                })
                .catch(error => {
                    console.log('error', error);
                });
        },

        fetchLikes(id: string) {
            axios.get(`/api/posts/${id}/likes/`)
                .then(response => {
                    console.log(response.data);
                    this.usersWhoLiked = response.data;
                    this.showLikesList = this.usersWhoLiked.length > 0;
                })
                .catch(error => {
                    console.log('Error fetching likes:', error);
                });
        },

        toggleButton() {
            this.showButton = !this.showButton;
        },

        deletePost() {
            this.$emit('deletePost', this.post.id);

            axios
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then(response => {
                    this.toastStore.showToast('5000', 'The post has been deleted!', 'bg-red-300')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        reportPost() {
            axios
                .post(`/api/posts/${this.post.id}/report/`)
                .then(response => {
                    console.log(response.data);

                    this.toastStore.showToast('5000', 'The post has been reported!', 'bg-emerald-300')
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

    <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <RouterLink :to="{ name: 'profile', params: { 'id': post.created_by.id } }">
                <img :src="post.created_by.get_avatar" class="h-[40px] w-[40px] object-cover rounded-full">
            </RouterLink>

            <p>
                <strong>
                    <RouterLink :to="{ name: 'profile', params: { 'id': post.created_by.id } }">
                        {{ post.created_by.name }}
                    </RouterLink>
                </strong>
            </p>
        </div>

        <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
    </div>

    <template v-if="post.attachments.length">
        <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
    </template>

    <p>
        {{ post.body }}
    </p>

    <div class="my-6 flex justify-between">
        <div class="flex space-x-6">
            <div class="flex items-center space-x-2">
                <i @click="likePost(post.id)" :class="[isLiked ? 'fa-solid' : 'fa-regular', 'fa-heart', 'fa-lg']"></i>
                <span class="text-gray-500 text-xs" @click="fetchLikes(post.id)">{{ post.likes_count }} likes</span>
            </div>

            <!-- <div v-if="showLikesList" class="mt-2 bg-white shadow rounded-lg p-2">
                <div v-if="usersWhoLiked.length" class="text-xs">
                    <p>Liked by:</p>
                    <ul>
                        <li v-for="user in usersWhoLiked" :key="user.id">{{ user.name }}</li>
                    </ul>
                </div>
            </div> -->

            <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3
                                    7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969
                                    0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                    </path>
                </svg>

                <RouterLink :to="{ name: 'postview', params: { id: post.id } }" class="text-gray-500 text-xs">{{
                    post.comments_count }} comments</RouterLink>
            </div>

            <div v-if="post.is_private">
                <i class="fa-regular fa-eye-slash"></i>
            </div>
        </div>

        <div>
            <div @click="toggleButton">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12
                                12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                    </path>
                </svg>
            </div>
        </div>
    </div>

    <div v-if="showButton" class="">
        <div class="flex space-x-6 items-center">
            <div @click="deletePost" v-if="userStore.user.id === post.created_by.id" class="flex items-center space-x-2">
                <i class="fa-regular fa-trash-can text-red-500"></i>
                <span class="text-red-500 text-xs">Delete post</span>
            </div>

            <div @click="reportPost" class="flex items-center space-x-2">
                <i class="fa-regular fa-flag"></i>
                <span class="text-xs">Report post</span>
            </div>
        </div>
    </div>
</template>
