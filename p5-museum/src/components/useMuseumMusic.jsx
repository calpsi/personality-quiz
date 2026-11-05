'use client';
import {useEffect, useRef, useState} from 'react';

const storageKey = 'quiet-collection-music-v1';
const defaults = {volume: 30, muted: false};

export function useMuseumMusic() {
  const player = useRef(null);
  const prefs = useRef(defaults);
  const [settings, setSettings] = useState(defaults);
  const [playback, setPlayback] = useState('idle');

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey));
      if (Number.isInteger(saved?.volume) && saved.volume >= 0 && saved.volume <= 100 && typeof saved.muted === 'boolean') {
        prefs.current = saved;
        setSettings(saved);
      }
    } catch {}
    return () => {
      if (!player.current) return;
      player.current.pause();
      player.current = null;
    };
  }, []);

  async function start() {
    if (prefs.current.muted || !prefs.current.volume) return false;
    if (!player.current) {
      const audio = new Audio();
      audio.preload = 'auto';
      audio.loop = true;
      audio.playsInline = true;
      audio.setAttribute('playsinline', '');
      audio.volume = prefs.current.volume / 100;
      audio.src = window.MUSEUM_MUSIC_URL || 'assets/sergequadrado-moment-14023.mp3';
      audio.addEventListener('playing', () => setPlayback('playing'));
      audio.addEventListener('pause', () => setPlayback('paused'));
      audio.addEventListener('error', () => setPlayback('unavailable'));
      player.current = audio;
      audio.load();
    }
    const audio = player.current;
    audio.muted = prefs.current.muted;
    audio.volume = prefs.current.volume / 100;
    try {
      if (audio.paused) await audio.play();
      setPlayback('playing');
      return true;
    } catch {
      setPlayback('blocked');
      return false;
    }
  }

  function change(patch, duringVisit) {
    const next = {...prefs.current, ...patch};
    prefs.current = next;
    setSettings(next);
    try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch {}
    const current = player.current;
    if (current) {
      current.muted = next.muted;
      current.volume = next.volume / 100;
      if (next.muted || !next.volume) {
        current.pause();
        setPlayback('paused');
      }
    }
    if (duringVisit) start();
  }
  return {settings, change, start, playback};
}
