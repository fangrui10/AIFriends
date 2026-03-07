<script setup>
import streamApi from '@/js/http/streamApi';
import MicIcon from '../../icons/MicIcon.vue';
import SendIcon from '../../icons/SendIcon.vue';
import { ref, useTemplateRef } from 'vue';

const props = defineProps(['friendId'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')
let isProcessing = false

function focus() {
    inputRef.value.focus()
}


async function handleSend() {
    if (isProcessing) return
    isProcessing = true
    const content = message.value.trim()
    if (!content) return

    message.value = ''

    try {
        await streamApi('/api/friend/message/chat/', {
            body: {
                friend_id: props.friendId,
                message: content,
            },
            onmessage(data, isDone) {
                if (isDone) {
                    isProcessing = false
                } else if (data.content) {
                    console.log(data.content)
                }
            },
            onerror(err) {
                console.error(err)
                isProcessing = false
            },

        })
    } catch (err) {
        console.error(err)
        isProcessing = false
    }

}

defineExpose({
    focus,
})
</script>

<template>
    <form @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
        <input v-model="message" ref="input-ref"
            class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20" type="text"
            placeholder="文本输入。。。">
        <div class="absolute right-2 w-8 h-8 flex items-center justify-center cursor-pointer">
            <SendIcon @click="handleSend" />
        </div>
        <div class="absolute right-10 w-8 h-8 flex items-center justify-center cursor-pointer">
            <MicIcon />
        </div>
    </form>
</template>

<style scoped></style>