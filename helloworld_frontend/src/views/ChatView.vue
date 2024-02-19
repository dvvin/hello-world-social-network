<script lang="ts">
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
    name: 'chat',

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            conversations: [] as any,
            activeConversation: {} as any,
            body: ''
        }
    },

    mounted() {
        this.getConversations()
    },

    methods: {
        setActiveConversation(id: string) {
            this.activeConversation = id
            this.getMessages()
        },
        getConversations() {
            axios
                .get('http://127.0.0.1:8000/api/chat/')
                .then(response => {
                    this.conversations = response.data

                    if (this.conversations.length) {
                        this.activeConversation = this.conversations[0].id
                    }

                    this.getMessages()
                })
                .catch(error => {
                    console.log(error)
                })
        },

        getMessages() {
            axios
                .get(`http://127.0.0.1:8000/api/chat/${this.activeConversation}/`)
                .then(response => {
                    this.activeConversation = response.data
                })
                .catch(error => {
                    console.log(error)
                })
        },

        submitForm() {
            axios
                .post(`http://127.0.0.1:8000/api/chat/${this.activeConversation.id}/send/`, {
                    body: this.body
                })
                .then(response => {
                    this.activeConversation.messages.push(response.data)

                    this.body = ''
                })
                .catch(error => {
                    console.log(error)
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
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <div class="space-y-4">
                    <div class="flex items-center justify-between" v-for="(conversation, index) in conversations"
                        :key="conversation.id" v-on:click="setActiveConversation(conversation.id)"
                        :class="{ 'pt-4': index !== 0, 'border-t': index !== 0, 'border-gray-200': index !== 0 }">
                        <div class="flex items-center space-x-2">
                            <template v-for="user in conversation.users" v-bind:key="user.id">
                                <div v-if="user.id !== userStore.user.id">
                                    <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                                        <img :src="user.get_avatar" class="w-10 h-10 object-cover rounded-full">
                                    </RouterLink>
                                </div>
                                <p class="text-xs font-bold pl-3.5 " v-if="user.id !== userStore.user.id">{{ user.name }}</p>
                            </template>
                        </div>
                        <span class="text-xs text-gray-500">{{ conversation.modified_at_formatted }} ago</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="main-center col-span-3 space-y-4">
            <div v-if="activeConversation.messages && activeConversation.messages.length"
                class="bg-white border border-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <template v-for="message in activeConversation.messages" v-bind:key="message.id">
                        <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                            v-if="message.created_by.id == userStore.user.id">
                            <div>
                                <div class="bg-emerald-500 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">
                                    {{ message.created_at_formatted }} ago
                                </span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <RouterLink :to="{ name: 'profile', params: { id: message.created_by.id } }">
                                    <img :src="message.created_by.get_avatar" class="h-[40px] w-[40px] object-cover rounded-full">
                                </RouterLink>
                            </div>
                        </div>

                        <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <RouterLink :to="{ name: 'profile', params: { id: message.created_by.id } }">
                                    <img :src="message.created_by.get_avatar" class="h-[40px] w-[40px] object-cover rounded-full">
                                </RouterLink>
                            </div>
                            <div>
                                <div class="bg-violet-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}
                                    ago</span>
                            </div>
                        </div>
                    </template>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm">
                    <div class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What do you want to say?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button :disabled="!body.trim()" type="submit" class="text-white bg-gradient-to-r from-violet-500
                             to-emerald-500 hover:bg-gradient-to-l focus:ring-4 focus:outline-none focus:ring-violet-200
                             dark:focus:ring-emerald-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center">
                            <strong>Send</strong>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

