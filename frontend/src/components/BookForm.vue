<template>
  <form @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="title" class="form-label">Title</label>
      <input 
        type="text" 
        class="form-control"
        :class="{ 'is-invalid': errors.title }"
        id="title" 
        v-model="formData.title" 
        required
      >
      <div class="invalid-feedback">{{ errors.title }}</div>
    </div>

    <div class="mb-3">
      <label for="author" class="form-label">Author</label>
      <input 
        type="text" 
        class="form-control"
        :class="{ 'is-invalid': errors.author }"
        id="author" 
        v-model="formData.author" 
        required
      >
      <div class="invalid-feedback">{{ errors.author }}</div>
    </div>

    <div class="mb-3">
      <label for="isbn" class="form-label">ISBN</label>
      <input 
        type="text" 
        class="form-control"
        :class="{ 'is-invalid': errors.isbn }"
        id="isbn" 
        v-model="formData.isbn" 
        required
      >
      <div class="invalid-feedback">{{ errors.isbn }}</div>
    </div>

    <div class="mb-3">
      <label for="copies" class="form-label">Available Copies</label>
      <input 
        type="number" 
        class="form-control"
        :class="{ 'is-invalid': errors.copies_available }"
        id="copies" 
        v-model.number="formData.copies_available" 
        min="0" 
        required
      >
      <div class="invalid-feedback">{{ errors.copies_available }}</div>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
      <button type="submit" class="btn btn-primary" :disabled="!isValid">
        {{ isEditMode ? 'Update' : 'Add Book' }}
      </button>
    </div>
  </form>
</template>

<script>
export default {
  props: {
    book: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      formData: {
        title: '',
        author: '',
        isbn: '',
        copies_available: 1
      },
      errors: {
        title: '',
        author: '',
        isbn: '',
        copies_available: ''
      }
    }
  },
  computed: {
    isValid() {
      return this.validateForm() === true;
    },
    isEditMode() {
      return !!this.book;
    }
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = {
        title: '',
        author: '',
        isbn: '',
        copies_available: ''
      };

      if (!this.formData.title.trim()) {
        this.errors.title = 'Title is required';
        isValid = false;
      }

      if (!this.formData.author.trim()) {
        this.errors.author = 'Author is required';
        isValid = false;
      }

      const isbn = this.formData.isbn.replace(/[-\s]/g, '');
      if (!isbn) {
        this.errors.isbn = 'ISBN is required';
        isValid = false;
      } else if (![10, 13].includes(isbn.length)) {
        this.errors.isbn = 'ISBN must be 10 or 13 digits';
        isValid = false;
      } else if (!/^\d*$/.test(isbn)) {
        this.errors.isbn = 'ISBN must contain only numbers';
        isValid = false;
      }

      if (this.formData.copies_available < 0) {
        this.errors.copies_available = 'Copies must be 0 or greater';
        isValid = false;
      }

      return isValid;
    },
    handleSubmit() {
      if (this.validateForm()) {
        const formattedData = {
          ...this.formData,
          isbn: this.formData.isbn.replace(/[-\s]/g, '')
        };
        
        if (this.isEditMode) {
          this.$emit('update', { ...formattedData, id: this.book.id });
        } else {
          this.$emit('add', formattedData);
        }
      }
    },
    resetForm() {
      this.formData = {
        title: '',
        author: '',
        isbn: '',
        copies_available: 1
      };
      this.errors = {
        title: '',
        author: '',
        isbn: '',
        copies_available: ''
      };
    }
  },
  watch: {
    book: {
      immediate: true,
      handler(newBook) {
        if (newBook) {
          this.formData = { ...newBook };
        } else {
          this.resetForm();
        }
      }
    }
  }
}
</script>

<style scoped>
.invalid-feedback {
  display: block;
}
</style>
