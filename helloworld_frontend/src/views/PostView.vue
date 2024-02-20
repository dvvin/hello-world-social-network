<script lang="ts">
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'
import CommentItem from '../components/CommentItem.vue'

export default {
    name: 'PostView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        CommentItem
    },

    data() {
        return {
            post: {
                id: null,
                comments: {} as any,
                comments_count: 0
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
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

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css">
    </head>

    <div class="pb-6 font-m-plus-rounded-1c pt-6 max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-if="post.id">
                <FeedItem v-bind:post="post" />
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Leave a comment"></textarea>
                    </div>

                    <button :disabled="!body.trim()" type="submit" class="text-white bg-gradient-to-r from-violet-500
                             to-emerald-500 hover:bg-gradient-to-l focus:ring-4 focus:outline-none focus:ring-violet-200
                             dark:focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center ml-4 ">
                        <strong>Post</strong>
                    </button>
                </form>
            </div>

            <div class="p-4 ml-6 bg-white border border-gray-200 rounded-lg" v-for="comment in post.comments"
                v-bind:key="comment.id">
                <CommentItem v-bind:comment="comment" />
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
