import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore({
    id: "user",

    state: () => ({
        user: {
            isAuthenticated: false,
            id: null as string | null,
            name: null as string | null,
            email: null as string | null,
            access: null as string | null,
            refresh: null as string | null,
            avatar: null as string | null,
        },
    }),

    actions: {
        initStore() {
            if (localStorage.getItem('user.access')) {
                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.email = localStorage.getItem('user.email')
                this.user.avatar = localStorage.getItem('user.avatar')
                this.user.isAuthenticated = true

                this.refreshToken()
            }
        },

        setToken(data: any) {
            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)
        },

        removeToken() {
            this.user.refresh = null
            this.user.access = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.name = null
            this.user.email = null
            this.user.avatar = null

            localStorage.setItem('user.access', '')
            localStorage.setItem('user.refresh', '')
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.name', '')
            localStorage.setItem('user.email', '')
            localStorage.setItem('user.avatar', '')
        },

        setUserInfo(user: any) {
            this.user.id = user.id
            this.user.name = user.name
            this.user.email = user.email
            this.user.avatar = user.avatar

            if (this.user.id !== null) {
                localStorage.setItem('user.id', this.user.id)
            }

            if (this.user.name !== null) {
                localStorage.setItem('user.name', this.user.name)
            }

            if (this.user.email !== null) {
                localStorage.setItem('user.email', this.user.email)
            }

            if (this.user.avatar !== null) {
                localStorage.setItem('user.avatar', this.user.avatar)
            }
        },

        refreshToken() {
            axios.post('http://127.0.0.1:8000/api/refresh', {
                refresh: this.user.refresh
            })
                .then((response) => {
                    this.user.access = response.data.access

                    localStorage.setItem('user.access', response.data.access)

                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                })
                .catch((error) => {
                    this.removeToken()
                })
        },
    },
})
