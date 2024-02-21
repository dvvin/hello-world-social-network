import { createRouter, createWebHistory } from 'vue-router'
import FeedView from '../views/FeedView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import LikesView from '../views/LikesView.vue'
import PostView from '@/views/PostView.vue'
import ChatView from '@/views/ChatView.vue'
import TrendView from '@/views/TrendView.vue'
import EditProfileView from '@/views/EditProfileView.vue'
import EditPasswordView from '@/views/EditPasswordView.vue'
import NotificationsView from '@/views/NotificationsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: FeedView
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView
    },
    {
      path: '/profile/:id/likes',
      name: 'likes',
      component: LikesView
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/trends/:id',
      name: 'trendview',
      component: TrendView
    },
    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView
    },
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    }
  ]
})

export default router
