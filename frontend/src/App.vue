<script setup>
import { onMounted } from 'vue';
import NavBar from './components/navbar/NavBar.vue';
import { useUserStore } from './stores/user';
import api from '@/js/http/api';
import { useRoute, useRouter } from 'vue-router';
const user = useUserStore();
const route = useRoute();
const router = useRouter();
onMounted(async () => {
    try {
        const res = await api.get('/api/user/account/get_user_info/');
        const data = res.data;
        if (data.result === 'success') {
            user.setUserInfo(data);
            user.setHasPulledUserInfo(true);
        }
    } catch (error) {
        
    } finally {
        user.setHasPulledUserInfo(true)

        if (route.meta.needLogin && !user.isLogin()){
            // replace 相比于push不能后退，更加安全
            await router.replace({ 
                name: "user-account-login-index"
            })
        }
    }
});
</script>

<template>
    <NavBar>
        <RouterView />
    </NavBar>
</template>

<style scoped>

</style>
