import {Capacitor,CapacitorHttp} from '@capacitor/core';
import {createAuthTransport} from './https-transport.mjs';
export const authTransport=createAuthTransport({isNative:()=>Capacitor.isNativePlatform(),nativeRequest:options=>CapacitorHttp.request(options),webFetch:(...args)=>fetch(...args)});
