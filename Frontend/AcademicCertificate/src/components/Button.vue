<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <div class="button">
        <RouterLink to="/cadastro">Começar agora</RouterLink>
    </div>

</template>

<style>
    .button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 50px;
        width: 200px; 
        background-color: #96FF7C;
        border-radius: 30px;
        cursor: pointer;
    }

    .button a {
        text-decoration: none;
        color: black;
    }


</style>