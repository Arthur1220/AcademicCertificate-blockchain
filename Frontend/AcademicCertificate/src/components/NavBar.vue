<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
    <div class="header">
        <nav class="navbar">
            <div class="nav-links">
                <RouterLink to="/">Home</RouterLink>
                <RouterLink to="/cadastro">Cadastro</RouterLink>
                <RouterLink to="/login">Login</RouterLink>
            </div>
        </nav>
    </div>
</template>

<style scoped>  

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif ;
}

html {
    display: flex;
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
}

/* Estilo da barra de navegação */
.header {
    display: flex;
    justify-content: center;
    position: fixed; /* Fixa no topo da página */
    top: 0;         /* Posiciona no topo */
    left: 0;        /* Alinha à esquerda */
    height: 50px;   /* Altura da navbar */
    width: 100%;    /* Largura total da tela */
    z-index: 1000;  /* Garante que fique acima de outros elementos */
}

.navbar {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #333;
    color: white;
    padding: 10px 20px;
    width: 100%;    /* Largura da navbar ajustada para 100% */
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 15px;
}

.nav-links a{
    color: white;
    text-decoration: none;
    padding: 8px 15px;
    transition: background-color 0.3s ease;
}

.nav-links a:hover {
    background-color: #555;
    border-radius: 5px;
}

</style>
