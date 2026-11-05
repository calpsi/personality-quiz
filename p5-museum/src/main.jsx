import React from 'react';
import {createRoot} from 'react-dom/client';
import './app/globals.css';
import Home from './app/page.jsx';
createRoot(document.getElementById('museum')).render(<Home/>);
