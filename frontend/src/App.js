import React from 'react';
import { AudioPlayerProvider } from './contexts/AudioPlayerContext';
import HomePage from './pages/HomePage';
import AudioPlayerBar from './components/AudioPlayerBar';
import './App.css';

function App() {
  return (
    <AudioPlayerProvider>
      <div className="App pb-20"> {/* 底部留出播放栏空间 */}
        <HomePage />
        <AudioPlayerBar />
      </div>
    </AudioPlayerProvider>
  );
}

export default App;
