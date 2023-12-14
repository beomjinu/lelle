<template>
  <div class="flex flex-col h-screen pt-8 bg-dark text-white">
    <!-- title bar -->
    <div class="fixed top-0 w-full h-8" style="-webkit-app-region: drag;"></div>
    <!-- main content -->
    <div class="flex-1">
      <router-view/>
    </div>
  </div>
</template>