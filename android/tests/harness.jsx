import React from 'react';import {createRoot} from 'react-dom/client';import '../src/styles.mjs';
import App from '../src/App.jsx';import {ApiAuthAdapter} from '../src/auth/api-auth.mjs';
createRoot(document.getElementById('root')).render(<App authAdapter={new ApiAuthAdapter()}/>);
