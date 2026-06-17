<script setup>
import { ref, watch, onMounted, computed } from "vue";
import api from "../services/api.js";
import Multiselect from "vue-multiselect"
import "vue-multiselect/dist/vue-multiselect.css"

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      item_id:"",
      employee_id: "",
      location_id: "",
      quantity: 0,
    }),
  },

  submitLabel: {
    type: String,
    default: "Simpan",
  },

  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["submit", "cancel"]);

const items = ref([])
const employees = ref([])
const locations = ref([])

onMounted(async () => {
  try {
    const requests = [
      api.get("/employees"),
      api.get("/locations"),
    ]

    // Only fetch all items if not pre-filled
    if (!props.initialData?.item_id) {
      requests.unshift(api.get("/items"))
    } else {
      // Just fetch the one item we need for display
      requests.unshift(api.get(`/items/${props.initialData.item_id}`))
    }

    const [itemsRes, employeesRes, locationsRes] = await Promise.all(requests)

    // If locked, wrap single item in array so the watch still works
    items.value = props.initialData?.item_id 
      ? [itemsRes.data]   // single item → array of one
      : itemsRes.data     // full list

    employees.value = employeesRes.data
    locations.value = locationsRes.data
  } catch (error) {
    console.error("Failed to load assignment data", error)
  }
})

const form = ref({
  item_id: null,
  employee_id: null,
  location_id: null,
  quantity: 1,
  notes: "",
});

// Selected option objects for the multiselects (vue-multiselect needs objects)
const selectedItem = ref(null)
const selectedEmployee = ref(null)
const selectedLocation = ref(null)

watch(
  () => props.initialData,
  (value) => {
    form.value = { ...value };
  },
  { immediate: true }
);

// When items load OR form.item_id changes, sync the selected object
watch([items, () => form.value.item_id], ([itemList, itemId]) => {
  selectedItem.value = itemList.find(i => i.id === itemId) || null
})

watch([employees, () => form.value.employee_id], ([empList, empId]) => {
  selectedEmployee.value = empList.find(e => e.id === empId) || null
})

watch([locations, () => form.value.location_id], ([locList, locId]) => {
  selectedLocation.value = locList.find(l => l.id === locId) || null
})

// When user picks a new option, update form's *_id with the id
const onItemSelect = (option) => {
  form.value.item_id = option ? option.id : null
}

const onEmployeeSelect = (option) => {
  form.value.employee_id = option ? option.id : null
}

const onLocationSelect = (option) => {
  form.value.location_id = option ? option.id : null
}

const isItemLocked = computed(() => !!props.initialData?.item_id)

// Custom label combining first + last name
const employeeLabel = (employee) => `${employee.first_name} ${employee.last_name}`

const submitForm = () => {
  emit("submit", { ...form.value });
};
</script>

<template>
  <div class="card item-form-card">
    <form @submit.prevent="submitForm">

      <div class="form-group">
        <label>Item</label>
        <Multiselect
          v-model="selectedItem"
          :options="items"
          label="name"
          track-by="id"
          placeholder="Pilih item"
          :disabled="isItemLocked"      
          @update:model-value="onItemSelect"
        />
        <small v-if="isItemLocked" style="color: var(--text-muted)">
          
        </small>
      </div>

      <div class="form-group">
        <label>Karyawan</label>
        <Multiselect
          v-model="selectedEmployee"
          :options="employees"
          :custom-label="employeeLabel"
          track-by="id"
          placeholder="Pilih karyawan"
          @update:model-value="onEmployeeSelect"
        />
      </div>

      <div class="form-group">
        <label>Lokasi</label>
        <Multiselect
          v-model="selectedLocation"
          :options="locations"
          label="location_name"
          track-by="id"
          placeholder="Pilih lokasi"
          @update:model-value="onLocationSelect"
        />
      </div>

      <div class="form-group">
        <label>Quantity</label>
        <input
          v-model.number="form.quantity"
          type="number"
          min="1"
          required
        />
      </div>

      <div class="form-group">
        <label>Deskripsi</label>

        <input
          v-model="form.notes"
          type="text"
        />
      </div>

      <div class="form-actions">
        <button type="button" class="btn-ghost" @click="$emit('cancel')">
          Batal
        </button>

        <button type="submit" class="btn-acid" :disabled="loading">
          {{ loading ? "Menyimpan..." : submitLabel }}
        </button>
      </div>

    </form>
  </div>
</template>

<style scoped>
.item-form-card {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 600;
}

.form-group input,
.form-group select {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
}

.form-checkbox {
  display: flex;
  gap: 10px;
  align-items: center;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}
</style>