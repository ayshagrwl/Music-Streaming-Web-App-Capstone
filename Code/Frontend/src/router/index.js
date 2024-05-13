import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import AdminLogin from '../views/AdminLogin.vue'
import Dashboard from '../views/dashboard.vue'
import Album_add from '../views/Album_add.vue'
import Song_add from '../views/Song_add.vue'
import Song_action from '../views/Song_action.vue'
import Edit_album from '../views/Edit_album.vue'
import store from '../store/index.js'
import ViewLyrics from '../views/ViewLyrics.vue';
import Playlists from '../views/Playlists.vue';
import PlaylistSong from '../views/PlaylistSong.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminLogin
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/add-album',
      name: 'Album_add',
      component: Album_add,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/add_song/:id',
      name: 'Song_add',
      component: Song_add,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/song_action/:id',
      name: 'Song_action',
      component: Song_action,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/edit_album/:id',
      name: 'Edit_album',
      component: Edit_album,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path: '/lyrics/:id',
      name: 'ViewLyrics',
      component: ViewLyrics,
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/playlists/:songId',
      name: 'playlists',
      component: Playlists,
      props:true,
      meta: {
        requiresAuth: true,
      }
    },
    {
      path: '/playlist_songs/:playlistId',
      name: 'PlaylistSong',
      component: PlaylistSong,
      props:true,
      meta: {
        requiresAuth: true,
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.token) {
    // Redirect to login page if the route requires authentication but the token is missing
    next('/login');
  } else if (from.name === 'dashboard' && (to.name === 'login' || to.name === 'signup')) {
    // Auto logout when clicking on the backward button from the dashboard to login or signup
    store.dispatch('logout').then(() => {
      next(); 
    }).catch((error) => {
      // Handle any errors that occurred during the logout process
      console.error('Logout failed:', error);
      next(); 
    });
  } else {
    next();
  }
});


export default router
