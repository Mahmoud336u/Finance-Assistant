import React from 'react';
import { ListItem, ListItemText } from '@mui/material';

function TransactionItem({ transaction }) {
  return (
    <ListItem>
      <ListItemText
        primary={`${transaction.description} - $${transaction.amount}`}
        secondary={`Category: ${transaction.category} | Date: ${transaction.date}`}
      />
    </ListItem>
  );
}

export default TransactionItem;
