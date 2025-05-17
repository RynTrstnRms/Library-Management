import axios from 'axios'

const apiService = {
  // Books
  getBooks() {
    return axios.get('books/')
  },
  
  addBook(bookData) {
    return axios.post('books/', bookData)
  },
  
  updateBook(id, bookData) {
    return axios.put(`books/${id}/`, bookData)
  },
  
  deleteBook(id) {
    return axios.delete(`books/${id}/delete/`)
  },

  // Transactions
  getTransactions() {
    return axios.get('transactions/')
  },
  
  getBorrowedBooks() {
    return axios.get('transactions/?status=borrowed')
  },

  getBooksByStatus(status) {
    return axios.get(`transactions/?status=${status}`)
  },

  getBorrowTransactions() {
    return axios.get('transactions/');
  },

  // Borrow/Return
  borrowBook(data) {
    return axios.post('borrow/', data)
  },
  
  returnBook(borrowId, returnData) {
    return axios.post(`return/${borrowId}/`, returnData)
  },

  // Users
  getUsers() {
    return axios.get('users/')
  },
  
  getUserDetails(userId) {
    return axios.get(`users/${userId}/`)
  },

  // Check if a book is borrowed by a specific user
  isBookBorrowedByUser(bookId, username) {
    return axios.get(`transactions/?book=${bookId}&user=${username}&status=borrowed`)
      .then(response => response.data.length > 0);
  },
}

export default apiService