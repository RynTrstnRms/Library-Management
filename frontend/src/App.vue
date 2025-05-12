EXAM\itew6-final-exam\frontend\src\App.vue
<template>
  <div id="app">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center" to="/">
          <i class="fas fa-book-reader me-2"></i>
          Library Management System
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/books">
                <i class="fas fa-books me-1"></i> Books
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/borrow">
                <i class="fas fa-hand-holding-book me-1"></i> Borrow
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/return">
                <i class="fas fa-undo me-1"></i> Return
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/transactions">
                <i class="fas fa-history me-1"></i> Transactions
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="py-4">
      <div class="container">
        <router-view></router-view>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-light py-4 mt-auto">
      <div class="container">
        <div class="text-center">
          <p class="mb-0">&copy; 2025 Library Management System ni Tantris. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
:root {
  --primary-color: #0d6efd;
  --secondary-color: #6c757d;
  --success-color: #198754;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #0dcaf0;
  --light-color: #f8f9fa;
  --dark-color: #212529;
}

body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--light-color);
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
}

.navbar-brand {
  font-weight: 600;
}

.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.table {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075);
}

.table thead th {
  background-color: var(--primary-color);
  color: white;
  border-bottom: none;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-weight: 500;
}

.alert {
  border-radius: 8px;
  border: none;
}
</style>