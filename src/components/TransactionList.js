import React, { useState, useEffect } from 'react';
import { Container, Typography, List, Button, Modal } from '@mui/material';
import { getTransactions, updateTransaction } from '../services/api';
import TransactionItem from './TransactionItem';
import TransactionEditor from './TransactionEditor';

function TransactionList() {
  const [transactions, setTransactions] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const data = await getTransactions();
      setTransactions(data);
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
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
    } catch (error) {
      console.error('Failed to update transaction:', error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Transactions</Typography>
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
