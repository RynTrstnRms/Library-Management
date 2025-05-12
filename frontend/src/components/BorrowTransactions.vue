<template>
  <div class="container mt-5">
    <div class="card shadow-sm">
      <div class="card-header bg-white py-3">
        <div class="d-flex justify-content-between align-items-center">
          <h3 class="mb-0">
            <i class="fas fa-history me-2"></i>
            Borrow Transactions
          </h3>
          <div class="search-container">
            <div class="input-group">
              <span class="input-group-text bg-light">
                <i class="fas fa-search"></i>
              </span>
              <input 
                type="text" 
                class="form-control border-start-0" 
                v-model="userSearch" 
                placeholder="Search by username..."
              >
            </div>
          </div>
        </div>
      </div>

      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead>
              <tr class="bg-light">
                <th class="px-4">Book</th>
                <th>User</th>
                <th>Status</th>
                <th>Borrowed On</th>
                <th>Returned On</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="t in filteredTransactions" :key="t.id">
                <td class="px-4">
                  <div class="fw-bold">{{ t.book.title }}</div>
                </td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="user-icon me-2">
                      {{ t.user.username.charAt(0).toUpperCase() }}
                    </div>
                    {{ t.user.username }}
                  </div>
                </td>
                <td>
                  <span 
                    class="badge rounded-pill"
                    :class="{
                      'bg-success': t.status === 'returned',
                      'bg-warning text-dark': t.status === 'borrowed'
                    }"
                  >
                    {{ t.status.toUpperCase() }}
                  </span>
                </td>
                <td>
                  <i class="far fa-calendar-alt me-2 text-muted"></i>
                  {{ formatDate(t.borrow_date) }}
                </td>
                <td>
                  <span v-if="t.return_date">
                    <i class="far fa-calendar-check me-2 text-success"></i>
                    {{ formatDate(t.return_date) }}
                  </span>
                  <span v-else class="text-muted">
                    <i class="far fa-clock me-2"></i>
                    Not Yet Returned
                  </span>
                </td>
              </tr>
              <tr v-if="filteredTransactions.length === 0">
                <td colspan="5" class="text-center py-4">
                  <div class="text-muted">
                    <i class="fas fa-search fa-2x mb-3"></i>
                    <p class="mb-0">No transactions found</p>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      transactions: [],
      userSearch: ''
    }
  },
  computed: {
    filteredTransactions() {
      if (!this.userSearch) return this.transactions;
      const search = this.userSearch.toLowerCase();
      return this.transactions.filter(t => 
        t.user.username.toLowerCase().includes(search)
      );
    }
  },
  mounted() {
    axios.get('transactions/')
      .then(res => {
        this.transactions = res.data
      })
      .catch(() => {
        alert("Error fetching transactions.")
      })
  },
  methods: {
    formatDate(datetime) {
      return new Date(datetime).toLocaleString()
    }
  }
}
</script>

<style scoped>
.search-container {
  width: 300px;
}

.input-group-text {
  border-right: 0;
}

.badge {
  font-size: 0.8rem;
  padding: 0.6em 1em;
}

.table th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.table td {
  vertical-align: middle;
  padding: 1rem 0.75rem;
}

.user-icon {
  width: 32px;
  height: 32px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  color: #495057;
}

.card {
  border: none;
  border-radius: 10px;
}

.card-header {
  border-bottom: 1px solid rgba(0,0,0,0.125);
}

.table-hover tbody tr:hover {
  background-color: #f8f9fa;
  cursor: pointer;
}

.bg-light {
  background-color: #f8f9fa !important;
}

i {
  width: 16px;
  text-align: center;
}

.rounded-pill {
  padding-left: 1rem;
  padding-right: 1rem;
}
</style>
