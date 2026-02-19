import React, { createContext, useContext, useState, useRef, useCallback, useEffect } from 'react';
import { getBriefAudioUrl, getTTSVoices } from '../services/api';

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

// 语音预设配置（火山引擎豆包音色）
// 注意：voice_type 需要与后端 volcengineTTS.js 中的配置一致
const voicePresets = {
  'BV001_streaming': { name: '通用女声', description: '标准女声' },
  'BV002_streaming': { name: '通用男声', description: '标准男声' },
  'BV700_streaming': { name: '灿灿', description: '活泼女声' },
  'BV701_streaming': { name: '炀炀', description: '温暖男声' },
  'BV705_streaming': { name: '甜美女声', description: '甜美可爱' },
  'BV406_streaming': { name: '知性女声', description: '知性稳重' },
};

// 是否使用云端 TTS（火山引擎）
const USE_CLOUD_TTS = true;

export const AudioPlayerProvider = ({ children }) => {
  // 播放列表状态
  const [playlist, setPlaylist] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState('BV001_streaming');
  
  // 播放模式
  const [playMode, setPlayMode] = useState('single'); // 'single' | 'continuous'
  
  // Refs
  const audioRef = useRef(null); // HTML5 Audio 元素（用于云端 TTS）
  const speechSynthesisRef = useRef(window.speechSynthesis);
  const utteranceRef = useRef(null);
  const audioContextRef = useRef(null);
  const voicesRef = useRef([]);
  
  // 初始化
  useEffect(() => {
    // 创建 Audio 元素
    audioRef.current = new Audio();
    
    // 加载浏览器语音（备用）
    const loadVoices = () => {
      voicesRef.current = speechSynthesisRef.current.getVoices().filter(
        voice => voice.lang === 'zh-CN' || voice.lang === 'zh'
      );
    };
    
    speechSynthesisRef.current.onvoiceschanged = loadVoices;
    loadVoices();
    
    return () => {
      speechSynthesisRef.current.cancel();
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
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
  const playAt = useCallback(async (index) => {
    if (index < 0 || index >= playlist.length) return;
    
    const brief = playlist[index];
    setCurrentIndex(index);
    setIsLoading(true);
    
    // 停止当前播放
    if (audioRef.current) {
      audioRef.current.pause();
    }
    speechSynthesisRef.current.cancel();
    
    // 播放开始音效
    try {
      const audioContext = getAudioContext();
      playStartSound(audioContext);
    } catch (e) {
      console.log('音效播放失败:', e);
    }
    
    // 等待音效播完
    await new Promise(resolve => setTimeout(resolve, 400));
    
    if (USE_CLOUD_TTS && brief._id) {
      // 使用云端 TTS（火山引擎）
      try {
        const audioUrl = getBriefAudioUrl(brief._id, selectedVoice);
        
        audioRef.current.src = audioUrl;
        
        audioRef.current.oncanplaythrough = () => {
          setIsLoading(false);
          setIsPlaying(true);
          setIsPaused(false);
          audioRef.current.play();
        };
        
        audioRef.current.onended = () => {
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
        
        audioRef.current.onerror = (e) => {
          console.error('云端 TTS 播放失败，回退到浏览器 TTS:', e);
          setIsLoading(false);
          // 回退到浏览器 TTS
          playWithBrowserTTS(brief, index);
        };
        
        audioRef.current.load();
        
      } catch (error) {
        console.error('云端 TTS 错误:', error);
        setIsLoading(false);
        playWithBrowserTTS(brief, index);
      }
    } else {
      // 使用浏览器 TTS
      setIsLoading(false);
      playWithBrowserTTS(brief, index);
    }
  }, [playlist, selectedVoice, playMode, getAudioContext]);
  
  // 浏览器 TTS 播放（备用）
  const playWithBrowserTTS = useCallback((brief, index) => {
    const text = `${brief.title}。${brief.summary}`;
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    
    if (voicesRef.current.length > 0) {
      utterance.voice = voicesRef.current[0];
    }
    
    utterance.onend = () => {
      try {
        const audioContext = getAudioContext();
        playEndSound(audioContext);
      } catch (e) {}
      
      if (playMode === 'continuous' && index < playlist.length - 1) {
        setTimeout(() => {
          playAt(index + 1);
        }, 1500);
      } else {
        setIsPlaying(false);
        setIsPaused(false);
      }
    };
    
    utterance.onerror = () => {
      setIsPlaying(false);
      setIsPaused(false);
    };
    
    utteranceRef.current = utterance;
    speechSynthesisRef.current.speak(utterance);
    setIsPlaying(true);
    setIsPaused(false);
  }, [playMode, playlist.length, getAudioContext, playAt]);
  
  // 播放/暂停切换
  const togglePlay = useCallback(() => {
    if (USE_CLOUD_TTS && audioRef.current) {
      if (isPaused) {
        audioRef.current.play();
        setIsPaused(false);
        setIsPlaying(true);
      } else if (isPlaying) {
        audioRef.current.pause();
        setIsPaused(true);
        setIsPlaying(false);
      } else if (playlist.length > 0) {
        playAt(currentIndex >= 0 ? currentIndex : 0);
      }
    } else {
      // 浏览器 TTS
      if (isPaused) {
        speechSynthesisRef.current.resume();
        setIsPaused(false);
        setIsPlaying(true);
      } else if (isPlaying) {
        speechSynthesisRef.current.pause();
        setIsPaused(true);
        setIsPlaying(false);
      } else if (playlist.length > 0) {
        playAt(currentIndex >= 0 ? currentIndex : 0);
      }
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
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    speechSynthesisRef.current.cancel();
    setIsPlaying(false);
    setIsPaused(false);
    setIsLoading(false);
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
    isLoading,
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
