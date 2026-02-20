import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AudioPlayerProvider } from './contexts/AudioPlayerContext';
import HomePage from './pages/HomePage';
import KnowledgePage from './pages/KnowledgePage';
import EntityPage from './pages/EntityPage';
import AudioPlayerBar from './components/AudioPlayerBar';
import './App.css';

function App() {
  return (
    <Router>
      <AudioPlayerProvider>
        <div className="App pb-20"> {/* 底部留出播放栏空间 */}
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/knowledge" element={<KnowledgePage />} />
            <Route path="/entity/:id" element={<EntityPage />} />
          </Routes>
          <AudioPlayerBar />
        </div>
      </AudioPlayerProvider>
    </Router>
  );
}

export default App;
