<script setup>
import { ref } from "vue";
import { createLocation } from "../../services/locationService.js";
import { useRouter } from "vue-router";
import LocationForm from "../../components/LocationForm.vue";

const router = useRouter();

const loading = ref(false);

const handleSubmit = async (locationData) => {
  try {
    loading.value = true;

    await createLocation(locationData);

    router.push("/locations");
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  router.push("/locations");
};
</script>

<template>
  <section class="container create-page">
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Tambah Lokasi
      </h1>
    </div>

    <LocationForm
      :loading="loading"
      submit-label="Tambah Lokasi"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </section>
</template>
