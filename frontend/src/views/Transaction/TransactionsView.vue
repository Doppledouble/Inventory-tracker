<script setup>
import { ref, onMounted, watch } from "vue";
import { getTransactions } from "../../services/transactionService.js";
import { useTableControls } from "../../composables/useTableControls.js";

const transactions = ref([]);

// for type of action in each transaction
const typeLabel = {
  add: "Penambahan",
  remove: "Pengurangan",
  adjustment: "Penyesuaian",
  return: "Pengembalian",
  assignment: "Pemakaian",
};

const quantityClass = (transaction) => {
  if (transaction.quantity > 0) return "qty-positive";
  if (transaction.quantity < 0) return "qty-negative";
  return "";
};

// This is for filtering and sorting
const { filters, result, toggleSort, getSortIcon } = useTableControls(
  // this is the whole transaction data
  transactions, 
  [ // Keys for sorting that are received from each table column header
    { key: "item", type: "text", resolve: (t) => t.item?.name },
    { key: "type", type: "text", resolve: (t) => t.transaction_type },
    { key: "quantity", type: "number", resolve: (t) => t.quantity },
    { key: "employee", type: "text", resolve: (t) => `${t.employee?.first_name ?? ""} ${t.employee?.last_name ?? ""}` },
    { key: "notes", type: "text", resolve: (t) => t.notes ?? "" },
    { key: "created_at", type: "date", resolve: (t) => new Date(t.created_at) },
  ],
  // Below means data will be sorted on "created_at" column by default
  "created_at"
);

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
      <div class="section-tag">Inventory Management</div>
      <h1 class="section-title">Riwayat Transaksi</h1>
    </div>

    <!-- TABLE -->
    <div class="card dashboard-table-area">
      <div class="dash-table-header">
        <span>Total Transaksi: {{ result.length }}</span>
      </div>

      <div class="dash-table">

        <!-- SORT HEADERS -->
        <div class="dash-table-row head">
          <div class="dash-cell sortable" @click="toggleSort('item')">
            <!-- getSortIcon() is used for showing arrows indicating if its sorted by ASC or DESC order-->
            
            Nama Barang <i :class="['ti', getSortIcon('item')]" aria-hidden="true" /> 
          </div>
          <div class="dash-cell sortable" @click="toggleSort('type')">
            Aksi <i :class="['ti', getSortIcon('type')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('quantity')">
            Jumlah <i :class="['ti', getSortIcon('quantity')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('employee')">
            Dilakukan Oleh <i :class="['ti', getSortIcon('employee')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('notes')">
            Catatan <i :class="['ti', getSortIcon('notes')]" aria-hidden="true" />
          </div>
          <div class="dash-cell sortable" @click="toggleSort('created_at')">
            Tanggal <i :class="['ti', getSortIcon('created_at')]" aria-hidden="true" />
          </div>
        </div>

        <!-- FILTER ROW -->
        <div class="dash-table-row filter-row">
          <div class="dash-cell">
            <input v-model="filters.item" placeholder="Cari barang..." />
          </div>
          <div class="dash-cell">
            <select v-model="filters.type">
              <option value="">Semua</option>
              <option value="add">Penambahan</option>
              <option value="remove">Pengurangan</option>
              <option value="adjustment">Penyesuaian</option>
              <option value="return">Pengembalian</option>
              <option value="assignment">Pemakaian</option>
            </select>
          </div>
          <div class="dash-cell">
            <input v-model="filters.quantity" placeholder="Cari..." type="number" />
          </div>
          <div class="dash-cell">
            <input v-model="filters.employee" placeholder="Cari karyawan..." />
          </div>
          <div class="dash-cell">
            <input v-model="filters.notes" placeholder="Cari catatan..." />
          </div>
          <div class="dash-cell">
            <input v-model="filters.created_at" placeholder="dd/mm/yyyy" />
          </div>
        </div>

        <!-- DATA ROWS -->
        <div
          v-for="transaction in result"
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
            {{ transaction.quantity > 0 ? "+" : "" }}{{ transaction.quantity }}
          </div>

          <div class="dash-cell">
            {{
              transaction.employee
                ? `${transaction.employee.first_name} ${transaction.employee.last_name}`
                : "—"
            }}
          </div>

          <div class="dash-cell">{{ transaction.notes || "—" }}</div>

          <div class="dash-cell">
            {{ new Date(transaction.created_at).toLocaleDateString() }}
          </div>
        </div>

        <div v-if="result.length === 0" class="empty-state">
          Belum ada riwayat transaksi.
        </div>

      </div>
    </div>
  </section>
</template>

<style scoped>
.transaction-page {
  padding-top: 20px;
}

/* table column style setting*/
.dash-table-row {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr 0.5fr 1fr 1fr 0.8fr;
  gap: 16px;
  padding: 12px 20px;
  align-items: center;
  border-bottom: 1px solid var(--border-light);
  font-size: 13px;
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

.type-badge {
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.type-badge.add   { background: #E1F5EE; color: #0F6E56; }
.type-badge.remove     { background: #FEE2E2; color: #991B1B; }
.type-badge.return     { background: #f2ffee; color: #0da904; }
.type-badge.assignment { background: #ffffee; color: #c35303; }
.type-badge.adjustment { background: #EEF2FF; color: #3730A3; }

.qty-positive { color: #0F6E56; font-weight: 600; }
.qty-negative { color: #991B1B; font-weight: 600; }
</style>