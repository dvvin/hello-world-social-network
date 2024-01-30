<script lang="ts">
import axios from 'axios'
import { useUserStore } from '@/stores/user';

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: [] as string[],
        }
    },

    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('http://127.0.0.1:8000/api/login', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)

                        console.log(response.data.access)

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log('error', error)
                    })

                await axios
                    .get('http://127.0.0.1:8000/api/me')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)

                        this.$router.push('/feed')
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
                <div class="pt-20 px-12 sm:px-24 md:px-48 lg:px-12 lg:mt-16 xl:px-24 xl:max-w-2xl">
                    <h2 class="text-center text-4xl text-emerald-500 font-display font-semibold lg:text-left xl:text-5xl
                    xl:text-bold">
                        helloYou!
                    </h2>

                    <div class="mt-12">
                        <form v-on:submit.prevent="submitForm">
                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        Email
                                    </div>
                                </div>
                                <input v-model="form.email"
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="" placeholder="Username/Email">
                            </div>
                            
                            <div class="mt-8">
                                <div class="flex justify-between items-center">
                                    <div class="text-sm font-bold text-gray-700 tracking-wide">
                                        Password
                                    </div>
                                </div>
                                <input v-model="form.password"
                                    class="w-full text-lg py-2 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
                                    type="password" placeholder="Password">
                            </div>

                            <template>
                                <div v-if="errors">
                                    <div class="bg-red-300 text-white rounded-lg p-6">
                                        <p v-for="error in errors" v-bind:key="error">
                                            {{ error }}
                                        </p>
                                    </div>
                                </div>
                            </template>

                            <div class="mt-10">
                                <button class="bg-emerald-500 text-gray-100 p-4 w-full rounded-full tracking-wide
                                font-semibold font-display focus:outline-none focus:shadow-outline hover:bg-emerald-600
                                shadow-lg">
                                    Login
                                </button>
                            </div>
                        </form>
                        <div class="mt-12 text-sm font-display font-semibold text-gray-700 text-center">
                            Don't have an account?
                            <RouterLink :to="{ name: 'signup' }"
                                class="cursor-pointer text-emerald-600 hover:text-emerald-800">
                                Join Today!
                            </RouterLink>
                        </div>
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
