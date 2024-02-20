<script lang="ts">
import axios from 'axios'

export default {
    name: 'trends',

    data() {
        return {
            trends: [] as any
        }
    },

    mounted() {
        this.getTrends()
    },

    methods: {
        getTrends() {
            axios
                .get('/api/posts/trends/')
                .then(response => {
                    this.trends = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        }
    }
}
</script>

<template>
    <div class="fixed w-[308px] p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">Trends</h3>
        <div class="space-y-4">
            <div class="flex items-center justify-between" v-for="trend in trends" v-bind:key="trend.id">
                <p class="text-xs">
                    <strong>#{{ trend.hashtag }}</strong><br>
                    <span class="text-gray-500">{{ trend.occurences }} posts</span>
                </p>

                <RouterLink :to="{ name: 'trendview', params: { id: trend.hashtag } }"
                    class="py-2 px-3 bg-violet-600 hover:bg-violet-700 text-white text-xs rounded-lg">
                    Explore
                </RouterLink>
            </div>
        </div>
    </div>
</template>
