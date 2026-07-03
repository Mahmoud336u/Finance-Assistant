import React, { useState, useEffect } from 'react';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { getCategories } from '../services/api';

function TransactionEditor({ transaction, onSave, onCancel }) {
  const [description, setDescription] = useState(transaction?.description ?? '');
  const [amount, setAmount] = useState(transaction?.amount ?? '');
  const [date, setDate] = useState(transaction?.date ?? '');
  const [category, setCategory] = useState(transaction?.category ?? '');
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await getCategories();
        setCategories(data);
      } catch (err) {
        setError('Failed to load categories. Please try again.');
        console.error('Failed to fetch categories:', err);
      }
    };
    fetchCategories();
  }, []);

  if (!transaction) {
    return null;
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    const updatedTransaction = { ...transaction, description, amount, date, category };
    onSave(updatedTransaction);
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <TextField
        label="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Amount"
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Date"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        fullWidth
        margin="normal"
      />
      <FormControl fullWidth margin="normal">
        <InputLabel>Category</InputLabel>
        <Select value={category} onChange={(e) => setCategory(e.target.value)}>
          {categories.map((cat) => (
            <MenuItem key={cat.id} value={cat.name}>{cat.name}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <Button type="submit" variant="contained" color="primary">
        Save
      </Button>
      <Button onClick={onCancel} variant="outlined" color="secondary">
        Cancel
      </Button>
    </form>
  );
}

export default TransactionEditor;
