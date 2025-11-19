import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from './components/ui/sonner';
import HomePage from './pages/HomePage';
import "./App.css";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
        <Toaster position="top-center" richColors />
      </BrowserRouter>
    </div>
  );
}

export default App;