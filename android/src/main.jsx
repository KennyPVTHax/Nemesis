import React from 'react';
import './styles.mjs';
import {createRoot} from 'react-dom/client';
import App from './App.jsx';
class ErrorBoundary extends React.Component{state={error:false};static getDerivedStateFromError(){return {error:true}}render(){return this.state.error?<main className="auth-page"><section className="auth-card"><h1>Unable to render this screen</h1><p>The application encountered an error. No customer data was loaded.</p><button className="primary" onClick={()=>location.reload()}>Return to login</button></section></main>:this.props.children}}
createRoot(document.getElementById('root')).render(<ErrorBoundary><App/></ErrorBoundary>);
