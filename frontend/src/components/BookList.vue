<template>
  <div>
    <div class="toast-container position-fixed top-0 end-0 p-3">
      <div 
        class="toast align-items-center text-white bg-success border-0" 
        role="alert" 
        ref="successToast"
      >
        <div class="d-flex">
          <div class="toast-body">
            {{ toastMessage }}
          </div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3><i class="fa-solid fa-list"></i> Book Management</h3>
      <button class="btn btn-success" @click="openAddModal">
        <i class="fas fa-plus me-2"></i>Add Book
      </button>
    </div>

    <div class="mb-4">
      <input 
        type="text" 
        class="form-control" 
        v-model="searchQuery" 
        placeholder="Search books by title, author, or ISBN..."
      >
    </div>

    <div class="row g-4">
      <div v-for="book in filteredBooks" :key="book.id" class="col-md-6 col-lg-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ book.title }}</h5>
            <p class="card-text">
              <i class="fas fa-user me-2"></i>{{ book.author }}<br>
              <i class="fas fa-barcode me-2"></i>{{ book.isbn }}
            </p>
            <div class="mt-auto d-flex justify-content-between align-items-center">
              <span class="badge" :class="book.copies_available > 0 ? 'bg-success' : 'bg-danger'">
                {{ book.copies_available }} copies available
              </span>
              <div class="btn-group">
                <button class="btn btn-warning btn-sm" @click="openEditModal(book)">
                  <i class="fas fa-edit me-1"></i>
                </button>
                <button class="btn btn-danger btn-sm" @click="confirmDelete(book)">
                  <i class="fas fa-trash me-1"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div class="modal fade" id="bookModal" tabindex="-1" ref="bookModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedBook ? 'Edit Book' : 'Add New Book' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <BookForm 
              :book="selectedBook"
              @add="createBook"
              @update="updateBook"
              @cancel="closeModal"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeDeleteModal"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete "{{ bookToDelete?.title }}"?</p>
            <p class="text-muted mb-0">This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="confirmDeleteBook">
              Delete Book
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import BookForm from './BookForm.vue'
import apiService from '@/services/api'

export default {
  components: { BookForm },
  data() {
    return {
      books: [],
      selectedBook: null,
      showForm: false,
      searchQuery: '',
      modal: null,
      deleteModal: null,
      bookToDelete: null,
      successToast: null,
      toastMessage: ''
    }
  },
  computed: {
    filteredBooks() {
      const query = this.searchQuery.toLowerCase()
      return this.books.filter(book => 
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query) ||
        book.isbn.toLowerCase().includes(query)
      )
    }
  },
  methods: {
    fetchBooks() {
      apiService.getBooks()
        .then(response => this.books = response.data)
        .catch(error => console.error('Error fetching books:', error))
    },
    openAddModal() {
      this.selectedBook = null;  // Ensure selectedBook is null for new books
      this.modal.show();
    },
    openEditModal(book) {
      this.selectedBook = { ...book };  // Make a copy of the book data
      this.modal.show();
    },
    closeModal() {
      this.modal.hide();
      this.selectedBook = null;
    },
    showToast(message) {
      this.toastMessage = message;
      this.successToast.show();
    },
    createBook(bookData) {
      apiService.addBook(bookData)
        .then(() => {
          this.fetchBooks()
          this.closeModal()
          this.showToast('Book added successfully!')
        })
        .catch(error => console.error('Error creating book:', error))
    },
    updateBook(book) {
      apiService.updateBook(book.id, book)
        .then(() => {
          this.closeModal()
          this.fetchBooks()
          this.showToast('Book updated successfully!')
        })
        .catch(error => console.error('Error updating book:', error))
    },
    deleteBook(id) {
      axios.delete(`books/${id}/delete/`).then(this.fetchBooks);
    },
    openDeleteModal(book) {
      this.bookToDelete = book;
      this.deleteModal.show();
    },
    closeDeleteModal() {
      this.deleteModal.hide();
      this.bookToDelete = null;
    },
    confirmDeleteBook() {
      if (this.bookToDelete) {
        apiService.deleteBook(this.bookToDelete.id)
          .then(() => {
            this.fetchBooks()
            this.closeDeleteModal()
            this.showToast('Book deleted successfully!')
          })
          .catch(error => console.error('Error deleting book:', error))
      }
    },
    confirmDelete(book) {
      this.openDeleteModal(book);
    }
  },
  mounted() {
    this.fetchBooks();
    // Change how we initialize the modal
    this.modal = new bootstrap.Modal(this.$refs.bookModal);
    this.deleteModal = new bootstrap.Modal(this.$refs.deleteModal);
    this.successToast = new bootstrap.Toast(this.$refs.successToast, {
      animation: true,
      delay: 3000
    });
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card:hover {
  transform: translateY(-5px);
}

.card-body {
  position: relative;
  min-height: 200px;
  padding: 1.25rem;
}

.badge {
  font-size: 0.875rem;
  padding: 0.5em 0.75em;
}

.btn-group {
  margin-left: auto;
}

.modal-dialog {
  max-width: 500px;
}

.modal-content {
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.modal-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.modal-body {
  padding: 20px;
}

.modal-header.bg-danger .btn-close {
  filter: invert(1) grayscale(100%) brightness(200%);
}

.toast-container {
  z-index: 1050;
}

.toast {
  opacity: 1 !important;
}
</style>
