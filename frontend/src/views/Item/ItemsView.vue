<script setup>
import { ref, onMounted } from "vue";
import { getItems,deleteItem } from "../../services/itemService.js";
import { createAssignment } from "../../services/assignmentService.js"
import { useTableControls } from "../../composables/useTableControls.js";
import { useRouter } from "vue-router";

const router = useRouter();
const items = ref([]);

const addItem = () => {
  router.push("/items/create");
};

const editItem = (id) => {
  router.push(`/items/${id}/edit`);
};

const assignItem = (itemId) => {
  router.push({ 
    name: 'assignment-create', 
    query: { item_id: itemId }  
  })
}

const prefetchItemCreate = () => {
  import("./ItemCreateView.vue");
};

const { filters, result, toggleSort, getSortIcon } = useTableControls(
  items, 
  [ 
    { key: "name", type: "text", resolve: (t) => t.name },
    { key: "category", type: "text", resolve: (t) => t.category },
    { key: "count", type: "number", resolve: (t) => t.count },
    { key: "unit", type: "text", resolve: (t) => t.unit },
  ],
  "created_at" // default sort key
);

const loadItems = async () => {
  try {
    const response = await getItems();
    items.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(loadItems);

const deleteItemHandler = async (id) => {
  const confirmed = confirm(
    "Yakin ingin menghapus barang ini?"
  );

  if (!confirmed) return;

  try {
    await deleteItem(id);

    // Refresh data
    await loadItems();
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <section class="item-page">
    <!-- HEADER -->
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Daftar Barang
      </h1>
    </div>
    
    <!-- SECTION 1 : DASHBOARD -->
    <div class="card dashboard-table-area">
      <div class="dash-table-header">
        <span>Total Barang: {{ items.length }}</span>

        <button
          class="btn-acid"
          @pointerenter="prefetchItemCreate"
          @click="addItem"
        >
          + Tambah Barang
        </button>
      </div>
      
      <div class="dash-table">
        <div class="dash-table-row head">
          <div class="dash-cell sortable" @click="toggleSort('name')">
            Nama <i :class="['ti', getSortIcon('name')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('category')">
            Kategory <i :class="['ti', getSortIcon('category')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('count')">
            Jumlah <i :class="['ti', getSortIcon('count')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('unit')">
            Unit <i :class="['ti', getSortIcon('unit')]" aria-hidden="true" />
          </div>
          <div class="dash-cell">Aksi</div>
        </div>

        <!-- FILTER ROW -->
        <div class="dash-table-row filter-row">
          <div class="dash-cell">
            <input v-model="filters.name" placeholder="Cari barang..." />
          </div>
          <div class="dash-cell">
            <input v-model="filters.category" placeholder="Cari kategori..." />
          </div>
          <div class="dash-cell">
            <input v-model="filters.count" placeholder="Cari jumlah..." type="number"/>
          </div>
          <div class="dash-cell">
            <input v-model="filters.unit" placeholder="Cari satuan..."/>
          </div>          
        </div>

        <div
          v-for="item in result"
          :key="item.id"
          class="dash-table-row"
        >
          <div class="dash-cell dash-cell-name">
            <div class="dash-cell-icon">
              {{ item.name?.charAt(0) }}
            </div>
            {{ item.name }}
          </div>

          <div class="dash-cell">
            {{ item.category }}
          </div>

          <div class="dash-cell">
            {{ item.count }}
          </div>

          <div class="dash-cell">
            {{ item.unit }}
          </div>

          <div class="dash-cell action-buttons">
            <button
              class="btn-acid btn-small"
              @click="assignItem(item.id)"
            >
              Assign
            </button>
            
            <button
              class="btn-ghost btn-small"
              @click="editItem(item.id)"
            >
              Edit
            </button>
            
            <button
              class="btn-danger btn-small"
              @click="deleteItemHandler(item.id)"
            >
              Hapus
            </button>
          </div>
        </div>

        <div
          v-if="items.length === 0"
          class="empty-state"
        >
          Belum ada data barang.
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.item-page {
  padding-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-small {
  padding: 8px 14px;
  font-size: 12px;
}

.btn-danger {
  padding: 8px 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  background: #ef4444;
  color: white;
  transition: transform 0.2s ease;
}

.btn-danger:hover {
  transform: translateY(-2px);
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.dash-cell-icon {
  background: var(--accent);
  color: var(--text);
  font-weight: 700;
}

.dash-table-row {
    display: grid;
    grid-template-columns:
        1fr
        1fr
        1fr
        1fr
        1fr;
    gap: 16px;
    padding: 12px 20px;
    align-items: center;
    border-bottom: 1px solid var(--border-light);
    font-size: 13px;
}

.dash-table-row .dash-cell:not(:first-child) {
  text-align: center;
  justify-content: center;
  display: flex;
  align-items: center;
}
</style>