import type { Metadata,Viewport } from 'next';
import './globals.css';
export const metadata:Metadata={title:'The Quiet Collection — What are you?',description:'A dreamlike natural history museum personality quiz. Eight choices, one specimen, and a small hamster to keep you company.'};
export const viewport:Viewport={width:'device-width',initialScale:1,themeColor:'#292b20'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>;}
