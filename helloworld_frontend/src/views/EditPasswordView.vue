<script lang="ts">
import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: {
                old_password: '',
                new_password1: '',
                new_password2: ''
            },
            errors: [] as string[],
        }
    },

    // created() {
    //     this.form.email = this.userStore.user.email as string;
    //     this.form.name = this.userStore.user.name as string;
    // },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.new_password1 !== this.form.new_password2) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()

                formData.append('old_password', this.form.old_password);
                formData.append('new_password1', this.form.new_password1);
                formData.append('new_password2', this.form.new_password2);

                axios
                    .post('/api/editpassword', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast('5000', 'Your password has been changed!', 'bg-emerald-500')

                            this.$router.push(`/profile/${this.userStore.user.id}`)
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data) {
                                this.errors.push(data[key][0].message)
                            }
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
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

    <body class>
        <div class="lg:flex">
            <div class="font-m-plus-rounded-1c lg:w-1/2 h-[740px] rounded-l-xl bg-white xl:max-w-screen-sm">
                <div class="mt-10 px-12 sm:px-24 md:px-48 lg:px-12 lg:mt-16 xl:px-24 xl:max-w-2xl">
                    <h2 class="text-center text-4xl text-emerald-500 font-display font-semibold lg:text-left xl:text-5xl
                    xl:text-bold">
                        Edit Profile
                    </h2>

                    <div class="mt-12">
                        <form v-on:submit.prevent="submitForm">
                            <div>
                                <div class="text-sm font-bold text-gray-700 tracking-wide">
                                    Old password:
                                </div>
                                <input v-model="form.old_password"
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="password" placeholder="Old Password">
                            </div>

                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        New password:
                                    </div>
                                </div>
                                <input v-model="form.new_password1"
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="password" placeholder="New Password">
                            </div>

                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        Repeat password:
                                    </div>
                                </div>
                                <input v-model="form.new_password2"
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="password" placeholder="Repeat Password">
                            </div>

                            <template v-if="errors.length > 0">
                                <div class="mt-6 bg-red-300 text-white rounded-lg p-6">
                                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                                </div>
                            </template>

                            <div class="mt-10">
                                <button class="bg-emerald-500 text-gray-100 p-4 w-full rounded-full tracking-wide
                                font-semibold font-display focus:outline-none focus:shadow-outline hover:bg-emerald-600
                                shadow-lg">
                                    Save Changes
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <div class="rounded-r-xl hidden lg:flex bg-purple-100 items-center justify-center flex-1 ">
                <div class="">
                    <div>
                        <img src="/hw_logo_trans.png" alt="Logo" class="rounded-r-xl h-[740px]">
                    </div>
                </div>
            </div>
        </div>


    </body>
</template>
