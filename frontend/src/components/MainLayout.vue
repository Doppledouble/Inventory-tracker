<script setup>
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const itemsMenuOpen = ref(false);

watch(
  () => route.path,
  (newPath) => {
    if (newPath.startsWith("/items")) {
      itemsMenuOpen.value = true;
    }
  },
  { immediate: true }
);

const toggleItemsMenu = () => {
  itemsMenuOpen.value = !itemsMenuOpen.value;
};
</script>

<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-mark">RAT</div>
        <div>
          <h3>Ryadi Artha Tjipta</h3>
          <p>Inventory Tracker</p>
        </div>
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/employees">Employees</RouterLink>
        
        <button
          class="nav-parent"
          :class="{ active: route.path.startsWith('/items') }"
          @click="toggleItemsMenu"
        >
          <span>Items</span>
          <i :class="['ti', itemsMenuOpen ? 'ti-chevron-up' : 'ti-chevron-down']" />
        </button>

          <transition name="dropdown">
            <div v-if="itemsMenuOpen" class="nav-submenu">
              <RouterLink
                to="/items/material"
                :class="{ active: route.path === '/items/material' }"
              >
                Materials
              </RouterLink>

              <RouterLink
                to="/items/tool"
                :class="{ active: route.path === '/items/tool' }"
              >
                Tools
              </RouterLink>
            </div>
          </transition>
        
        <RouterLink to="/assignments">Assignments</RouterLink>
        <RouterLink to="/transactions">History</RouterLink>
      </nav>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.nav-parent {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  font: inherit;
  color: inherit;
  padding: 12px 16px;
  border-radius: 8px;
  text-align: left;
}

.nav-parent:hover,
.nav-parent.active {
  background: white;
}

.nav-parent i {
  font-size: 14px;
}

.nav-submenu {
  display: flex;
  flex-direction: column;
  padding-left: 16px;
  margin-bottom: 4px;
}

.nav-submenu a {
  padding: 10px 16px;
  font-size: 13px;
  opacity: 0.85;
}

.nav-submenu a.active {
  background: var(--accent);
  color: var(--text);
  font-weight: 700;
}

.app-layout {
  min-height: 100vh;
  display: flex;
  background: var(--bg);
}

.sidebar {
  width: 260px;
  flex-shrink: 0;

  background: var(--surface);
  border-right: 1px solid var(--border);

  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;

  padding: 24px;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;

  margin-bottom: 40px;
}

.logo-mark {
  width: 46px;
  height: 42px;

  border-radius: 12px;

  background: var(--accent);

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: 800;
}

.sidebar-logo h3 {
  font-size: 16px;
  margin: 0;
}

.sidebar-logo p {
  margin: 0;
  color: var(--text-muted);
  font-size: 13px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-nav a {
  padding: 12px 16px;

  border-radius: 10px;

  color: var(--text-muted);

  font-weight: 500;

  transition: all .2s ease;
}

.sidebar-nav a:hover {
  background: white;
  color: var(--text);
}

.sidebar-nav a.router-link-active {
  background: var(--accent);
  color: var(--text);
  font-weight: 700;
}

.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 40px;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.25s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>