<template>
  <form @submit.prevent="handleSubmit" novalidate>
    <div class="mb-3">
      <label for="title" class="form-label">Title</label>
      <input 
        type="text" 
        class="form-control"
        :class="{ 'is-invalid': submitted && errors.title }"
        id="title" 
        v-model="formData.title"
      >
      <div class="invalid-feedback" v-show="submitted && errors.title">
        {{ errors.title }}
      </div>
    </div>

    <div class="mb-3">
      <label for="author" class="form-label">Author</label>
      <input 
        type="text" 
        class="form-control"
        :class="{ 'is-invalid': submitted && errors.author }"
        id="author" 
        v-model="formData.author"
      >
      <div class="invalid-feedback" v-show="submitted && errors.author">
        {{ errors.author }}
      </div>
    </div>

    <div class="mb-3">
      <label for="isbn" class="form-label">ISBN</label>
      <input 
        type="text" 
        class="form-control"
        :class="{ 'is-invalid': submitted && errors.isbn }"
        id="isbn" 
        v-model="formData.isbn"
      >
      <div class="invalid-feedback" v-show="submitted && errors.isbn">
        {{ errors.isbn }}
      </div>
    </div>

    <div class="mb-3">
      <label for="copies" class="form-label">Available Copies</label>
      <input 
        type="number" 
        class="form-control"
        :class="{ 'is-invalid': submitted && errors.copies_available }"
        id="copies" 
        v-model.number="formData.copies_available"
        min="0"
      >
      <div class="invalid-feedback" v-show="submitted && errors.copies_available">
        {{ errors.copies_available }}
      </div>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <button type="button" class="btn btn-secondary" @click="cancel">Cancel</button>
      <button type="submit" class="btn btn-primary">
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
      },
      submitted: false
    }
  },
  computed: {
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
      }

      if (this.formData.copies_available < 0) {
        this.errors.copies_available = 'Copies must be 0 or greater';
        isValid = false;
      }

      return isValid;
    },
    handleSubmit() {
      this.submitted = true;
      
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
    cancel() {
      this.submitted = false;
      this.$emit('cancel');
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
      this.submitted = false;
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
  display: none;
}

.is-invalid ~ .invalid-feedback {
  display: block;
}
</style>
