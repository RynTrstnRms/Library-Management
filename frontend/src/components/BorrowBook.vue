<template>
  <div class="container mt-4">
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div class="row">

      <!-- Books Section -->
      <div class="col-md-8">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h3>
              <i class="fas fa-book me-2"></i>
              Book Borrowing
            </h3>
          </div>
          <div class="search-box">
            <input type="text" v-model="bookSearch" class="form-control"
              placeholder="Search books by title or author...">
          </div>
        </div>
        <div class="row">
          <div v-for="book in filteredBooks" :key="book.id" class="col-md-6 mb-4">
            <div class="card h-100"
              :class="{ 'unavailable': book.copies_available === 0, 'selected': selectedBooks.find(b => b.id === book.id) }">
              <div class="card-body">
                <h5 class="card-title">{{ book.title }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">by {{ book.author }}</h6>
                <p class="card-text">
                  <span class="badge" :class="book.copies_available > 0 ? 'bg-success' : 'bg-danger'">
                    {{ book.copies_available }} copies available
                  </span>
                </p>
                <button class="btn" :class="selectedBooks.find(b => b.id === book.id) ? 'btn-danger' : 'btn-primary'"
                  @click="toggleBookSelection(book)" :disabled="book.copies_available === 0 || borrowInProgress">
                  {{selectedBooks.find(b => b.id === book.id) ? 'Remove' : 'Select Book'}}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Borrowing Form Section -->
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h4>Borrowing Details</h4>
          </div>
          <div class="card-body">
            <form @submit.prevent="borrowBooks">
              <!-- Selected Books Display -->
              <div class="mb-3">
                <label class="form-label">Selected Books ({{ selectedBooks.length }})</label>
                <div class="selected-books-list">
                  <div v-for="book in selectedBooks" :key="book.id" class="selected-book-item">
                    <span>{{ book.title }}</span>
                    <button type="button" class="btn-close" @click="removeBook(book)"></button>
                  </div>
                  <div v-if="!selectedBooks.length" class="text-muted">
                    No books selected
                  </div>
                </div>
              </div>

              <!-- User Selection -->
              <div class="mb-3">
                <label class="form-label">Select User</label>
                <div class="user-search-container">
                  <input type="text" class="form-control" v-model="userSearch" @focus="showUserList = true"
                    :placeholder="selectedUser ? selectedUser.username : 'Search users...'">
                  <!-- Only show dropdown when searching and results exist -->
                  <div class="user-dropdown" v-if="showUserList && userSearch && filteredUsers.length > 0">
                    <div v-for="user in filteredUsers" :key="user.id" class="user-dropdown-item"
                      @click="selectUser(user)">
                      <div class="user-info">
                        <div class="username">{{ user.username }}</div>
                        <div class="email text-muted">{{ user.email }}</div>
                      </div>
                    </div>
                  </div>
                  <!-- Show no results message -->
                  <div class="user-dropdown" v-if="showUserList && userSearch && filteredUsers.length === 0">
                    <div class="user-dropdown-item text-muted">
                      No users found
                    </div>
                  </div>
                </div>
                <!-- Show selected user -->
                <div v-if="selectedUser" class="selected-user mt-2">
                  Selected: {{ selectedUser.username }} ({{ selectedUser.email }})
                </div>
              </div>

              <button class="btn btn-primary w-100" :disabled="!canBorrow || borrowInProgress">
                {{ borrowInProgress ? 'Borrowing...' : `Borrow ${selectedBooks.length} Book${selectedBooks.length !== 1
                  ? 's' : ''}` }}
              </button>
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
            <h5 class="modal-title">Books Borrowed Successfully!</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeSuccessModal"></button>
          </div>
          <div class="modal-body">
            <div class="borrow-details">
              <h6>Borrowing Details:</h6>
              <div class="details-item">
                <strong>Books:</strong>
                <ul class="borrowed-books-list">
                  <li v-for="book in borrowDetails.books" :key="book.title">
                    {{ book.title }} by {{ book.author }}
                  </li>
                </ul>
              </div>
              <div class="details-item">
                <strong>Borrowed By:</strong> {{ borrowDetails.username }}
              </div>
              <div class="details-item">
                <strong>Date:</strong> {{ borrowDetails.date }}
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="closeSuccessModal">OK</button>
          </div>
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
      books: [],
      users: [],
      book_id: '',
      username: '',
      borrowInProgress: false,
      successMessage: '',
      errorMessage: '',
      selectedBookTitle: '',
      bookSearch: '',
      userSearch: '',
      successModal: null,
      selectedBooks: [],
      borrowDetails: {
        books: [],
        username: '',
        date: ''
      },
      showUserList: false,
      selectedUser: null
    }
  },
  computed: {
    filteredBooks() {
      if (!this.bookSearch) return this.books;
      const search = this.bookSearch.toLowerCase();
      return this.books.filter(book =>
        book.title.toLowerCase().includes(search) ||
        book.author.toLowerCase().includes(search)
      );
    },
    filteredUsers() {
      if (!this.userSearch) return [];
      const search = this.userSearch.toLowerCase();
      return this.users.filter(user =>
        user.username.toLowerCase().includes(search) ||
        user.email.toLowerCase().includes(search)
      );
    },
    canBorrow() {
      return this.selectedBooks.length > 0 && this.selectedUser;
    }
  },
  mounted() {
    this.fetchBooks();
    this.fetchUsers();
    this.successModal = new bootstrap.Modal(this.$refs.successModal);
  },
  methods: {
    toggleBookSelection(book) {
      const index = this.selectedBooks.findIndex(b => b.id === book.id);
      if (index === -1) {
        this.selectedBooks.push(book);
      } else {
        this.selectedBooks.splice(index, 1);
      }
    },
    removeBook(book) {
      const index = this.selectedBooks.findIndex(b => b.id === book.id);
      if (index !== -1) {
        this.selectedBooks.splice(index, 1);
      }
    },
    selectBook(book) {
      this.book_id = book.id;
      this.selectedBookTitle = `${book.title} by ${book.author}`;
    },
    fetchBooks() {
      axios.get('books/')
        .then(res => {
          this.books = res.data;
        })
        .catch(error => {
          console.error('Error fetching books:', error);
          this.errorMessage = 'Error fetching books. Please try again.';
        });
    },
    fetchUsers() {
      axios.get('users/')
        .then(res => {
          this.users = res.data;
        })
        .catch(error => {
          console.error('Error fetching users:', error);
          this.errorMessage = 'Error fetching users. Please try again.';
        });
    },
    borrowBooks() {
      if (!this.canBorrow) return;

      this.borrowInProgress = true;
      this.successMessage = '';
      this.errorMessage = '';

      // Create an array of promises for each book borrow request
      const borrowPromises = this.selectedBooks.map(book => {
        return axios.post('borrow/', {
          book_id: book.id,
          username: this.username
        });
      });

      Promise.all(borrowPromises)
        .then(() => {
          this.borrowDetails = {
            books: this.selectedBooks.map(book => ({
              title: book.title,
              author: book.author
            })),
            username: this.username,
            date: new Date().toLocaleString()
          };

          this.successModal.show();
          this.selectedBooks = [];
          this.username = '';
          this.selectedUser = null;
          this.fetchBooks();
        })
        .catch(err => {
          const message = err.response?.data?.error || "Failed to borrow books.";
          this.errorMessage = message;
          console.error(err);
        })
        .finally(() => {
          this.borrowInProgress = false;
        });
    },
    selectUser(user) {
      this.selectedUser = user;
      this.username = user.username;
      this.userSearch = '';
      this.showUserList = false;
    },
    closeSuccessModal() {
      this.successModal.hide();
    },
    handleClickOutside(event) {
      const container = this.$el.querySelector('.user-search-container');
      if (container && !container.contains(event.target)) {
        this.showUserList = false;
      }
    }
  },
  mounted() {
    this.fetchBooks();
    this.fetchUsers();
    this.successModal = new bootstrap.Modal(this.$refs.successModal);
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside);
  }
}
</script>

<style scoped>
.alert {
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 4px;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.unavailable {
  opacity: 0.7;
}

.selected {
  border: 2px solid #0d6efd;
}

.selected-book {
  font-weight: bold;
  color: #0d6efd;
  margin-bottom: 0;
}

.search-box {
  width: 300px;
}

.user-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 10px;
}

.user-item {
  padding: 8px;
  border-bottom: 1px solid #dee2e6;
  transition: background-color 0.2s;
}

.user-item:hover {
  background-color: #f8f9fa;
}

.form-control {
  border-radius: 20px;
  padding-left: 15px;
  padding-right: 15px;
}

.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  border-color: #86b7fe;
}

.borrow-details {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.details-item {
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #dee2e6;
}

.details-item:last-child {
  border-bottom: none;
}

.modal-header.bg-success .btn-close-white {
  filter: brightness(0) invert(1);
}

.user-search-container {
  position: relative;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
}

.user-dropdown-item {
  padding: 8px 12px;
  cursor: pointer;
}

.user-dropdown-item:hover {
  background-color: #f8f9fa;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: 500;
}

.email {
  font-size: 0.875rem;
}

.selected-user {
  background-color: #e9ecef;
  padding: 8px 12px;
  border-radius: 4px;
}

.selected-books-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 10px;
}

.selected-book-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 4px;
}

.borrowed-books-list {
  margin: 0;
  padding-left: 20px;
}
</style>
