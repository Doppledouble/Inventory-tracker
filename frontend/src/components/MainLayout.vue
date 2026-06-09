<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-mark">
          RAT
        </div>

        <div>
          <h3>Ryadi Artha Tjipta</h3>
          <p>Inventory Tracker</p>
        </div>
      </div>

      <nav class="sidebar-nav">
        <RouterLink to="/employees">
          Employees
        </RouterLink>

        <RouterLink to="/locations">
          Locations
        </RouterLink>

        <RouterLink to="/items">
          Assets
        </RouterLink>

        <RouterLink to="/assignments">
          Assignments
        </RouterLink>
      </nav>
    </aside>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
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
</style>