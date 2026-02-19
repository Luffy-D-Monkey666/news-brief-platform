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

// 语音预设配置（火山引擎豆包音色 - 与官方控制台名称完全一致）
// 根据用户提供的音色表更新
const voicePresets = {
  // === 通用场景 ===
  'zh_female_vv_uranus_bigtts': { name: 'vivi 2.0', description: '通用场景', lang: 'cn' },
  'zh_female_xiaohe_uranus_bigtts': { name: '小何', description: '通用场景', lang: 'cn' },
  'zh_male_m191_uranus_bigtts': { name: '云舟', description: '通用场景', lang: 'cn' },
  'zh_male_taocheng_uranus_bigtts': { name: '小天', description: '通用场景', lang: 'cn' },
  
  // === 视频配音 ===
  'zh_male_dayi_saturn_bigtts': { name: '大壹', description: '视频配音', lang: 'cn' },
  'zh_female_mizai_saturn_bigtts': { name: '黑猫侦探社咪仔', description: '视频配音', lang: 'cn' },
  'zh_female_jitangnv_saturn_bigtts': { name: '鸡汤女', description: '视频配音', lang: 'cn' },
  'zh_female_meilinvyou_saturn_bigtts': { name: '魅力女友', description: '视频配音', lang: 'cn' },
  'zh_female_santongyongns_saturn_bigtts': { name: '流畅女声', description: '视频配音', lang: 'cn' },
  'zh_male_ruyayichen_saturn_bigtts': { name: '儒雅逸辰', description: '视频配音', lang: 'cn' },
  
  // === 角色扮演 ===
  'saturn_zh_female_cancan_tob': { name: '知性灿灿', description: '角色扮演', lang: 'cn' },
  'saturn_zh_female_keainvsheng_tob': { name: '可爱女生', description: '角色扮演', lang: 'cn' },
  'saturn_zh_female_tiaopigongzhu_tob': { name: '调皮公主', description: '角色扮演', lang: 'cn' },
  'saturn_zh_male_shuanglangshaonian_tob': { name: '爽朗少年', description: '角色扮演', lang: 'cn' },
  'saturn_zh_male_tiancaitongzhuo_tob': { name: '天才同桌', description: '角色扮演', lang: 'cn' },
  
  // === 有声阅读 ===
  'zh_female_xueayi_saturn_bigtts': { name: '儿童绘本', description: '有声阅读', lang: 'cn' },
  
  // === 英文音色 ===
  'en_male_tim_uranus_bigtts': { name: 'Tim', description: '英文', lang: 'en' },
  'en_female_dacey_uranus_bigtts': { name: 'Dacey', description: '英文', lang: 'en' },
  'en_female_stokie_uranus_bigtts': { name: 'Stokie', description: '英文', lang: 'en' },
};

// 默认音色 - 使用知性灿灿（角色扮演类）
const DEFAULT_VOICE = 'saturn_zh_female_cancan_tob';

export const AudioPlayerProvider = ({ children }) => {
  // 播放列表状态
  const [playlist, setPlaylist] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(-1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState(DEFAULT_VOICE);
  
  // 播放模式
  const [playMode, setPlayMode] = useState('single'); // 'single' | 'continuous'
  
  // Refs
  const audioRef = useRef(null);
  const audioContextRef = useRef(null);
  const currentVoiceRef = useRef(selectedVoice); // 追踪当前使用的音色
  
  // 同步 selectedVoice 到 ref
  useEffect(() => {
    currentVoiceRef.current = selectedVoice;
  }, [selectedVoice]);
  
  // 初始化
  useEffect(() => {
    // 创建 Audio 元素
    audioRef.current = new Audio();
    audioRef.current.crossOrigin = 'anonymous';
    
    return () => {
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
  
  // 停止当前播放
  const stopCurrentPlayback = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current.src = '';
    }
    setIsPlaying(false);
    setIsPaused(false);
    setIsLoading(false);
  }, []);
  
  // 播放指定索引的新闻
  const playAt = useCallback(async (index, voice = null) => {
    if (index < 0 || index >= playlist.length) return;
    
    const brief = playlist[index];
    const voiceToUse = voice || currentVoiceRef.current;
    
    // 先停止当前播放
    stopCurrentPlayback();
    
    setCurrentIndex(index);
    setIsLoading(true);
    
    // 播放开始音效
    try {
      const audioContext = getAudioContext();
      playStartSound(audioContext);
    } catch (e) {
      console.log('音效播放失败:', e);
    }
    
    // 等待音效播完
    await new Promise(resolve => setTimeout(resolve, 400));
    
    if (brief._id) {
      try {
        const audioUrl = getBriefAudioUrl(brief._id, voiceToUse);
        console.log(`[AudioPlayer] 播放: ${brief.title}, voice=${voiceToUse}`);
        
        audioRef.current.src = audioUrl;
        
        audioRef.current.oncanplaythrough = () => {
          setIsLoading(false);
          setIsPlaying(true);
          setIsPaused(false);
          audioRef.current.play().catch(e => {
            console.error('播放失败:', e);
            setIsPlaying(false);
          });
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
          console.error('音频加载失败:', e);
          setIsLoading(false);
          setIsPlaying(false);
        };
        
        audioRef.current.load();
        
      } catch (error) {
        console.error('TTS 错误:', error);
        setIsLoading(false);
        setIsPlaying(false);
      }
    } else {
      setIsLoading(false);
    }
  }, [playlist, playMode, getAudioContext, stopCurrentPlayback]);
  
  // 播放/暂停切换
  const togglePlay = useCallback(() => {
    if (audioRef.current) {
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
    }
  }, [isPaused, isPlaying, playlist, currentIndex, playAt]);
  
  // 播放全部（连续播放模式）
  const playAll = useCallback(() => {
    if (playlist.length === 0) return;
    setPlayMode('continuous');
    playAt(0);
  }, [playlist, playAt]);
  
  // 播放单条（从卡片触发）- 这是统一入口
  const playSingle = useCallback((brief) => {
    const index = playlist.findIndex(b => b._id === brief._id);
    if (index >= 0) {
      setPlayMode('single');
      playAt(index);
    } else {
      // 如果 brief 不在 playlist 中（可能视图刚切换），直接播放
      console.log('[AudioPlayer] brief 不在 playlist 中，直接播放');
      setPlayMode('single');
      // 临时设置 index 并播放
      setCurrentIndex(0);
      playBriefDirectly(brief);
    }
  }, [playlist, playAt]);
  
  // 直接播放指定的 brief（不依赖 playlist）
  const playBriefDirectly = useCallback(async (brief, voice = null) => {
    const voiceToUse = voice || currentVoiceRef.current;
    
    // 先停止当前播放
    stopCurrentPlayback();
    setIsLoading(true);
    
    // 播放开始音效
    try {
      const audioContext = getAudioContext();
      playStartSound(audioContext);
    } catch (e) {
      console.log('音效播放失败:', e);
    }
    
    // 等待音效播完
    await new Promise(resolve => setTimeout(resolve, 400));
    
    if (brief._id) {
      try {
        const audioUrl = getBriefAudioUrl(brief._id, voiceToUse);
        console.log(`[AudioPlayer] 直接播放: ${brief.title}, voice=${voiceToUse}`);
        
        audioRef.current.src = audioUrl;
        
        audioRef.current.oncanplaythrough = () => {
          setIsLoading(false);
          setIsPlaying(true);
          setIsPaused(false);
          audioRef.current.play().catch(e => {
            console.error('播放失败:', e);
            setIsPlaying(false);
          });
        };
        
        audioRef.current.onended = () => {
          // 播放结束音效
          try {
            const audioContext = getAudioContext();
            playEndSound(audioContext);
          } catch (e) {
            console.log('音效播放失败:', e);
          }
          setIsPlaying(false);
          setIsPaused(false);
        };
        
        audioRef.current.onerror = (e) => {
          console.error('音频加载失败:', e);
          setIsLoading(false);
          setIsPlaying(false);
        };
        
        audioRef.current.load();
        
      } catch (error) {
        console.error('TTS 错误:', error);
        setIsLoading(false);
        setIsPlaying(false);
      }
    } else {
      setIsLoading(false);
    }
  }, [getAudioContext, stopCurrentPlayback]);
  
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
    stopCurrentPlayback();
    setCurrentIndex(-1);
  }, [stopCurrentPlayback]);
  
  // 切换语音 - 如果正在播放，用新音色重新播放当前内容
  const changeVoice = useCallback((voiceKey) => {
    console.log(`[AudioPlayer] 切换音色: ${selectedVoice} -> ${voiceKey}`);
    setSelectedVoice(voiceKey);
    currentVoiceRef.current = voiceKey;
    
    // 如果正在播放或暂停中，用新音色重新播放
    if ((isPlaying || isPaused) && currentIndex >= 0) {
      playAt(currentIndex, voiceKey);
    }
  }, [selectedVoice, isPlaying, isPaused, currentIndex, playAt]);
  
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
