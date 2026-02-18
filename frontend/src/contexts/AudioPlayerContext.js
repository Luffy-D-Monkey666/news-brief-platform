import React, { createContext, useContext, useState, useRef, useCallback, useEffect } from 'react';

const AudioPlayerContext = createContext(null);

// 音效配置（使用 Web Audio API 生成简单音效）
const createBeep = (audioContext, frequency, duration, type = 'sine') => {
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();
  
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  
  oscillator.frequency.value = frequency;
  oscillator.type = type;
  
  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
  
  oscillator.start(audioContext.currentTime);
  oscillator.stop(audioContext.currentTime + duration);
};

// 开始音效：愉快的上升音
const playStartSound = (audioContext) => {
  createBeep(audioContext, 523.25, 0.1); // C5
  setTimeout(() => createBeep(audioContext, 659.25, 0.1), 100); // E5
  setTimeout(() => createBeep(audioContext, 783.99, 0.15), 200); // G5
};

// 结束音效：柔和的下降音
const playEndSound = (audioContext) => {
  createBeep(audioContext, 783.99, 0.1); // G5
  setTimeout(() => createBeep(audioContext, 523.25, 0.2), 150); // C5
};

// 语音预设配置
const voicePresets = {
  siri_female: { pitch: 1.0, rate: 1.0, name: 'Siri (女声)' },
  siri_male: { pitch: 0.9, rate: 1.0, name: 'Siri (男声)' },
  xiao_ai: { pitch: 1.05, rate: 1.02, name: '小爱同学' },
  ideal_assistant: { pitch: 0.95, rate: 0.98, name: '理想同学' },
  nomi: { pitch: 0.92, rate: 1.0, name: 'NOMI' }
};

export const AudioPlayerProvider = ({ children }) => {
  // 播放列表状态
  const [playlist, setPlaylist] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState('siri_female');
  
  // 播放模式
  const [playMode, setPlayMode] = useState('single'); // 'single' | 'continuous'
  
  // Refs
  const speechSynthesisRef = useRef(window.speechSynthesis);
  const utteranceRef = useRef(null);
  const audioContextRef = useRef(null);
  const voicesRef = useRef([]);
  
  // 初始化 AudioContext 和语音
  useEffect(() => {
    // 加载语音
    const loadVoices = () => {
      voicesRef.current = speechSynthesisRef.current.getVoices().filter(
        voice => voice.lang === 'zh-CN' || voice.lang === 'zh'
      );
    };
    
    speechSynthesisRef.current.onvoiceschanged = loadVoices;
    loadVoices();
    
    return () => {
      speechSynthesisRef.current.cancel();
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);
  
  // 获取 AudioContext（懒加载，需要用户交互后才能创建）
  const getAudioContext = useCallback(() => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }
    return audioContextRef.current;
  }, []);
  
  // 获取当前播放的新闻
  const currentBrief = playlist[currentIndex] || null;
  
  // 设置播放列表
  const setPlaylistFromBriefs = useCallback((briefs) => {
    setPlaylist(briefs);
    setCurrentIndex(-1);
    setIsPlaying(false);
    setIsPaused(false);
  }, []);
  
  // 播放指定索引的新闻
  const playAt = useCallback((index) => {
    if (index < 0 || index >= playlist.length) return;
    
    // 取消当前播放
    speechSynthesisRef.current.cancel();
    
    const brief = playlist[index];
    const text = `${brief.title}。${brief.summary}`;
    
    // 创建新的 utterance
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    
    // 设置语音
    if (voicesRef.current.length > 0) {
      utterance.voice = voicesRef.current[0];
    }
    
    // 应用语音预设
    const preset = voicePresets[selectedVoice];
    utterance.pitch = preset.pitch;
    utterance.rate = preset.rate;
    
    // 播放开始音效
    try {
      const audioContext = getAudioContext();
      playStartSound(audioContext);
    } catch (e) {
      console.log('音效播放失败:', e);
    }
    
    // 延迟 500ms 后开始朗读（等音效播完）
    setTimeout(() => {
      utterance.onend = () => {
        // 播放结束音效
        try {
          const audioContext = getAudioContext();
          playEndSound(audioContext);
        } catch (e) {
          console.log('音效播放失败:', e);
        }
        
        // 连续播放模式下，1.5秒后播放下一条
        if (playMode === 'continuous' && index < playlist.length - 1) {
          setTimeout(() => {
            playAt(index + 1);
          }, 1500);
        } else {
          setIsPlaying(false);
          setIsPaused(false);
        }
      };
      
      utterance.onerror = (e) => {
        console.error('语音播放错误:', e);
        setIsPlaying(false);
        setIsPaused(false);
      };
      
      utteranceRef.current = utterance;
      speechSynthesisRef.current.speak(utterance);
    }, 500);
    
    setCurrentIndex(index);
    setIsPlaying(true);
    setIsPaused(false);
  }, [playlist, selectedVoice, playMode, getAudioContext]);
  
  // 播放/暂停切换
  const togglePlay = useCallback(() => {
    if (isPaused) {
      speechSynthesisRef.current.resume();
      setIsPaused(false);
      setIsPlaying(true);
    } else if (isPlaying) {
      speechSynthesisRef.current.pause();
      setIsPaused(true);
      setIsPlaying(false);
    } else if (playlist.length > 0) {
      // 从头开始或继续
      playAt(currentIndex >= 0 ? currentIndex : 0);
    }
  }, [isPaused, isPlaying, playlist, currentIndex, playAt]);
  
  // 播放全部（连续播放模式）
  const playAll = useCallback(() => {
    if (playlist.length === 0) return;
    setPlayMode('continuous');
    playAt(0);
  }, [playlist, playAt]);
  
  // 播放单条
  const playSingle = useCallback((brief) => {
    const index = playlist.findIndex(b => b._id === brief._id);
    if (index >= 0) {
      setPlayMode('single');
      playAt(index);
    }
  }, [playlist, playAt]);
  
  // 上一条
  const playPrevious = useCallback(() => {
    if (currentIndex > 0) {
      playAt(currentIndex - 1);
    }
  }, [currentIndex, playAt]);
  
  // 下一条
  const playNext = useCallback(() => {
    if (currentIndex < playlist.length - 1) {
      playAt(currentIndex + 1);
    }
  }, [currentIndex, playlist.length, playAt]);
  
  // 停止
  const stop = useCallback(() => {
    speechSynthesisRef.current.cancel();
    setIsPlaying(false);
    setIsPaused(false);
  }, []);
  
  // 切换语音
  const changeVoice = useCallback((voiceKey) => {
    setSelectedVoice(voiceKey);
  }, []);
  
  const value = {
    // 状态
    playlist,
    currentIndex,
    currentBrief,
    isPlaying,
    isPaused,
    playMode,
    selectedVoice,
    voicePresets,
    
    // 方法
    setPlaylistFromBriefs,
    playAt,
    playSingle,
    playAll,
    playPrevious,
    playNext,
    togglePlay,
    stop,
    changeVoice,
    setPlayMode,
  };
  
  return (
    <AudioPlayerContext.Provider value={value}>
      {children}
    </AudioPlayerContext.Provider>
  );
};

export const useAudioPlayer = () => {
  const context = useContext(AudioPlayerContext);
  if (!context) {
    throw new Error('useAudioPlayer must be used within an AudioPlayerProvider');
  }
  return context;
};

export default AudioPlayerContext;
