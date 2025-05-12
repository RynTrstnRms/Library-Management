
<template>
  <div class="home">
    <div class="row align-items-center">
      <div class="col-md-6">
        <h1 class="display-4 mb-4">Welcome to Library Management System</h1>
        <p class="lead mb-4">Efficiently manage your library's books and borrowing transactions with our comprehensive system.</p>
        <div class="d-grid gap-3 d-md-flex">
          <router-link to="/books" class="btn btn-primary btn-lg">
            <i class="fas fa-book me-2" style="color: #ffffff;"></i>View Books
          </router-link>
          <router-link to="/borrow" class="btn btn-outline-primary btn-lg">
            <i class="fas fa-hand-holding me-2"></i>Borrow a Book
          </router-link>
        </div>
      </div>
      <div class="col-md-6 text-center">
        <img src="@/assets/logo.svg" alt="Library" class="img-fluid mt-4 mt-md-0" style="max-width: 400px;">
      </div>
    </div>

    <!-- STATUS SA HOMEPAGE -->
    <div class="row mt-5">
      <div class="col-md-4">
        <div class="card text-center p-4">
          <div class="card-body">
            <i class="fas fa-book fa-3x mb-3 text-primary"></i>
            <h5 class="card-title">Total Books</h5>
            <p class="card-text display-6">{{ totalBooks }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-4">
          <div class="card-body">
            <i class="fas fa-solid fa-book-open fa-3x mb-3 text-success"></i>
            <h5 class="card-title">Books Borrowed</h5>
            <p class="card-text display-6">{{ borrowedBooks }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center p-4">
          <div class="card-body">
            <i class="fas fa-users fa-3x mb-3 text-info"></i>
            <h5 class="card-title">Active Users</h5>
            <p class="card-text display-6">{{ activeUsers }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HomeView',
  data() {
    return {
      totalBooks: 0,
      borrowedBooks: 0,
      activeUsers: 0
    }
  },
  mounted() {
    this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        const [books, transactions, users] = await Promise.all([
          axios.get('books/'),
          axios.get('transactions/'),
          axios.get('users/')
        ])
        
        this.totalBooks = books.data.length
        this.borrowedBooks = transactions.data.filter(t => t.status === 'borrowed').length
        this.activeUsers = users.data.length
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }
  }
}
</script>

<style scoped>
.home {
  padding: 2rem 0;
}

.display-4 {
  font-weight: 600;
  color: var(--dark-color);
}

.lead {
  color: var(--secondary-color);
}

.card {
  height: 100%;
  border-radius: 10px;
}

.fas {
  color: var(--primary-color);
}
</style>
