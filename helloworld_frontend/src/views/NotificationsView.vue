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
                .get('http://127.0.0.1:8000/api/notifications')
                .then(response => {
                    console.log(response.data)

                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        async readNotification(notification: any) {
    console.log('readNotification', notification.id)

    await axios
        .post(`http://127.0.0.1:8000/api/notifications/read/${notification.id}/`)
        .then(response => {
            console.log(response.data)

            if (notification.notification_type == 'postlike' || notification.notification_type == 'postcomment') {
                // Ensure post_id is present
                if (notification.post_id) {
                    this.$router.push({name: 'postview', params: {id: notification.post_id}})
                } else {
                    console.error('Post ID missing for notification', notification.id);
                }
            } else {
                // Assume created_by is the correct field for other notification types
                // Make sure to replace 'created_by' with 'created_for_id' if your data structure has this field
                if (notification.created_by) {
                    this.$router.push({name: 'friends', params: {id: notification.created_for_id}})
                } else {
                    console.error('Created For ID missing for notification', notification.id);
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
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="notification in notifications"
                v-bind:key="notification.id" v-if="notifications.length">
                {{ notification.body }}

                <button class="underline" @click="readNotification(notification)">Read more</button>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
                You don't have any unread notifications!
            </div>
        </div>
    </div>
</template>
