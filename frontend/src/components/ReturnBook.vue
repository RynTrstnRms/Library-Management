<template>
  <div class="container mt-4">
    <div class="card shadow-sm">
      <div class="card-header bg-white py-3">
        <div class="d-flex justify-content-between align-items-center">
          <h3 class="mb-0">
            <i class="fas fa-undo-alt me-2"></i>
            Return Management
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
                <th class="px-4">Book Details</th>
                <th>Borrowed By</th>
                <th>Borrow Date</th>
                <th class="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="transaction in filteredTransactions" :key="transaction.id">
                <td class="px-4">
                  <div class="fw-bold">{{ transaction.book.title }}</div>
                  <small class="text-muted">ISBN: {{ transaction.book.isbn }}</small>
                </td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="user-avatar me-2">
                      {{ transaction.user.username.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <div>{{ transaction.user.username }}</div>
                      <small class="text-muted">{{ transaction.user.email }}</small>
                    </div>
                  </div>
                </td>
                <td>
                  <div>
                    <i class="far fa-calendar-alt me-2 text-primary"></i>
                    {{ formatDate(transaction.borrow_date) }}
                  </div>
                  <small class="text-muted">
                    {{ getDaysAgo(transaction.borrow_date) }}
                  </small>
                </td>
                <td class="text-center">
                  <button 
                    class="btn btn-outline-success btn-sm"
                    @click="openReturnModal(transaction)"
                    :disabled="returnInProgress"
                  >
                    <i class="fas fa-check me-1"></i>
                    Return Book
                  </button>
                </td>
              </tr>
              <tr v-if="filteredTransactions.length === 0">
                <td colspan="4" class="text-center py-5">
                  <div class="text-muted">
                    <i class="fas fa-books fa-2x mb-3"></i>
                    <p class="mb-0">No borrowed books found</p>
                    <small>All books have been returned</small>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Return Validation Modal -->
    <div class="modal fade" id="returnModal" tabindex="-1" ref="returnModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-light">
            <h5 class="modal-title">
              <i class="fas fa-clipboard-check me-2"></i>
              Return Book - Condition Check
            </h5>
            <button type="button" class="btn-close" @click="closeReturnModal"></button>
          </div>
          <div class="modal-body">
            <div class="book-info mb-4 p-3 bg-light rounded">
              <h6 class="mb-2">Book Details:</h6>
              <div><strong>Title:</strong> {{ selectedTransaction?.book.title }}</div>
              <div><strong>Borrower:</strong> {{ selectedTransaction?.user.username }}</div>
            </div>

            <form @submit.prevent="confirmReturn">
              <div class="mb-3">
                <label class="form-label">Book Condition</label>
                <select 
                  class="form-select"
                  :class="{ 'is-invalid': returnDetails.condition === 'severe' }"
                  v-model="returnDetails.condition" 
                  required
                >
                  <option value="">Select condition...</option>
                  <option value="good">✨ Good - No damage</option>
                  <option value="minor">📝 Minor damage - Slight wear</option>
                  <option value="moderate">⚠️ Moderate damage - Visible wear</option>
                  <option value="severe">❌ Severe damage - Needs replacement</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Additional Notes</label>
                <textarea 
                  class="form-control" 
                  v-model="returnDetails.notes"
                  rows="3"
                  placeholder="Describe any damages or issues..."
                ></textarea>
              </div>

              <div v-if="needsFine" class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                A fine may be applied due to reported damage.
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button type="button" class="btn btn-light" @click="closeReturnModal">
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="btn btn-success" 
                  :disabled="returnInProgress"
                >
                  <i class="fas fa-check me-1"></i>
                  {{ returnInProgress ? 'Processing...' : 'Confirm Return' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <div class="modal fade" id="successModal" tabindex="-1" ref="successModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">
              <i class="fas fa-check-circle me-2"></i>
              Book Return Successful!
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeSuccessModal"></button>
          </div>
          <div class="modal-body">
            <div class="return-details">
              <h6 class="mb-3">Return Details:</h6>
              <div class="details-item">
                <i class="fas fa-book me-2 text-primary"></i>
                <strong>Book:</strong> {{ returnedBookDetails?.title }}
              </div>
              <div class="details-item">
                <i class="fas fa-user me-2 text-primary"></i>
                <strong>Returned By:</strong> {{ returnedBookDetails?.username }}
              </div>
              <div class="details-item">
                <i class="fas fa-calendar-check me-2 text-primary"></i>
                <strong>Return Date:</strong> {{ formatDate(new Date()) }}
              </div>
              <div class="details-item">
                <i class="fas fa-clipboard-check me-2 text-primary"></i>
                <strong>Condition:</strong> 
                <span :class="{
                  'text-success': returnedBookDetails?.condition === 'good',
                  'text-warning': returnedBookDetails?.condition === 'minor',
                  'text-danger': ['moderate', 'severe'].includes(returnedBookDetails?.condition)
                }">
                  {{ returnedBookDetails?.condition }}
                </span>
              </div>
              <div v-if="returnedBookDetails?.notes" class="details-item">
                <i class="fas fa-comment me-2 text-primary"></i>
                <strong>Notes:</strong> {{ returnedBookDetails?.notes }}
              </div>
              <div v-if="needsFine" class="alert alert-warning mt-3">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Notice:</strong> Fine may be applicable due to reported damage
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="closeSuccessModal">Done</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api'

export default {
  data() {
    return {
      borrowedBooks: [],
      returnInProgress: false,
      successMessage: '',
      errorMessage: '',
      userSearch: '',
      returnModal: null,
      successModal: null,
      selectedTransaction: null,
      returnDetails: {
        condition: '',
        notes: '',
        fineAcknowledged: false
      },
      returnedBookDetails: null
    }
  },
  computed: {
    filteredTransactions() {
      if (!this.userSearch) return this.borrowedBooks;
      const search = this.userSearch.toLowerCase();
      return this.borrowedBooks.filter(t => 
        t.user.username.toLowerCase().includes(search)
      );
    },
    needsFine() {
      return ['moderate', 'severe'].includes(this.returnDetails.condition);
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    async fetchBorrowedBooks() {
      try {
        const response = await apiService.getBorrowedBooks()
        this.borrowedBooks = response.data.filter(t => t.status === 'borrowed')
      } catch (error) {
        this.errorMessage = 'Error fetching borrowed books'
        console.error(error)
      }
    },
    openReturnModal(transaction) {
      this.selectedTransaction = transaction;
      this.returnDetails = {
        condition: '',
        notes: '',
        fineAcknowledged: false
      };
      this.returnModal.show();
    },

    closeReturnModal() {
      this.returnModal.hide();
      this.selectedTransaction = null;
    },

    async confirmReturn() {
      if (!this.selectedTransaction) return;

      this.returnInProgress = true;
      try {
        await apiService.returnBook(this.selectedTransaction.id, {
          condition: this.returnDetails.condition,
          notes: this.returnDetails.notes,
          damage_reported: this.returnDetails.condition !== 'good'
        });
        
        this.returnedBookDetails = {
          title: this.selectedTransaction.book.title,
          username: this.selectedTransaction.user.username,
          condition: this.returnDetails.condition,
          notes: this.returnDetails.notes
        };

        this.closeReturnModal();
        this.successModal.show();
        await this.fetchBorrowedBooks();
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Error returning book';
        console.error(error);
      } finally {
        this.returnInProgress = false;
      }
    },

    closeSuccessModal() {
      this.successModal.hide();
      this.returnedBookDetails = null;
    },

    getDaysAgo(date) {
      const days = Math.floor((new Date() - new Date(date)) / (1000 * 60 * 60 * 24));
      if (days === 0) return 'Today';
      if (days === 1) return 'Yesterday';
      return `${days} days ago`;
    }
  },
  mounted() {
    this.fetchBorrowedBooks();
    this.returnModal = new bootstrap.Modal(this.$refs.returnModal);
    this.successModal = new bootstrap.Modal(this.$refs.successModal);
  }
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}

.search-container {
  width: 300px;
}

.user-avatar {
  width: 35px;
  height: 35px;
  background-color: #e9ecef;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #495057;
}

.table th {
  text-transform: uppercase;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.table td {
  vertical-align: middle;
  padding: 1rem 0.75rem;
}

.btn-outline-success:hover {
  color: white;
}

.return-details {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.25rem;
}

.details-item {
  padding: 0.75rem 0;
  border-bottom: 1px solid #dee2e6;
}

.details-item:last-child {
  border-bottom: none;
}

.modal-header.bg-success .btn-close-white {
  filter: brightness(0) invert(1);
}

.book-info {
  border-left: 4px solid #0d6efd;
}

.form-select option {
  padding: 8px;
}
</style>