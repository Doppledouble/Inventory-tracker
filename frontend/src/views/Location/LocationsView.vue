<script setup>
import { ref, onMounted } from "vue";
import { getLocations,deleteLocation } from "../../services/locationService.js";
import { useRouter } from "vue-router";

const router = useRouter();
const locations = ref([]);

const addLocation = () => {
  router.push("/locations/create");
};

const editLocation = (id) => {
  router.push(`/locations/${id}/edit`);
};

const prefetchLocationCreate = () => {
  import("./LocationCreateView.vue");
};

const loadLocations = async () => {
  try {
    const response = await getLocations();
    locations.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(loadLocations);

const deleteLocationHandler = async (id) => {
  const confirmed = confirm(
    "Yakin ingin menghapus lokasi ini?"
  );

  if (!confirmed) return;

  try {
    await deleteLocation(id);

    // Refresh data
    await loadLocations();
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <section class="container location-page">
    <!-- HEADER -->
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Daftar Lokasi
      </h1>
    </div>
    
    <!-- SECTION 1 : DASHBOARD -->
    <div class="card dashboard-table-area">
      <div class="dash-table-header">
        <span>Total Lokasi: {{ locations.length }}</span>

        <button
          class="btn-acid"
          @pointerenter="prefetchLocationCreate"
          @click="addLocation"
        >
          + Tambah Lokasi
        </button>
      </div>
      
      <div class="dash-table">
        <div class="dash-table-row head">
          <div class="dash-cell">Nama Lokasi</div>
          <div class="dash-cell">Kota</div>
          <div class="dash-cell">Deskripsi</div>
          <div class="dash-cell">Aksi</div>
        </div>

        <div
          v-for="location in locations"
          :key="location.id"
          class="dash-table-row"
        >
          <div class="dash-cell dash-cell-name">
            <div class="dash-cell-icon">
              {{ location.location_name?.charAt(0) }}
            </div>
            {{ location.location_name }}
          </div>

          <div class="dash-cell">
            {{ location.city }}
          </div>

          <div class="dash-cell">
            {{ location.description }}
          </div>

          <div class="dash-cell action-buttons">
            <button
              class="btn-ghost btn-small"
              @click="editLocation(location.id)"
            >
              Edit
            </button>

            <button
              class="btn-danger"
              @click="deleteLocationHandler(location.id)"
            >
              Hapus
            </button>
          </div>
        </div>

        <div
          v-if="locations.length === 0"
          class="empty-state"
        >
          Belum ada data lokasi.
        </div>
      </div>
    </div>
  </section>
</template>

<style>
.location-page {
  padding-top: 80px;
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

</style>