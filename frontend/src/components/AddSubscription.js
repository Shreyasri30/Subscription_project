import React, { useState, useEffect } from 'react';
import axiosInstance from '../axiosInstance';  
import axios from 'axios';

const AddSubscription = () => {
  const [formData, setFormData] = useState({
    customer_id: '',
    product_id: '',  
    start_date: '',
    end_date: '',
    users: ''
  });

  const [customers, setCustomers] = useState([]);  
  const [products, setProducts] = useState([]);    
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const response = await axiosInstance.get('customers/');
        setCustomers(response.data);  
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    };

    fetchCustomers();  
  }, []);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axiosInstance.get('products/');  
        setProducts(response.data);  
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    };

    fetchProducts();  
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const submissionData = {
      customer_id: formData.customer_id,
      product_id: formData.product_id,
      start_date: formData.start_date,
      end_date: formData.end_date,
      users: formData.users
    };
  
    console.log("Exact data being sent:", submissionData);  
  
    try {
      const response = await axiosInstance.post('add_subscription/', 
        JSON.stringify(submissionData), 
        {
          headers: {
            'Content-Type': 'application/json' 
          }
        }
      );
      console.log('Response from server:', response.data);
      setMessage('Subscription added successfully!');
      alert('Subscription added successfully!');
    } catch (error) {
      console.error('Full error details:', error);
      console.error('Error response:', error.response ? error.response.data : 'No response');
      setMessage('Failed to add subscription. Please try again.');
      alert(`Failed to add subscription: ${error.response ? error.response.data.error : error.message}`);
    }
  };

  return (
    <div>
      <h2>Add Subscription</h2>

      <form onSubmit={handleSubmit} style={{ maxWidth: '500px', margin: 'auto' }}>
        <select
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
          required
          style={{ width: '105%', padding: '15px', fontSize: '18px', marginBottom: '10px' }}  
        >
          <option value="">Select a customer</option>
          {customers.map(customer => (
            <option key={customer.customer_id} value={customer.customer_id}>
              {customer.name}
            </option>
          ))}
        </select>

        <select
          name="product_id"
          value={formData.product_id}
          onChange={handleChange}
          required
          style={{ width: '105%', padding: '15px', fontSize: '18px', marginBottom: '10px' }} 
        >
          <option value="">Select a product</option>
          {products.map(product => (
            <option key={product.id} value={product.id}>
              {product.product_name}
            </option>
          ))}
        </select>

        <div>
  <label>Start Date:</label>
  <input
    type="date"
    name="start_date"
    value={formData.start_date}
    onChange={handleChange}
    required
  />
</div>

<div>
  <label>End Date:</label>
  <input
    type="date"
    name="end_date"
    value={formData.end_date}
    onChange={handleChange}
    required
  />
</div>

        <div>
          <label>Number of Users:</label>
          <input
            type="text"
            name="users"
            value={formData.users}
            onChange={handleChange}
            placeholder="Enter number of users"
          />
        </div>

        {message && <p>{message}</p>}

        <button type="submit">Add Subscription</button>
      </form>
    </div>
  );
};

export default AddSubscription;