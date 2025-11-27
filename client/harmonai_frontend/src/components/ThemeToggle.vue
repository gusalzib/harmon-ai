<template>
  <button @click="toggleTheme" class="theme-toggle">
    {{ isDark ? '☀️ ' + $t('nav.lighttheme') :  '🌙' + $t('nav.darktheme')  }}
  </button>
</template>

<script>
export default {
  name: 'ThemeToggle',
  data() {
    return {
      isDark: false
    }
  },
  mounted() {
    const saved = localStorage.getItem('theme')
    this.isDark = saved === 'dark'
    document.documentElement.classList.toggle('dark-theme', this.isDark)
  },
  methods: {
    toggleTheme() {
      this.isDark = !this.isDark
      const html = document.documentElement
      html.classList.toggle('dark-theme', this.isDark)
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light')

      // emit a global event so charts can react to theme switches. Without it, chart labels will not switch color and there will be inconsistencies
      // window.dispatchEvent(new Event('theme-changed'))
    }
  }
}
</script>

<style src="src\assets\main.css"></style>
