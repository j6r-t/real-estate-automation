<template>
  <div class="container page-content">
    <h2>Contact Us</h2>
    <p>Get in touch with us for any inquiries or to schedule a visit.</p>
    
    <div class="contact-info">
      <div class="info-item">
        <h3>Address</h3>
        <p>123 Real Estate Ave, City, Country</p>
      </div>
      <div class="info-item">
        <h3>Email</h3>
        <p>contact@agencyname.com</p>
      </div>
      <div class="info-item">
        <h3>Phone</h3>
        <p>+1 234 567 890</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-content {
  padding: 4rem 1rem;
}
.contact-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}
.info-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
