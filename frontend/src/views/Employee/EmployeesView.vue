<script setup>
import { ref, onMounted } from "vue";
import { getEmployees,deleteEmployee } from "../../services/employeeService.js";
import { useTableControls } from "../../composables/useTableControls.js";
import { useRouter } from "vue-router";

const router = useRouter();
const employees = ref([]);

const addEmployee = () => {
  router.push("/employees/create");
};

const editEmployee = (id) => {
  router.push(`/employees/${id}/edit`);
};

const prefetchEmployeeCreate = () => {
  import("./EmployeeCreateView.vue");
};

const { filters, result, toggleSort, getSortIcon } = useTableControls(
  employees, 
  [ 
    { key: "first_name", type: "text", resolve: (t) => t.first_name },
    { key: "last_name", type: "text", resolve: (t) => t.last_name },
    { key: "email", type: "text", resolve: (t) => t.email },
  ],
  "created_at" // default sort key
);

const loadEmployees = async () => {
  try {
    const response = await getEmployees();
    employees.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(loadEmployees);

const deleteEmployeeHandler = async (id) => {
  const confirmed = confirm(
    "Yakin ingin menghapus karyawan ini?"
  );

  if (!confirmed) return;

  try {
    await deleteEmployee(id);

    // Refresh data
    await loadEmployees();
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <section class=" employee-page">
    <!-- HEADER -->
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Daftar Karyawan
      </h1>
    </div>
    
    <!-- SECTION  DASHBOARD -->
    <div class="card dashboard-table-area">
      <div class="dash-table-header">
        <span>Total Karyawan: {{ employees.length }}</span>

        <button
          class="btn-acid"
          @pointerenter="prefetchEmployeeCreate"
          @click="addEmployee"
        >
          + Tambah Karyawan
        </button>
      </div>
      
      <div class="dash-table">
        <div class="dash-table-row head">
          <div class="dash-cell sortable" @click="toggleSort('first_name')">
            Nama Depan <i :class="['ti', getSortIcon('first_name')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('last_name')">
            Nama Belakang <i :class="['ti', getSortIcon('last_name')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('email')">
            E-Mail <i :class="['ti', getSortIcon('email')]" aria-hidden="true" />
          </div>
          <div class="dash-cell">Aksi</div>
        </div>

        <!-- FILTER ROW -->
        <div class="dash-table-row filter-row">
          <div class="dash-cell">
            <input v-model="filters.first_name" placeholder="Cari nama depan..." />
          </div>
          <div class="dash-cell">
            <input v-model="filters.last_name" placeholder="Cari nama belakang..." />
          </div>
          <div class="dash-cell">
            <input v-model="filters.email" placeholder="Cari email..." />
          </div>
        </div>


        <div
          v-for="employee in result"
          :key="employee.id"
          class="dash-table-row"
        >
          <div class="dash-cell dash-cell-name">
            <div class="dash-cell-icon">
              {{ employee.first_name?.charAt(0) }}
            </div>
            {{ employee.first_name }}
          </div>

          <div class="dash-cell">
            {{ employee.last_name }}
          </div>

          <div class="dash-cell">
            {{ employee.email }}
          </div>

          <div class="dash-cell action-buttons">
            <button
              class="btn-ghost btn-small"
              @click="editEmployee(employee.id)"
            >
              Edit
            </button>

            <button
              class="btn-danger"
              @click="deleteEmployeeHandler(employee.id)"
            >
              Hapus
            </button>
          </div>
        </div>

        <div
          v-if="employees.length === 0"
          class="empty-state"
        >
          Belum ada data karyawan.
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.employee-page {
  padding-top: 20px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.dash-table-row{
  gap: 16px;
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

.dash-table-row .dash-cell:not(:first-child) {
  text-align: center;
  justify-content: center;
  display: flex;
  align-items: center;
}
</style>