import React, { useState } from 'react';
import { Container, Typography, Button, TextField } from '@mui/material';

function DataImport() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = () => {
    // Logic to upload CSV file to backend (implement with FormData and API call)
    if (file) {
      console.log('Uploading file:', file);
      // Example: const formData = new FormData(); formData.append('file', file); axios.post('/upload', formData);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>Data Import</Typography>
      <Typography variant="h6">Upload CSV</Typography>
      <TextField type="file" onChange={handleFileChange} fullWidth margin="normal" />
      <Button variant="contained" color="primary" onClick={handleUpload}>
        Upload
      </Button>
      <Typography variant="h6" style={{ marginTop: 20 }}>Connect via Plaid</Typography>
      <Button variant="contained" color="secondary">
        Connect Bank Account (Plaid)
      </Button>
      {/* Plaid integration requires the Plaid Link SDK */}
    </Container>
  );
}

export default DataImport;
