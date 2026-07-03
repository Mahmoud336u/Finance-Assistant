import React, { useEffect, useState } from 'react';
import { Alert, Container, List, ListItem, ListItemText, Typography } from '@mui/material';
import { getBudgetSuggestions } from '../services/api';

function BudgetSuggestions() {
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const data = await getBudgetSuggestions();
        setSuggestions(data);
      } catch (err) {
        setError('Failed to load budget suggestions. Please try again later.');
        console.error('Failed to fetch suggestions:', err);
      }
    };
    fetchSuggestions();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Budget Suggestions</Typography>
      {error && <Alert severity="error">{error}</Alert>}
      <List>
        {suggestions.map((suggestion, index) => (
          <ListItem key={index}>
            <ListItemText primary={suggestion} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default BudgetSuggestions;
