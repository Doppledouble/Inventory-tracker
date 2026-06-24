<script setup>
import { ref, watch, onMounted } from "vue";
import api from "../services/api.js";
import Multiselect from "vue-multiselect"
import "vue-multiselect/dist/vue-multiselect.css"

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      name: "",
      category: "",
      type: "",
      count: 1,
      unit: "",
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
    
const locations = ref([])

const emit = defineEmits([
  "submit",
  "cancel"
]);

const form = ref({
    name: "",
    category: "",
    type: "",
    count: 1,
    unit: "",
});

watch(
  () => props.initialData,
  (value) => {
    form.value = { ...value };
  },
  { immediate: true }
);

const submitForm = () => {
  emit("submit", 
  { ...form.value });
};
</script>

<template>
  <div class="card item-form-card">
    <form @submit.prevent="submitForm">

      <div class="form-group">
        <label>Nama Barang</label>

        <input
          v-model="form.name"
          type="text"
          required
        />
      </div>

      <div class="form-group">
        <label>Kategori</label>

        <input
          v-model="form.category"
          type="text"
        />
      </div>

      <div class="form-group">
        <label>Tipe Barang</label>
        <select v-model="form.type">
          <option value="" disabled>Pilih tipe barang</option>
          <option value="material">Material</option>
          <option value="tool">Tool</option>
        </select>
      </div>      

      <div class="form-group">
        <label>Jumlah</label>

        <input
          v-model.number="form.count"
          type="number"
        />
      </div>

      <div class="form-group">
        <label>Unit/Satuan</label>

        <input
          v-model.number="form.unit"
          type="text"
        />
      </div>

      <div class="form-actions">

        <button
          type="button"
          class="btn-ghost"
          @click="$emit('cancel')"
        >
          Batal
        </button>

        <button
          type="submit"
          class="btn-acid"
          :disabled="loading"
        >
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