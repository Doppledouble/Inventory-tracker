<script setup>
import { ref, onMounted } from "vue";
import { getActiveAssignments,returnAssignment } from "../../services/assignmentService.js";
import { useRouter } from "vue-router";

const router = useRouter();
const assignments = ref([]);

const addAssignment = () =>{
  router.push("/assignments/create");
}

const editAssignment = (id) => {
  router.push(`/assignments/${id}/edit`);
};

const loadAssignments = async () => {
  try {
    const response = await getActiveAssignments();
    assignments.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(loadAssignments);

const returnAssignmentHandler = async (id) => {
  const confirmed = confirm("Yakin ingin mengembalikan barang ini?");

  if (!confirmed) return;

  try {
    await returnAssignment(id);

    // Refresh data
    await loadAssignments();
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <section class="assignment-page">
    <!-- HEADER -->
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Daftar Pemakaian
      </h1>
    </div>
    
    <!-- SECTION 1 : DASHBOARD -->
    <div class="card dashboard-table-area">
      <div class="dash-table-header">
        <span>Total Barang: {{ assignments.length }}</span>

        <button
          class="btn-acid"
          @click="addAssignment"
        >
          + Tambah Pemakaian
        </button>
      </div>
      
      <div class="dash-table">
        <div class="dash-table-row head">
          <div class="dash-cell">Nama Barang</div>
          <div class="dash-cell">Nama PIC</div>
          <div class="dash-cell">Jumlah</div>
          <div class="dash-cell">Lokasi</div>
          <div class="dash-cell">Tanggal Dipakai</div>
          <div class="dash-cell">Aksi</div>
        </div>

        <div
          v-for="assignment in assignments"
          :key="assignment.id"
          class="dash-table-row"
        >
          <div class="dash-cell dash-cell-name">
            <div class="dash-cell-icon">
              {{ assignment.item?.name?.charAt(0) }}
            </div>
            {{ assignment.item?.name }}
          </div>

          <div class="dash-cell">
            {{ assignment.employee?.first_name }} {{ assignment.employee?.last_name }}
          </div>

          <div class="dash-cell">
            {{ assignment.quantity }}
          </div>

          <div class="dash-cell">
            {{ assignment.location?.location_name }}
          </div>

          <div class="dash-cell">
            {{ new Date(assignment.assigned_at).toLocaleDateString() }}
          </div>

          <div class="dash-cell action-buttons">
            <button
              class="btn-ghost btn-small"
              @click="editAssignment(assignment.id)"
            >
              Edit
            </button>

            <button
              class="btn-danger btn-small"
              @click="returnAssignmentHandler(assignment.id)"
            >
              Kembalikan
            </button>
          </div>
        </div>

        <div
          v-if="assignments.length === 0"
          class="empty-state"
        >
          Belum ada data barang.
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.assignment-page {
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
  grid-template-columns: 1fr 0.5fr 0.5fr 0.5fr 1fr 0.5fr;
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