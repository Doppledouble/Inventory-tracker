<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({
      city: "",
      location_name: "",
      description: "",
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

const emit = defineEmits([
  "submit",
  "cancel"
]);

const form = ref({
  city: "",
  location_name: "",
  description: "",
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
  { ...form.value, });
};
</script>

<template>
  <div class="card location-form-card">
    <form @submit.prevent="submitForm">

      <div class="form-group">
        <label>Kota</label>

        <input
          v-model="form.city"
          type="text"
          required
        />
      </div>

      <div class="form-group">
        <label>Nama Lokasi</label>

        <input
          v-model="form.location_name"
          type="text"
          required
        />
      </div>

      <div class="form-group">
        <label>Deskripsi</label>

        <input
          v-model="form.description"
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
.location-form-card {
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

.form-group input {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: 10px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}
</style>