<script lang="ts">
import axios from 'axios'

export default {
    name: 'notifications',

    data() {
        return {
            notifications: [] as any
        }
    },

    mounted() {
        this.getNotifications()
    },

    methods: {
        getNotifications() {
            axios
                .get('/api/notifications')
                .then(response => {
                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        async readNotification(notification: any) {
            await axios
                .post(`/api/notifications/read/${notification.id}/`)
                .then(response => {
                    if (notification.notification_type == 'postlike' || notification.notification_type == 'postcomment') {
                        if (notification.post_id) {
                            this.$router.push({ name: 'postview', params: { id: notification.post_id } })
                        }
                    } else {
                        if (notification.created_by) {
                            this.$router.push({ name: 'friends', params: { id: notification.created_for_id } })
                        }
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
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

    <div class="font-m-plus-rounded-1c max-w-7xl mx-auto grid grid-cols-4 gap-4 pt-6">
        <div class="main-center col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="notification in notifications"
                v-bind:key="notification.id" v-if="notifications.length">
                {{ notification.body }}

                <button class="underline" @click="readNotification(notification)">Read more</button>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
                There are no notifications
            </div>
        </div>
    </div>
</template>
