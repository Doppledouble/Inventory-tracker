<script setup>
import { ref, onMounted } from "vue";
import { getEmployees,deleteEmployee } from "../../services/employeeService.js";
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
  <section class="container employee-page">
    <!-- HEADER -->
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Daftar Karyawan
      </h1>
    </div>
    
    <!-- SECTION 1 : DASHBOARD -->
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
          <div class="dash-cell">Nama Depan</div>
          <div class="dash-cell">Nama Belakang</div>
          <div class="dash-cell">E-mail</div>
          <div class="dash-cell">Aksi</div>
        </div>

        <div
          v-for="employee in employees"
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

<style>
.employee-page {
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