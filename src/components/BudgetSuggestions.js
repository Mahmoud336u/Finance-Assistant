import React, { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, ListItemText } from '@mui/material';
import { getBudgetSuggestions } from '../services/api';

function BudgetSuggestions() {
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const data = await getBudgetSuggestions();
        setSuggestions(data);
      } catch (error) {
        console.error('Failed to fetch suggestions:', error);
      }
    };
    fetchSuggestions();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Budget Suggestions</Typography>
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
