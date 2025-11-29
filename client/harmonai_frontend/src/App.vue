<template>
  <div class="nav-bar">
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
        <div class="nav-links">
          <RouterLink to="/">{{ $t('nav.home') }}</RouterLink>
          <RouterLink to="/profile">{{ $t('nav.profile') }}</RouterLink>
          <RouterLink to="/about">{{ $t('nav.about') }}</RouterLink>
          <RouterLink to="/login">{{ $t('nav.login') }}</RouterLink>
          <RouterLink to="/logout">{{ $t('nav.logout') }}</RouterLink>
          <RouterLink to="/signup">{{ $t('nav.signup') }}</RouterLink>
          <ThemeToggle />
        </div>
        <LanguageSwitcher />
    </header>
  </div>


  <RouterView />
</template>
<script setup>
import { RouterLink, RouterView } from 'vue-router'
import ThemeToggle from '@/components/ThemeToggle.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue';
</script>
<style src="src\assets\main.css"></style>
