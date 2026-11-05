'use client';
import {useEffect, useRef, useState} from 'react';

const storageKey = 'quiet-collection-music-v1';
const defaults = {volume: 30, muted: false};

export function useMuseumMusic() {
  const player = useRef(null);
  const prefs = useRef(defaults);
  const [settings, setSettings] = useState(defaults);

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
      player.current.audio.pause();
      player.current.context?.close().catch(() => {});
      player.current = null;
    };
  }, []);

  function start() {
    if (prefs.current.muted || !prefs.current.volume) return;
    if (!player.current) {
      const audio = new Audio('/assets/sergequadrado-moment-14023.mp3');
      audio.loop = true;
      const AudioEngine = window.AudioContext || window.webkitAudioContext;
      const context = AudioEngine ? new AudioEngine() : null;
      const gain = context?.createGain();
      if (gain) {
        context.createMediaElementSource(audio).connect(gain);
        gain.connect(context.destination);
        gain.gain.value = prefs.current.volume / 100;
      } else audio.volume = prefs.current.volume / 100;
      player.current = {audio, context, gain};
    }
    const {audio, context} = player.current;
    context?.resume().catch(() => {});
    if (audio.paused) audio.play().catch(() => {});
  }

  function change(patch, duringVisit) {
    const next = {...prefs.current, ...patch};
    prefs.current = next;
    setSettings(next);
    try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch {}
    const current = player.current;
    if (current) {
      current.audio.muted = next.muted;
      if (current.gain) current.gain.gain.setTargetAtTime(next.volume / 100, current.context.currentTime, .025);
      else current.audio.volume = next.volume / 100;
    }
    if (duringVisit) start();
  }
  return {settings, change, start};
}
