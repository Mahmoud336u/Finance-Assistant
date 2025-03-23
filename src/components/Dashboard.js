import React, { useEffect, useState } from 'react';
import { Container, Typography, Grid } from '@mui/material';
import { getSummary } from '../services/api';
import ChartPie from './ChartPie';
import ChartBar from './ChartBar';

function Dashboard() {
  const [summary, setSummary] = useState({
    totalExpenses: 0,
    totalIncome: 0,
    categoryDistribution: [],
    monthlyExpenses: [],
  });

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getSummary();
        setSummary(data);
      } catch (error) {
        console.error('Failed to fetch summary:', error);
      }
    };
    fetchSummary();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6">Total Expenses: ${summary.totalExpenses || 0}</Typography>
          <Typography variant="h6">Total Income: ${summary.totalIncome || 0}</Typography>
        </Grid>
        <Grid item xs={12} md={6}>
          <ChartPie data={summary.categoryDistribution} />
        </Grid>
        <Grid item xs={12}>
          <ChartBar data={summary.monthlyExpenses} />
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;
