import React, { useState, useEffect } from 'react';
import { Container, Typography, Button } from '@mui/material';
import { PlaidLink } from 'react-plaid-link';
import { getLinkToken, exchangePublicToken } from '../services/api';

function DataImport() {
  const [linkToken, setLinkToken] = useState(null);

  useEffect(() => {
    const fetchLinkToken = async () => {
      try {
        const token = await getLinkToken();
        setLinkToken(token);
      } catch (error) {
        console.error('Failed to fetch link token:', error);
      }
    };
    fetchLinkToken();
  }, []);

  const handleOnSuccess = async (publicToken, metadata) => {
    try {
      await exchangePublicToken(publicToken);
      // Optionally, refresh data or show success message
    } catch (error) {
      console.error('Failed to exchange public token:', error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Data Import</Typography>
      {linkToken && (
        <PlaidLink
          token={linkToken}
          onSuccess={handleOnSuccess}
          onExit={(err) => console.error('Plaid Link exited:', err)}
        >
          <Button variant="contained" color="primary">
            Connect Bank Account
          </Button>
        </PlaidLink>
      )}
      {/* Retain existing CSV upload functionality if present */}
    </Container>
  );
}

export default DataImport;
