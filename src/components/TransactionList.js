import React, { useEffect, useState } from 'react';
import { Container, Typography, List } from '@mui/material';
import { getTransactions } from '../services/api';
import TransactionItem from './TransactionItem';

function TransactionList() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const data = await getTransactions();
        setTransactions(data);
      } catch (error) {
        console.error('Failed to fetch transactions:', error);
      }
    };
    fetchTransactions();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Transactions</Typography>
      <List>
        {transactions.map((transaction) => (
          <TransactionItem key={transaction.id} transaction={transaction} />
        ))}
      </List>
    </Container>
  );
}

export default TransactionList;
