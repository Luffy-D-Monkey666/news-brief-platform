import React, { useState } from 'react';
import { useAudioPlayer } from '../contexts/AudioPlayerContext';
import {
  FaPlay,
  FaPause,
  FaStepBackward,
  FaStepForward,
  FaStop,
  FaVolumeUp,
  FaSpinner
} from 'react-icons/fa';

const AudioPlayerBar = () => {
  const {
    playlist,
    currentIndex,
    currentBrief,
    isPlaying,
    isPaused,
    isLoading,
    playMode,
    selectedVoice,
    voicePresets,
    playPrevious,
    playNext,
    togglePlay,
    stop,
    changeVoice,
    playAll,
  } = useAudioPlayer();
  
  const [showVoiceMenu, setShowVoiceMenu] = useState(false);
  
  // 如果没有播放列表，不显示播放栏
  if (playlist.length === 0) return null;
  
  // 如果没有正在播放且没有暂停，显示最小化版本
  const isMinimized = !isPlaying && !isPaused && currentIndex === -1;
  
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50">
      <div className="max-w-7xl mx-auto px-4 py-3">
        {isMinimized ? (
          // 最小化状态：显示播放全部按钮
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <FaVolumeUp className="text-gray-400" />
              <span className="text-sm text-gray-600">
                {playlist.length} 条新闻可收听
              </span>
            </div>
            <button
              onClick={playAll}
              className="flex items-center gap-2 px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors text-sm font-medium"
            >
              <FaPlay className="text-xs" />
              播放全部
            </button>
          </div>
        ) : (
          // 播放状态：完整控制栏
          <div className="flex items-center gap-4">
            {/* 当前播放信息 */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-gray-400">
                  {currentIndex + 1} / {playlist.length}
                </span>
                {playMode === 'continuous' && (
                  <span className="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded">
                    连续播放
                  </span>
                )}
              </div>
              <h4 className="text-sm font-medium text-gray-900 truncate">
                {currentBrief?.title || '准备播放...'}
              </h4>
            </div>
            
            {/* 播放控制按钮 */}
            <div className="flex items-center gap-2">
              {/* 上一条 */}
              <button
                onClick={playPrevious}
                disabled={currentIndex <= 0}
                className={`p-2 rounded-full transition-colors ${
                  currentIndex <= 0
                    ? 'text-gray-300 cursor-not-allowed'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="上一条"
              >
                <FaStepBackward />
              </button>
              
              {/* 播放/暂停 */}
              <button
                onClick={togglePlay}
                disabled={isLoading}
                className={`p-3 rounded-full transition-colors ${
                  isLoading 
                    ? 'bg-gray-300 cursor-not-allowed' 
                    : 'bg-black text-white hover:bg-gray-800'
                }`}
                title={isLoading ? '加载中...' : isPlaying ? '暂停' : isPaused ? '继续' : '播放'}
              >
                {isLoading ? (
                  <FaSpinner className="animate-spin" />
                ) : isPlaying ? (
                  <FaPause />
                ) : (
                  <FaPlay className="ml-0.5" />
                )}
              </button>
              
              {/* 下一条 */}
              <button
                onClick={playNext}
                disabled={currentIndex >= playlist.length - 1}
                className={`p-2 rounded-full transition-colors ${
                  currentIndex >= playlist.length - 1
                    ? 'text-gray-300 cursor-not-allowed'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="下一条"
              >
                <FaStepForward />
              </button>
              
              {/* 停止 */}
              <button
                onClick={stop}
                className="p-2 rounded-full text-gray-600 hover:bg-gray-100 transition-colors"
                title="停止"
              >
                <FaStop />
              </button>
            </div>
            
            {/* 语音选择 */}
            <div className="relative">
              <button
                onClick={() => setShowVoiceMenu(!showVoiceMenu)}
                className="flex items-center gap-2 px-3 py-2 text-xs text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <FaVolumeUp />
                <span className="hidden sm:inline">{voicePresets[selectedVoice].name}</span>
              </button>
              
              {showVoiceMenu && (
                <div className="absolute bottom-full right-0 mb-2 w-40 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-10">
                  {Object.entries(voicePresets).map(([key, preset]) => (
                    <button
                      key={key}
                      onClick={() => {
                        changeVoice(key);
                        setShowVoiceMenu(false);
                      }}
                      className={`w-full px-4 py-2 text-left text-sm hover:bg-gray-50 transition-colors ${
                        selectedVoice === key ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
                      }`}
                    >
                      {preset.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      
      {/* 播放进度条 */}
      {(isPlaying || isPaused) && (
        <div className="h-1 bg-gray-100">
          <div 
            className="h-full bg-black transition-all duration-300"
            style={{ 
              width: `${((currentIndex + 1) / playlist.length) * 100}%` 
            }}
          />
        </div>
      )}
    </div>
  );
};

export default AudioPlayerBar;
