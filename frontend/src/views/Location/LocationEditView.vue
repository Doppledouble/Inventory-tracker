<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

import LocationForm from "../../components/LocationForm.vue";
import { getLocationById,updateLocation } from "../../services/locationService.js";

const route = useRoute();
const router = useRouter();

const locationId = route.params.id;

console.log("locationId:", locationId);

const loading = ref(false);

const location = ref({
  city: "",
  location_name: "",
  description: "",
});

onMounted(async () => {
  try {
    const response = await getLocationById(locationId);

    location.value = response.data;
  } catch (error) {
    console.error(error);
  }
});

const handleSubmit = async (locationData) => {
  try {
    loading.value = true;

    await updateLocation(locationId, locationData);

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
        Update Lokasi
      </h1>
    </div>

    <LocationForm
      :initial-data="location"
      :loading="loading"
      submit-label="Update Lokasi"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </section>
</template>
