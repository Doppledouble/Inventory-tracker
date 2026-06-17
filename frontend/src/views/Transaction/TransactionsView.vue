<script setup>
import { ref, onMounted } from "vue";
import { getTransactions } from "../../services/transactionService.js";

const transactions = ref([]);


const loadTransactions = async () => {
  try {
    const response = await getTransactions();
    transactions.value = response.data;
  } catch (error) {
    console.error(error);
  }
};

onMounted(loadTransactions);
</script>

<template>
  <section class="transaction-page">
    <!-- HEADER -->
    <div class="section-header">
      <div class="section-tag">
        Inventory Management
      </div>

      <h1 class="section-title">
        Riwayat Transaksi
      </h1>
    </div>

    <!-- TABLE -->
    <div class="card dashboard-table-area">
      <div class="dash-table-header">
        <span>Total Transaksi: {{ transactions.length }}</span>
      </div>

      <div class="dash-table">
        <div class="dash-table-row head">
          <div class="dash-cell">Nama Barang</div>
          <div class="dash-cell">Aksi</div>
          <div class="dash-cell">Jumlah</div>
          <div class="dash-cell">Dilakukan Oleh</div>
          <div class="dash-cell">Catatan</div>
          <div class="dash-cell">Tanggal</div>
        </div>

        <div
          v-for="transaction in transactions"
          :key="transaction.id"
          class="dash-table-row"
        >
          <div class="dash-cell dash-cell-name">
            <div class="dash-cell-icon">
              {{ transaction.item?.name?.charAt(0) }}
            </div>
            {{ transaction.item?.name }}
          </div>

          <div class="dash-cell">
            <span :class="['type-badge', transaction.transaction_type]">
              {{ typeLabel[transaction.transaction_type] }}
            </span>
          </div>

          <div class="dash-cell" :class="quantityClass(transaction)">
            {{ transaction.quantity > 0 ? '+' : '' }}{{ transaction.quantity }}
          </div>

          <div class="dash-cell">
            {{ transaction.employee
              ? `${transaction.employee.first_name} ${transaction.employee.last_name}`
              : '—' 
            }}
          </div>

          <div class="dash-cell">
            {{ transaction.notes || '—' }}
          </div>

          <div class="dash-cell">
            {{ new Date(transaction.created_at).toLocaleDateString() }}
          </div>
        </div>

        <div v-if="transactions.length === 0" class="empty-state">
          Belum ada riwayat transaksi.
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// Label mapping for transaction types
const typeLabel = {
  purchase: 'Pembelian',
  damage: 'Kerusakan',
  adjustment: 'Penyesuaian',
  return: 'Pengembalian',
  assignment: 'Pemakaian',
}

// Color class based on quantity (positive = green, negative = red)
const quantityClass = (transaction) => {
  if (transaction.quantity > 0) return 'qty-positive'
  if (transaction.quantity < 0) return 'qty-negative'
  return ''
}
</script>

<style scoped>
.transaction-page {
  padding-top: 20px;
}

.dash-table-row {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr 0.5fr 1fr 1fr 0.8fr;
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

.dash-cell-icon {
  background: var(--accent);
  color: var(--text);
  font-weight: 700;
}

.empty-state {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

/* Transaction type badge */
.type-badge {
  align-items: center;
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
}

.type-badge.purchase {
  background: #E1F5EE;
  color: #0F6E56;
}

.type-badge.damage {
  background: #FEE2E2;
  color: #991B1B;
}

.type-badge.return {
  background: #f2ffee;
  color: #0da904;
}

.type-badge.assignment {
  background: #ffffee;
  color: #c35303;
}

.type-badge.adjustment {
  background: #EEF2FF;
  color: #3730A3;
}

/* Quantity colors */
.qty-positive {
  color: #0F6E56;
  font-weight: 600;
}

.qty-negative {
  color: #991B1B;
  font-weight: 600;
}
</style>