<script setup>
import { ref } from "vue";
import { createAssignment } from "../../services/assignmentService.js";
import { useRouter } from "vue-router";
import AssignmentForm from "../../components/AssignmentForm.vue";

const router = useRouter();

const loading = ref(false);

const handleSubmit = async (assignmentData) => {
  try {
    loading.value = true;

    await createAssignment(assignmentData);

    router.push("/assignments");
  } catch (error) {
    console.error(error);
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  router.push("/assignments");
};
</script>

<template>
  <section class="container create-page">
    <div class="section-header">
      <div class="section-tag">
        Employee Management
      </div>

      <h1 class="section-title">
        Assign Barang
      </h1>
    </div>

    <AssignmentForm
      :loading="loading"
      submit-label="Assign Barang"
      @submit="handleSubmit"
      @cancel="handleCancel"
    />
  </section>
</template>
