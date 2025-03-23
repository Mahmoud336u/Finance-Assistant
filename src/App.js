import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Dashboard from './components/Dashboard';
import TransactionList from './components/TransactionList';
import BudgetSuggestions from './components/BudgetSuggestions';
import DataImport from './components/DataImport';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/signup" component={Signup} />
          <Route path="/dashboard" component={Dashboard} />
          <Route path="/transactions" component={TransactionList} />
          <Route path="/budget" component={BudgetSuggestions} />
          <Route path="/import" component={DataImport} />
          <Route path="/" exact component={Login} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
