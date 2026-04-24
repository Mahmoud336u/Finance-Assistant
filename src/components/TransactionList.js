import React, { useState, useEffect } from 'react';
import { Alert, Button, Container, List, Modal, Typography } from '@mui/material';
import { getTransactions, updateTransaction } from '../services/api';
import TransactionItem from './TransactionItem';
import TransactionEditor from './TransactionEditor';

function TransactionList() {
  const [transactions, setTransactions] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const data = await getTransactions();
      setTransactions(data);
      setError('');
    } catch (err) {
      setError('Failed to load transactions. Please try again later.');
      console.error('Failed to fetch transactions:', err);
    }
  };

  const handleEdit = (transaction) => {
    setSelectedTransaction(transaction);
    setModalOpen(true);
  };

  const handleSave = async (updatedTransaction) => {
    try {
      await updateTransaction(updatedTransaction.id, updatedTransaction);
      setModalOpen(false);
      fetchTransactions();
    } catch (err) {
      setError('Failed to update transaction. Please try again.');
      console.error('Failed to update transaction:', err);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Transactions</Typography>
      {error && <Alert severity="error">{error}</Alert>}
      <List>
        {transactions.map((transaction) => (
          <div key={transaction.id}>
            <TransactionItem transaction={transaction} />
            <Button onClick={() => handleEdit(transaction)}>Edit</Button>
          </div>
        ))}
      </List>
      <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
        <div style={{ backgroundColor: 'white', padding: '20px', margin: 'auto', width: '50%' }}>
          <TransactionEditor
            transaction={selectedTransaction}
            onSave={handleSave}
            onCancel={() => setModalOpen(false)}
          />
        </div>
      </Modal>
    </Container>
  );
}

export default TransactionList;
